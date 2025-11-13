import uuid
import json
import urllib.request
from datetime import datetime
from app.domain.venda import Venda
from app.domain.item_venda import ItemVenda
from app.repository.vendas_repository import create_venda, create_item

URL_CLIENTES = "http://clientes:8001"
URL_PRODUTOS = "http://produtos:8002"
URL_COTACOES = "http://cotacoes:8004"

def chamar_api(url):
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Erro ao chamar {url}: {e}")
        return None


def validar_cliente(client_id):
    resp = chamar_api(f"{URL_CLIENTES}/clientes/{client_id}")
    return resp and resp.get("data")


def validar_produto(product_id, quantidade):
    resp = chamar_api(f"{URL_PRODUTOS}/produtos/{product_id}")
    if not resp or not resp.get("data"):
        return None
    produto = resp["data"]
    if produto["quantity"] < quantidade:
        return None
    return produto


def obter_cotacoes():
    return chamar_api(f"{URL_COTACOES}/cotacoes")


def nova_venda(client_id):
    if not validar_cliente(client_id):
        raise ValueError("Cliente não encontrado")
    
    venda = Venda(str(uuid.uuid4()), client_id)
    create_venda(venda)
    return venda


def adicionar_item(sell_id, product_id, quantity):
    produto = validar_produto(product_id, quantity)
    if not produto:
        raise ValueError("Produto inválido ou sem estoque")

    item = ItemVenda(sell_id, product_id, quantity)
    create_item(item)
    return item


def efetivar_venda(sell_id, itens):
    total_brl = 0.0
    for i in itens:
        produto = validar_produto(i["product_id"], i["quantity"])
        total_brl += produto["price"] * i["quantity"]

    cotacoes = obter_cotacoes()
    totais = {"BRL": total_brl}

    if cotacoes:
        for c in cotacoes["data"]:
            code = c["code"]
            value = c["value"]
            totais[code] = round(total_brl * value, 2)

    return totais
