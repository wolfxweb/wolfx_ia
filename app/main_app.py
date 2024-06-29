import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
# Configuração da conexão MySQL
MYSQL_HOST = "mysql"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DATABASE = "wolfx_bd"
# Configuração do banco de dados
db_config = {
    'host': MYSQL_HOST,
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'database': MYSQL_DATABASE
}

# Função para obter conexão com o banco de dados
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Interface do Streamlit
st.title("Gerenciamento de Usuários")

menu = ["Adicionar Usuário", "Listar Usuários"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Adicionar Usuário":
    st.subheader("Adicionar Novo Usuário")

    with st.form(key='usuario_form'):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type='password')
        nivel_acesso = st.selectbox("Nível de Acesso", ["Admin", "User"])
        submit_button = st.form_submit_button(label='Adicionar Usuário')

    if submit_button:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, nivel_acesso) VALUES (%s, %s, %s, %s)",
            (nome, email, senha, nivel_acesso)
        )
        conn.commit()
        conn.close()
        st.success("Usuário adicionado com sucesso")

elif choice == "Listar Usuários":
    st.subheader("Lista de Usuários")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()

    for usuario in usuarios:
        st.write(f"ID: {usuario['id']}")
        st.write(f"Nome: {usuario['nome']}")
        st.write(f"Email: {usuario['email']}")
        st.write(f"Nível de Acesso: {usuario['nivel_acesso']}")
        st.write("---")
