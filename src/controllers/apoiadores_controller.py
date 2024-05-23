import pymysql
from flask import make_response, jsonify, Response
from src.models import Apoiadores
from src.domain.entities import EApoiadores
from src.domain.configs.database import session
from src.domain.securitys import HashFeature
from src.convertors.repositories import PydanticFactory
from src.utils.http_manager import HttpCodesResponses
from src.domain.securitys import RoutesSecurity

class ApoiadoresControllers:
    """"""

    def __init__(self) -> None:
        """"""
        self._session = session

    def registrar(self, apoiador: EApoiadores) -> dict | bool:
        """"""
        try:
            registrado = self.pegar_apoiador(apoiador.email)

            if registrado:
                return make_response(jsonify({
                    'response': None,
                    'msg': 'Já existe um usuário com este email!'
                }), HttpCodesResponses().response_codes.CONFLICT.value)

            senha = HashFeature.encript(apoiador.senha)

            novo_apoiador = Apoiadores(
                nome = apoiador.nome, sobrenome = apoiador.sobrenome, profissao = apoiador.profissao,
                especializacao = apoiador.especializacao, nacionalidade = apoiador.nacionalidade,
                disponibilidade = apoiador.disponibilidade, atuacao = apoiador.atuacao,
                foto = apoiador.foto, sala_de_meet = apoiador.sala_de_meet, senha = senha,
                estado = apoiador.estado, csv = apoiador.csv, email = apoiador.email,
                telefone = apoiador.telefone
            )
            self._session.add(novo_apoiador)
            self._session.commit()
            
            registrado = self.pegar_apoiador(apoiador.email)

            if registrado:
                apoiador_ = PydanticFactory.convert(novo_apoiador).dict()
                apoiador_.pop('senha')
                token = RoutesSecurity().generateKey(apoiador.email)
                return make_response(jsonify({
                    'response': apoiador_,
                    'token': token,
                    'msg': 'Usuário registrado com sucesso!'
                }), HttpCodesResponses().response_codes.CREATED.value)
            else:
                return make_response(jsonify({
                    'response': None,
                    'msg': 'Não foi possível realizar o cadastro. Tente depois!'
                }), HttpCodesResponses().response_codes.INTERNAL_SERVER_ERROR.value)
        except pymysql.err.IntegrityError:
            return make_response(jsonify({
                'response': None,
                'msg': 'Não foi possível registrar seu usuário. Existe dados duplicados.'
            }), HttpCodesResponses().response_codes.INTERNAL_SERVER_ERROR.value)

    def pegar_apoiadores(self, ) -> list[dict] | bool:
        """"""
        apoiadores = self._session.query(Apoiadores).all()

        if apoiadores == []:
            return False
        
        lista_apoiadores = []

        for user in apoiadores:
            user_ = PydanticFactory.convert(user).dict()
            user_.pop('senha')
            lista_apoiadores.append(user_)

        return lista_apoiadores

    def pegar_apoiador(self, email: str, senha: bool = False, object: bool = False) -> bool | object:
        """"""
        apoiador = self._session.query(Apoiadores).filter_by(email = email).first()

        if apoiador == None:
            return False

        if object:
            return apoiador
        else:
            if senha:
                return PydanticFactory.convert(apoiador).dict()
            else:
                apoiador_ = PydanticFactory.convert(apoiador).dict()
                apoiador_.pop('senha')
                return apoiador_

    def apagar_apoiador(self, email: str) -> bool | None:
        """"""
        apoiador = self.pegar_apoiador(email = email, object=True)

        if not apoiador:
            return None

        try:
            self._session.delete(apoiador)
            self._session.commit()
            #--------
            apoiador = self.pegar_apoiador(email = email)
            
            if not apoiador:
                return True
            else:
                return False
        except:
            return any

    def atualizar_apoiador(self, email: str, apoiador: EApoiadores) -> bool:
        """"""
        apoiador_ = self.pegar_apoiador(email = email, object = True)

        if not apoiador_:
            return None

        if apoiador.nome:
            apoiador_.nome = apoiador.nome
        if apoiador.email:
            apoiador_.email = apoiador.email
        if apoiador.senha:
            senha = HashFeature.encript(apoiador.senha)
            apoiador_.senha = senha

        self._session.add(apoiador_)
        self._session.commit()

        novo_apoiador = self.pegar_apoiador(email = apoiador_.email)

        if isinstance(novo_apoiador, dict):
            return make_response(jsonify({
                'response': novo_apoiador,
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
        apoiador = self.pegar_apoiador(email, True)

        if not apoiador:
            return make_response(jsonify({
                'response': None,
                'msg': 'Não existe nenhum usuário com este email'
            }), HttpCodesResponses().response_codes.GONE.value)
        logado = HashFeature.verify(senha, apoiador.get('senha'))
        return logado

    def change_state(self, email: str) -> Response:
        apoiador = self.pegar_apoiador(email = email, object = True)
        state = None
        if not apoiador:
            return make_response(jsonify({
                'response': None,
                'msg': 'Não existe um usuário com este email'
            }), HttpCodesResponses().response_codes.GONE.value)

        if apoiador.estado:
            apoiador.estado = False
            state = False
        else:
            apoiador.estado = True
            state = True
        
        self._session.add(apoiador)
        self._session.commit()
        
        return make_response(jsonify({
            'response': state,
            'msg': 'Estado atualizado com sucesso!'
        }), HttpCodesResponses().response_codes.OK.value)

    def atualizar_link(self, email: str, link: str) -> Response:
        
        apoiador = self.pegar_apoiador(email = email, object = True)
        
        if not apoiador:
            return make_response(jsonify({
                'response': None,
                'msg': 'Não existe nenhum apoiador registrado com este email!'
            }), HttpCodesResponses().response_codes.GONE.value)
        
        apoiador.sala_de_meet = link
        
        self._session.add(apoiador)
        self._session.commit()
        
        return make_response(jsonify({
            'response': self.pegar_apoiador(email),
            'msg': 'Link atualizado com sucesso!'
        }), HttpCodesResponses().response_codes.OK.value)



