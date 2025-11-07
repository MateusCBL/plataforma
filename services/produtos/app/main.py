from http.server import HTTPServer
from app.api.produtos_handler import ProdutosHandler

def run(server_class=HTTPServer, handler_class=ProdutosHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor de produtos rodando na porta {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()