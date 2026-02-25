from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
import os
from . import functions, schemas

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

@app.get("/dbdescribe")
def dbdescribe():
    return functions.get_full_structure()

@app.get("/env")
def show_env():
    return {"database_url": os.getenv("DATABASE_URL")} ## TODO: Security issue: password exposed 

@app.get("/items", response_model=list[schemas.ItemRead])
def read_items(db: Session = Depends(get_db)):
    return functions.get_items(db)

@app.get("/items/{item_id}", response_model=schemas.ItemRead)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = functions.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

### POST

@app.post("/items", response_model=schemas.ItemRead)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return functions.create_item(db, item)

### PUT

@app.put("/items/{item_id}", response_model=schemas.ItemRead)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = functions.update_item(db, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

### DELETE

@app.delete("/items/{item_id}", response_model=schemas.ItemRead)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = functions.delete_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item