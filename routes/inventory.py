from decimal import Decimal

from flask import Blueprint, jsonify, request
from utils.app_logger import get_logger
from utils.token_authentication import decode_token
from db.inventoryDB import InventoryDB
from utils.utils import generate_id

inventory_bp = Blueprint('inventories', __name__, url_prefix='/inventory')
info_logger = get_logger(logger_name='InfoLogger', log_file='app.log')
error_logger = get_logger(logger_name='ErrorLogger', log_file='error.log')

@inventory_bp.route('/count', methods=['GET'])
def get_data_count():
    category = request.args.get('category')
    cargo_name = request.args.get('cargo_name')
    model = request.args.get('model')
    try:
        with InventoryDB() as db:
            if not category and not cargo_name and not model:
                count = db.show_inventory_count()
            else:
                data = {
                    "category": category,
                    "cargo_name": cargo_name,
                    "model": model
                }
                count = db.show_inventory_count(data)
                print(f'get count: {count}')
            return jsonify({"success": True, "count": count}) if count != 0 else jsonify({"success": False})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({"error": str(e)})


@inventory_bp.route('/page/<page_number>', methods=['GET'])
# @token_required
def list_inventories_by_page(page_number):
    print(request.headers)
    category = request.args.get('category')
    try:
        with InventoryDB() as db:
            if not category:
                res = db.show_inventories_paginated(page=int(page_number))
            elif category:
                print(f'data: {category}')
                res = db.show_inventories_paginated(page=int(page_number), category=category)

            return jsonify({"success": True, "data": res}) if res else jsonify(
                {"success": False, "message": "没有库存数据"})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({"error": str(e)})


@inventory_bp.route('/all', methods=['GET'])
def get_all_inventories():
    category = request.args.get('category')
    try:
        with InventoryDB() as db:
            res = db.get_all_inventories(category=category)
            if res:
                return jsonify({"success": True, "data": res})
            else:
                return jsonify({"success": False, "message": "无数据"})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({"error": str(e)})


@inventory_bp.route('/<cargo_id>', methods=['GET'])
def get_inventory_by_id(cargo_id):
    try:
        with InventoryDB() as db:
            inventory = db.get_inventory_by_id(cargo_id)
            if inventory:
                return jsonify({"success": True, "inventory": inventory})
            else:
                return jsonify({"success": False, "message": "记录不存在"})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({"error": str(e)})


@inventory_bp.route('/create', methods=['POST'])
def create_inventory():
    data = request.get_json()
    _, login_user_id = decode_token(request.headers.get('Authorization'))
    try:
        with InventoryDB() as db:
            cargo_name = data.get("cargo_name")
            model = data.get("model")
            data_model_exists = db.cargo_model_exists(cargo_name, model)
            if data_model_exists:
                return jsonify({"success": False, "message": "该产品和型号已存在, 无需新建条目"})
            else:
                count = db.get_total_inventory_count()
                cargo_id = "C" + generate_id(count)
                newData = {
                    "cargo_id": cargo_id,
                    "cargo_name": cargo_name,
                    "model": model,
                    "categories": data.get("categories"),
                    "count": int(data.get("count")),
                    "price": float(data.get('price'))
                }
                res = db.create_inventory(inventory_info=newData)
                if res:
                    info_logger.info(f"用户 {login_user_id} 创建了新的库存条目 {cargo_id};")
                    return jsonify({"success": True, "message": "成功创建库存条目"})
                else:
                    return jsonify({"success": False, "message": "创建条目失败"})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({"error": str(e)})


@inventory_bp.route('/import', methods=['POST'])
def import_inventory():
    try:
        _, login_user_id = decode_token(request.headers.get('Authorization'))
        data = request.get_json()
        dataset = data['dataset']
        length = len(data['dataset'])
        skipped, imported = 0, 0
        skipped_row = []
        with InventoryDB() as db:
            for i in range(length):
                count = db.get_total_inventory_count()
                cargo_id = "C" + generate_id(count)
                dataset[i].update({'cargo_id': cargo_id})
                exists = db.cargo_model_exists(dataset[i].get('cargo_name'), dataset[i].get('model'))
                if exists:
                    skipped += 1
                    skipped_row.append(f'{i}. {dataset[i].get("cargo_name")} - {dataset[i].get("model")}')
                else:
                    res = db.create_inventory(inventory_info=dataset[i])
                    imported += 1 if res else 0
        if imported == 0:
            return jsonify({"success": False, "skipped_row": skipped_row})
        else:
            info_logger.info(f'用户 {login_user_id} 执行了批量导入库存条目操作;')
            return jsonify({"success": True, "imported": imported, "skipped": skipped, "skipped_row": skipped_row})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({"error": str(e)})


@inventory_bp.route('/update/<cargo_id>', methods=['POST'])
def update_inventory_by_id(cargo_id):
    _, login_user_id = decode_token(request.headers.get('Authorization'))
    data = request.get_json()
    try:
        with InventoryDB() as db:
            data["cargo_id"] = cargo_id
            print(data)
            res = db.update_inventory(data)
            if res:
                info_logger.info(f'用户 {login_user_id} 更新了库存条目 {cargo_id} 的信息;')
                return jsonify({'success': True, 'message': '库存记录更新成功'})
            else:
                return jsonify({'success': False, 'message': '库存记录更新失败'})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({"error": str(e)})


@inventory_bp.route('/categories/get', methods=['GET'])
def get_categories():
    try:
        with InventoryDB() as db:
            categories = db.get_categories()
            print(categories)
            if categories:
                return jsonify({"success": True, "categories": categories}), 200
            else:
                return jsonify({"success": False, "message": "没有分类数据"}), 401
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({"error": str(e)}), 500


@inventory_bp.route('/delete', methods=['DELETE'])
def batch_delete_inventory():
    _, login_user_id = decode_token(request.headers.get('Authorization'))
    data = request.get_json()
    id_list = data['ids']
    try:
        with InventoryDB() as db:
            res = db.batch_delete_inventories(id_list=id_list)
            if res:
                info_logger.info(f'用户 {login_user_id} 执行了批量删除; 被删除的条目: {id_list}')
                return jsonify({'success': True, 'message': '批量删除成功'}), 200
            else:
                return jsonify({'success': False}), 401
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({"error": str(e)}), 500


@inventory_bp.route('/search', methods=['GET'])
def search_inventory():
    cargo_name = request.args.get('cargo_name')
    model = request.args.get('model')
    category = request.args.get('category')
    data = {
        "cargo_name": cargo_name,
        "model": model,
        "category": category
    }
    try:
        with InventoryDB() as db:
            if not data['category']:
                res = db.get_inventory_by_name_and_model(data=data)
            else:
                res = db.search_by_category(data['category'])
            return jsonify({"success": True, "data": res}) if res else jsonify(
                {"success": False, 'message': "没有匹配的数据"})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({"error": str(e)}), 500
