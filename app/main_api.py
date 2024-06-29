from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# MYSQL_HOST = "mysql"
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "root"
# MYSQL_DATABASE = "wolfx_bd"
# # Configuração do banco de dados
# db_config = {
#     'host': MYSQL_HOST,
#     'user': MYSQL_USER,
#     'password': MYSQL_PASSWORD,
#     'database': MYSQL_DATABASE
# }


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


@app.get("/")
def root():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
      #  cursor.execute("SHOW TABLES")
      #  tables = cursor.fetchall()
        conn.close()
       # return {"tables": [table[0] for table in tables]}
        return {"databases": [db[0] for db in databases]}
    else:
        return {"message": "Erro ao conectar com o MySQL."}

@app.get("/tabela")
def root():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        # Criação da tabela 'usuarios' se não existir
        create_table_query = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            senha VARCHAR(255) NOT NULL,
            nivel_acesso VARCHAR(50) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        conn.commit()
        
        # Verificar se a tabela foi criada com sucesso
        cursor.execute("SHOW TABLES LIKE 'usuarios'")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {"message": "Tabela 'usuarios' criada com sucesso."}
        else:
            return {"message": "Erro ao criar a tabela 'usuarios'."}
    else:
        return {"message": "Erro ao conectar com o MySQL."}
 

    
@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def obter_usuario(usuario_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
    usuario = cursor.fetchone()
    conn.close()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@app.post("/usuarios", response_model=Usuario)
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

@app.put("/usuarios/{usuario_id}", response_model=Usuario)
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

@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
    conn.commit()
    conn.close()
    return {"message": "Usuário deletado com sucesso"}
