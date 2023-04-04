from typing import Dict,List,Union
from datetime import datetime
import environ
import pymysql
import json

def _get_env(secret_file: str)-> environ.Env:
    env : environ.Env = environ.Env(DEBUG=(bool,False))
    env.read_env(secret_file)
    return env

class MySQL:
    def __init__(self,secret_file:str) -> None:
        self._HOST : str = _get_env(secret_file=secret_file)('HOST')
        self._PORT : int = int(_get_env(secret_file=secret_file)('PORT'))
        self._USER : str = _get_env(secret_file=secret_file)('USERNAME')
        self._PASS : str = _get_env(secret_file=secret_file)('PASS')
        self._DB   : str = _get_env(secret_file=secret_file)('DB')    
    
    def connect_db(self)-> None:
        self.con : pymysql.Connection = pymysql.connect(
            host=self._HOST,
            port=self._PORT,
            user=self._USER,
            passwd=self._PASS,
            db=self._DB,
            charset='utf8mb4',
            use_unicode=True
        )
        self.cursor : self.con.cursor = self.con.cursor()

    def __del__(self)-> None:
        try:
            self.con.close()
            self.cursor.close()
        except:
            return
        
class CRUD(MySQL):
    def __init__(self,secret_file:str) -> None:
        super().__init__(secret_file=secret_file)
    
    def create(self,create_query:str)-> None:
        self.cursor.execute(create_query)
        self.con.commit()
    
    def read(self,read_query:str)-> List[Dict[str,Union[str,int]]]:
        self.cursor.execute(read_query)
        columns = [column[0] for column in self.cursor.description]
        datas = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        return datas        
        
    def update(self,update_query:str)-> None:
        self.cursor.execute(update_query)
        self.con.commit()

    def delete(self,delete_query:str)-> None:
        self.curosr.execute(delete_query)
        self.con.commit()
    
    def insert(self,insert_query:str)-> None:
        self.cursor.execute(insert_query)
        self.con.commit()