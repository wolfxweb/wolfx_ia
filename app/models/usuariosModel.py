# models/usuariosModel.py

from pydantic import BaseModel

class Usuario(BaseModel):
    id: int = None
    nome: str
    email: str
    senha: str
    nivel_acesso: str
