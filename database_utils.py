import pandas as pd
import yaml
from sqlalchemy import create_engine, inspect, text

yaml_file = 'db_creds.yaml'

class DatabaseConnector:

  def __init__(self,file_path):
    self.file_path = file_path
    self.table_list = []

  def path(self):
    return self.file_path
  
  def read_db_creds(self):
    with open(self.file_path,'r') as file:
      return yaml.safe_load(file)
    
  def init_db_engine(self):
    creds = self.read_db_creds()
    conn_str = f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
    return create_engine(conn_str)
    
  def list_db_tables(self,schema='public'):
    engine = self.init_db_engine()
    self.table_list = inspect(engine).get_table_names(schema=schema)
    return self.table_list
  
  def upload_to_db(self,df,password,table_name='dim_users'):
    conn_str = f"postgresql://postgres:{password}@localhost:5432/sales_data"
    with create_engine(conn_str).connect() as conn:
      df.to_sql(table_name, con=conn, index=False, if_exists='replace')
    

if __name__ == '__main__': # to test code 
  inst = DatabaseConnector(yaml_file)
  with open('pw.txt','r') as pw:
    password = pw.read().strip()# strip() to remove newline break in .txt files
  df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]})
  inst.upload_to_db(df,password,table_name='new table test')
