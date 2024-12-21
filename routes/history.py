from flask import Blueprint, jsonify, request
from db.historyDB import HistoryDB
from utils.token_authentication import decode_token
from utils.app_logger import get_logger

history_bp = Blueprint('history', __name__, url_prefix='/history')

info_logger = get_logger(logger_name='InfoLogger', log_file='app.log')
error_logger = get_logger(logger_name='ErrorLogger', log_file='error.log')


@history_bp.route('/search', methods=['GET'])
def search_history_by_date():
    year = request.args.get('year')
    month = request.args.get('month')
    print(year, month)
    try:
        with HistoryDB() as db:
            res = db.get_history_by_date(year, month)
            if res:
                return jsonify({'success': True, 'data': res})
            else:
                return jsonify({'success': False})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})


@history_bp.route('/import', methods=['POST'])
def bacth_insert():
    _, login_user_id = decode_token(request.headers.get('Authorization'))
    data = request.get_json()
    print(data)
    dataset = data.get("dataset")
    try:
        with HistoryDB() as db:
            res, succeed, failed = db.import_record(dataset)
            print(res)
            if res:
                info_logger.info(f'用户 {login_user_id} 批量导入了历史数据;')
            return jsonify({'success': res, 'succeed': succeed, 'failed': failed})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})
