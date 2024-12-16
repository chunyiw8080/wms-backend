import os
from utils.app_logger import get_logger
from flask import Blueprint, jsonify, request

# info_logger = get_logger(logger_name='InfoLogger', log_file='app.log')
error_logger = get_logger(logger_name='ErrorLogger', log_file='error.log')
logs_bp = Blueprint('logs', __name__, url_prefix='/logs')


@logs_bp.route('/getfiles', methods=['GET'])
def get_log_files():
    """
    读取日志列表
    """
    log_dir = os.path.abspath('./logs/')
    try:
        files = os.listdir(log_dir)
        filtered_files = [file for file in files if file.startswith("app")]
        if len(filtered_files) == 0:
            return jsonify({'success': False})
        else:
            return jsonify({'success': True, 'data': filtered_files})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'success': False})

@logs_bp.route('/content/<filename>', methods=['GET'])
def get_log_content(filename):
    """
    根据给定的日志文件名读取其内容
    :param filename: 日志文件名
    :return: json形式的日志文本数据
    """
    log_dir = os.path.abspath('./logs/')
    file_path = os.path.join(log_dir, filename)

    try:
        if filename not in os.listdir(log_dir):
            return jsonify({'success': False}), 403

        if not os.path.isfile(file_path):
            return jsonify({'success': False}), 404

        with open(file_path, 'r', encoding='utf-8') as file:
            log_content = file.readlines()
        if log_content is not None:
            return jsonify({'success': True, 'data': log_content})
        else:
            return jsonify({'success': False})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'success': False})