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
    df = tabula.read_pdf(url, pages='all')
    df2 = tabula.read_pdf(url)
    tabula.convert_into_by_batch("input_directory", output_format='csv', pages='all')


  

if __name__=='__main__': # just to test functionality
  yaml_file = 'db_creds.yaml'
  instance = DatabaseConnector(yaml_file)
  
  extractor = DataExtractor()
  df = extractor.read_rds_table(instance,'legacy_users')
  # print(len(df))
  # for name in instance.list_db_tables():
  #   if 'user' in name:
  #     print(name)
  print(df.head())

  # print(len(instance.retrieve_pdf_data(pdf_link)))