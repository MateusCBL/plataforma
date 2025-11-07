import psycopg2
import os

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db_cotacoes"),
        database=os.getenv("DB_NAME", "cotacoes_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "postgres")
    )

def salvar_cotacao(cotacao):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO cotacoes (code, value, created_at)
        VALUES (%s, %s, %s)
        ON CONFLICT (code)
        DO UPDATE SET value = EXCLUDED.value, created_at = EXCLUDED.created_at
    """, (cotacao.code, cotacao.value, cotacao.created_at))
    conn.commit()
    cur.close()
    conn.close()

def listar_cotacoes():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT code, value, created_at FROM cotacoes")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return [{"code": d[0], "value": d[1], "created_at": d[2]} for d in data]

def buscar_cotacao(code):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT code, value, created_at FROM cotacoes WHERE code = %s", (code,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    if data:
        return {"code": data[0], "value": data[1], "created_at": data[2]}
    return None