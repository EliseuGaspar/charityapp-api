from pydantic import BaseModel


class UserDantic(BaseModel):
    nome : str
    sobrenome: str
    provincia: str
    municipio: str
    bi: str
    telefone: str
    email: str
    senha: str
