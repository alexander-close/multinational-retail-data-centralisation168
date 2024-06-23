from database_utils import DatabaseConnector
import pandas as pd
import tabula

pdf_link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'

class DataExtractor:
  def __init__(self):
    self.name = 'DataExtractor'

  def read_rds_table(self,instance,table_name):
    engine = instance.init_db_engine()
    if table_name in instance.list_db_tables():
      return pd.read_sql_table(table_name,engine)
    else:
      return 'Table not in schema.'
    
  def retrieve_pdf_data(self,url):
    df_list = tabula.read_pdf(url, pages='all')
    df = pd.DataFrame()
    for dfs in df_list:
      df = pd.concat([df,dfs])
    return df

  

if __name__=='__main__': # to test functionality
  yaml_file = 'db_creds.yaml'
  # instance = DatabaseConnector(yaml_file)
  
  extractor = DataExtractor()
  df = extractor.retrieve_pdf_data(pdf_link)

  print(len(df))