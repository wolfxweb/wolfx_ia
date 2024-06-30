# controllers/usuarios/usuarioController.py
from sqlalchemy.orm import Session
from typing import List
from models.usuariosModel import Usuario as UsuarioModel
from database import SessionLocal

class UsuarioController:
    def __init__(self):
        self.db: Session = SessionLocal()

    def __del__(self):
        self.db.close()

    def listar_usuarios(self) -> List[UsuarioModel]:
        return self.db.query(UsuarioModel).all()

    def obter_usuario(self, usuario_id: int) -> UsuarioModel:
        return self.db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()

    def criar_usuario(self, usuario: UsuarioModel) -> UsuarioModel:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def atualizar_usuario(self, usuario_id: int, usuario: UsuarioModel) -> UsuarioModel:
        usuario_atual = self.db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
        if usuario_atual:
            usuario_atual.nome = usuario.nome
            usuario_atual.email = usuario.email
            usuario_atual.senha = usuario.senha
            usuario_atual.nivel_acesso = usuario.nivel_acesso
            self.db.commit()
            self.db.refresh(usuario_atual)
        return usuario_atual

    def deletar_usuario(self, usuario_id: int) -> bool:
        usuario = self.db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False
