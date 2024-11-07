from datetime import datetime
from functools import wraps
from flask import session, redirect, url_for, flash, jsonify
from pypinyin import pinyin, Style


def convert_name_to_pinyin(name: str) -> str:
    pinyin_result = pinyin(name, style=Style.NORMAL)  # 默认拼音形式
    # 拼接拼音为字符串
    pinyin_string = ''.join([item[0] for item in pinyin_result])
    return pinyin_string


def generate_id(count: int) -> str:
    numeric_part = str(count + 1).zfill(4)
    return f"{numeric_part}"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查 session 中的 'login' 是否存在，且为 True
        if not session.get('login'):  # 如果没有 'login' 或其值为 False
            # 返回 401 状态码表示未授权
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        return f(*args, **kwargs)  # 如果用户已登录，继续执行原函数
    return decorated_function




