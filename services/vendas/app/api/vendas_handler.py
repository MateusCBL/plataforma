from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import json, time
from app.services.vendas_service import nova_venda, adicionar_item, efetivar_venda

class VendasHandler(BaseHTTPRequestHandler):
    def _json(self, code, message, data=None, error=None, start=None):
        elapsed = int((time.time() - start) * 1000) if start else 0
        resp = {
            "message": message,
            "timestamp": time.time(),
            "elapsed": elapsed,
            "error": error,
            "data": data
        }
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(resp, default=str).encode())

    def do_POST(self):
        start = time.time()
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length or 0)) if length > 0 else {}

        try:
            if parsed.path == "/vendas":
                client_id = body.get("client_id")
                venda = nova_venda(client_id)
                self._json(201, "Venda criada", {"id": venda.id}, start=start)

            elif parsed.path == "/vendas/item":
                item = adicionar_item(body["sell_id"], body["product_id"], body["quantity"])
                self._json(201, "Item adicionado", {"id": item.sell_id}, start=start)

            elif parsed.path == "/vendas/efetivar":
                totais = efetivar_venda(body["sell_id"], body["itens"])
                self._json(200, "Venda finalizada", {"totais": totais}, start=start)

            else:
                self._json(404, "Rota não encontrada", start=start)

        except ValueError as e:
            self._json(400, "Erro de validação", error=str(e), start=start)
        except Exception as e:
            self._json(500, "Erro interno", error=str(e), start=start)