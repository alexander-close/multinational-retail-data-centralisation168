import pandas as pd
import yaml
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from typing import Union

with open('keys.yaml','r') as f:
  keys = yaml.safe_load(f)
  PW = keys['PW']

class DatabaseConnector:

  def __init__(self):
    self.current_creds: Union[dict,str] = 'No credentials given.'
    self.connection: Union[Engine, None]= None
    self.table_list: list = []
    
  
  def read_db_creds(self, file_path:str='db_creds.yaml')->dict:
    '''
    By default, looks for a `./db_creds.yaml` file.  The following
    fields are required:  `RDS_USER`, `RDS_PASSWORD`, `RDS_HOST`,
    `RDS_PORT` and `RDS_DATABASE`.
    '''
    with open(file_path,'r') as f:
      self.current_creds = yaml.safe_load(f)
      return self.current_creds
    
  def init_db_engine(self, file_path:str=self.current_creds) -> Engine:
    '''
    The method `read_db_creds()` should be called first.  Previous
    open connections will be closed.
    '''
    if type(self.current_creds) == str:
      raise ValueError('Database credentials not supplied; run `read_db_creds()`.')
    if self.connection is not None:
      self.close_connection(print_message=False)
    creds = self.read_db_creds(file_path)
    conn_str = "postgresql://{}:{}@{}:{}/{}".format(creds['RDS_USER'],
                                                    creds['RDS_PASSWORD'],
                                                    creds['RDS_HOST'],
                                                    creds['RDS_PORT'],
                                                    creds['RDS_DATABASE']
                                            )
    self.connection = create_engine(conn_str)
    return self.connection
    
  def list_db_tables(self, schema:str='public')->list:
    engine = self.init_db_engine()
    self.table_list = inspect(engine).get_table_names(schema=schema)
    return self.table_list
  
  def upload_to_db(
        self,
        df,
        table_name:str,
        password:str = PW,
        db_name:str = 'sales_data'
  ):
    conn_str = f"postgresql://postgres:{password}@localhost:5432/{db_name}"
    with create_engine(conn_str).connect() as conn:
      df.to_sql(table_name, con=conn, index=False, if_exists='replace')

  def close_connection(self, print_message:bool=True):
    if self.connection is not None:
      try:
        self.connection.close()
        if print_message:
          print('Previous connection on {self.current_creds} closed.')
      except Exception as e:
        print(f'Error closing the connection on {self.current_creds}: {e}')
      self.connection = None
