import yaml
from sqlalchemy import create_engine

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
    instance = DatabaseConnector(yaml_file)
    creds = instance.read_db_creds()
    conn_str = f"postgresql://{creds['RDS_USER']}:\
    {creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:\
    {creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
    engine = create_engine(conn_str)
    return engine.connect()


# init_db_engine = psycopg2.connect(host=HOST, user=USER, password=PASSWORD, dbname=DBNAME, port=PORT)

if __name__ == '__main__':
  inst = DatabaseConnector(yaml_file)
  inst.init_db_engine()