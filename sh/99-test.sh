URL="http://127.0.0.1:8000"
AUTH_TOKEN="allyourbasesbelongtous"

#URL_PATH="producao?id=2"
URL_PATH="comercio?id=1"

time curl -X 'GET' \
  "${URL}/${URL_PATH}" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer ${AUTH_TOKEN}"