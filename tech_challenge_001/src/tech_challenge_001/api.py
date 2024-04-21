import argparse
import logging
import uvicorn
import os
from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from tech_challenge_001 import __version__
from tech_challenge_001.query_engine import TechChallengeQueryEngine

__author__ = "Ivan Falcao"
__copyright__ = "Ivan Falcao"
__license__ = "MIT"

parser = argparse.ArgumentParser()
parser.add_argument('--basedir', default='')
args = parser.parse_args()

api_keys_path = os.path.join(args.basedir, 'keys', 'api_keys_list.txt')

print(f'API Keys Path: {api_keys_path}')
api_keys = open(api_keys_path, 'r').read().split('\n')
print(api_keys)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )

app = FastAPI()
logger = logging.getLogger("uvicorn")

@app.get("/")
async def root():
    return {"message": "Tech Challenge API Service"}

@app.get("/update_data", dependencies=[Depends(api_key_auth)])
def update_data():
    return query_engine.update_data()

@app.get("/query", dependencies=[Depends(api_key_auth)])
async def query_endpoint(query: str):
    result = query_engine.query(query)
    return {"result": result}

@app.get("/producao", dependencies=[Depends(api_key_auth)])
async def get_producao_data(
        id: int | None  = None
        , control: str | None  = None
        , cultivar: str | None  = None
        , ano: str | None  = None
    ):

    params = {}

    if id is not None:
        params['id'] = id

    if control is not None:
        params['control'] = control

    if cultivar is not None:
        params['cultivar'] = cultivar

    if ano is not None:
        params['ano'] = ano

    result = query_engine.query_producao(**params)
    return {"result": result}

@app.get("/exportacao", dependencies=[Depends(api_key_auth)])
async def get_exportacao(
        id: int | None  = None
        , pais: str | None  = None
        , ano: str | None  = None
    ):

    params = {}

    if id is not None:
        params['id'] = id

    if pais is not None:
        params['país'] = pais

    if ano is not None:
        params['ano'] = ano

    result = query_engine.query_exportacao(**params)
    return {"result": result}

@app.get("/importacao", dependencies=[Depends(api_key_auth)])
async def get_importacao(
        id: int | None  = None
        , pais: str | None  = None
        , ano: str | None  = None
    ):

    params = {}

    if id is not None:
        params['id'] = id

    if pais is not None:
        params['país'] = pais

    if ano is not None:
        params['ano'] = ano

    result = query_engine.query_importacao(**params)
    return {"result": result}

@app.get("/producao", dependencies=[Depends(api_key_auth)])
async def get_producao_data(
        id: int | None  = None
        , control: str | None  = None
        , cultivar: str | None  = None
        , ano: str | None  = None
    ):

    params = {}

    if id is not None:
        params['id'] = id

    if control is not None:
        params['control'] = control

    if cultivar is not None:
        params['cultivar'] = cultivar

    if ano is not None:
        params['ano'] = ano

    result = query_engine.query_producao(**params)
    return {"result": result}


@app.get("/processamento", dependencies=[Depends(api_key_auth)])
async def get_processamento_data(
        id: int | None  = None
        , control: str | None  = None
        , cultivar: str | None  = None
        , ano: str | None  = None
    ):

    params = {}

    if id is not None:
        params['id'] = id

    if control is not None:
        params['control'] = control

    if cultivar is not None:
        params['cultivar'] = cultivar

    if ano is not None:
        params['ano'] = ano

    result = query_engine.query_processamento(**params)
    return {"result": result}

# Main execution
if __name__ == "__main__":
    query_engine = TechChallengeQueryEngine(basedir=args.basedir, logger=logger)
    uvicorn.run(app, port=8000, host='0.0.0.0')
