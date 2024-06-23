import yaml
from sqlalchemy import create_engine, inspect

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
    return inspect(engine).get_table_names(schema=schema)
  
  def upload_to_db(self,df,table):
    pass 

if __name__ == '__main__': # to test code 
  inst = DatabaseConnector(yaml_file)
  print(inst.list_db_tables())
  