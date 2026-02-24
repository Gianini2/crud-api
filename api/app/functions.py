from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from . import models, schemas
import os

BASE_DATABASE_URL = os.getenv("DATABASE_URL")

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session):
    return db.query(models.Item).all()


def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    db_item = get_item(db, item_id)
    if not db_item:
        return None

    for field, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if not db_item:
        return None

    db.delete(db_item)
    db.commit()
    return db_item


def get_database_list():
    engine = create_engine(BASE_DATABASE_URL)

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT datname FROM pg_database WHERE datistemplate = false;")
        )
        databases = [row[0] for row in result]

    return databases


def get_schemas_for_database(database_name: str):
    base_url = BASE_DATABASE_URL.rsplit("/", 1)[0]
    new_url = f"{base_url}/{database_name}"

    engine = create_engine(new_url)

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT schema_name
                FROM information_schema.schemata
                WHERE schema_name NOT IN ('pg_catalog', 'information_schema');
            """)
        )
        schemas = [row[0] for row in result]

    return schemas

def get_tables_for_schema(database_name: str, schema_name: str):
    base_url = BASE_DATABASE_URL.rsplit("/", 1)[0]
    new_url = f"{base_url}/{database_name}"

    engine = create_engine(new_url)

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = :schema_name
                  AND table_type = 'BASE TABLE';
            """),
            {"schema_name": schema_name}
        )

        tables = [row[0] for row in result]

    return tables

def get_full_structure():
    databases = get_database_list()

    structure = []

    for db in databases:
        schemas = get_schemas_for_database(db)

        schema_list = []

        for schema in schemas:
            tables = get_tables_for_schema(db, schema)

            schema_list.append({
                "schema": schema,
                "tables": tables
            })

        structure.append({
            "database": db,
            "schemas": schema_list
        })

    return structure