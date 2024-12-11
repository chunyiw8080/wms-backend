from datetime import datetime
from typing import Dict
from weasyprint import HTML
from io import BytesIO
from flask import Blueprint, jsonify, request, render_template, send_file
from db.ordersDB import OrdersDB
from db.inventoryDB import InventoryDB
from db.employeeDB import EmployeeDB
from utils.utils import generate_id
from utils.order_utils import get_current_order_count, get_current_inventory_count, calculate_new_price
from utils.threading_utils import run_in_thread
from utils.token_authentication import token_required

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
            res = db.get_full_orders()
            if res:
                return jsonify({"success": True, "data": res})
                # print(res)
                # return render_template('table.html', data=res, key_translation=key_translation)
            else:
                return jsonify({"success": False, "message": "无订单数据"})
    except Exception as e:
        return jsonify({"error": str(e)})


@order_bp.route('/page/<page_number>', methods=['GET'])
def get_order_pagination(page_number):
    try:
        with OrdersDB() as db:
            res = db.get_orders_by_page(page_number)
            if res:
                return jsonify({"success": True, "data": res})
            else:
                return jsonify({"success": False})
    except Exception as e:
        return jsonify({"error": str(e)})


@order_bp.route('/count', methods=['GET'])
def get_order_count():
    try:
        with OrdersDB() as db:
            res = db.get_order_count()
            if res:
                return jsonify({"success": True, "data": res})
            else:
                return jsonify({"success": False})
    except Exception as e:
        return jsonify({"error": str(e)})


@order_bp.route('/<order_id>', methods=['GET'])
def get_order_by_id(order_id):
    try:
        with OrdersDB() as db:
            res = db.search_orders_by_condition(order_id=order_id)
            if res:
                return jsonify({"success": True, "data": res})
            else:
                return jsonify({"success": False, "message": "订单不存在"})
    except Exception as e:
        return jsonify({"error": str(e)})


@order_bp.route('/search', methods=['GET'])
def get_order_by_search():
    # 获取url中的查询条件并转为字典
    condition = request.args.to_dict()
    print(condition)
    try:
        with OrdersDB() as db:
            res = db.search_orders_by_condition(conditions=condition)
            print("res: ", res)
            if res:
                return jsonify({"success": True, "data": res})
            else:
                return jsonify({"success": False})
    except Exception as e:
        return jsonify({"error": str(e)})


def _validate_data(data: Dict[str, str]):
    try:
        with OrdersDB() as db:
            # 判断给定的货品名和型号在inventory表中是否已存在
            cargo_name = data['cargo_name']
            model = data['model']
            print(cargo_name, model)
            cargo_id = db.get_cargo_id_by_cargo_name_model(cargo_name, model)
            if not cargo_id:
                return {"success": False, "message": "库存条目中没有对应的货品名和型号，请先创建库存"}

            # 判断员工姓名是否已存在
            employee_name = data['employee_name']
            with EmployeeDB() as e_db:
                employee_id = e_db.get_employee_id_by_name(employee_name)
                print(employee_id.get("employee_id"))
                if not employee_id:
                    return {"success": False, "message": "员工不存在"}

        return {"success": True, "cargo_id": cargo_id, "employee_id": employee_id}
    except Exception as e:
        return {"success": False, "message": str(e)}


@order_bp.route('/create', methods=['POST'])
def create_order():
    data = request.get_json()
    print(f'order data: {data}')
    result = _validate_data(data)
    print(result)
    if result['success'] is False:
        message = result['message']
        return jsonify({"success": False, "message": message})
    cargo_id = result['cargo_id'].get('cargo_id')
    employee_id = result['employee_id'].get('employee_id')
    print(f'cargo_id, employee_id : {cargo_id}, {employee_id}')
    try:
        with OrdersDB() as db:
            # 获取当天的订单数量，用于构造订单id
            count = db.get_today_order_count()
            # 获取当天日期的str类型
            current_date = datetime.now()
            formatted_date = current_date.strftime("%Y%m%d")
            # 构造order id: 202411010001
            order_id = formatted_date + generate_id(count)

            """
            # 判断给定的货品名和型号在inventory表中是否已存在
            cargo_name = data['cargo_name']
            model = data['model']
            cargo_id = db.get_cargo_id_by_cargo_name_model(cargo_name, model)
            if not cargo_id:
                return jsonify({"success": False, "message": "库存条目中没有对应的货品名和型号，请先创建库存"})

            employee_name = data['employee_name']
            with EmployeeDB() as e_db:
                employee_id = e_db.get_employee_id_by_name(employee_name)
                print(employee_id.get("employee_id"))
                if not employee_id:
                    return jsonify({"success": False, "message": "员工不存在"})
            """

            # 当前日期
            date_string = current_date.strftime("%Y-%m-%d")
            date_object = datetime.strptime(date_string, "%Y-%m-%d")

            # 构造数据
            order_info = {
                "order_id": order_id,
                "order_type": data['order_type'],
                "cargo_id": cargo_id,
                "price": data['price'],
                "provider": data['provider'] if data['provider'] else 'null',
                "project": data['project'] if data['project'] else 'null',
                "status": data['status'],
                "employee_id": employee_id,
                "published_at": date_object,
                "processed_at": datetime(1970, 1, 1).strftime("%Y-%m-%d"),
                "count": data['count'],
            }
            res = db.create_order(order_info, single=True)
            if res:
                return jsonify({"success": True, "message": "订单创建成功"})
            else:
                return jsonify({"success": False, "message": "订单创建失败"})
    except Exception as e:
        return jsonify({"error": str(e)})

@order_bp.route('/import', methods=['POST'])
def batch_create():
    data = request.get_json()
    dataset = data['dataset']
    failed_order_ids = []
    try:
        with OrdersDB() as db:
            for item in dataset:
                res = db.create_order(item)
                print(res)
                print(item['order_id'])
                if not res:

                    failed_order_ids.append(item['order_id'])
            if failed_order_ids is None:
                return jsonify({"success": True})
            else:
                return jsonify({"success": True, "failed_order_ids": failed_order_ids})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


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
            # print(f'order_type: {order_type}')
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
                    new_price = calculate_new_price(o_db, order_id, 'inbound')
                    # 更新库存：数量和新的单价
                    res1 = o_db.update_inventory(order_id, new_count, new_price)
                # 当订单类型为出库时
                if order_type == 'outbound':
                    # 计算新的数量
                    new_count = origin_count - operated_count
                    # 更新库存：库存数量和新的单价
                    new_price = calculate_new_price(o_db, order_id, 'outbound')
                    res1 = o_db.update_inventory(order_id, new_count, new_price)
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

@order_bp.route('/print/<order_id>', methods=['GET'])
@token_required
def print_order(order_id):
    # Linux上安装依赖库
    # sudo apt update
    # sudo apt install -y libgobject-2.0-0 libcairo2 libpango-1.0-0 gir1.2-pango-1.0 gir1.2-gtk-3.0
    with OrdersDB() as o_db:
        order_data = o_db.print_orders(order_id)
        if order_data is not None:
            now_date = datetime.now().strftime("%Y-%m-%d")
            rendered_html = render_template('print-receipt.html', data=order_data, now_date=now_date)

            pdf_stream = BytesIO()  # 使用内存缓冲区存储 PDF
            HTML(string=rendered_html).write_pdf(pdf_stream)
            pdf_stream.seek(0)

            return send_file(pdf_stream, as_attachment=True, download_name=f"出入库单-{order_id}.pdf", mimetype="application/pdf")
        else:
            return jsonify({"success": False})

