from datetime import timedelta

import jwt
from flask import Flask, session, request, jsonify

from config.settings import TOKEN_SECRET_KEY
from routes.users import users_bp
from routes.employee import employee_bp
from routes.inventory import inventory_bp
from routes.orders import order_bp
from routes.providers import provider_bp
from routes.project import project_bp
from task import start_scheduler_in_thread
from utils.token_authentication import verify_token

app = Flask(__name__)

app.register_blueprint(users_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(order_bp)
app.register_blueprint(provider_bp)
app.register_blueprint(project_bp)

# @app.before_request
def global_token_verification():
    # 获取当前路由
    endpoint = request.path  # 使用 `request.path` 获取完整的 URL 路径

    # 排除不需要 Token 验证的路由
    exempt_routes = ["/users/login", "/users/logout"]  # 列出所有不需要验证的路由

    if endpoint in exempt_routes:
        return  # 直接放行

    # 对其他路由强制执行 Token 验证
    token = request.headers.get('Authorization')

    if not token or not token.startswith("Bearer "):
        return jsonify({
            "success": False,
            "message": "Token is missing or improperly formatted."
        }), 401

    token = token.split(" ")[1]

    try:
        # 解码 Token
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=["HS256"])
        request.user = payload  # 将解码后的信息注入 request 对象
        if verify_token(payload):
            return jsonify({
                "success": False,
                "message": "Token is Invalid."
            }), 401
    except jwt.ExpiredSignatureError:
        return jsonify({
            "success": False,
            "message": "Token has expired. Please log in again."
        }), 401
    except jwt.InvalidTokenError:
        return jsonify({
            "success": False,
            "message": "Invalid token. Please log in again."
        }), 401


if __name__ == '__main__':
    start_scheduler_in_thread()
    app.run(debug=True)
