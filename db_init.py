import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

USER=os.environ["POSTGRES_USER"]
PASSWORD=os.environ["POSTGRES_PASSWORD"]
POST_DB=os.environ["POSTGRES_DB"]

PORT=os.environ["PORT"]

with psycopg.connect(f"postgresql://{USER}:{PASSWORD}@localhost:{PORT}/{POST_DB}") as conn:
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id SERIAL PRIMARY KEY,
                documento TEXT,
                pagina INT,
                origen TEXT,
                metodo TEXT,
                texto TEXT,
                embedding vector(1024)
            );
        """)

print("Tabla creada")
print("Extension creada")