import os, datetime
from flask import Blueprint, request, send_file, make_response, jsonify
from src.convertors.requests import Convertors
from src.controllers import TransactionsConroller
from src.utils.http_manager import HttpCodesResponses
from src.domain.securitys import RoutesSecurity
from src.components.pdfGenerator.pdf_generator import PDF
from src.components.pdf_sign.src.domain.app import AES
from flasgger import swag_from
from uuid import uuid4

transaction_routes = Blueprint('transaction_routes', __name__)


@transaction_routes.post('/transactions')
@swag_from({
    'parameters': [
        {
            'in': 'header',
            'name': 'Authorization',
            'type': 'string',
            'required': True
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'home_bank',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'destination_bank',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'receiver',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'sender',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'sender_iban',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'receiver_iban',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'sent_amount',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'date_sent',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'date_received',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'operation',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'transaction',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'date_and_time_of_transaction',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'reference',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'amount',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'description',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'entity',
            'requerid': False
        },{
            'in': 'formData',
            'type': 'string',
            'name': 'channel',
            'requerid': False
        },
    ]
})
@RoutesSecurity.tokenRequired
def register_transaction(*args):
    """
    Cadastra atividade de uma nova transação
    ---
    responses:
        200:
            description: ...
    """
    try:
        home_bank = request.form['home_bank']
        destination_bank = request.form['destination_bank']
        receiver = request.form['receiver']
        sender = request.form['sender']
        sender_iban = request.form['sender_iban']
        receiver_iban = request.form['receiver_iban']
        sent_amount = request.form['sent_amount']
        date_sent = request.form['date_sent']
        date_received = request.form['date_received']
        transaction_reference = str(uuid4())
        operation = request.form['operation']
        transaction = request.form['transaction']
        date_and_time_of_transaction = request.form['date_and_time_of_transaction']
        reference = request.form['reference']
        amount = request.form['amount']
        description = request.form['description']
        entity = request.form['entity']
        channel = request.form['channel']
    except:
        return make_response(jsonify({
            'response': None,
            'msg': 'Impossivel registrar a transação, dados em falta!'
        }), HttpCodesResponses().response_codes.PRECONDITION_FALEID.value)
    
    transaction_ = Convertors.form_to_domain(home_bank, destination_bank,
    receiver, sender, sender_iban, receiver_iban, sent_amount, date_sent,
    date_received, transaction_reference, operation, transaction,
    date_and_time_of_transaction, reference, amount, description, entity, channel)
    
    response = TransactionsConroller().register_transaction(transaction_)
    
    if response.status_code == 201:
        created = PDF(transaction_).create_pdf()
        if created:
            return send_file(
                    path_or_file = '../../temp/pdf/document.pdf',
                    mimetype = 'application/pdf',
                    download_name = f'ProfValidator_Transaction_{str(datetime.datetime.now())[:11]}_.pdf'
                )
        else:
            return make_response(jsonify({
                'response': None,
                'msg': 'Não foi possível gerar o pdf!'
            }), HttpCodesResponses().response_codes.INTERNAL_SERVER_ERROR.value)
    
    return response

@transaction_routes.post('/check_qr')
@swag_from({
    'parameters': [
        {
            'in': 'header',
            'name': 'Authorization',
            'required': True,
            'type': 'string'
        },{
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "required": True
                    }
                }
            }
        }  
    ]
})
@RoutesSecurity.tokenRequired
def check_qrcode(*args):
    """
    Checa a o comprovativo com base na hash integrada no qrCode
    ---
    responses:
        200:
            description: ...
    """
    hash_ = request.json.get('data')
    hash_decrypted = AES(os.getenv('secretKey')).decrypt(hash_)
    response = TransactionsConroller().get_transaction(transaction = hash_decrypted)
    return response

