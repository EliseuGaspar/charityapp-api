from sqlalchemy import (
    Column,Integer, String, TIMESTAMP,
    BOOLEAN
)
from datetime import datetime
from src.domain.configs.database import base


class Apoiadores(base):
    """"""
    _objectID = "apoiadores"
    __tablename__ = "apoiadores"

    id = Column(Integer, unique = True, nullable = False, autoincrement = True, primary_key = True,)
    nome = Column(String(255), nullable = False)
    email = Column(String(255), nullable = False, unique = True)
    telefone = Column(String(255), nullable = False, unique = True)
    senha = Column(String(255), nullable = False)
    sobrenome = Column(String(255), nullable = False)
    profissao = Column(String(255), nullable = False)
    especializacao = Column(String(255), nullable = False)
    nacionalidade = Column(String(255), nullable = False)
    disponibilidade = Column(String(255), nullable = False)
    atuacao = Column(String(255), nullable = False)
    foto = Column(String(255), nullable = True)
    sala_de_meet = Column(String(255), nullable = True, default = '')
    csv = Column(String(255), nullable = True, unique = True)
    estado = Column(BOOLEAN, nullable = True, default = False)
    created_at = Column(TIMESTAMP, default = datetime.now())
    
    def __init__(self, nome: str, sobrenome: str, profissao: str, especializacao: str,
    nacionalidade: str, disponibilidade: str, atuacao: str, foto: str, sala_de_meet: str,
    estado: str, csv: str, email: str, senha: str, telefone: str) -> None:
        """"""
        self.nome = nome
        self.sobrenome = sobrenome
        self.profissao = profissao
        self.especializacao = especializacao
        self.nacionalidade = nacionalidade
        self.disponibilidade = disponibilidade
        self.atuacao = atuacao
        self.foto = foto
        self.sala_de_meet = sala_de_meet
        self.csv = csv
        self.estado = estado
        self.email = email
        self.senha = senha
        self.telefone = telefone
