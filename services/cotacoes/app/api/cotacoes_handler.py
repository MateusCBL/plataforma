from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import json, time
from app.services.cotacoes_service import obter_cotacoes, obter_cotacao_especifica

class CotacoesHandler(BaseHTTPRequestHandler):
    def _json(self, code, message, data=None, error=None, start=None):
        elapsed = int((time.time() - start) * 1000)
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

    def do_GET(self):
        start = time.time()
        parsed = urlparse(self.path)
        path = parsed.path.split("/")
        try:
            if parsed.path == "/cotacoes":
                data = obter_cotacoes()
                self._json(200, "Cotações retornadas", data, start=start)
            elif len(path) == 3 and path[1] == "cotacoes":
                code = path[2].upper()
                data = obter_cotacao_especifica(code)
                if data:
                    self._json(200, f"Cotação {code} retornada", data, start=start)
                else:
                    self._json(404, f"Cotação {code} não encontrada", start=start)
            else:
                self._json(404, "Rota inválida", start=start)
        except Exception as e:
            self._json(500, "Erro interno", error=str(e), start=start)