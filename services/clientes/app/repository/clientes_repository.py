import psycopg2, os
from app.domain.cliente import Cliente
from app.log import logger

def get_db_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5433"),
        database=os.getenv("DB_NAME", "clientsdb"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASS", "password")
    )

class ClientesRepository:
    def list_clients(self):
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, name, surname, email, birthdate, active, created_at, updated_at FROM clients;")
        rows = cur.fetchall()
        conn.close()
        return [Cliente(*r).to_dict() for r in rows]

    def create_client(self, name, surname, email, birthdate):
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO clients (name, surname, email, birthdate, active)
            VALUES (%s, %s, %s, %s, TRUE)
            RETURNING id;
        """, (name, surname, email, birthdate))
        client_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        logger.info(f"Cliente criado id={client_id}")
        return client_id