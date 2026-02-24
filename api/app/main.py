from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.get("/env")
def show_env():
    return {"database_url": os.getenv("DATABASE_URL")}