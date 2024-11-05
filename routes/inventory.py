from decimal import Decimal

from flask import Blueprint, jsonify, request
from unicodedata import decimal

from db.inventoryDB import InventoryDB
from utils.utils import generate_id
inventory_bp = Blueprint('inventories', __name__, url_prefix='/inventory')


@inventory_bp.route('/all', methods=['GET'])
def list_inventories():
    try:
        with InventoryDB() as db:
            inventories = db.show_inventories()
            if inventories:
                return jsonify({"success": True, "inventories": inventories})
            else:
                return jsonify({"success": False, "message": "没有库存数据"})
    except Exception as e:
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
        return jsonify({"error": str(e)})


@inventory_bp.route('/create', methods=['POST'])
def create_inventory():
    data = request.get_json()
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
                    "price": Decimal(str(data['price']))
                }
                res = db.create_inventory(inventory_info=newData)
                if res:
                    return jsonify({"success": True, "message": "成功创建库存条目"})
                else:
                    return jsonify({"success": False, "message": "创建条目失败"})
    except Exception as e:
        return jsonify({"error": str(e)})
