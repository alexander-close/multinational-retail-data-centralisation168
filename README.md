Repo for AICore RDS project, June 2024.

Project title: Multinational Retail Data Centralisation

Installations needed: 

&nbsp; &nbsp; &nbsp; pandas

&nbsp; &nbsp; &nbsp; tabula

&nbsp; &nbsp; &nbsp; requests

&nbsp; &nbsp; &nbsp; boto3

&nbsp; &nbsp; &nbsp; PyYAML

&nbsp; &nbsp; &nbsp; sqlalchemy

&nbsp; &nbsp; &nbsp; psycopg2

The project builds three classes:

**DatabaseConnector** (in database_util.py): a connector with methods:

&nbsp; &nbsp; &nbsp; -- read_db_creds() reads database creditials from a local yaml file

&nbsp; &nbsp; &nbsp; -- init_db_engine() builds an engine using the credentials

&nbsp; &nbsp; &nbsp; -- list_db_tables() prints (by default public) table names

&nbsp; &nbsp; &nbsp; -- upload_to_db() provides upload capabilities to your own locally hosted database

**DataExtractor** (data_extraction.py): an extractor which imports the previous class, with the methods:

&nbsp; &nbsp; &nbsp; -- read_rds_table() takes an instance of the connector class and extracts a given table as a DataFrame

&nbsp; &nbsp; &nbsp; -- retrieve_pdf_data() extracts a weblink PDF file and returns it as a DataFrame

&nbsp; &nbsp; &nbsp; -- list_number_of_stores() is an API that reads an AWS web address and returns the number of stores in the database

&nbsp; &nbsp; &nbsp; -- retrieve_stores_data() returns the stores from an AWS web address as a DataFrame

&nbsp; &nbsp; &nbsp; -- extract_from_s3() extracts csv data from an AWS bucket and returns a DataFrame

**DataCleaning** (in data_cleaning.py) is a data cleaner with methods:

&nbsp; &nbsp; &nbsp; -- clean_user_data() is currently inert

&nbsp; &nbsp; &nbsp; -- clean_card_data() is currently inert

&nbsp; &nbsp; &nbsp; --convert_product_weights() cleans the 'weight' data of an extracted product DataFrame

&nbsp; &nbsp; &nbsp; -- clean_products_data() is currently inert

&nbsp; &nbsp; &nbsp; -- clean_orders_data() removes the unneeded columns 'first_name', 'last_name' and '1' from an extracted orders DataFrame


**Licence**: A. Close 2024