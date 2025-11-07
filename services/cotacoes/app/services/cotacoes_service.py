import urllib.request
import json
from datetime import datetime, timedelta
from app.domain.cotacao import Cotacao
from app.repository.cotacoes_repository import salvar_cotacao, listar_cotacoes, buscar_cotacao

API_URL = "https://open.er-api.com/v6/latest/BRL"

MOEDAS = ["USD", "EUR", "GBP", "CNY"]

def precisa_atualizar(cotacao):
    if not cotacao:
        return True
    agora = datetime.utcnow()
    return (agora - cotacao["created_at"]) > timedelta(days=1)

def atualizar_cotacoes():
    try:
        with urllib.request.urlopen(API_URL) as response:
            data = json.loads(response.read().decode())
            rates = data.get("rates", {})
            for code in MOEDAS:
                if code in rates:
                    cot = Cotacao(code, rates[code])
                    salvar_cotacao(cot)
    except Exception as e:
        print(f"Erro ao atualizar cotações: {e}")

def obter_cotacoes():
    todas = listar_cotacoes()
    if not todas or precisa_atualizar(todas[0]):
        atualizar_cotacoes()
        todas = listar_cotacoes()
    return todas

def obter_cotacao_especifica(code):
    cotacao = buscar_cotacao(code)
    if precisa_atualizar(cotacao):
        atualizar_cotacoes()
        cotacao = buscar_cotacao(code)
    return cotacao