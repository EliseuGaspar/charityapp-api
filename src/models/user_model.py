""""""
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
)
from datetime import datetime
from src.domain.configs.database import base


class Usuarios(base):
    """Model class for users - represented the table 'users' in database"""
    __tablename__ = 'usuarios'
    _objectID = 'usuarios'

    id = Column(Integer, nullable = False, primary_key = True, autoincrement = True)
    nome = Column(String(255), nullable = False)
    sobrenome = Column(String(255), nullable = False)
    provincia = Column(String(255), nullable = False)
    municipio = Column(String(255), nullable = False)
    bi = Column(String(255), nullable = False)
    telefone = Column(String(255), nullable = False)
    email = Column(String(255), nullable = False, unique = True)
    senha = Column(String(255), nullable = False)
    created_at = Column(TIMESTAMP, default = datetime.now)
    updated_at = Column(TIMESTAMP, default = datetime.now, onupdate = datetime.now)

    def __init__(self, nome : str, sobrenome : str, provincia : str, municipio: str, bi: str,
        telefone: str, email: str, senha: str) -> None:
        self.nome = nome
        self.sobrenome = sobrenome
        self.provincia = provincia
        self.municipio = municipio
        self.bi = bi
        self.telefone = telefone
        self.email = email
        self.senha = senha
    
    @property
    def objectID(self) -> str:
        return self._objectID
