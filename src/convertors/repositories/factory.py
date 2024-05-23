from typing import Type
from pydantic import BaseModel
from .models import UserDantic, ApoiadoresDantic, AdminDantic


class PydanticFactory:
    """"""

    @staticmethod
    def convert(entitie: object) -> BaseModel:
        """"""
        if entitie._objectID == 'usuarios':
            return UserDantic(**entitie.__dict__)
        elif entitie._objectID == 'apoiadores':
            return ApoiadoresDantic(**entitie.__dict__)
        elif entitie._objectID == 'admin':
            return AdminDantic(**entitie.__dict__)
