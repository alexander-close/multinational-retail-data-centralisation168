import yaml
from sqlalchemy import create_engine, inspect, MetaData,text

yaml_file = 'db_creds.yaml'

class DatabaseConnector:

  def __init__(self,file_path):
    self.file_path = file_path

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
    with engine.connect() as conn:
        result = conn.execute(f"select count(*) from legacy_users")
        tables = [row[0] for row in result]
    return tables
    # inspector = inspect(engine)
    # return inspector.get_table_names(schema=schema)

  def list_tables(self, schema='public'):
    engine = self.init_db_engine()
    metadata = MetaData()
    metadata.reflect(engine, schema=schema)
    return list(metadata.tables.keys())
  
  def upload_to_db(self,df,table):
    pass 

if __name__ == '__main__': # to test code 
  inst = DatabaseConnector(yaml_file)
  engine = inst.init_db_engine()
  with engine.connect() as conn:
    result = conn.execute(f"select count(*) from legacy_users")
    tables = [row[0] for row in result]
    print(tables)
  