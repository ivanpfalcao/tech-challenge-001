URL="http://127.0.0.1:8000"
AUTH_TOKEN="akljnv13bvi2vfo0b0bw"
URL_PATH="producao?id=2"

time curl -X 'GET' \
  "${URL}/${URL_PATH}" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer ${AUTH_TOKEN}"