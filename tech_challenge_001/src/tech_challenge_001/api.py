"""
Tech Challenge 001 - FIAP - ML Engineering 2024

This webservice runs an API service that retrieves data from 
http://vitibrasil.cnpuv.embrapa.br/ and store it in disk to be queried by Duckdb

"""

import argparse
import logging
import sys
import uvicorn
import requests
import os
import shutil
import asyncio

from fastapi import FastAPI
from datetime import datetime


from tech_challenge_001 import __version__

__author__ = "Ivan Falcao"
__copyright__ = "Ivan Falcao"
__license__ = "MIT"
basedir = ""
logger = logging.getLogger("uvicorn")

app = FastAPI()

def download_file(url, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename) 

    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as file:
            file.write(response.content)
        logger.info(f"File {url} downloaded successfully as '{filepath}'")

        return True
    else:
        logger.info("Failed to download file")
        return False

def file_download_controller(url, basedir, folder, filename):
    directory = os.path.join(basedir, folder, filename)
    try:
        logger.info(f"Removing dir: '{directory}/'")
        shutil.rmtree(directory)
    except Exception as e:
        logger.warn(e)

    if (download_file(url, directory ,f"{filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")):
        return {"source": f"{filename}", "url": url, "message": f"updated", "ret_code": 0}
    else:
        return {"source": f"{filename}", "url": url, "message": f"not updated", "ret_code": 1}
    
    
@app.get("/update_producao")
async def update_producao():
    url = "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"
    return file_download_controller(url, basedir, "data", "producao")


@app.get("/update_processamento")
async def update_processamento():
    url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv"
    return file_download_controller(url, basedir, "data", "processamento")

@app.get("/update_comercio")
async def update_comercio():
    url = "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv"
    return file_download_controller(url, basedir, "data", "comercio")


@app.get("/update_importacao")
async def update_importacao():
    url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv"
    return file_download_controller(url, basedir, "data", "importacao")    

@app.get("/update_exportacao")
async def update_exportacao():
    url = "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv"
    return file_download_controller(url, basedir, "data", "exportacao")       

    
@app.get("/update_data")
async def update_data():
    resp_list = []
    results = []
    resp_list.append(update_producao())
    resp_list.append(update_processamento())
    resp_list.append(update_comercio())
    resp_list.append(update_importacao())
    resp_list.append(update_exportacao())

    results.extend(await asyncio.gather(*resp_list))

    return results

@app.get("/")
async def root():
    return {"message": f"Hello World {basedir}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--basedir')
    args = parser.parse_args()

    basedir = args.basedir
    
    #run server
    uvicorn.run(app)