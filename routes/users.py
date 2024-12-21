import jwt
from datetime import datetime
from flask import Blueprint, jsonify, request

from db.userDB import UserDB
from db.employeeDB import EmployeeDB
from utils.app_logger import get_logger
from utils.utils import generate_id
from utils.token_authentication import generate_token, decode_token
from config.settings import TOKEN_SECRET_KEY

# 创建蓝图对象
users_bp = Blueprint('users', __name__, url_prefix='/users')

info_logger = get_logger(logger_name='InfoLogger', log_file='app.log')
error_logger = get_logger(logger_name='ErrorLogger', log_file='error.log')


# 返回全部用户
@users_bp.route('/all', methods=['GET'])
def list_all_users():
    try:
        with UserDB() as db:
            users = db.fetch_users()
            if users:
                return jsonify({'success': True, 'users': users}), 200
            else:
                return jsonify({'success': False, 'message': 'No users found'}), 404
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)}), 500


# 返回指定user_id的用户
@users_bp.route('/<user_id>', methods=['GET'])
def list_user_by_id(user_id):
    try:
        with UserDB() as db:
            user = db.fetch_user_by_id(user_id)
            if user:
                return jsonify({"success": True, "user": user})
            else:
                return jsonify({"success": False, "message": "用户不存在"})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)}), 500


@users_bp.route('/search', methods=['GET'])
def search_user():
    condition = request.args.get('condition')
    try:
        with UserDB() as db:
            res = db.fetch_user_by_id_or_username(condition)
            if res:
                print(res)
                return jsonify({"success": True, "data": [res]})
            else:
                return jsonify({'success': False})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})


# 登录验证
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    hashed_password = data.get('password')
    try:
        with UserDB() as db:
            token = request.headers.get('Authorization')
            if token and token.startswith("Bearer "):
                token = token.split(" ")[1]
                payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=["HS256"])
                token_id = payload.get('token_id')

                res = db.verify_token(token_id)
                if res:
                    return jsonify({"success": False, "message": 'Invalid token'}), 401
            result = db.login_authentications(username, hashed_password)
            if not result:
                return jsonify({"success": False})
            else:
                user_id = result.get('user_id')
                privilege = result.get('privilege')
                token = generate_token(user_id, privilege)

                info_logger.info(f'用户 {username} 登录;')
                return jsonify({"success": True, "token": token}), 200
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)}), 500


@users_bp.route('/create', methods=['POST'])
def create_user():
    token = request.headers.get('Authorization')
    _, login_user_id = decode_token(token)
    data = request.get_json()
    # print(data)
    employee_name = data.get('employee_name')
    try:
        with EmployeeDB() as e_db:
            employee_id = e_db.get_employee_by_name_or_id(employee_id=None, employee_name=employee_name)['employee_id']
            print(f'employee_id: {employee_id}')
            # 验证员工是否已存在，若给定的员工姓名不匹配数据库中的任何记录，返回错误
            if not employee_id:
                return jsonify(
                    {"success": False, "message": "该员工id不存在, 请先创建员工数据!"}), 401
        with UserDB() as u_db:
            total = u_db.get_user_count()
            user_id = "U" + generate_id(total)
            print(f'user_id: {user_id}')
            # 验证数据库用户名在数据库中是否已存在
            username = request.json.get('username')
            exists = u_db.user_exists(username=username)
            if exists:
                return jsonify({"success": False, "message": "该用户名已存在"})

            # 构造数据集
            data = {
                'user_id': user_id,
                'username': data.get('username'),
                'password':  data.get('password'),
                'employee_id': employee_id,
                'created_at': datetime.now().date(),
                'status': data.get('status'),
                'privilege': data.get('privilege')
            }
            res = u_db.create_user(data)
            if res:
                info_logger.info(f'用户 {login_user_id} 创建了新用户 {user_id}')
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False}), 401
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)}), 500


@users_bp.route('/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        with UserDB() as db:
            res = db.delete_user(user_id)
            if res:
                return jsonify({"success": True, "message": "已成功删除用户"}), 200
            else:
                return jsonify({"success": False, "message": "该用户不存在"}), 401
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)}), 500


@users_bp.route('/update/<user_id>', methods=['POST'])
def update_user(user_id):
    token = request.headers.get('Authorization')
    _, login_user_id = decode_token(token)
    data = request.get_json()
    try:
        with UserDB() as db:
            exists = db.fetch_user_by_id(user_id=user_id)
            if not exists:
                return jsonify({"success": False, "message": "用户不存在"})
            newData = {
                "password": data.get('password'),
                "status": data.get('status'),
                "privilege": data.get('privilege')
            }
            # print(newData)
            res = db.update_user(user_id, newData)
            if res:
                info_logger.info(f'用户 {login_user_id} 更新了用户 {user_id} 的信息')
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False}), 401
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)}), 500


@users_bp.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    print(token)
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
        try:
            payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=["HS256"])
            token_id = payload.get('token_id')  # 从 payload 中获取 token ID
            user_id = payload.get('user_id')
            with UserDB() as db:
                res = db.destroy_token(token_id=token_id, user_id=user_id)
                if res:
                    return jsonify({"success": True, "token_id": token_id, "user_id": user_id})
                else:
                    return jsonify({"success": False}), 401
        except Exception as e:
            error_logger.error(f'{request.url} - {str(e)}')
            return jsonify({"error": str(e)})
