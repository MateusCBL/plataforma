from http.server import BaseHTTPRequestHandler, HTTPServer
import json, time, uuid
from urllib.parse import urlparse
from datetime import datetime
from app.repository.clientes_repository import ClientesRepository
from app.log import logger

PORT = 8000

class ClientesHandler(BaseHTTPRequestHandler):
    repo = ClientesRepository()

    def _json_response(self, message, data=None, error=None, start_time=None):
        elapsed = int((time.time() - start_time) * 1000) if start_time else 0
        return json.dumps({
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "elapsed": elapsed,
            "error": error,
            "data": data
        }).encode("utf-8")

    def do_GET(self):
        start = time.time()
        parsed = urlparse(self.path)
        if parsed.path == "/clients":
            data = self.repo.list_clients()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(self._json_response("Lista de clientes", data, None, start))
            logger.info("GET /clients OK")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(self._json_response("Rota não encontrada", None, "not_found", start))
            logger.error("GET rota inválida")

def run_server():
    server = HTTPServer(("", PORT), ClientesHandler)
    logger.info(f"Servidor iniciado {PORT}")
    server.serve_forever()