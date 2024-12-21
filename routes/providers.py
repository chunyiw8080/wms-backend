from flask import Blueprint, jsonify, request

from utils.app_logger import get_logger
from db.provider_projectDB import ProviderProjectDB
from utils.token_authentication import decode_token

provider_bp = Blueprint('providers', __name__, url_prefix='/providers')

info_logger = get_logger(logger_name='InfoLogger', log_file='app.log')
error_logger = get_logger(logger_name='ErrorLogger', log_file='error.log')

@provider_bp.route('/all', methods=['GET'])
def list_providers():
    try:
        with ProviderProjectDB() as db:
            data = db.list('provider')
            if data:
                return jsonify({'success': True, 'data': data})
            else:
                return jsonify({'success': False, 'data': ""})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})


@provider_bp.route('/create', methods=['POST'])
def create_provider():
    token = request.headers.get('Authorization')
    _, login_user_id = decode_token(token)
    data = request.get_json()
    provider_name = data['provider_name']
    print(f'Provider: {provider_name}')
    try:
        with ProviderProjectDB() as db:
            exists = db.data_exists('provider', 'provider_name', provider_name)
            if exists:
                return jsonify({'success': False, 'message': '供应商已存在'})
            else:
                res = db.create('provider', 'provider_name', provider_name)
                if res:
                    info_logger.info(f'用户 {login_user_id} 创建了新的供应商条目;')
                    return jsonify({'success': True, 'message': '供应商已添加'})
                else:
                    return jsonify({'success': False, 'message': '添加失败'})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})


@provider_bp.route('/delete/<provider_name>', methods=['DELETE'])
def delete_provider(provider_name):
    try:
        with ProviderProjectDB() as db:
            exists = db.data_exists('provider', 'provider_name', provider_name)
            if not exists:
                return jsonify({'success': False, 'message': '供应商不存在'})
            else:
                res = db.delete('provider', 'provider_name', provider_name)
                if res:
                    return jsonify({'success': True, 'message': '供应商已删除'})
                else:
                    return jsonify({'success': False, 'message': '删除失败'})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})

@provider_bp.route('/search', methods=['GET'])
def search_project():
    provider_name = request.args.get('name')
    try:
        with ProviderProjectDB() as db:
            res = db.search('provider', 'provider_name', provider_name)
            print(res)
            if res:
                return jsonify({'success': True, 'data': [res]})
            else:
                return jsonify({'success': False})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})

@provider_bp.route('/update/<provider_name>', methods=['POST'])
def update_project(provider_name):
    _, login_user_id = decode_token(request.headers.get('Authorization'))
    data = request.get_json()
    try:
        with ProviderProjectDB() as db:
            res = db.update('provider', 'provider_name', data['provider_name'], provider_name)
            if res:
                info_logger.info(f'用户 {login_user_id} 更新了供应商 {provider_name} 的信息;')
                return jsonify({'success': True})
            else:
                return jsonify({'success': False})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})
