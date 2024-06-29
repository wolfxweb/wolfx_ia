from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import langchain

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    db = SessionLocal()
    item = db.execute(f"SELECT * FROM items WHERE id = {item_id}").fetchone()
    db.close()
    if item:
        return {"item": dict(item)}
    return {"error": "Item not found"}

# Example Langchain usage
@app.get("/langchain_example")
def langchain_example():
    # Placeholder for Langchain integration
    return {"message": "Langchain integration here"}
