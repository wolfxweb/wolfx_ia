# routes/categoria_routes.py
from fastapi import APIRouter, HTTPException
#from models.categoriaModel import Categoria

router = APIRouter()
# models/categoriaModel.py
from pydantic import BaseModel

class Categoria(BaseModel):
    nome: str

@router.post("/predictcategoria", response_model=Categoria)
def predict_categoria(categoria: Categoria):
    # Implementação da lógica de predição aqui
    # Exemplo de retorno
    return categoria
