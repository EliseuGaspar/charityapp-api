from flask import make_response, jsonify, Response
from src.models import Usuarios
from src.domain.entities import EUsuario
from src.domain.configs.database import session
from src.domain.securitys import HashFeature
from src.convertors.repositories import PydanticFactory
from src.utils.http_manager import HttpCodesResponses
from src.domain.securitys import RoutesSecurity

class UsersControllers:
    """"""

    def __init__(self) -> None:
        """"""
        self._session = session

    def registrar(self, usuario: EUsuario) -> dict | bool:
        """"""
        registrado = self.pegar_usuario(usuario.email)

        if registrado:
            return make_response(jsonify({
                'response': None,
                'msg': 'Já existe um usuário com este email!'
            }), HttpCodesResponses().response_codes.CONFLICT.value)

        senha = HashFeature.encript(usuario.senha)

        novo_usuario = Usuarios(email = usuario.email, nome = usuario.nome, senha = senha,
        sobrenome = usuario.sobrenome, provincia = usuario.provincia, municipio = usuario.municipio,
        bi = usuario.bi, telefone = usuario.telefone)
        self._session.add(novo_usuario)
        self._session.commit()
        
        registrado = self.pegar_usuario(usuario.email)

        if registrado:
            usuario_ = PydanticFactory.convert(novo_usuario).dict()
            usuario_.pop('senha')
            token = RoutesSecurity().generateKey(usuario.email)
            return make_response(jsonify({
                'response': usuario_,
                'token': token,
                'msg': 'Usuário registrado com sucesso!'
            }), HttpCodesResponses().response_codes.CREATED.value)
        else:
            return make_response(jsonify({
                'response': None,
                'msg': 'Não foi possível realizar o cadastro. Tente depois!'
            }), HttpCodesResponses().response_codes.INTERNAL_SERVER_ERROR.value)

    def pegar_usuarios(self, ) -> list[dict] | bool:
        """"""
        usuarios = self._session.query(Usuarios).all()

        if usuarios == []:
            return False
        
        lista_usuarios = []

        for user in usuarios:
            user_ = PydanticFactory.convert(user).dict()
            user_.pop('senha')
            lista_usuarios.append(user_)

        return lista_usuarios

    def pegar_usuario(self, email: str, senha: bool = False, object: bool = False) -> bool | object:
        """"""
        usuario = self._session.query(Usuarios).filter_by(email = email).first()

        if usuario == None:
            return False

        if object:
            return usuario
        else:
            if senha:
                return PydanticFactory.convert(usuario).dict()
            else:
                usuario_ = PydanticFactory.convert(usuario).dict()
                usuario_.pop('senha')
                return usuario_

    def apagar_usuario(self, email: str) -> bool | None:
        """"""
        usuario = self.pegar_usuario(email = email, object=True)

        if not usuario:
            return None

        try:
            self._session.delete(usuario)
            self._session.commit()
            #--------
            usuario = self.pegar_usuario(email = email)
            
            if not usuario:
                return True
            else:
                return False
        except:
            return any

    def atualizar_usuario(self, email: str, usuario: EUsuario) -> bool:
        """"""
        usuario_ = self.pegar_usuario(email = email, object = True)

        if not usuario_:
            return None

        if usuario.nome:
            usuario_.nome = usuario.nome
        if usuario.email:
            usuario_.email = usuario.email
        if usuario.senha:
            senha = HashFeature.encript(usuario.senha)
            usuario_.senha = senha

        self._session.add(usuario_)
        self._session.commit()

        novo_usuario = self.pegar_usuario(email = usuario_.email)

        if isinstance(novo_usuario, dict):
            return make_response(jsonify({
                'response': novo_usuario,
                'msg': 'Dados do usuário salvos com sucesso!'
            }))
        return make_response(jsonify({
            'response': None,
            'msg': 'Não foi possível salvar os dados.'
        }))

    def login(self, json: dict) -> Response:
        """"""
        email = json.get('email')
        senha = json.get('senha')
        usuario = self.pegar_usuario(email, True)

        if not usuario:
            return make_response(jsonify({
                'response': None,
                'msg': 'Não existe nenhum usuário com este email'
            }), HttpCodesResponses().response_codes.GONE.value)
        logado = HashFeature.verify(senha, usuario.get('senha'))
        return logado