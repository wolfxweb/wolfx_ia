# Inclui o roteador de usuários com prefixo /api
from fastapi import FastAPI
from routes.usuario_routes import router as usuario_router

app = FastAPI()

# Inclui o roteador de usuários com prefixo /api
app.include_router(usuario_router, prefix="/api")
