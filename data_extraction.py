import pandas as pd
import tabula
import requests
import boto3
import yaml
from io import BytesIO
from database_utils import DatabaseConnector

with open('constants.yaml', 'r') as f:
  consts = yaml.safe_load(f)
PDF_URL = consts['PDF_URL']
ENDPOINT = consts['ENDPOINT']

with open('keys.yaml', 'r') as g:
  keys = yaml.safe_load(g)
headers = {'x-api-key':keys['x-api-key']}

class DataExtractor:
  def __init__(self):
    self.instance: object = DatabaseConnector()
    self.number_stores: int = 0

  def read_rds_table(self, table_name:str) -> pd.DataFrame | str:
    engine = self.instance.init_db_engine()
    if table_name in self.instance.list_db_tables():
      return pd.read_sql_table(table_name,engine)
    else:
      return 'Table not in schema.'
    
  def retrieve_pdf_data(self, url:str=PDF_URL) -> pd.DataFrame:
    df_list = tabula.read_pdf(url, pages='all')
    df = pd.DataFrame()
    for dfs in df_list:
      df = pd.concat([df, dfs])
    return df
  
  def list_number_of_stores(
      self,
      headers:dict,
      endpoint=ENDPOINT
      ) -> int | None:
    endpoint = endpoint.format('number_stores')
    NOS = requests.get(endpoint, headers=headers)
    if NOS.status_code < 400:
      self.number_stores = NOS.json()['number_stores']
      self.NOS_endpoint = endpoint
      return NOS.json()['number_stores']
    else:
      return print(f'Code {NOS.status_csode}. Try self.number_stores')
    
  def retrieve_stores_data(
        self,
        headers:dict=headers,
        endpoint=ENDPOINT
  ) -> pd.DataFrame | None:
    df = pd.DataFrame()
    NOS = self.list_number_of_stores(headers, endpoint)
    if type(NOS) == int:
      for i in range(NOS):
        RAS = requests.get(endpoint.format(f'store_details/{i}'),
                           headers=headers).json()
        df = pd.concat([df, pd.DataFrame([RAS])])
      return df
    else:
      print("NOS not an int")

  def extract_from_s3(self, url) -> pd.DataFrame:
    bucket, file = url.replace('s3://','').split('/')[0],url.replace('s3://','').split('/')[1:]
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key='/'.join(file))
    data = response['Body'].read()
    return pd.read_csv(BytesIO(data))
