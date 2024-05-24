import os
from flasgger import swag_from
from flask import Blueprint, make_response, jsonify, request, send_file
from src.convertors.requests import Convertors
from src.controllers import ApoiadoresControllers
from src.utils.http_manager import HttpCodesResponses
from src.domain.securitys import RoutesSecurity
from src.utils.serialsIDs import generateSerialID


apoiadores_routes = Blueprint('apoiadores_routes', __name__)


@apoiadores_routes.get('/apoiador')
@swag_from({
    'parameters': [
        {
            "in": "query",
            "name": "email",
            "required": False,
        },
        {
            "in": "query",
            "name": "estado",
            "required": False,
        }
]})
def get_apoiador_endpoint(*args):
    """
    Busca os usuários no storage sistema
    ---
    responses:
        200: 
            description: ...
    """
    email = request.args.get('email')
    estado = request.args.get('estado')
    if not email and not estado:
        apoiadores = ApoiadoresControllers().pegar_apoiadores()
        return make_response(jsonify({
            'response': apoiadores,
            'msg': 'retornado todos os usuários do storage'
        }))
    if estado:
        apoiadores = ApoiadoresControllers().pegar_apoiadores(estado = True)
        return make_response(jsonify({
            'response': apoiadores,
            'msg': 'Retornado todos os apoiadores verificados!'
        }), HttpCodesResponses().response_codes.OK.value)

    apoiador = ApoiadoresControllers().pegar_apoiador(email)
    
    if not apoiador:
        return make_response(jsonify({
            'response': None,
            'msg': 'Não existe nenhum usuário com este email.'
        }))
    
    return make_response(jsonify({
        'response': apoiador,
        'msg': f'Retornado os dados de {email}'
    }))

@apoiadores_routes.post('/apoiador') 
@swag_from({
    'parameters': [
        {
            'in': 'formData',
            'type': 'string',
            'name': 'nome',
            'requerid': True
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'email',
            'requerid': True
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'telefone',
            'requerid': True
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'senha',
            'requerid': True
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'sobrenome',
            'requerid': True
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'profissao',
            'requerid': True
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'bibliografia',
            'requerid': True
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'especializacao',
            'requerid': True
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'nacionalidade',
            'requerid': True
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'disponibilidade',
            'requerid': True
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'atuacao',
            'requerid': True
        },{
            'in': 'formData',
            'type': 'file',
            'name': 'foto.png',
            'requerid': True
        },{
            'in': 'formData',
            'type': 'file',
            'name': 'csv.pdf',
            'requerid': True
        }
    ]
})
def register_user_endpoint(*args):
    """
    Resgistra usuário no storage do sistema
    ---
    responses:
            200: 
                description: ...
    """
    files = request.files
    id_ = generateSerialID()
    _FILE = None
    if not files:
        return make_response(jsonify({
            'response': '',
            'msg': ''
        }), HttpCodesResponses().response_codes.PRECONDITION_FALEID.value)
    else:
        for file in files:
            if file[file.rfind('.')+1:] != 'png' and file[file.rfind('.')+1:] != 'pdf':
                return make_response(jsonify({
                    'response': None,
                    'msg': 'O ficheiro precisa ser um PDF'
                }), HttpCodesResponses().response_codes.UNSSUPORTED_MEDIA_TYPE.value)
            _FILE = f"{id_}.{file[file.rfind('.')+1:]}"
            file_ = files[file]
            if file[file.rfind('.')+1:] != 'pdf':
                path = os.path.join('src', 'files', 'docs', f'{id_}.pdf')
                file_.save(path)
            else:
                path = os.path.join('src', 'files', 'images', f'{id_}.png')
                file_.save(path)
        if os.path.exists(path):
            pass
        else:
            return make_response(jsonify({
                'response': False,
                'msg': 'Não foi possivel salvar os seus arquivos. Tente de novo mais tarde!'
            }))
    json = {
        'nome': request.form['nome'],
        'sobrenome': request.form['sobrenome'],
        'email': request.form['email'],
        'telefone': request.form['telefone'],
        'senha': request.form['senha'],
        'profissao': request.form['profissao'],
        'especializacao': request.form['especializacao'],
        'nacionalidade': request.form['nacionalidade'],
        'disponibilidade': request.form['disponibilidade'],
        'atuacao': request.form['atuacao'],
        'bibliografia': request.form['bibliografia'],
        'photo': f'{id_}.png',
        'csv': f'{id_}.pdf'
    }
    domain = Convertors.json_to_domain(json=json, entitie='apoiadores')
    response = ApoiadoresControllers().registrar(domain)
    return response

@apoiadores_routes.post('/apoiador/login')
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
    response = ApoiadoresControllers().login(json)
    
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

@apoiadores_routes.put('/apoiador')
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
    response = ApoiadoresControllers().atualizar_apoiador(current_mail, user)
    return response

@apoiadores_routes.post('/update-state')
@swag_from({
    'parameters': [
        {
            'in': 'query',
            'name': 'email',
            'type': 'string',
            'required': True
        }
    ]
})
def change_state_apoiador(*args):
    """
    Muda o estado de um apoiador (se true para false, se false para true)
    ---
    responses:
        200:
            description: ...
    """
    email_apoiador = request.args.get('email')
    response = ApoiadoresControllers().change_state(email_apoiador)
    return response

@apoiadores_routes.get('/get-csv')
@swag_from({
    'parameters': [
        {
            'in': 'query',
            'name': 'email',
            'type': 'string',
            'required': True
        }
    ]
})
def pegar_csv(*args):
    """
    Pega o curriculo de um usuário
    ---
    responses:
        200:
            description: ...
    """
    email = request.args.get('email')
    apoiador = ApoiadoresControllers().pegar_apoiador(email)
    
    if not apoiador:
        return make_response(jsonify({
            'response': None,
            'msg': 'Não existe nenhum apoiador com este email!'
        }), HttpCodesResponses().response_codes.GONE.value)
    
    return send_file(f'../../files/docs/{apoiador.get("csv")}', mimetype = 'application/pdf', download_name = 'curriculo.pdf')

@apoiadores_routes.post('/link-meet')
@swag_from({
    'parameters': [
    {
        'in': 'query',
        'name': 'email',
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
            "link": {
                "type": "string",
                "required": True
            }
        }
    }
}]})
def update_meet(*args):
    """
    Atualiza o link pro meet
    ---
    responses:
        200:
            description: ...
    """
    json = request.json
    email = request.args.get('email')
    response = ApoiadoresControllers().atualizar_link(email = email, link = json.get('link'))
    return response


