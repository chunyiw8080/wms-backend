from flask import Blueprint, jsonify, request

from db.provider_projectDB import ProviderProjectDB

provider_bp = Blueprint('providers', __name__, url_prefix='/providers')


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
        return jsonify({'error': str(e)})


@provider_bp.route('/create', methods=['POST'])
def create_provider():
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
                    return jsonify({'success': True, 'message': '供应商已添加'})
                else:
                    return jsonify({'success': False, 'message': '添加失败'})
    except Exception as e:
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
        return jsonify({'error': str(e)})
