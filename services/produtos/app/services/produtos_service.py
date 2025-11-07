import uuid
from datetime import datetime
from app.domain.produto import Produto
from app.repository.produtos_repository import inserir_produto

def criar_produto(data):
    produto = Produto(
        id=str(uuid.uuid4()),
        nome=data.get("nome"),
        descricao=data.get("descricao"),
        preco=data.get("preco"),
        estoque=data.get("estoque"),
        ativo=True,
        criado_em=datetime.now(),
        atualizado_em=datetime.now()
    )
    inserir_produto(produto)
    return produto.to_dict()