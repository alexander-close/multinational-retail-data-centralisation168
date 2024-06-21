from database_utils.py import DatabaseConnector as DbC

class DataExtractor:
  def __init__(self,yaml_file):
    self.yaml_file=yaml_file
  def read_rds_table(self):
    connector = DbC(self.yaml_file)
    return 'worked'

inst = DataExtractor('db_creds.yaml')
inst.reads_rdstable()
