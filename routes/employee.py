from flask import Blueprint, jsonify, request
from db.employeeDB import EmployeeDB
from utils.utils import generate_id

# 创建蓝图对象
employee_bp = Blueprint('employees', __name__, url_prefix='/employees')


@employee_bp.route('/all', methods=['GET'])
def list_all_employees():
    try:
        with EmployeeDB() as db:
            employees = db.fetch_employees()
            return jsonify(employees)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@employee_bp.route('/create', methods=['POST'])
def create_employees():
    data = request.get_json()
    try:
        with EmployeeDB() as db:
            count = db.get_employee_count()
            employee_id = "E" + generate_id(count)

            data = {
                "employee_id": employee_id,
                "employee_name": data.get('employee_name'),
                "gender": data.get('gender'),
                "position": data.get('position'),
            }
            res = db.create_employee(data)
            if res:
                return jsonify({"success": True, "message": "员工条目已成功创建"})
            else:
                return jsonify({"success": False, "message": "创建员工条目失败"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@employee_bp.route('/<employee_id>', methods=['GET'])
def list_employee_by_id(employee_id):
    try:
        with EmployeeDB() as db:
            employee = db.get_employee_by_name_or_id(employee_id=employee_id)
            if employee:
                return jsonify({"success": True, "employee": employee})
            else:
                return jsonify({"success": False, "message": "用户不存在"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@employee_bp.route('/delete/<employee_id>', methods=['DELETE'])
def delete_employee_by_id(employee_id):
    try:
        with EmployeeDB() as db:
            exists = db.employee_exists(employee_id=employee_id)
            if exists:
                res = db.delete_employee_by_id(employee_id=employee_id)
                if res:
                    return jsonify({"success": True, "message": "员工记录已删除"}), 200
                else:
                    return jsonify({"success": False, "message": "删除失败"}), 401
            else:
                return jsonify({"success": False, "message": "员工不存在"}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@employee_bp.route('/update/<employee_id>', methods=['PATCH'])
def update_employee(employee_id):
    try:
        with EmployeeDB() as db:
            exists = db.employee_exists(employee_id=employee_id)
            if exists:
                data = request.get_json()
                newData = {
                    "employee_name": data.get('employee_name'),
                    "gender": data.get('gender'),
                    "position": data.get('position')
                }
                res = db.update_employee(employee_id=employee_id, data=newData)
                print(f'res: {res}')
                if res:
                    return jsonify({"success": True, "message": "员工信息已成功更新"}), 200
                else:
                    return jsonify({"success": False, "message": "更新失败"}), 401
            else:
                return jsonify({"success": False, "message": "用户不存在"}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500