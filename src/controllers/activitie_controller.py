from flask import make_response, jsonify, Response
from src.models import Activities
from src.domain.entities import Activities_Entitie
from src.domain.configs.database import session
from src.convertors.repositories import PydanticFactory
from src.utils.http_manager import HttpCodesResponses


class ActivitieController:
    
    def __init__(self) -> None:
        self._session = session
    
    def register(self, activitie: Activities_Entitie) -> Response:
        """"""
        activi = Activities(
            activitie.user, activitie.pdf_name,
            activitie.date_activitie, activitie.status
        )
        self._session.add(activi)
        self._session.commit()
        return True
    
    def get_activities(self, user_email: str) -> dict:
        """"""
        activities = self._session.query(Activities).filter_by(user = user_email).all()
        _list = []
        for activitie in activities:
            _activitie = PydanticFactory.convert(activitie).dict()
            _list.append(_activitie)
        
        return make_response(jsonify({
            'response': _list,
        }), HttpCodesResponses().response_codes.OK.value)
    
    def delete(self, id: int) -> bool:
        """"""
        activitie = self._session.query(Activities).filter_by(id = id).first()
        
        if activitie:
            self._session.delete(activitie)
            self._session.commit()
            return make_response(jsonify({
                'response': True,
                'msg': 'Documento deletado com sucesso!'
            }), HttpCodesResponses().response_codes.OK.value)
        return make_response(jsonify({
            'response': False,
            'msg': 'Não foi possivel deletar o documento!'
        }), HttpCodesResponses().response_codes.OK.value)
    
    def update_name(self, id: int, name: str) -> bool:
        """"""
        activitie = self._session.query(Activities).filter_by(id = id).first()
        
        if activitie:
            activitie.pdf_name = name
            self._session.add(activitie)
            self._session.commit()
            return make_response(jsonify({
                'response': True,
                'msg': 'Documento atualizado com sucesso!'
            }), HttpCodesResponses().response_codes.OK.value)
        return make_response(jsonify({
            'response': False,
            'msg': 'Não foi possivel atualizar o documento!'
        }), HttpCodesResponses().response_codes.OK.value)
