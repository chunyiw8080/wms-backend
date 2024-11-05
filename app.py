from flask import Flask

from routes.users import users_bp
from routes.employee import employee_bp
from routes.inventory import inventory_bp
from routes.orders import order_bp
from routes.providers import provider_bp
from routes.project import project_bp

app = Flask(__name__)


app.register_blueprint(users_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(order_bp)
app.register_blueprint(provider_bp)
app.register_blueprint(project_bp)

if __name__ == '__main__':
    app.run(debug=True)
