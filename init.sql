-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS wolfx_bd;

USE wolfx_bd;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(200),
    email VARCHAR(200),
    senha VARCHAR(200),
    nivel_acesso VARCHAR(200)
);
