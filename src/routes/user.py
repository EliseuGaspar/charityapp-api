from flasgger import swag_from
from flask import Blueprint, make_response, jsonify, request
from src.convertors.requests import Convertors
from src.controllers import UsersControllers
from src.utils.http_manager import HttpCodesResponses
from src.domain.securitys import RoutesSecurity


user_routes = Blueprint('user_routes', __name__)


@user_routes.get('/users')
@swag_from({
    'parameters': [
        {
            "in": "query",
            "name": "email",
            "required": False,
        }
]})
def get_users_endpoint(*args):
    """
    Busca os usuários no storage sistema
    ---
    responses:
        200: 
            description: ...
    """
    email = request.args.get('email')
    if not email:
        usuarios = UsersControllers().pegar_usuarios()
        return make_response(jsonify({
            'response': usuarios,
            'msg': 'retornado todos os usuários do storage'
        }))

    usuario = UsersControllers().pegar_usuario(email)
    
    if not usuario:
        return make_response(jsonify({
            'response': None,
            'msg': 'Não existe nenhum usuário com este email.'
        }))
    
    return make_response(jsonify({
        'response': usuario,
        'msg': f'Retornado os dados de {email}'
    }))

@user_routes.post('/users') 
@swag_from({
    'parameters': [
    {
    "in": "body",
    "name": "body",
    "required": True,
    "schema": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "required": True
            },
            "senha": {
                "type": "string",
                "required": True
            },
            "nome": {
                "required": True,
                "type": "string"
            },
            "sobrenome": {
                "type": "string",
                "required": True
            },
            "provincia": {
                "type": "string",
                "required": True
            },
            "municipio": {
                "required": True,
                "type": "string"
            },
            "bi": {
                "type": "string",
                "required": True
            },
            "telefone": {
                "required": True,
                "type": "string"
            }
        }
    }
}]})
def register_user_endpoint(*args):
    """
    Resgistra usuário no storage do sistema
    ---
    responses:
            200: 
                description: ...
    """
    json = request.json

    domain = Convertors.json_to_domain(json=json)
    response = UsersControllers().registrar(domain)
    return response

@user_routes.post('/users/login')
@swag_from({
    'parameters': [
        {
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                "email": {
                "type": "string",
                "required": True
                },
                "senha": {
                    "type": "string",
                    "required": True
            }
        }
    }
}]})
def user_login():
    """
    Realiza login de um usuário
    ---
    responses:
        200:
            description: ...
    """
    json = request.json
    response = UsersControllers().login(json)
    
    if isinstance(response, bool):
        if response == True:
            token = RoutesSecurity().generateKey(json.get('email'))
            return make_response(jsonify({
                'response': token,
                'msg': 'usuário logado com sucesso!'
            }), HttpCodesResponses().response_codes.OK.value)
        else:
            return make_response(jsonify({
                'response': None,
                'msg': 'Senha incorreta!'
            }), HttpCodesResponses().response_codes.MISDIRECTED_REQUEST.value)
    return response

@user_routes.put('/users')
@swag_from({
    'parameters' : [
        {
            'in': 'header',
            'name': 'Authorization',
            'type': 'string',
            'required': True
        },
        {
        "in": "body",
        "name": "body",
        "required": True,
        "schema": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "required": True
                },
                "password": {
                    "type": "string",
                    "required": True
                },
                "name": {
                    "required": True,
                    "type": "string"
                }
            }
        }
    }
]})
@RoutesSecurity.tokenRequired
def update_datas(*args):
    """
    Atualiza os dados do usuário
    ---
    responses:
        200:
            description: ...
    """
    current_mail = args[0]
    json = request.json
    user = Convertors.json_to_domain(json)
    response = UsersControllers().update_user(current_mail, user)
    return response

