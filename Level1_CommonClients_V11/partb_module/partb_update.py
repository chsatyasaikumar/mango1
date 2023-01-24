'''
#Updating details like transporter_name, transporter_id in document_details table
'''
from __future__ import print_function
import os
import traceback
import datetime
import warnings
import json
import boto3
import requests
import psycopg2
from comman_module.db_config import make_connection, get_dict_cursor, \
        exist_conn_closed, exist_cur_conn_closed
from comman_module.save_data import upload_file_details_with_conn
from comman_module.function import error_upload_file, send_sqs
from .partb_config import TRANS_PARAM
from .partb_update_query import T_UPDATE_QUERY, INSERT_QUERY,\
        T_EWB_DTLS_UDT_QUERY, EWB_LOAD_ID_QUERY
warnings.simplefilter(action='ignore', category=FutureWarning)
#Helper function
#Updating the transporter_id and transporter_name in document_details table
def update_document_details(test_data, updated_by, load_id, source_system, load_type,\
    upload_data_dict, l1_bucket, b_filename, config_dict, database):
    # pylint: disable-msg=R0913
    # pylint: disable-msg=W0703
    # pylint: disable-msg=R0915
    '''
    Input  -
       params: test_data - The csv file being read
       params: size - The size of the above csv file
       params: updated_by - The user who is uploading the file
       params: load_id - The load id that is generated after insertion
       params: source_system - The source system defined in configuration.py
                                #in common module in update_data_dict
       params: load_type - The load type defined in configuration.py
                            #in common module in update_data_dict
       params: config_dict: configuration of transporter update url
    Output - The transporter_name and transporter_id in document_details table
              #is being uploaded
    '''
    msg, count = "", 0
    indian_current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #Getting the environment variables
    transporter_update_flag = config_dict.get("transporter_update_flag", "")
    transporter_update_url = config_dict.get("transporter_update_url", "")
    trans_upd_sqs_url = config_dict.get("transporter_update_sqs_url", "")
    customer_id = config_dict.get("CustomerId", "")
    api_request_list = []
    str_load_id = str(load_id[0])
    conn = None
    try:
        #Creating te database connection.Calling make_connection() function
        conn = make_connection(database)
        #Getting the cursor object.Calling get_dict_cursor() function
        cursor = get_dict_cursor(conn)
        for i in test_data.index:
            param = TRANS_PARAM.copy()
            udid = test_data._get_value(i, 'UDID').upper()
            mis3 = test_data._get_value(i, 'MIS3')
            transporter_name = test_data._get_value(i, 'Transporter Name')
            transporter_id = test_data._get_value(i, 'Transporter ID')
            document_no = test_data._get_value(i, 'Document No')
            #Checking if transporter_name key is present in data dict
            t_name = transporter_name if transporter_name else "transporter_name"
            #Checking if transporter_id is present or not
            t_id = transporter_id if transporter_id else "transporter_id"
            #Creating a tuple
            insert_data = (document_no, transporter_name, transporter_id, mis3, udid, updated_by,\
                indian_current_date, load_id[0], source_system, load_type)
            # execute_ insert query
            cursor.execute(INSERT_QUERY, insert_data)
            #Checking if transporter_id or transporter_name is present or not
            if transporter_id or transporter_name:
                update_history = 'Transporter Name and ID updated by load id '\
                    + str_load_id + ' <br>'
                #Updating the transporter_name and transporter_id #in document_details table.
                update_data = (t_name, t_id, updated_by, update_history, indian_current_date, udid)
                #Executing the query.Calling execute_query() function
                cursor.execute(T_UPDATE_QUERY, update_data)
                #Updating the transporter_name and transporter_id in ewb_details table
                ewb_update_data = (t_name, t_id, updated_by, indian_current_date,\
                    update_history, udid)
                #Executing the above query.Calling execute_query() function
                cursor.execute(T_EWB_DTLS_UDT_QUERY, ewb_update_data)
                #Checking the status of udid and transporter_id
                if udid and transporter_id:
                    #Getting all the records
                    cursor.execute(EWB_LOAD_ID_QUERY, (udid,))
                    query_result = cursor.fetchall()
                    #Checking the status of above line
                    if query_result and transporter_update_flag == "Y":
                        create_request_param(udid, query_result, transporter_id, transporter_name,\
                            customer_id, param, api_request_list)
            count += 1
        msg = "Transporter successfully updated."
        upload_data_dict["status"] = msg
        try:
            print("L1: INSERTING DATA INTO UPLOAD TABLE")
            upload_file_details_with_conn(load_id, upload_data_dict, conn, cursor)
            print("L1: INSERTED DATA INTO UPLOAD TABLE")
            exist_cur_conn_closed(conn, cursor)
            print("TRANSPORTER UPDATE API CALLING")
            print("transporter_update_url -> {0}".format(transporter_update_url))
            print("api_request_list -> {0}".format(api_request_list))
            # api_request(api_request_list, transporter_update_url, trans_upd_sqs_url)
            if api_request_list:
                api_request(api_request_list, transporter_update_url, \
                    trans_upd_sqs_url, database)
        except psycopg2.DatabaseError as error:
            exist_conn_closed(conn)
            msg = "Transporter updation failed."
            print("L1 EXCEPTION OCCURED Getting insertion error on upload table")
            print("L1: EXCEPTION OCCURED ", error)
            error_upload_file(l1_bucket, b_filename, upload_data_dict["original_file_name"])
        except Exception as error:
            print("L1: EXCEPTION OCCURED ", str(error))
            traceback.print_exc()
            msg = "Transporter updation failed."
            exist_conn_closed(conn)
        return True, msg
    except Exception as error:
        msg = "Transporter updation failed."
        print("L1: EXCEPTION OCCURED ", str(error))
        traceback.print_exc()
        # Rolling back to the previous operation.Calling rollback() function
        exist_conn_closed(conn)
        return False, msg

# def api_request(api_request_list, transporter_update_url, trans_upd_sqs_url):
#     # pylint: disable-msg=W0703
#     '''
#         Calling transporter update api for transporter update
#         Input -
#             params: api_request_list - Dict of list
#             params: transporter_update_url - Transporter Update API URL
#     '''
#     header_data = {"token": os.environ.get("token", "")}
#     for api_param in api_request_list:
#         try:
#             if trans_upd_sqs_url:
#                 lambda_payload = {
#                     "queryStringParameters": api_param,
#                     "headers": header_data
#                 }
#                 send_sqs(lambda_payload, trans_upd_sqs_url)
#             elif transporter_update_url:
#                 response = requests.get(transporter_update_url, headers=header_data, \
#                     params=api_param)
#                 print("L1: RESPONSE URL ", str(response.url))
#                 print("L1: RESPONSE CONTENT ", str(response.content))
#             else:
#                 break
#         except Exception as error:
#             print("L1: EXCEPTION OCCURED WHEN CALLING TRANSPORTER UPDATE", error)

def create_request_param(udid, query_result, transporter_id, transporter_name,\
    customer_id, param, api_request_list):
    # pylint: disable-msg=R0913
    '''
        Creating PARAM dict and appending to list
        Input -
            params:udid - UDID
            params: query_result : Query Result
            params: transporter_id - Transporter ID
            params: transporter_name: Transporter Name
            params: customer_id - Cliebt ID
            params: param: PARAM dict
            params: api_request_list: list of dict param
    '''
    # param["ids"] = ",".join([udid + ";" + str(x["load_id"]) for x in query_result])
    # param["transporter_id"] = transporter_id
    # param["transporter_name"] = transporter_name
    # param["CustomerId"] = customer_id
    # api_request_list.append(param)
    for row in query_result:
        req_body = {}
        req_body["User_GSTIN"] = row["user_gstin"]
        req_body["transporterId"] = transporter_id
        req_body["ewbNo"] = int(row["eway_bill_no"])
        api_request_list.append(req_body)

def partb_send_sqs(sqs_message, sqs_url):
    '''
    Summery Line.
        Sqs send
    Parameters:
        sqs_message: sqs message
        customer_id(str): client id
    Return:
        None
    '''
    try:
        s3_oject = boto3.client('sqs', region_name='ap-south-1')
        print(f'sqs message -> {json.dumps(sqs_message)}')
        response = s3_oject.send_message(\
            QueueUrl=sqs_url,\
            MessageBody=json.dumps(sqs_message))
        print("Message Send in Queue")
        print(response)
    except Exception as error:
        traceback.print_exc()

def api_request(api_request_list, transporter_update_url, trans_upd_sqs_url, database):
    # pylint: disable-msg=W0703
    '''
        Calling transporter update api for transporter update
        Input -
            params: api_request_list - Dict of list
            params: transporter_update_url - Transporter Update API URL
    '''
    token = database.get("token", "").split(",")[0].strip()
    api_headers = {"customerid": os.environ.get("customer_id"), \
        "token": token, "transporterupdate": "Y"}
    try:
        if trans_upd_sqs_url:
            lambda_payload = {}
            lambda_payload["headers"] = api_headers
            lambda_payload["body"] = json.dumps(api_request_list)
            partb_send_sqs(lambda_payload, trans_upd_sqs_url)
        elif transporter_update_url:
            response = requests.post(transporter_update_url, headers=api_headers, \
                body=json.dumps(api_request_list))
            print("L1: RESPONSE URL ", str(response.url))
            print("L1: RESPONSE CONTENT ", str(response.content))
    except Exception as error:
        print("L1: EXCEPTION OCCURED WHEN CALLING TRANSPORTER UPDATE", error)
