set -e

docker-compose up -d --build

echo "Aguardando postgres inicializar..."
until docker exec $(docker ps -q -f "name=postgres") pg_isready -U postgres >/dev/null 2>&1; do
  echo "waiting for postgres..."
  sleep 1
done
echo "Postgres pronto."

echo "Aguardando serviço de clientes iniciar (10s)..."
sleep 10

echo "Executando tests clients-service..."
./clients-service/test-code.sh

echo "PARABÉNS: testes executados com sucesso."

#!/usr/bin/env bash