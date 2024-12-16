from flask import Blueprint, jsonify, request
from utils.app_logger import get_logger
from db.provider_projectDB import ProviderProjectDB
from utils.token_authentication import decode_token

project_bp = Blueprint('project', __name__, url_prefix='/project')
info_logger = get_logger(logger_name='InfoLogger', log_file='app.log')
error_logger = get_logger(logger_name='ErrorLogger', log_file='error.log')

@project_bp.route('/all', methods=['GET'])
def list_project():
    try:
        with ProviderProjectDB() as db:
            data = db.list('project')
            if data:
                return jsonify({'success': True, 'data': data})
            else:
                return jsonify({'success': False, 'data': ""})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})


@project_bp.route('/create', methods=['POST'])
def create_project():
    token = request.headers.get('Authorization')
    _, login_user_id = decode_token(token)
    data = request.get_json()
    project_name = data['project_name']
    try:
        with ProviderProjectDB() as db:
            exists = db.data_exists('project', 'project_name', project_name)
            if exists:
                return jsonify({'success': False, 'message': '供应商已存在'})
            else:
                res = db.create('project', 'project_name', project_name)
                if res:
                    info_logger.info(f'用户 {login_user_id} 创建了新的项目 {project_name};')
                    return jsonify({'success': True, 'message': '供应商已添加'})
                else:
                    return jsonify({'success': False, 'message': '添加失败'})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})


@project_bp.route('/delete/<project_name>', methods=['DELETE'])
def delete_project(project_name):
    try:
        with ProviderProjectDB() as db:
            exists = db.data_exists('project', 'project_name', project_name)
            if not exists:
                return jsonify({'success': False, 'message': '供应商不存在'})
            else:
                res = db.delete('project', 'project_name', project_name)
                if res:
                    return jsonify({'success': True, 'message': '供应商已删除'})
                else:
                    return jsonify({'success': False, 'message': '删除失败'})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})

@project_bp.route('/search', methods=['GET'])
def search_project():
    project_name = request.args.get('name')
    try:
        with ProviderProjectDB() as db:
            res = db.search('project', 'project_name', project_name)
            print(res)
            if res:
                return jsonify({'success': True, 'data': [res]})
            else:
                return jsonify({'success': False})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})

@project_bp.route('/update/<project_name>', methods=['POST'])
def update_project(project_name):
    token = request.headers.get('Authorization')
    _, login_user_id = decode_token(token)
    data = request.get_json()
    print(data['project_name'])
    try:
        with ProviderProjectDB() as db:
            res = db.update('project', 'project_name', data['project_name'], project_name)
            if res:
                info_logger.info(f'用户 {login_user_id} 更新了项目 {project_name} 的信息;')
                return jsonify({'success': True})
            else:
                return jsonify({'success': False})
    except Exception as e:
        error_logger.error(f'{request.url} - {str(e)}')
        return jsonify({'error': str(e)})

