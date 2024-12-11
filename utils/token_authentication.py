from functools import wraps

import jwt, uuid, datetime
from flask import jsonify, request
from pytz import timezone
from config.settings import TOKEN_SECRET_KEY
from db.userDB import UserDB


def generate_token(user_id, permissions):
    china_timezone = timezone('Asia/Shanghai')
    now = datetime.datetime.now(china_timezone)
    payload = {
        'token_id': str(uuid.uuid4()),
        'user_id': user_id,
        'permissions': permissions,  # 用户权限信息
        'exp': now + datetime.timedelta(hours=2),  # Token 有效期
        'iat': now  # 签发时间
    }
    return jwt.encode(payload, TOKEN_SECRET_KEY, algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
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
            request.user = payload  # 将解码后的信息注入 request 对象，供后续逻辑使用
            if verify_token(payload) is True:
                return jsonify({
                    "success": False,
                    "message": "Token is Invalid."
                })
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

        return f(*args, **kwargs)  # 调用原始视图函数

    return decorated

def verify_token(payload):
    token_id = payload.get('token_id')
    try:
        with UserDB() as db:
            res = db.verify_token(token_id)
            return res
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
