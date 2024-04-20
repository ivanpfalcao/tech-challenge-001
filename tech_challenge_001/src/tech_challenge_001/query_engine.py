import logging
import requests
import os
import shutil
from datetime import datetime
import duckdb

class TechChallengeQueryEngine:
    def __init__(self, basedir, logger):
        self.logger = logger
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
            self.logger.info(f"File {url} downloaded successfully as '{filepath}'")
            return True
        else:
            self.logger.error(f"Failed to download file. Status Code: {response.status_code}")
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

    def build_select_query(self, table_name, **kwargs):
        """
        Builds a SELECT * query with optional WHERE clauses from table name and kwargs.

        Args:
            table_name (str): Name of the table to query.
            **kwargs: Keyword arguments representing conditions for WHERE clause.
                - Keys are column names.
                - Values are the comparison values.

        Returns:
            str: The constructed SELECT * query with optional WHERE clause.
        """

        query = f"SELECT * FROM {table_name}"
        where_clauses = []
        where_values = []

        for col, value in kwargs.items():
            where_clauses.append(f"{col} = ?")
            where_values.append(value)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        logging.info(f"Executing query: {query}")
        out_dict = self.conn.execute(query, where_values).pl().to_dicts()
        return out_dict
    
    def query_producao(self, **kwargs):
        return self.build_select_query('tb_processamento_unp', **kwargs)
    
    def query_exportacao(self, **kwargs):
        return self.build_select_query('tb_exportacao_unp', **kwargs)

    def query_importacao(self, **kwargs):
        return self.build_select_query('tb_importacao_unp', **kwargs)
    
    def query_processamento(self, **kwargs):
        return self.build_select_query('tb_processamento_unp', **kwargs)    