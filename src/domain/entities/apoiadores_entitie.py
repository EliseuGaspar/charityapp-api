""""""
from dataclasses import dataclass

@dataclass
class EApoiadores:
    nome: str
    email: str
    senha: str
    telefone: str
    sobrenome: str
    profissao: str
    especializacao: str
    nacionalidade: str
    disponibilidade: str #hora
    atuacao: str #local/remota
    foto: str #link da foto do mesmo(Firebase)
    sala_de_meet: str #link da sala de meet
    estado: bool
    csv: str

