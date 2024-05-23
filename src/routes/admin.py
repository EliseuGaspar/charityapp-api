import os
from flask import Blueprint, make_response, jsonify, request
from flasgger import swag_from
from src.utils.http_manager import HttpCodesResponses
from src.controllers.admin_controller import AdminController
from src.convertors.requests import Convertors
from src.domain.securitys import RoutesSecurity

admin = Blueprint('admin_routes', __name__)

@admin.post('/admin/login')
def login_admin(*args):
    """
    Login para administradores
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
        200:
            description: Login realizado com sucesso!
        400:
            description: Argumentos para login em falta!
    """

    json = request.json
    if not json.get('email') or not json.get('password'):
        return make_response(jsonify({
            'response': None,
            'msg': 'email argument not passed.'
        }), HttpCodesResponses().response_codes.BAD_REQUEST.value)
    
    loged = AdminController().login(email = json.get('email'), password = json.get('password'))

    if loged:
        return make_response(jsonify({
            'response': {
                'status': True,
                'token': RoutesSecurity().generateKey(json.get('email'), acess = 'admin')
            },
            'msg': ''
        }), HttpCodesResponses().response_codes.OK.value)
    else:
        return make_response(jsonify({
            'response': {
                'status': False,
                'token': None
            },
            'msg': ''
        }), HttpCodesResponses().response_codes.OK.value)

@admin.post('/admin')
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
            "name" : {
                "type": "string",
                "required": True
            },
            "password": {
                "type": "string",
                "required": True
            }
        }
    }
}]})
def register_admin(*args):
    """
    Registra um novo admin no banco de dados
    ---
    responses:
        200:
            description: ...
    """
    datas = request.json
    domain = Convertors.json_to_domain(datas, entitie = 'admin')
    response = AdminController().register(domain)
    return response

@admin.get('/admin')
@swag_from({
    'parameters': [
    {
    'name': 'Authorization',
    'in': 'header',
    'type': 'string',
    'required': True,
    'description': 'Token de um admin'
    },{
        'name': 'email',
        'in': 'query',
        'type': 'string',
        'required': False,
        'description': 'email do administrador'
    }
]})
@RoutesSecurity.AdminAcess
def get_admin(*args):
    """
    Retorna um ou vários administradores
    ---
    responses:
        200:
            description: ...
    """
    admin_email = request.args.get('email')

    if admin_email:
        _admin = AdminController().get_admin(admin_email)
        return make_response(jsonify({
        'response': _admin,
        'msg': 'returned admin'
    }), HttpCodesResponses().response_codes.OK.value)

    _admin = AdminController().get_admins()
    return make_response(jsonify({
        'response': _admin,
        'msg': 'returned all admins registered in database'
    }), HttpCodesResponses().response_codes.OK.value)

@admin.put('/admin')
@swag_from({
    'parameters': [
    {
    'name': 'Authorization',
    'in': 'header',
    'type': 'string',
    'required': True,
    'description': 'Token de um admin'
    },{
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
            "name" : {
                "type": "string",
                "required": True
            },
            "password": {
                "type": "string",
                "required": True
            }
        }
    }
}]})
@RoutesSecurity.AdminAcess
def update_person_datas(*args):
    """
    Atualiza os dados de um administrador
    ---
    responses:
        200:
            description: ...
    """
    json = request.json
    json['current_email'] = args[0]
    response = AdminController().update_datas(infos = json)
    return response