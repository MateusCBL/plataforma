from app.api.clientes_handler import run_server
from app.log import logger

if __name__ == "__main__":
    logger.info("Iniciando serviço de clientes...")
    run_server()