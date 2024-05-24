from typing import Type, Dict
from dataclasses import dataclass
from src.domain.entities import EUsuario, EApoiadores, EAdmin

class Convertors:

    _objectID = 'convertors'

    @staticmethod
    def json_to_domain(json: Type[Dict], entitie: str = "usuario") -> Type[dataclass]:
        """"""
        if entitie == 'admin':
            return Convertors.__admin__(json)
        elif entitie == 'usuario':
            return EUsuario(nome = json.get('nome'), email = json.get('email'), senha = json.get('senha'),
                        sobrenome = json.get('sobrenome'), provincia = json.get('provincia'),
                        municipio = json.get('municipio'), telefone = json.get('telefone'),
                        bi = json.get('bi')
                    )
        else:
            return EApoiadores(
                nome = json.get('nome'), email = json.get('email'), senha = json.get('senha'),
                telefone = json.get('telefone'), sobrenome = json.get('sobrenome'),
                profissao = json.get('profissao'), especializacao = json.get('especializacao'),
                nacionalidade = json.get('nacionalidade'), disponibilidade = json.get('disponibilidade'),
                atuacao = json.get('atuacao'), foto = json.get('photo'), sala_de_meet = json.get('sala_de_meet'),
                estado = json.get('estado'), csv = json.get('csv'), bibliografia = json.get('bibliografia')
            )

    @staticmethod
    def __admin__(json: Type[Dict]) -> Type[dataclass]:
        """"""
        admin = EAdmin(
            nome = json.get('nome'),
            email = json.get('email'),
            senha = json.get('senha')
        )
        return admin
