from http.server import BaseHTTPRequestHandler
import json
from app.services.produtos_service import criar_produto

class ProdutosHandler(BaseHTTPRequestHandler):

    def _send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        if self.path == "/produtos":
            length = int(self.headers.get("Content-Length"))
            body = json.loads(self.rfile.read(length).decode())
            try:
                novo_produto = criar_produto(body)
                self._send_json(201, {"message": "Produto criado", "produto": novo_produto})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        else:
            self._send_json(404, {"error": "Rota não encontrada"})