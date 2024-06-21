from database_utils import DatabaseConnector
import pandas as pd

class DataExtractor:
  def __init__(self):
    pass

  def read_rds_table(self,instance,table):
    engine = instance.init_db_engine()
    if table in instance.list_db_tables():
      return pd.read_sql_table(table,engine)
    else:
      return 'Table not in schema.'
  

if __name__=='__main__': # just to test functionality
  yaml_file = 'db_creds.yaml'
  instance = DatabaseConnector(yaml_file)
  extractor = DataExtractor()
  df = extractor.read_rds_table(instance, 'table')
  # print(len(df))
  for name in instance.list_db_tables():
    if 'user' in name:
      print(name)

