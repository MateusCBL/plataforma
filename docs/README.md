## 🚀 Objetivo do Projeto

Aplicar os conceitos de:
- Arquitetura de microsserviços  
- Integração entre APIs  
- Comunicação entre containers  
- Boas práticas de logs, camadas e testes  

O sistema permite:
- Gerenciar **clientes**
- Gerenciar **produtos**
- Consultar **cotações de moedas estrangeiras**
- Registrar e controlar **vendas** integradas aos demais serviços

---

## 🧱 Estrutura de Microsserviços

Cada serviço é independente, com seu próprio banco de dados e container.

| Serviço | Descrição | Porta |
|----------|------------|-------|
| `clientes` | CRUD de clientes | 8001 |
| `produtos` | CRUD de produtos, controle de estoque e preço | 8002 |
| `vendas` | Controle de vendas, integração com clientes, produtos e cotações | 8003 |
| `cotacoes` | Serviço que fornece cotações de moedas (USD, EUR, GBP, CNY) | 8004 |

---

## ⚙️ Tecnologias Utilizadas

| Tecnologia | Uso |
|-------------|-----|
| **Python 3.10+** | Linguagem principal |
| **Flask** | Framework web para criação das APIs REST |
| **SQLite** | Banco de dados leve para cada microsserviço |
| **Docker & Docker Compose** | Contêinerização e orquestração dos serviços |
| **urllib / json (padrão do Python)** | Comunicação entre serviços (HTTP) |
| **datetime, uuid, logging** | Controle de logs, IDs e timestamps |
| **pytest / bash script** | Execução de testes automatizados (`test-code.sh` e `run-tests.sh`) |

> Obs: Foi utilizado o **mínimo de bibliotecas externas possíveis**, priorizando módulos nativos do Python.

---

## 🧩 Lógica Geral do Sistema

### 🧍 Cadastro de Clientes
Permite:
- Criar, listar, editar e inativar clientes  
- Armazenar informações básicas como nome, email e data de nascimento  

### 📦 Cadastro de Produtos
Permite:
- Cadastrar produtos, alterar características e preço  
- Atualizar estoque  
- Listar produtos convertendo automaticamente o preço para outras moedas via **serviço de cotações**

### 💱 Serviço de Cotações
- Fornece as taxas de câmbio diárias (BRL → USD, EUR, GBP, CNY)  
- Usa cache interno para não consultar a API externa mais de uma vez por dia  
- Pode retornar **todas as moedas** ou apenas **uma específica**  

### 🧾 Controle de Vendas
- Cria uma venda para um cliente (verificando via API de clientes)  
- Adiciona produtos (verificando disponibilidade via API de produtos)  
- Efetiva a venda (reduz estoque e calcula total)  
- Calcula automaticamente o **valor total da venda em todas as moedas**  
- Suporta cancelamento e alteração de itens

## 🐳 Executando o Projeto

1️⃣ Clone o repositório:
git clone https://github.com/<seu-usuario>/plataforma-tcc
cd plataforma-tcc
2️⃣ Dê permissão aos scripts:
chmod +x test-code.sh run-tests.sh
3️⃣ Construa e suba todos os containers
docker compose up --build
4️⃣ Teste se tudo está funcionando
./run-tests.sh
