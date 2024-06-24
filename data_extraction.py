from database_utils import DatabaseConnector
import pandas as pd
import tabula
import requests
import boto3
from io import BytesIO

pdf_link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'

class DataExtractor:
  def __init__(self):
    self.number_stores = 0

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
  
  def list_number_of_stores(self,endpoint,headers):
    NOS = requests.get(endpoint,headers=headers)
    if NOS.status_code < 400:
      self.number_stores = NOS.json()['number_stores']
      self.NOS_endpoint = endpoint
      return NOS.json()['number_stores']
    else:
      return print(f'Code {NOS.status_code}. Try self.number_stores')
    
  def retrieve_stores_data(self,endpoint,headers):
    df = pd.DataFrame()
    NOS = self.list_number_of_stores(self.NOS_endpoint,headers=headers)
    if type(NOS) == int:
      for i in range(NOS):
        RAS = requests.get(endpoint+f'{i}',headers=headers).json()
        df = pd.concat([df,pd.DataFrame([RAS])])
      return df
    else:
      print("Code error")

  def extract_from_s3(self,url):
    bucket,file = url.replace('s3://','').split('/')[0],url.replace('s3://','').split('/')[1:]
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key='/'.join(file))
    data = response['Body'].read()
    return pd.read_csv(BytesIO(data))


  

if __name__=='__main__': # to test functionality
  yaml_file = 'db_creds.yaml'
  # instance = DatabaseConnector(yaml_file)
  
  # extractor = DataExtractor()
  # df = extractor.retrieve_pdf_data(pdf_link)

  # print(len(df))