import urllib.request
import json

BASE_URL = "http://cotacoes:8004/cotacoes"

def obter_cotacoes():
    try:
        with urllib.request.urlopen(BASE_URL) as response:
            data = json.loads(response.read().decode())
            return {item["code"]: item["value"] for item in data["data"]}
    except Exception as e:
        print(f"[ERRO] Falha ao obter cotações: {e}")
        return {}