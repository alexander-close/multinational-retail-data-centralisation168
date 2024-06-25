class DataCleaning:
  def __init__(self):
    pass

  def clean_user_data(self):
    # needs to fix NULL values, errors with dates, incorrectly typed values and rows filled with the wrong information
    pass

  def clean_card_data(self):
    pass
    # cleans data to remove any erroneous values, NULL values or errors with formatting

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