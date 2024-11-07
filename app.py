from datetime import timedelta

from flask import Flask, session, request, jsonify

from routes.users import users_bp
from routes.employee import employee_bp
from routes.inventory import inventory_bp
from routes.orders import order_bp
from routes.providers import provider_bp
from routes.project import project_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # 设置过期时间为 30 分钟

app.register_blueprint(users_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(order_bp)
app.register_blueprint(provider_bp)
app.register_blueprint(project_bp)


@app.before_request
def before_request_handler():
    session.permanent = True

    # 如果是登录和登出等不需要验证的路由，跳过检查
    if request.endpoint in ['users.login', 'users.logout']:
        return

    # 检查 session 中的 'login' 是否存在且为 True
    if not session.get('login'):
        return jsonify({'error': 'Unauthorized, please login first'}), 401


if __name__ == '__main__':
    app.run(debug=True)
