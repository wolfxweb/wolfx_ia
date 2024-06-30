# models/categoriaModel.py
from pydantic import BaseModel

class Categoria(BaseModel):
    nome: str
