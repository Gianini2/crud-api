from sqlalchemy import create_engine, text
import os


BASE_DATABASE_URL = os.getenv("DATABASE_URL")


def get_database_list():
    engine = create_engine(BASE_DATABASE_URL)

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT datname FROM pg_database WHERE datistemplate = false;")
        )
        databases = [row[0] for row in result]

    return databases


def get_schemas_for_database(database_name: str):
    # reconstruir URL com outro database
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


def get_full_structure():
    databases = get_database_list()

    structure = []

    for db in databases:
        schemas = get_schemas_for_database(db)
        structure.append({
            "database": db,
            "schemas": schemas
        })

    return structure