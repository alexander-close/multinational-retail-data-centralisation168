# Multinational Retail Data Centralisation

This repo contains Python scripts for the AICore RDS project, June 2024.

### Table of Contents

* [Outline of the project](#outline-of-the-project)
* [Installation](#installations-needed)
* [Structure of the code](#structure-of-the-code)
* [Other files](#other-files)
* [Usage](#usage)

## Outline of the project

The purpose of this code is to scrape data from a number of distinct legacy sources and centralise everything onto a single RDBMS after cleaning.

Specifically, data is to be ingested from a PDF file (containing credit card information) in an AWS S3 bucket, from an AWS RDS database (where legacy user information can be found), and from an URL address (physical store information) to be accessed via an API.

When the data is extracted and converted into Pandas DataFrame format it is then cleaned before being sent to a local database management system operated by the user.



### Dependencies: 

`pandas`
&nbsp; `tabula`
&nbsp; `requests`
&nbsp; `boto3`
&nbsp; `PyYAML`
&nbsp; `sqlalchemy`
&nbsp; `psycopg2`

## Structure of the code

The project builds three classes.

**1) `DatabaseConnector`** (`database_util.py`): a connector with the following methods.

&nbsp; &nbsp; &nbsp; - `read_db_creds()` reads database credentials from a local yaml file

&nbsp; &nbsp; &nbsp; - `init_db_engine()` builds an engine using the credentials

&nbsp; &nbsp; &nbsp; - `list_db_tables()` prints (by default public) table names

&nbsp; &nbsp; &nbsp; - `upload_to_db()` provides upload capabilities to your own locally hosted database

**2) `DataExtractor`** (`data_extraction.py`): an extractor which imports the previous class, with the methods:

&nbsp; &nbsp; &nbsp; - `read_rds_table()` takes an instance of the connector class and extracts a given table as a DataFrame

&nbsp; &nbsp; &nbsp; - `retrieve_pdf_data()` extracts a web link PDF file and returns it as a DataFrame

&nbsp; &nbsp; &nbsp; - `list_number_of_stores()` is an API that reads an AWS web address and returns the number of stores in the database

&nbsp; &nbsp; &nbsp; - `retrieve_stores_data()` returns the stores from an AWS web address as a DataFrame

&nbsp; &nbsp; &nbsp; - `extract_from_s3()` extracts CSV data from an AWS bucket and returns a DataFrame

**3) `DataCleaning`** (`data_cleaning.py`) is a data cleaner with the following methods.

&nbsp; &nbsp; &nbsp; - `clean_user_data()` currently converts datetime information into the correct format.

&nbsp; &nbsp; &nbsp; - `clean_card_data()` currently converts datetime information into the correct format.

&nbsp; &nbsp; &nbsp; - `convert_product_weights()` cleans the '`weight`' data of an extracted product DataFrame.

&nbsp; &nbsp; &nbsp; - `clean_products_data()` is currently inert.

&nbsp; &nbsp; &nbsp; - `clean_orders_data()` removes the unneeded columns '`first_name`', '`last_name`' and '`1`' from an extracted orders DataFrame.

### Other files
The scripts reference a number of external `yaml` files.

* `db_creds.yaml`, wherein are stored credentials to access the AWS RDB.
* `keys.yaml`, containing other credentials such as the users database password and PI keys.
* `constants.yaml`, which stores the URL endpoint and S3 location. 

**Licence**: A. Close 2024