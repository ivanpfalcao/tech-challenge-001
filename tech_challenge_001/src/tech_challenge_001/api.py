import argparse
import logging
import uvicorn
import requests
import os
import shutil
from datetime import datetime
import duckdb
from fastapi import FastAPI

# Assuming tech_challenge_001 contains necessary version information
from tech_challenge_001 import __version__

__author__ = "Ivan Falcao"
__copyright__ = "Ivan Falcao"
__license__ = "MIT"

app = FastAPI()
logger = logging.getLogger("uvicorn")

class TechChallengeAPI:
    def __init__(self, basedir):
        self.basedir = basedir
        self.conn = duckdb.connect(database=':memory:')
        self.initialize_db()

    def download_file(self, url, directory, filename):
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

    def file_download_controller(self, url, folder, filename):
        directory = os.path.join(self.basedir, folder, filename)

        shutil.rmtree(directory)
        final_filename = f"{filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        if self.download_file(url, directory, final_filename):
            return {"source": filename, "url": url, "message": "updated", "ret_code": 0}
        else:
            return {"source": filename, "url": url, "message": "not updated", "ret_code": 1}

    def create_view(self, table):
        self.conn.execute(f"""
            CREATE VIEW tb_{table} AS 
            SELECT *
            FROM read_csv_auto('{self.basedir}/data/{table}/*', header=true)
        """)          

    def initialize_db(self):
        self.update_data()
        table_list = [
            'comercio'
            ,'exportacao'
            ,'importacao'
            ,'processamento'
            ,'producao'
        ]

        for table in table_list:
            self.create_view(table)    

        self.conn.execute(f"""
            SET old_implicit_casting = true;
            CREATE VIEW tb_exportacao_unp AS (
                UNPIVOT tb_exportacao
                ON COLUMNS(* EXCLUDE (Id, País))
                INTO
                    NAME ano
                    VALUE valor
            )                
        """)
        self.conn.execute(f"""
            CREATE VIEW tb_importacao_unp AS (
                UNPIVOT tb_importacao
                ON COLUMNS(* EXCLUDE (Id, País))
                INTO
                    NAME ano
                    VALUE valor
            )                
        """)        
        self.conn.execute(f"""
            
            CREATE VIEW tb_processamento_unp AS (
                UNPIVOT tb_processamento
                ON COLUMNS(* EXCLUDE (id, control, cultivar))
                INTO
                    NAME ano
                    VALUE valor
            );              
        """)
        self.conn.execute(f"""
            CREATE VIEW tb_producao_unp AS (
                UNPIVOT tb_producao
                ON COLUMNS(* EXCLUDE (id, produto))
                INTO
                    NAME ano
                    VALUE valor
            )                
        """)                                  

    def update_data(self):
        response = []
        response.append(self.update_producao())
        response.append(self.update_processamento())
        response.append(self.update_comercio())
        response.append(self.update_importacao())
        response.append(self.update_exportacao())
        return response

    def update_producao(self):
        url = "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"
        return self.file_download_controller(url, "data", "producao")

    def update_processamento(self):
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv"
        return self.file_download_controller(url, "data", "processamento")

    def update_comercio(self):
        url = "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv"
        return self.file_download_controller(url, "data", "comercio")

    def update_importacao(self):
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv"
        return self.file_download_controller(url, "data", "importacao")

    def update_exportacao(self):
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv"
        return self.file_download_controller(url, "data", "exportacao")

    def query(self, query_str):
        out_df = self.conn.execute(query_str).pl().to_dicts()
        return out_df

# FastAPI endpoint definitions
@app.get("/")
async def root():
    return {"message": "Tech Challenge API Service"}

@app.get("/update_data")
def update_data():
    return api.update_data()

@app.get("/query")
async def query_endpoint(query: str):
    result = api.query(query)
    return {"result": result}

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--basedir', default='')
    args = parser.parse_args()

    api = TechChallengeAPI(basedir=args.basedir)
    uvicorn.run(app)
