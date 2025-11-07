class Produto:
    def __init__(self, id, nome, descricao, preco, estoque, ativo=True, criado_em=None, atualizado_em=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.ativo = ativo
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "estoque": self.estoque,
            "ativo": self.ativo,
            "criado_em": str(self.criado_em) if self.criado_em else None,
            "atualizado_em": str(self.atualizado_em) if self.atualizado_em else None
        }