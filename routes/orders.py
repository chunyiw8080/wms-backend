from datetime import datetime

from flask import Blueprint, jsonify, request, render_template
from db.ordersDB import OrdersDB
from db.inventoryDB import InventoryDB
from utils.utils import generate_id
from utils.order_utils import get_current_order_count, get_current_inventory_count, calculate_new_price
from utils.threading_utils import run_in_thread

# 创建蓝图对象
order_bp = Blueprint('orders', __name__, url_prefix='/orders')

key_translation = {
    'order_id': '订单编号',
    'order_type': '订单类型',
    'cargo_id': '货物编号',
    'price': '价格',
    'provider': '供应商',
    'project': '项目',
    'status': '状态',
    'employee_id': '员工编号',
    'published_at': '发布时间',
    'processed_at': '处理时间',
    'count': '数量'
}


@order_bp.route('/all', methods=['GET'])
def get_all_orders():
    try:
        with OrdersDB() as db:
            res = db.list_orders(order_id=None)
            if res:
                return jsonify({"success": True, "data": res})
                # print(res)
                # return render_template('table.html', data=res, key_translation=key_translation)
            else:
                return jsonify({"success": False, "message": "无订单数据"})
    except Exception as e:
        return jsonify({"error": str(e)})


@order_bp.route('/<order_id>', methods=['GET'])
def get_order_by_id(order_id):
    try:
        with OrdersDB() as db:
            res = db.list_orders(order_id)
            if res:
                return jsonify({"success": True, "data": res})
            else:
                return jsonify({"success": False, "message": "订单不存在"})
    except Exception as e:
        return jsonify({"error": str(e)})


@order_bp.route('/search', methods=['GET'])
def get_order_by_search():
    # 获取url中的查询条件并转为字典
    query = request.args.to_dict()
    try:
        with OrdersDB() as db:
            # 根据cargo_name和model获取cargo_id用于查询
            cargo_name = query['cargo_name']
            model = query['model']
            if cargo_name and model:
                query_result = db.get_cargo_id_by_cargo_name_model(cargo_name, model)
                if query_result:
                    query.update({'cargo_id': query_result['cargo_id']})
                else:
                    query.update({'cargo_id': ""})

            employee_name = query['employee_name']
            if employee_name:
                query_result = db.get_employee_id_by_name(employee_name)
                print(f'query_result: {query_result}')
                if query_result:
                    query.update({'employee_id': query_result['employee_id']})
            del query['cargo_name'], query['model'], query['employee_name']
            res = db.search_orders_by_condition(query)
            if res:
                return jsonify({"success": True, "data": res}), 200
            else:
                return jsonify({"success": False, "data": ""}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@order_bp.route('/create', methods=['POST'])
def create_order():
    data = request.get_json()
    try:
        with OrdersDB() as db:
            # 获取当天的订单数量，用于构造订单id
            count = db.get_today_order_count()
            # 获取当天日期的str类型
            current_date = datetime.now()
            formatted_date = current_date.strftime("%Y%m%d")
            # 构造order id: 202411010001
            order_id = formatted_date + generate_id(count)

            # 判断给定的货品名和型号在inventory表中是否已存在
            cargo_name = data['cargo_name']
            model = data['model']
            cargo_id = db.get_cargo_id_by_cargo_name_model(cargo_name, model)
            if not cargo_id:
                return jsonify({"success": False, "message": "库存条目中没有对应的货品名和型号，请先创建库存"})

            # 当前日期
            date_string = current_date.strftime("%Y-%m-%d")
            date_object = datetime.strptime(date_string, "%Y-%m-%d")

            # 构造数据
            order_info = {
                "order_id": order_id,
                "order_type": data['order_type'],
                "cargo_id": cargo_id['cargo_id'],
                "price": data['price'],
                "provider": data['provider'],
                "project": data['project'],
                "status": data['status'],
                "employee_id": data['employee_id'],
                "published_at": date_object,
                "processed_at": None,
                "count": data['count'],
            }
            res = db.create_order(order_info)
            if res:
                return jsonify({"success": True, "message": "订单创建成功"})
            else:
                return jsonify({"success": False, "message": "订单创建失败"})
    except Exception as e:
        return jsonify({"error": str(e)})


@order_bp.route('/update/<order_id>', methods=['POST'])
def update_order(order_id):
    try:
        with OrdersDB() as o_db:
            exists = o_db.order_exists(order_id)
            if not exists:
                return jsonify({"success": False, "message": "订单不存在"})
            data = request.get_json()
            # 获得订单的当前状态(waiting, pass or reject)
            currentData = o_db.list_orders(order_id)
            currentStatus = currentData['status']
            print(currentStatus)
            # 获得订单的类型(出库or入库)
            order_type = currentData['order_type']
            print(f'order_type: {order_type}')
            # 获得订单要出库或入库的数量
            operated_count = get_current_order_count(o_db, order_id)
            print(f'operated_count: {operated_count}')
            # 获得当前数量
            origin_count = get_current_inventory_count(o_db, order_id)
            print(f'origin_count: {origin_count}')

            if currentStatus == 'waiting' and data['status'] == 'pass':
                res1 = None
                # 当订单类型为入库时
                if order_type == 'inbound':
                    # 计算新的库存数量
                    new_count = origin_count + operated_count
                    # 计算单价的加权平均数
                    new_price = calculate_new_price(o_db, order_id)
                    # 更新库存：数量和新的单价
                    res1 = o_db.update_inventory(order_id, new_count, new_price)
                # 当订单类型为出库时
                if order_type == 'outbound':
                    # 计算新的数量
                    new_count = origin_count - operated_count
                    # 更新库存：库存数量
                    res1 = o_db.update_inventory(order_id, new_count)
                # 更新订单状态
                res2 = o_db.update_order_by_id(order_id=order_id, status=data['status'])
                if res1 and res2:
                    return jsonify({"success": True, "message": "订单已确认"})
                else:
                    return jsonify({"success": False, "message": "订单状态更新失败"})
            # 当订单被取消时：只修改订单状态为取消，不对库存进行变更
            if currentStatus == 'waiting' and data['status'] == 'reject':
                res = o_db.update_order_by_id(order_id=order_id, status=data['status'])
                if res:
                    return jsonify({"success": True, "message": "订单已被取消"})
                else:
                    return jsonify({"success": False, "message": "订单状态更新失败"})
            # 一旦订单被确认(通过或取消)，不允许修改订单状态
            if currentStatus == 'pass' or currentStatus == 'reject':
                return jsonify({"success": False, "message": "不被允许的操作"})
    except Exception as e:
        return jsonify({"error": str(e)})


