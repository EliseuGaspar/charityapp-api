import os, datetime
from uuid import uuid4
from flasgger import swag_from
from flask import Blueprint, make_response, jsonify, request, send_file, session, Response
from src.utils.http_manager import HttpCodesResponses
from src.intermediaries import SignIntermediaries
from src.domain.securitys.jwt_manager import RoutesSecurity
from src.domain.entities import Activities_Entitie
from src.controllers.activitie_controller import ActivitieController
from controllers.apoiadores_controller import TransactionsConroller

files = Blueprint('files_routes', __name__)

@files.post('/upload_file')
@swag_from({
    'parameters': [
        {
        'name': 'Authorization',
        'in': 'header',
        'type': 'string',
        'required': True,
        'description': 'Token de usuário'
        },{
        'name': 'comprovativo.pdf',
        'in': 'formData',
        'type': 'file',
        'required': True
        },{
        'in': 'query',
        'name': 'reference',
        'required': True,
        'type': 'string'
    }
]})
@RoutesSecurity.tokenRequired
def get_pdf_file(*args):
    '''
    Upload de ficheiros para validação
    ---
    responses:
        200:
            description: ...
    '''
    try:
        path = os.path.join('src', 'temp', 'docs')
        os.remove(path)
    except Exception as e:
        pass

    files = request.files
    _FILE = None
    if not files:
        return make_response(jsonify({
            'response': '',
            'msg': ''
        }), HttpCodesResponses().response_codes.PRECONDITION_FALEID.value)
    else:
        for file in files:
            if file[file.rfind('.')+1:] != 'pdf':
                return make_response(jsonify({
                    'response': None,
                    'msg': 'O ficheiro precisa ser um PDF'
                }), HttpCodesResponses().response_codes.UNSSUPORTED_MEDIA_TYPE.value)
            _FILE = f"document.{file[file.rfind('.')+1:]}"
            file_ = files[file]
            path = os.path.join('src', 'temp', 'docs', 'document.pdf')
            file_.save(path)
            sign_intermediaries = SignIntermediaries(path)
        if os.path.exists(path):
            reference = request.args.get('reference')
            response = sign_intermediaries.sign({
                'reference': reference
            })
            if response:
                return send_file(
                    path_or_file = '../../temp/docs/document_signed.pdf',
                    mimetype = 'application/pdf',
                    download_name = f'ProfValidator_SignedPDF_{str(datetime.datetime.now())[:11]}_.pdf'
                )
            return make_response(jsonify({
                'response': None,
                'msg': f'{HttpCodesResponses().codes_response.SEE_OTHER.value}',
                'uri': 'http://localhost:3000/response_redirects'
            }), HttpCodesResponses().response_codes.SEE_OTHER.value)
        else:
            return make_response(jsonify({
                'response': None,
                'msg': "File don't save"
            }), HttpCodesResponses().response_codes.INTERNAL_SERVER_ERROR.value)

@files.get('/img')
def get_svg_file(*args):
    return send_file('../../temp/image/qrCode.png')

@files.post('/verify_pdf')
@swag_from({
    'parameters': [
        {
        'name': 'Authorization',
        'in': 'header',
        'type': 'string',
        'required': True,
        'description': 'Token de usuário'
        },{
        'name': 'comprovativo.pdf',
        'in': 'formData',
        'type': 'file',
        'required': True
    }
]})
@RoutesSecurity.tokenRequired
def check_pdf_authenticity(*args):
    '''
    Verifica veracidade do comprovativo
    ---
    responses:
        200:
            description: ...
    '''
    try:
        path = os.path.join('src', 'temp', 'docs')
        os.remove(path)
    except Exception as e:
        pass
    files = request.files
    _FILE = None

    if files is None:
        return make_response(jsonify({
            'response': False,
            'msg': ''
        }), HttpCodesResponses().response_codes.PRECONDITION_FALEID.value)
    else:
        for file in files:
            if file[file.rfind('.')+1:] != 'pdf':
                return make_response(jsonify({
                    'response': None,
                    'msg': ''
                }), HttpCodesResponses().response_codes.UNSSUPORTED_MEDIA_TYPE.value)
            _FILE = f"document.{file[file.rfind('.')+1:]}"
            file_ = files[file]
            path = os.path.join('src', 'temp', 'docs', 'document.pdf')
            file_.save(path)
            sign_intermediaries = SignIntermediaries(path)
        if os.path.exists(path):
            response = sign_intermediaries.check()
            if response:
                domain = Activities_Entitie(
                    user = args[0], pdf_name = f'document_{str(uuid4())[:12]}',
                    date_activitie = f'{str(datetime.datetime.now())[:19]}',
                    status = True
                )
                ActivitieController().register(domain)
                datas = TransactionsConroller().get_transaction(session.get('reference'))
                session['reference'] = None
                return datas
            domain = Activities_Entitie(
                    user = args[0], pdf_name = f'document_{str(uuid4())[:12]}',
                    date_activitie = f'{str(datetime.datetime.now())[:19]}',
                    status = False
                )
            ActivitieController().register(domain)
            return make_response(jsonify({
                'response': False,
                'msg': 'Comprovativo Invalido!',
            }), HttpCodesResponses().response_codes.OK.value)
        else:
            return make_response(jsonify({
                'response': None,
                'msg': "File don't save"
            }), HttpCodesResponses().response_codes.INTERNAL_SERVER_ERROR.value)