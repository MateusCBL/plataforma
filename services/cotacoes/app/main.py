from http.server import HTTPServer
from app.api.cotacoes_handler import CotacoesHandler

def run():
    server = HTTPServer(("", 8004), CotacoesHandler)
    print("Serviço de Cotações rodando na porta 8004...")
    server.serve_forever()

if __name__ == "__main__":
    run()