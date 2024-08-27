import pandas as pd
import yaml
from sqlalchemy import create_engine, inspect, text

with open('keys.yaml','r') as f:
  keys = yaml.safe_load(f)
  PW = keys['PW']

class DatabaseConnector:

  def __init__(self):
    self.current_creds = {'No credentials given.'}
    self.table_list = []
  
  def read_db_creds(self,file_path)->dict:
    with open(file_path,'r') as f:
      self.current_creds = yaml.safe_load(f)
      return self.current_creds
    
  def init_db_engine(self,file_path:str='db_creds.yaml'):
    # method allows use of different credentials when making engine
    creds = self.read_db_creds(file_path)
    conn_str = "postgresql://{}:{}@{}:{}/{}".format(creds['RDS_USER'],
                                                    creds['RDS_PASSWORD'],
                                                    creds['RDS_HOST'],
                                                    creds['RDS_PORT'],
                                                    creds['RDS_DATABASE']
                                            )
    return create_engine(conn_str)
    
  def list_db_tables(self,schema='public')->list:
    engine = self.init_db_engine()
    self.table_list = inspect(engine).get_table_names(schema=schema)
    return self.table_list
  
  def upload_to_db(self,df,table_name:str,password:str=PW,db_name:str='sales_data'):
    conn_str = f"postgresql://postgres:{password}@localhost:5432/{db_name}"
    with create_engine(conn_str).connect() as conn:
      df.to_sql(table_name, con=conn, index=False, if_exists='replace')
