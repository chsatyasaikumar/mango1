'''
    saving document status in upload table
'''
from __future__ import print_function
import datetime
import psycopg2
from .db_config import make_connection, close_connection, execute_selectquery, get_cursor,\
                        get_dict_cursor
from .configuration import UP_D_INSERT_QUERY
from .function import error_upload_file
#Called from lambda_function.py
#Getting the load_id
def get_load_id(database):
    # pylint: disable-msg=W0703
    '''
    Input  -
       params: database - The database name
    Output - The load_id is known
    '''
    data = None
    #Query to get the sequence id
    select_query = "select nextval('demo.upload_id_seq')"
    try:
        #Creating the database connection
        conn = make_connection(database)
        #Creating the cursor
        cursor = get_cursor(conn)
        #Executing the query
        data = execute_selectquery(select_query, cursor)
        #Printing the load id
        print("L1:The load id is ", str(data))
        #Closing the database connection
        close_connection(conn)
    except Exception as error:
        print("L1:EXCEPTION OCCURED ", str(error))
    return data

#Called from lambda_function.py
def upload_file_details(data, database, upload_data_dict, b_filename, l1_bucket, s3_object=None,\
    upload_file_name=None, local_file_location=None, flag_upload=False):
    # pylint: disable-msg=R0913
    # pylint: disable-msg=W0703
    '''
    Input  -
       params: data - The data to be inserted
       params: database - The name of the database
       params: upload_data_dict - The dictionary that contains company_name , company_id etc
       params: b_filename - backup file name from L1 bucket
       params: l1_bucket - L1 bucket name
       params: s3_object - boto3 s3 cleint object
       params: local_file_location - after transformation file name
       params: upload_file_name - file name which used for process L2
       params: flag_upload - used for check upload required or not
       params: process_bucket_name - L2 Bucket Name
    Output - The details are inserted into upload table
    '''
    #Getting the Indian timestamp
    upload_data_dict["created_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = None
    #Insert query
    try:
        #Creating the database connection
        conn = make_connection(database)
        #Creating the cursor
        cursor = get_dict_cursor(conn)
        #Creating a tuple
        upload_data_dict["id"] = data[0]
        upload_data_dict["load_id"] = data[0]
        upload_data_dict["updated_date"] = upload_data_dict["created_date"]
        #Executing the query
        # execute_query(conn, insert_query, insert_data, cursor)
        try:
            # Checking if file upload required for L2 process
            if flag_upload:
                print("L1: INSERTING DATA INTO UPLOAD TABLE")
                cursor.execute(UP_D_INSERT_QUERY, upload_data_dict)
                print("L1: INSERTED DATA INTO UPLOAD TABLE")
                # Uploading file for L2 process
                s3_object.upload_file(local_file_location, l1_bucket, "process-" + upload_file_name)
            else:
                cursor.execute(UP_D_INSERT_QUERY, upload_data_dict)
            conn.commit()
            print("L1: SUCCESSFULLY INSERTED")
        except psycopg2.DatabaseError as error:
            print("L1 EXCEPTION OCCURED Getting insertion error on upload table")
            print("L1: EXCEPTION OCCURED ", error)
            # START MOVING FILE FROM BACKUP TO INCOMING-FILE FOR REPROCESS
            error_upload_file(l1_bucket, b_filename, upload_data_dict["original_file_name"])
        except Exception as error:
            print("L1: EXCEPTION OCCURED ", error)
        conn.close()
    except Exception as error:
        print("L1:EXCEPTION OCCURED ", error)
        if conn and conn.closed == 0:
            conn.close()

def upload_file_details_with_conn(data, upload_data_dict, conn, cursor, conn_flag=False,\
    data_base=None):
    # pylint: disable-msg=R0913
    # pylint: disable-msg=W0703
    '''
    Input  -
       params: data - The data to be inserted
       params: upload_data_dict - The dictionary that contains company_name , company_id etc
       params: conn - connection of database
    Output - The details are inserted into upload table
    '''
    #Getting the Indian timestamp
    upload_data_dict["created_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    upload_data_dict["updated_date"] = upload_data_dict["created_date"]
    upload_data_dict["id"] = data[0]
    upload_data_dict["load_id"] = data[0]
    #Creating a tuple
    #Executing the query
    if conn_flag:
        database = data_base
        conn = None
        try:
            conn = make_connection(database)
            cursor = get_dict_cursor(conn)
            cursor.execute(UP_D_INSERT_QUERY, upload_data_dict)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as error:
            print(error)
        if conn and conn.closed == 0:
            conn.close()
    else:
        cursor.execute(UP_D_INSERT_QUERY, upload_data_dict)
        conn.commit()
  