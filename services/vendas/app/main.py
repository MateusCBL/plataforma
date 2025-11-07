from http.server import HTTPServer
from app.api.vendas_handler import VendasHandler

def run(server_class=HTTPServer, handler_class=VendasHandler):
    server = server_class(("", 8003), handler_class)
    print("Vendas service running on port 8003")
    server.serve_forever()

if __name__ == "__main__":
    run()