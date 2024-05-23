import jwt
import datetime
from functools import wraps
from src.domain.app import app
from flask import request, make_response, jsonify
from src.utils.http_manager import HttpCodesResponses


class RoutesSecurity:
    """Class responsible for security-related operations."""

    def __init__(self) -> None:
        """Initialize Security object."""
        pass

    @staticmethod
    def tokenRequired(f):
        """Decorator to require token for authorization."""
        @wraps(f)
        def decorated(*args, **kwargs):
            """Decorator function."""
            token = request.headers.get('Authorization')

            if not token:
                return make_response(jsonify({
                    'response': None,
                    'msg': 'Token Unsent'
                }), HttpCodesResponses().response_codes.NETWORK_AUTENTICATION_REQUIRED.value)

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

                if data.get('user'):
                    currentUser = data.get('user')
                else:
                    return make_response(jsonify({
                        'response': None,
                        'msg': 'Invalid token or invalid user'
                    }), HttpCodesResponses().response_codes.FORBIDDEN.value)
            except jwt.exceptions.ExpiredSignatureError:
                return make_response(jsonify({
                    'response': None,
                    'msg': 'Sessão expirada! Volte a fazer login.'
                }), HttpCodesResponses().response_codes.NETWORK_AUTENTICATION_REQUIRED.value)
            except Exception as e:
                return make_response(jsonify({
                    'response': None,
                    'msg': f'{HttpCodesResponses().codes_response.INTERNAL_SERVER_ERROR.value}',
                }), HttpCodesResponses().response_codes.INTERNAL_SERVER_ERROR.value)

            return f(currentUser)
        return decorated

    @staticmethod
    def AdminAcess(f):
        """Decorator to require token for authorization."""
        @wraps(f)
        def decorated(*args, **kwargs):
            """Decorator function."""
            token = request.headers.get('Authorization')
            if not token:
                return make_response(jsonify({
                    'response': None,
                    'msg': 'Token Unsent'
                }), HttpCodesResponses().response_codes.NETWORK_AUTENTICATION_REQUIRED.value)

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                if data.get('user'):
                    currentUser = data.get('user')
                    acess = data.get('acess')
                    if acess != 'admin':
                        return make_response(jsonify({
                            'response': None,
                            'msg': 'Invalid token, you need administrator access'
                        }), HttpCodesResponses().response_codes.INVALID_TOKEN.value)
                else:
                    return make_response(jsonify({
                        'response': None,
                        'msg': 'Invalid token or invalid user'
                    }), HttpCodesResponses().response_codes.FORBIDDEN.value)
            except jwt.exceptions.DecodeError:
                return make_response(jsonify({
                    'response': None,
                    'msg': 'your token is damaged, log in again to get another one'
                }), HttpCodesResponses().response_codes.FORBIDDEN.value)
            except:
                return make_response(jsonify({
                    'response': None,
                    'msg': f'{HttpCodesResponses().codes_response.INTERNAL_SERVER_ERROR.value}',
                }), HttpCodesResponses().response_codes.INTERNAL_SERVER_ERROR.value)

            return f(currentUser)
        return decorated

    """def authorized(self, key: str) -> bool:
        #Check if the provided key is authorized.
        data = None

        try:
            data = jwt.decode(key, app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception as e:
            return False

        user = data.get('user')

        if user == ControlUser.get_current_user():
            return True

        return False"""

    def generateKey(self, email: str, acess: str = 'normal') -> str:
        """Generate a new key."""
        payload = {
            "user": f"{email}",
            "acess": acess,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }

        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

        return token
