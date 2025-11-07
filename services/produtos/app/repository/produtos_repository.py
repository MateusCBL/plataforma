import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "produtos_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "postgres")
    )

def inserir_produto(produto):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO produtos (id, nome, descricao, preco, estoque, ativo, criado_em, atualizado_em)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (produto.id, produto.nome, produto.descricao, produto.preco, produto.estoque,
          produto.ativo, produto.criado_em, produto.atualizado_em))
    conn.commit()
    cur.close()
    conn.close()