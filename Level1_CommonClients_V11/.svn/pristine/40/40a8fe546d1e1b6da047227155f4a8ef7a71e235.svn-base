'''
    Reading env variable
'''
from __future__ import print_function
import os
#Called from lambda_function.py
#Getting the environment variables
#Used on prod/dev/qa
def get_env():
    '''
     Output - Reading the environment variable
    '''
    #Getting the data from env
    database = os.environ.get('database')
    host = os.environ.get('host')
    port = os.environ.get('port')
    user = os.environ.get('user')
    password = os.environ.get('password')
    emails = os.environ.get('emails')
    db_dict = {}
    #Checking if all environment variables exist or not
    flag = (database and host and port and user and password and emails)
    if flag:
        db_dict['database'] = database
        db_dict['host'] = host
        db_dict['port'] = port
        db_dict['user'] = user
        db_dict['password'] = password
        db_dict['email_ides'] = emails.split(',')
    return db_dict



ORACLE_SOURCE_TYPE = os.environ.get('ORACLE_SOURCE_TYPE')
SAP_SOURCE_TYPE = os.environ.get('SAP_SOURCE_TYPE')
TALLY_SOURCE_TYPE = os.environ.get('TALLY_SOURCE_TYPE')
