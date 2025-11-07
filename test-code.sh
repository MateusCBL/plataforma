set -e

BASE="http://localhost:8001"

echo "=> Test: create client"
CREATE_RESP=$(curl -s -X POST "$BASE/clients" -H "Content-Type: application/json" -d '{"name":"Mateus","surname":"Chaves","email":"mateus@example.com","birthdate":"2004-06-08"}')
echo "$CREATE_RESP" | python -m json.tool
ID=$(echo "$CREATE_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
echo "created id: $ID"

echo "=> Test: get client"
curl -s "$BASE/clients/$ID" | python -m json.tool

echo "=> Test: update client"
curl -s -X PUT "$BASE/clients/$ID" -H "Content-Type: application/json" -d '{"name":"MateusUpdated"}' | python -m json.tool

echo "=> Test: list clients (active=true)"
curl -s "$BASE/clients?active=true" | python -m json.tool

echo "=> Test: logical delete client"
curl -s -X DELETE "$BASE/clients/$ID" | python -m json.tool

echo "=> Test: list clients (active=false)"
curl -s "$BASE/clients?active=false" | python -m json.tool

echo "ALL CLIENTS TESTS OK"