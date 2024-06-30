from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

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

# Função para obter conexão com o banco de dados
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@router.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

@router.get("/usuarios/{usuario_id}", response_model=Usuario)
def obter_usuario(usuario_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
    usuario = cursor.fetchone()
    conn.close()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.post("/usuarios", response_model=Usuario)
def criar_usuario(usuario: Usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, nivel_acesso) VALUES (%s, %s, %s, %s)",
        (usuario.nome, usuario.email, usuario.senha, usuario.nivel_acesso)
    )
    conn.commit()
    usuario.id = cursor.lastrowid
    conn.close()
    return usuario

@router.put("/usuarios/{usuario_id}", response_model=Usuario)
def atualizar_usuario(usuario_id: int, usuario: Usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET nome = %s, email = %s, senha = %s, nivel_acesso = %s WHERE id = %s",
        (usuario.nome, usuario.email, usuario.senha, usuario.nivel_acesso, usuario_id)
    )
    conn.commit()
    conn.close()
    usuario.id = usuario_id
    return usuario

@router.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
    conn.commit()
    conn.close()
    return {"message": "Usuário deletado com sucesso"}
