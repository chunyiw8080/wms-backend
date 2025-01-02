import os

DB_HOST = os.getenv('DB_HOST', 'default_host')
DB_USER = os.getenv('DB_USER', 'default_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'default_password')
DB_NAME = os.getenv('DB_NAME', 'default_db')
DB_PORT = os.getenv('DB_PORT', 3306)

TOKEN_SECRET_KEY = os.getenv('TOKEN_SECRET_KEY', 'default_token')