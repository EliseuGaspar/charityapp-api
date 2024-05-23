from pydantic import BaseModel

class ApoiadoresDantic(BaseModel):
    """"""
    id: int
    nome: str
    email: str
    telefone: str
    senha: str
    sobrenome: str
    profissao: str
    especializacao: str
    nacionalidade: str
    disponibilidade: str
    atuacao: str
    foto: str
    sala_de_meet: str
    csv: str
    estado: bool