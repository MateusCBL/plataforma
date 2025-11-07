import psycopg2
import os

def get_db_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db_vendas"),
        database=os.getenv("DB_NAME", "vendas_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "postgres")
    )

def create_venda(venda):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO vendas (id, client_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (venda.id, venda.client_id, venda.status, venda.created_at, venda.updated_at))
    conn.commit()
    cur.close()
    conn.close()

def create_item(item):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO itens_venda (sell_id, product_id, quantity, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (item.sell_id, item.product_id, item.quantity, item.created_at, item.updated_at))
    conn.commit()
    cur.close()
    conn.close()