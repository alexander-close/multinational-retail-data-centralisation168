import pandas as pd

class DataCleaning:
  def __init__(self):
    pass

  def clean_user_data(self,df):
    df.date_of_birth = pd.to_datetime(df.date_of_birth, errors='coerce').dt.date
    df.join_date = pd.to_datetime(df.join_date, errors='coerce').dt.date
    df.card_number = str(df.card_number)
    return df

  def clean_card_data(self,df):
    df.expiry_date = pd.to_datetime(df.expiry_date).dt.date
    df.date_payment_confirmed = pd.to_datetime(df.date_payment_confirmed).dt.date
    return df
    

  def convert_product_weights(self,df):
    def kg(x):
      try:
        if type(x) == str:
          if x.endswith('kg'):
           return float(x[:-2].strip())
          elif x.endswith('g'):
           return float(x[:-1].strip()) / 1000
          else:
            return float(x[:-1].strip()) / 1000
        else:
          pass
      except:
        pass
    clean_df = df.copy()
    clean_df['weight'] = clean_df['weight'].map(kg)
    return clean_df
  
  def clean_products_data(self,df):
    pass
  def clean_orders_data(self,df):
    clean_df = df.copy()
    clean_df = clean_df.drop(labels=['first_name','last_name','1'],axis=1)
    return clean_df