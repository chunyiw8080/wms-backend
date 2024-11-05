from threading import Thread
from functools import wraps
from flask import jsonify, request, copy_current_request_context


def run_in_thread(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # 复制当前请求上下文
        @copy_current_request_context
        def run():
            return fn(*args, **kwargs)

        thread = Thread(target=run)
        thread.start()
        return jsonify({"success": True, "message": "请求正在处理"}), 202

    return wrapper






