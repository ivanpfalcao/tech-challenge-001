import argparse
import logging
import uvicorn
import requests
import os
import shutil
from datetime import datetime
import duckdb
from fastapi import FastAPI

from tech_challenge_001 import __version__
from tech_challenge_001.query_engine import TechChallengeQueryEngine

__author__ = "Ivan Falcao"
__copyright__ = "Ivan Falcao"
__license__ = "MIT"

app = FastAPI()
logger = logging.getLogger("uvicorn")

@app.get("/")
async def root():
    return {"message": "Tech Challenge API Service"}

@app.get("/update_data")
def update_data():
    return query_engine.update_data()

@app.get("/query")
async def query_endpoint(query: str):
    result = query_engine.query(query)
    return {"result": result}

@app.get("/producao")
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

@app.get("/producao")
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

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--basedir', default='')
    args = parser.parse_args()

    query_engine = TechChallengeQueryEngine(basedir=args.basedir, logger=logger)
    uvicorn.run(app)
