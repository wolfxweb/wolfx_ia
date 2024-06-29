# Use the official Lightweight Python image
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todos os arquivos do diretório atual para o diretório de trabalho do contêiner
COPY . .

# Exponha as portas que o Streamlit e FastAPI usarão
EXPOSE 8501
EXPOSE 8000

# Comando para rodar o Streamlit e FastAPI simultaneamente
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]
