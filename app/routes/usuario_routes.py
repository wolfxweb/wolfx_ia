from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, HTTPException, Depends

from controllers.usuarios.usuarioController import UsuarioController
from models.usuariosModel import Usuario 
router = APIRouter()


# class Usuario(BaseModel):
#     id: int = None
#     nome: str
#     email: str
#     senha: str
#     nivel_acesso: str
    
controller = UsuarioController()

@router.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    return controller.listar_usuarios()


@router.get("/usuarios/{usuario_id}", response_model=Usuario)
def obter_usuario(usuario_id: int):
    usuario = controller.obter_usuario(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.post("/usuarios", response_model=Usuario)
def criar_usuario(usuario: Usuario):
    return controller.criar_usuario(usuario)

@router.put("/usuarios/{usuario_id}", response_model=Usuario)
def atualizar_usuario(usuario_id: int, usuario: Usuario):
    usuario_atualizado = controller.atualizar_usuario(usuario_id, usuario)
    if usuario_atualizado is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario_atualizado

@router.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int):
    usuario_deletado = controller.deletar_usuario(usuario_id)
    if usuario_deletado is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário deletado com sucesso"}
