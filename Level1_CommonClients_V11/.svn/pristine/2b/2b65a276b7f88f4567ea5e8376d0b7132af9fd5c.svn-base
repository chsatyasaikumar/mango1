'''
#The purpose of this file is to make database connection
'''
from __future__ import print_function
import psycopg2
import psycopg2.extras

#Helper function
#Connecting to the database
def make_connection(database):
    # pylint: disable-msg=W0703
    '''
    Input  -
       params: database - The name of the database to be connected
    Output - Connected to the database
    '''
    conn = None
    #Checking if the database exist
    try:
        conn = psycopg2.connect(database=database["database_name"], user=database["user"],
                                password=database["password"], host=database["host"],
                                port=database["port"])
        print("L1: CONNECTED SUCCESSFULLY")
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", str(error))
    return conn

#Helper function
#Closing the database connection
def close_connection(conn):
    # pylint: disable-msg=W0703
    '''
    Input -
       params: conn - Connection object
    Output - The connection to the database is closed
    '''
    try:
        conn.close()
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", str(error))

#Helper function
#Creating cursor object
def get_cursor(conn):
    # pylint: disable-msg=W0703
    '''
    Input  -
       params: conn - Connection object
    Output - Cursor object is created
    '''
    cursor = None
    try:
        cursor = conn.cursor()
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", str(error))
    return cursor

#Helper function
#Creating dict cursor object
def get_dict_cursor(conn):
    # pylint: disable-msg=W0703
    '''
    Input  -
       params: conn - Connection object
    Output - Dict cursor object is created
    '''
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", str(error))
    return cursor

#Helper function
#Executing the specified query
def execute_query(conn, insert_query, data, cursor):
    '''
    Input  -
       params: conn - Connection object
       params: insert_query - The query to be executed
       params: data - The data to be inserted
    Output - The query is executed
    '''
    cursor.execute(insert_query, data)
    conn.commit()

#Helper function
#Executing the select query and fetching a single record
def execute_selectquery(query, cursor):
    # pylint: disable-msg=W0703
    '''
    Input  -
       params: query - The query to be executed
       params: cursor - Cursor object
    Output - The single record is fetched based on the query
    '''
    data = ()
    try:
        cursor.execute(query)
        data = cursor.fetchone()
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", str(error))
    return data

#Helper function
#Inserting the bulk data
def execute_many_query(insert_query, data, cursor):
    # pylint: disable-msg=W0703
    '''
     Input -
        params: insert_query - The query to be executed
        params: data - The data to be inserted
        params: cursor - cursor object
     Output - The bulk data are inserted into the database
    '''
    try:
        cursor.executemany(insert_query, data)
        print("L1: BULK DATA SUCCESSFULLY INSERTED")
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", str(error))
        print("L1: INSERTION FAILED")

#Helper function
#Executing query and fetching all the records
def fetchall_select_query(query, cursor):
    # pylint: disable-msg=W0703
    '''
    Input  -
        params: query - The query to be executed
       params: cursor - cursor object
       Output - All the records are fetched
    '''
    data = ()
    try:
        cursor.execute(query)
        data = cursor.fetchall()
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", str(error))
    return data

def exist_conn_closed(conn):
    '''
        checking if connection is not closed then closed the connection
        Input -
        param: conn - Database connection object
    '''
    if conn and conn.closed == 0:
        conn.close()

def exist_cur_conn_closed(conn, cursor):
    '''
    closing database connection and cursor
    Input -
        params: conn - Database connection object
        params: cursor -Database cursor object
    '''
    cursor.close()
    conn.close()
    