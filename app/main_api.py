# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.usuario_routes import router as usuario_router
from routes.categorias_routes import router as categoria_router
from database import engine, Base

app = FastAPI()

# Configuração CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router, prefix="/api")
app.include_router(categoria_router, prefix="/api")


#TODO Falta finalizar a configuração do alembic para criação das migrates automaticamente.
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
