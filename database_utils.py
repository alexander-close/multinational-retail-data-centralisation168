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

if __name__ == '__main__':
  inst = DatabaseConnector(yaml_file)

  engine = inst.init_db_engine()
  with engine.connect() as conn:
    result = conn.execute(f"select count(*) from legacy_users")
    tables = [row[0] for row in result]
    print(tables)
  # print(inst.list_db_tables())
  # engine = inst.init_db_engine()

  # inspector = inspect(engine)
  # print(inspector.get_table_names())

  # with engine.connect() as connection:
  #   result = connection.execute(text("SELECT * FROM information_schema.tables"))
    # for row in result:
    #   print(row)
  # print(tab)

# from sqlalchemy import create_engine,text

# DATABASE_TYPE = 'postgresql'
# DBAPI = 'psycopg2'
# HOST = 'data-handling-project-readonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com'
# USER = 'aicore_admin'
# PASSWORD = 'AiCore2022'
# DATABASE = 'postgres'
# PORT = 5432

# engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# with engine.connect() as connection:
#     result = connection.execute(text("select * from information_schema.tables"))
#     for row in result:
#         print(row)