# AWS-DataWarehouse
In this project, we explore how to create and use a **Redshift** data warehouse on AWS. 
Once the data warehouse is up and running, we copy some *Sparkify* data stored in S3, AWS storage environment. *Sparkify* is a pseudo start-up like Spotify and provides us with data on songs and user activities on their web-site.
After transferring and transforming (via an ETL process) this data into a STAR schema (with facts and dimensions), we access those tables from Tableau where we can create a beautiful dashboard and extract insights about our songs, customers and their interactions with our start-up.

# Files
This project includes the following files:
- dwh.cfg: a config file which includes the data warehouse settings. This file also includes the AWS key and associated secret which are necessary to create and access AWS resources.
- **sql_queries.py**: a file which includes all the SQL queries used in our project. In this project, we create and delete tables. We also insert data in our tables.
- **create_tables.py**: Python script which uses sql_queries to create our project tables.
- **etl.py**: Extract, Transform and Load (ETL) script which transfers data (from AWS S3) and transforms it into our STAR model data schema.
- **RedshiftSetup.ipynb**: Jupyter Notebook which highlights the various steps in order to create and delete a Redshit datawarehouse on AWS.
- **README.md**: The file you're reading right now.

# Instructions
## Create an AWS Admin Account
The first step for this project is to create your AWS Admin Account which allows you to secure a Redshift data warehouse, create users, copy files to S3, etc...
Simply log into AWS and create this user in the IAM console. Once the user is created, you will receive a key-secret pair. This pair shouldn't be stored online because it would allows others to use AWS at your expenses!! Handle with care!

## Update Data Warehouse Config file
Type in your key and secret in the dwh.cfg file. Make sure you don't *push* this file back to git for the reasons explained above.

## Secure an AWS Redshift data warehouse
Since you now have an AWS admin account, you can secure some AWS resources such as a redshift data warehouse. We can secure those resources by using the AWS admin console (online) or by using a Python API. We also create an ARN policy which enables Redshift to access S3 storage environment in ReadOnly mode. In our case, we decided to create this AWS Redshift resource with the Python SDK. We included the instructions in the following Jupyter Notebook: **RedshiftSetup.ipynb**

## Update Data Warehouse Config file
Once the Redshift data warehouse is up and running, you can add its end-point (a.k.a address) and ARN policy that we created in the previous step to the dwh.cfg file.

## Create Tables
Now, it's time to create some tables in our data warehouse. We can do so by simply running the following Python script: create_tables.py.

## ETL process
Assuming that the tables get created properly, we can now initiate our ETL process by running the ETL.py script.

## Access Redshift from Tableau
As a bonus, we can connect to Redshift from Tableau by providing the end-point and user credentials included in the config.dwb file.

