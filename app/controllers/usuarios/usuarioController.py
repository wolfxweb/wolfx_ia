from pydantic import BaseModel
from typing import List
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do banco de dados
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

# Modelo Pydantic para Usuário
class Usuario(BaseModel):
    id: int = None
    nome: str
    email: str
    senha: str
    nivel_acesso: str

# Classe para manipulação de usuários
class UsuarioController:
    def __init__(self):
        self.conn = mysql.connector.connect(**db_config)

    def __del__(self):
        self.conn.close()

    def listar_usuarios(self) -> List[Usuario]:
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        return [Usuario(**usuario) for usuario in usuarios]

    def obter_usuario(self, usuario_id: int) -> Usuario:
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            return None
        return Usuario(**usuario)

    def criar_usuario(self, usuario: Usuario) -> Usuario:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, nivel_acesso) VALUES (%s, %s, %s, %s)",
            (usuario.nome, usuario.email, usuario.senha, usuario.nivel_acesso)
        )
        self.conn.commit()
        usuario.id = cursor.lastrowid
        return usuario

    def atualizar_usuario(self, usuario_id: int, usuario: Usuario) -> Usuario:
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET nome = %s, email = %s, senha = %s, nivel_acesso = %s WHERE id = %s",
            (usuario.nome, usuario.email, usuario.senha, usuario.nivel_acesso, usuario_id)
        )
        self.conn.commit()
        usuario.id = usuario_id
        return usuario

    def deletar_usuario(self, usuario_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        self.conn.commit()
