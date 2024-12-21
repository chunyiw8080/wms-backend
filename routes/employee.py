from flask import Blueprint, jsonify, request
from db.employeeDB import EmployeeDB
from utils.token_authentication import decode_token
from utils.utils import generate_id
from utils.app_logger import get_logger

# 创建蓝图对象
employee_bp = Blueprint('employees', __name__, url_prefix='/employees')

info_logger = get_logger(logger_name='InfoLogger', log_file='app.log')
error_logger = get_logger(logger_name='ErrorLogger', log_file='error.log')


@employee_bp.route('/all', methods=['GET'])
def list_all_employees():
    try:
        with EmployeeDB() as db:
            employees = db.fetch_employees()
            if employees:
                return jsonify({"success": True, "data": employees})
            else:
                return jsonify({"success": False, "message": "没有员工数据"})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)}), 500


@employee_bp.route('/create', methods=['POST'])
def create_employees():
    _, login_user_id = decode_token(request.headers.get('Authorization'))
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
                info_logger.info(f'用户 {login_user_id} 创建了新的员工条目 {employee_id};')
                return jsonify({"success": True, "message": "员工条目已成功创建"})
            else:
                return jsonify({"success": False, "message": "创建员工条目失败"})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)}), 500


@employee_bp.route('/<employee_id>', methods=['GET'])
def list_employee_by_id(employee_id):
    try:
        with EmployeeDB() as db:
            employee = db.get_employee_by_name_or_id(employee_id=employee_id)
            if employee:
                return jsonify({"success": True, "data": employee})
            else:
                return jsonify({"success": False, "message": "用户不存在"})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)}), 500


@employee_bp.route('/search', methods=['GET'])
def search_employees_by_conditions():
    condition = request.args.get('condition')
    try:
        with EmployeeDB() as db:
            res = db.search_employee(condition=condition)
            if res:
                return jsonify({"success": True, "data": res})
            else:
                return jsonify({"success": False, "message": "无数据"})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)}), 500


@employee_bp.route('/delete', methods=['DELETE'])
def delete_employee_by_id():
    data = request.get_json()
    id_list = data.get('ids')
    try:
        with EmployeeDB() as db:
            for employee_id in id_list:
                print(employee_id)
                exists = db.employee_exists(employee_id=employee_id)
                if exists:
                    res = db.delete_employee(employee_id=employee_id)
                    if not res:
                        return jsonify({"success": False, "message": "删除失败"}), 401
            return jsonify({"success": True}), 200
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)}), 500


@employee_bp.route('/update/<employee_id>', methods=['POST'])
def update_employee(employee_id):
    _, login_user_id = decode_token(request.headers.get('Authorization'))
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
                    info_logger.info(f'用户 {login_user_id} 编辑了员工信息 {employee_id};')
                    return jsonify({"success": True, "message": "员工信息已成功更新"}), 200
                else:
                    return jsonify({"success": False, "message": "更新失败"}), 401
            else:
                return jsonify({"success": False, "message": "用户不存在"}), 401
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)}), 500
