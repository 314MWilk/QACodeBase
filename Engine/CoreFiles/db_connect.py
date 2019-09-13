from configparser import ConfigParser
import mysql.connector
import os
from pathlib2 import Path


def get_db_details():
    """Reads details from database_connect.ini"""
    cwd = Path(__file__).parents[2]
    os.chdir(str(cwd))
    db_config = ConfigParser()
    db_config.read("Configs/database_connect.ini")
    db_connect_details = db_config['CONNECT_DETAILS']
    host = db_connect_details['host']
    port = db_connect_details['port']
    user = db_connect_details['user']
    password = db_connect_details['password']
    database = db_connect_details['database']
    return host, port, user, password, database


def get_from_db(query, commit=False):
    """
    Performs query in database given in database_connect.ini file
    :param query: text of MySql query
    :param commit: should be True for update queries
    :return: Result of query given by MySql or error if query was not correct
    """
    host, port, user, password, database = get_db_details()
    cnx = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
    cursor = cnx.cursor()
    cursor.execute(query)
    if commit:
        cnx.commit()
    result = []
    for school in cursor:
        result.append(school)
    cursor.close()
    cnx.close()
    return result

