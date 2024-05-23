from flask import make_response, jsonify, Response
from src.models import Admin
from src.domain.entities import AdminEntitie
from src.domain.configs.database import session
from src.convertors.repositories import PydanticFactory
from src.utils.http_manager import HttpCodesResponses
from src.domain.securitys import HashFeature


class AdminController:

    def __init__(self):
        """"""
        self._session = session
    
    def register(self, admin: AdminEntitie):
        """"""
        admin_exist = self.get_admin(admin.email)

        if admin_exist != False:
            return make_response(jsonify({
                'response': None,
                'msg': "There's already a admin with that email"
            }), HttpCodesResponses().response_codes.CONFLICT.value)

        password = HashFeature.encript(admin.password)
        _admin = Admin(
            name = admin.name,
            email = admin.email,
            password = password
        )
        self._session.add(_admin)
        self._session.commit()

        admin_exist = self.get_admin(admin.email)

        if admin_exist != False:
            return (jsonify({
                'response': admin_exist,
                'msg': "registered new admin in system."
            }), HttpCodesResponses().response_codes.OK.value)
        else:
            return make_response(jsonify({
                'response': None,
                'msg': "failure to register this admin, for some reason it was not possible to do so. Try again later!"
            }), HttpCodesResponses().response_codes.INTERNAL_SERVER_ERROR.value)
    
    def get_admins(self, secrets: bool = False) -> list[dict]:
        """"""
        admins_list = []
        admins = self._session.query(Admin).all()
        for admin in admins:
            admin_ = PydanticFactory.convert(admin).dict()
            if not secrets:
                admin_.pop('password')
            admins_list.append(admin_)
        return admins_list
    
    def get_admin(self, email: str, secrets: bool = False) -> bool | dict:
        """"""
        admin = self._session.query(Admin).filter_by(email = email).first()
        if admin == None:
            return False  

        _admin = PydanticFactory.convert(admin).dict()
        if not secrets:
            _admin.pop('password')
        return _admin
    
    def login(self, email: str, password: str) -> bool:
        """"""
        admin_exist = self.get_admin(email, secrets=True)
        if not admin_exist:
            return False
        
        if admin_exist.get('password') == password:
            return True
        
        _password = HashFeature().verify(password, admin_exist.get('password'))

        return _password

    def update_datas(self, infos : dict) -> Response:
        """"""
        is_email = None
        email = infos.get('current_email')
        admin = self.get_admin(email = email, object = True)

        if not admin:
            return make_response(jsonify({
                'response': None,
                'msg': "it seems there is an error and uploading your information now. Try again later!"
            }), HttpCodesResponses().response_codes.INTERNAL_SERVER_ERROR.value)
        
        if infos.get('name') != None:
            admin.name = infos.get('name')
        if infos.get('email') != None:
            admin.email = infos.get('email')
            is_email = True
        if infos.get('password') != None:
            admin.password = HashFeature().encript(infos.get('password'))

        self._session.add(admin)
        self._session.commit()

        if is_email:
            _admin = self.get_admin(email = infos.get('email'))
        else:
            _admin = self.get_admin(email = infos.get('current_email'))

        if _admin:
            return make_response(jsonify({
                'response': _admin,
                'msg': 'update completed!'
            }), HttpCodesResponses().response_codes.OK.value)
        else:
            return make_response(jsonify({
                'response': None,
                'msg': 'For some reason we were unable to update your profile, please try again later!'
            }), HttpCodesResponses().response_codes.INTERNAL_SERVER_ERROR.value)
