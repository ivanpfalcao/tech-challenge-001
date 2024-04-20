BASEDIR=$(cd -P -- "$(dirname -- "${0}")" && pwd -P)

echo "BASEDIR: ${BASEDIR}"
#uvicorn tech_challenge_001.api:app --reload
python -m tech_challenge_001.api --basedir "${BASEDIR}"