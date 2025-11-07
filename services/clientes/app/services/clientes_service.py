import os 
import json
import psycopg2
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import time
import logging

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "clientsdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

LISTEN_PORT = int(os.getenv("LISTEN_PORT", 8001))

logger = logging.getLogger("clients_service")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s')
formatter.converter = time.gmtime
handler.setFormatter(formatter)
logger.addHandler(handler)

def now_iso():
    return datetime.utcnow().isoformat() + "Z"


def json_response(message, elapsed_ms, data=None, error=None):
    resp = {
        "message": message,
        "timestamp": now_iso(),
        "elapsed": int(elapsed_ms),
        "error": error,
    }
    if data is not None:
        resp["data"] = data
    return json.dumps(resp).encode("utf-8")


def get_db_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )

class SimpleHandler(BaseHTTPRequestHandler):
    server_version = "clients-service/0.1"

    def _send(self, status=200, body=b"", content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except Exception:
            return None

    def _log_request_timing(self, start, message):
        elapsed = (time.time() - start) * 1000.0
        logger.info(f"{message} (elapsed_ms={int(elapsed)})")
        return elapsed

    def do_POST(self):
        start = time.time()
        parsed = urlparse(self.path)
        if parsed.path == "/clients":
            body = self._read_json()
            if not body:
                elapsed = self._log_request_timing(start, "create-client: bad payload")
                resp = json_response("Payload inválido", elapsed, error="bad_payload")
                return self._send(400, resp)
            name = body.get("name")
            surname = body.get("surname")
            email = body.get("email")
            birthdate = body.get("birthdate")
            if not (name and surname and email and birthdate):
                elapsed = self._log_request_timing(start, "create-client: missing fields")
                resp = json_response("Campos obrigatórios ausentes", elapsed, error="missing_fields")
                return self._send(400, resp)
            client_id = str(uuid.uuid4())
            created_at = datetime.utcnow()
            try:
                conn = get_db_conn()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO clients (id, name, surname, email, birthdate, active, created_at, updated_at)
                    VALUES (%s,%s,%s,%s,%s,TRUE,%s,%s)
                """, (client_id, name, surname, email, birthdate, created_at, created_at))
                conn.commit()
                cur.close()
                conn.close()
                elapsed = self._log_request_timing(start, f"create-client id={client_id}")
                resp = json_response("Cliente criado com sucesso", elapsed, data={"id": client_id})
                return self._send(201, resp)
            except Exception as e:
                logger.error(f"DB error creating client\t{e}")
                elapsed = self._log_request_timing(start, "create-client: db_error")
                resp = json_response("Erro interno", elapsed, error=str(e))
                return self._send(500, resp)
        else:
            elapsed = self._log_request_timing(start, "post-not-found")
            resp = json_response("Rota não encontrada", elapsed, error="not_found")
            return self._send(404, resp)

    def do_PUT(self):
        start = time.time()
        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "clients":
            client_id = parts[1]
            body = self._read_json()
            if not body:
                elapsed = self._log_request_timing(start, "update-client: bad payload")
                resp = json_response("Payload inválido", elapsed, error="bad_payload")
                return self._send(400, resp)
            fields = {}
            for k in ("name", "surname", "email", "birthdate"):
                if k in body:
                    fields[k] = body[k]
            if not fields:
                elapsed = self._log_request_timing(start, "update-client: no fields")
                resp = json_response("Nenhum campo para atualizar", elapsed, error="no_fields")
                return self._send(400, resp)
            try:
                conn = get_db_conn()
                cur = conn.cursor()
                set_clause = ", ".join([f"{k} = %s" for k in fields.keys()] + ["updated_at = %s"])
                values = list(fields.values()) + [datetime.utcnow(), client_id]
                sql = f"UPDATE clients SET {set_clause} WHERE id = %s AND active = TRUE"
                cur.execute(sql, values)
                if cur.rowcount == 0:
                    conn.commit()
                    cur.close()
                    conn.close()
                    elapsed = self._log_request_timing(start, f"update-client not_found id={client_id}")
                    resp = json_response("Cliente não encontrado ou inativo", elapsed, error="not_found")
                    return self._send(404, resp)
                conn.commit()
                cur.close()
                conn.close()
                elapsed = self._log_request_timing(start, f"update-client id={client_id}")
                resp = json_response("Cliente atualizado", elapsed, data={"id": client_id})
                return self._send(200, resp)
            except Exception as e:
                logger.error(f"DB error updating client\t{e}")
                elapsed = self._log_request_timing(start, "update-client: db_error")
                resp = json_response("Erro interno", elapsed, error=str(e))
                return self._send(500, resp)
        else:
            elapsed = self._log_request_timing(start, "put-not-found")
            resp = json_response("Rota não encontrada", elapsed, error="not_found")
            return self._send(404, resp)

    def do_DELETE(self):
        start = time.time()
        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "clients":
            client_id = parts[1]
            try:
                conn = get_db_conn()
                cur = conn.cursor()
                cur.execute("UPDATE clients SET active = FALSE, updated_at = %s WHERE id = %s AND active = TRUE",
                            (datetime.utcnow(), client_id))
                if cur.rowcount == 0:
                    conn.commit()
                    cur.close()
                    conn.close()
                    elapsed = self._log_request_timing(start, f"delete-client not_found id={client_id}")
                    resp = json_response("Cliente não encontrado ou já inativo", elapsed, error="not_found")
                    return self._send(404, resp)
                conn.commit()
                cur.close()
                conn.close()
                elapsed = self._log_request_timing(start, f"delete-client id={client_id}")
                resp = json_response("Cliente inativado (delete lógico)", elapsed, data={"id": client_id})
                return self._send(200, resp)
            except Exception as e:
                logger.error(f"DB error deleting client\t{e}")
                elapsed = self._log_request_timing(start, "delete-client: db_error")
                resp = json_response("Erro interno", elapsed, error=str(e))
                return self._send(500, resp)
        else:
            elapsed = self._log_request_timing(start, "delete-not-found")
            resp = json_response("Rota não encontrada", elapsed, error="not_found")
            return self._send(404, resp)

    def do_GET(self):
        start = time.time()
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        if path == "/clients":
            active = None
            if "active" in qs:
                v = qs.get("active", ["true"])[0].lower()
                active = True if v in ("1", "true", "yes") else False
            try:
                conn = get_db_conn()
                cur = conn.cursor()
                if active is None:
                    cur.execute("SELECT id, name, surname, email, birthdate, active, created_at, updated_at FROM clients")
                else:
                    cur.execute("SELECT id, name, surname, email, birthdate, active, created_at, updated_at FROM clients WHERE active = %s", (active,))
                rows = cur.fetchall()
                cols = ["id","name","surname","email","birthdate","active","created_at","updated_at"]
                data = [dict(zip(cols, r)) for r in rows]
                cur.close()
                conn.close()
                elapsed = self._log_request_timing(start, f"list-clients count={len(data)}")
                resp = json_response("Lista de clientes", elapsed, data=data)
                return self._send(200, resp)
            except Exception as e:
                logger.error(f"DB error listing clients\t{e}")
                elapsed = self._log_request_timing(start, "list-clients: db_error")
                resp = json_response("Erro interno", elapsed, error=str(e))
                return self._send(500, resp)

        parts = path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "clients":
            client_id = parts[1]
            try:
                conn = get_db_conn()
                cur = conn.cursor()
                cur.execute("SELECT id, name, surname, email, birthdate, active, created_at, updated_at FROM clients WHERE id = %s", (client_id,))
                row = cur.fetchone()
                if not row:
                    cur.close()
                    conn.close()
                    elapsed = self._log_request_timing(start, f"get-client not_found id={client_id}")
                    resp = json_response("Cliente não encontrado", elapsed, error="not_found")
                    return self._send(404, resp)
                cols = ["id","name","surname","email","birthdate","active","created_at","updated_at"]
                data = dict(zip(cols, row))
                cur.close()
                conn.close()
                elapsed = self._log_request_timing(start, f"get-client id={client_id}")
                resp = json_response("Cliente encontrado", elapsed, data=data)
                return self._send(200, resp)
            except Exception as e:
                logger.error(f"DB error get client\t{e}")
                elapsed = self._log_request_timing(start, "get-client: db_error")
                resp = json_response("Erro interno", elapsed, error=str(e))
                return self._send(500, resp)

        elapsed = self._log_request_timing(start, "get-not-found")
        resp = json_response("Rota não encontrada", elapsed, error="not_found")
        return self._send(404, resp)

    def log_message(self, format, *args):
        return
    


def ensure_db():
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            email TEXT NOT NULL,
            birthdate DATE NOT NULL,
            active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        """)
        conn.commit()
        cur.close()
        conn.close()
        logger.info("DB ensure table clients")
    except Exception as e:
        logger.error(f"DB ensure failed\t{e}")


def run():
    ensure_db()
    logger.info(f"Service starting on port {LISTEN_PORT}")
    server = HTTPServer(("0.0.0.0", LISTEN_PORT), SimpleHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Service stopping by KeyboardInterrupt")
    except Exception as e:
        logger.critical(f"Service crashed\t{e}")
    finally:
        server.server_close()
        logger.info("Server stopped")


if __name__ == "__main__":
    run()