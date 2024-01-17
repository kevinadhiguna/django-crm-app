### -- Prerequisites -- ###
#
# (1) Install MySQL v8+
# (2) Install mysqlclient:
#     $ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
#     $ pip3 install mysqlclient
# (3) Install a python-mysql connector:
#     $ pip3 install mysql
#     $ pip3 install mysql-connector-python
#
### ------------------- ###

import mysql.connector

import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

# (1)
# env_filename = '.env'
# dotenv_path = join(dirname(__file__), env_filename)
# load_dotenv(dotenv_path)

# (2)
load_dotenv(find_dotenv())

dataBase = mysql.connector.connect(
    host = os.environ.get('DB_HOST'),
    user = os.environ.get('DB_USER'),
    passwd = os.environ.get('DB_PASSWORD'),
)

# Prepare a cursor object
cursorObject = dataBase.cursor()

dataBase_name = os.environ.get('DB_NAME')

# Create a database, only if it is not already present
if dataBase_name:
    cursorObject.execute(f"CREATE DATABASE IF NOT EXISTS {dataBase_name}")
    print("Database was created successfully!")
else:
    print("[x] Database name is not provided..")
