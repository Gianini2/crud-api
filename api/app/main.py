from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
import os
from . import functions, schemas

app = FastAPI()

# Dependency Injection of the session
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

@app.get("/getdata/schema/{schema}/table/{table}")
def get_table(schema: str, table: str, db: Session = Depends(get_db)):
    try:
        data = functions.get_table_data(db, schema, table)
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

### POST

@app.post("posttable/schema/{schema}/table/{table}")
def create_table_from_payload(
    schema: str,
    table: str,
    payload: list[dict],
    db: Session = Depends(get_db),
):
    try:
        if not payload:
            raise HTTPException(status_code=400, detail="Payload cannot be empty")

        return functions.insert_table_from_payload(db, schema, table, payload)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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