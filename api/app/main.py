from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
import os
from . import crud, schemas, metadata

app = FastAPI()

# Dependency Injection da sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### GET:

@app.get("/")
def read_root():
    return {"message": "I'm up =)"}

@app.get("/databases")
def list_databases():
    return metadata.get_full_structure()

@app.get("/env")
def show_env():
    return {"database_url": os.getenv("DATABASE_URL")}

@app.get("/items", response_model=list[schemas.ItemRead])
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.get("/items/{item_id}", response_model=schemas.ItemRead)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

### POST

@app.post("/items", response_model=schemas.ItemRead)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

### PUT

@app.put("/items/{item_id}", response_model=schemas.ItemRead)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

### DELETE

@app.delete("/items/{item_id}", response_model=schemas.ItemRead)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

## Simple test 1
# from fastapi import FastAPI
# from sqlalchemy import text
# from .database import engine

# app = FastAPI()

# @app.get("/")
# def read_root():
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT 1"))
#         return {"db_response": result.scalar()}