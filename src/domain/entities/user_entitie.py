from dataclasses import dataclass


@dataclass
class EUsuario:
    """"""
    nome : str
    sobrenome: str
    provincia: str
    municipio: str
    bi: str
    telefone: str
    email: str
    senha: str
    objectID : str = 'userdataclasse'

