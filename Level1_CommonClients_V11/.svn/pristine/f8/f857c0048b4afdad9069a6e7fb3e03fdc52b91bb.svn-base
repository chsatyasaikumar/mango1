'''
#Validating the fields of grn
'''
from __future__ import print_function
import os
import datetime
import requests
import boto3
import psycopg2
import pandas as pd
from comman_module.db_config import make_connection, get_dict_cursor, exist_conn_closed,\
                                exist_cur_conn_closed
from comman_module.save_data import upload_file_details_with_conn
from comman_module.function import validate_expression, send_sqs
from comman_module.configuration import GSTIN_REGEX_WITH_URP, DOC_NO_REGEX
from .grn_validation import grn_validate_date
from .grn_query import INSERT_QUERY
from .grn_configuration import DEFAULT_SUPPLY_TYPE, RENAME_DF_COL

def rowvalidation(or_row):
    '''
    scaning pandas df row by row
    validating data
    Input -
        params: row: singlow row dictionary
    '''
    row = or_row.copy()
    validation_remarks = ''
    # Checking if the user_gstin matches the corresponding regex.
    # Calling validate_expression() function
    flag_user_gstin = validate_expression(GSTIN_REGEX_WITH_URP, row["user_gstin"])
    #Checking the status of above line
    if not flag_user_gstin:
        validation_remarks = "User GSTIN is invalid/blank<br>"
    #Validating the supply_type
    upper_supply_type = row["supply_type"].upper()
    # Checking if the supply type is present in one of its allowed values
    flag_supply_type = bool(upper_supply_type in DEFAULT_SUPPLY_TYPE)
    #Checking the status of above line
    if not flag_supply_type:
        validation_remarks = validation_remarks + "Supply type is invalid/blank<br>"
    #Vaidating document_no
    # Checking if document_no matches the regex or not.
    # Calling validate_expression() function
    flag_document_no = validate_expression(DOC_NO_REGEX, row["document_no"])
    #Checking the status of above line
    if not flag_document_no:
        validation_remarks = validation_remarks + "Document number is invalid/blank<br>"
    #Validating document_date
    #Calling grn_validate_date() function
    flag_document_date, row["document_date"] = grn_validate_date(row["document_date"],\
        "%d/%m/%Y", "%Y-%m-%d")
    #Checking the status of above line
    if not flag_document_date:
        validation_remarks = validation_remarks + "Document date is invalid/blank<br>"
    #Validating delivery_document_no
    # Checking if delivery_document_no matches the regex or not.
    # Calling validate_expression() function
    flag_d_doc_no = validate_expression(DOC_NO_REGEX, row["delivery_document_no"])
    #Checking the status of above line
    if not flag_d_doc_no:
        validation_remarks = validation_remarks + "Delivery Document no is invalid/blank<br>"
    #Validating delivery_document_date
    # Calling grn_validate_date() function
    flag_d_document_date, row["delivery_document_date"] = grn_validate_date(
        row["delivery_document_date"], "%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M:%S")
    #Checking the status of above line
    if not flag_d_document_date:
        validation_remarks = validation_remarks + "Delivery Document date is invalid/blank<br>"
    udid = None
    #Checking if user_gstin, document_number and supply type fields are not empty
    #for creating udid
    if row["user_gstin"] and row["document_no"] and row["supply_type"]:
        udid = row["user_gstin"].upper() + ":" + row["document_no"].upper()\
               + ":" + upper_supply_type
    status = "Failure"
    #Checking if user_gstin, supply_type, document_no,
    #document_date, delivery_document_no, delivery_document_date are valid
    flag_status = (flag_user_gstin and flag_supply_type and flag_document_no and \
        flag_document_date and flag_d_doc_no and flag_d_document_date)
    if flag_status:
        status = "Success"
    return pd.Series([row["document_date"], row["delivery_document_date"], udid,\
        status, validation_remarks])

def grn_mapping_data(filepath, data, created_by_user, upload_data_dict,\
    l1_bucket, b_filename, config_dict, database):
    # pylint: disable-msg=R0913
    # pylint: disable-msg=W0703
    '''
         Input  -
            params: filepath - The location of the file path
            params: data - The data in csv file
            params: created_by_user - The user who have uploaded the file
            params: l1_bucket - bucket name of L1
            params: b_filename - file name from backup
            params: config_dict: configuration of grn update url
         Output - The fields are validated
    '''
    msg = ""
    count = 0
    flag_trigger_update = True
    try:
        test_data = pd.read_csv(filepath, encoding="ISO-8859-1", dtype=object)
        test_data = test_data.fillna("")
        test_data.rename(columns=RENAME_DF_COL, inplace=True)
        count = test_data.shape[0]
        # Checking the size of csv file
        if count > 0:
            test_data[["document_date", "delivery_document_date", "udid",\
                    "status", "remarks"]] = test_data.apply(rowvalidation, axis=1)
            test_data["created_by"] = test_data["updated_by"] = created_by_user
            test_data["created_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            test_data["updated_date"] = test_data["created_date"]
            test_data["load_id"] = str(data[0])
            all_list = test_data.T.to_dict().values()
            #Making database connection.Calling make_connection() functiona
            conn = make_connection(database)
            #Getting the dict_cursor object.Calling get_dict_cursor() function
            cursor = get_dict_cursor(conn)
            cursor.executemany(INSERT_QUERY, tuple(all_list))
            msg = "Data successfully loaded"
            upload_data_dict["status"] = msg
            upload_data_dict["import_from_file"] = count
            try:
                print("L1: INSERTING DATA INTO UPLOAD TABLE")
                upload_file_details_with_conn(data, upload_data_dict, conn, cursor)
                print("L1: INSERTED DATA INTO UPLOAD TABLE")
                exist_cur_conn_closed(conn, cursor)
                try:
                    header_data = {"token": os.environ.get("token", "")}
                    del_dtls_sqs_url = config_dict.get("auto_del_dtls_sqs_url", "")
                    if del_dtls_sqs_url:
                        lambda_payload = {
                            "queryStringParameters": {
                                "CustomerId": os.environ.get('customer_id', ''),
                                "load_id": str(data[0])
                            },
                            "headers": header_data
                        }
                        send_sqs(lambda_payload, del_dtls_sqs_url)
                    else:
                        auto_delivery_details = config_dict.get("auto_delivery_details", "")
                        #Checking if auto_delivery_details env variable is present
                        auto_delivery_details = auto_delivery_details + str(data[0])
                        requests.get(auto_delivery_details, headers=header_data)
                except Exception as error:
                    print("L1: EXCEPTION OCCURED ", str(error))
            except psycopg2.DatabaseError as error:
                exist_conn_closed(conn)
                msg = "Data upload failed."
                print("L1 EXCEPTION OCCURED Getting insertion error on upload table")
                print("L1: EXCEPTION OCCURED ", error)
                s3_resource = boto3.resource('s3')
                copy_source = {
                    "Bucket" : l1_bucket,
                    "Key": b_filename
                }
                try:
                    s3_resource.meta.client.copy(copy_source, l1_bucket, "error/" + \
                        upload_data_dict["original_file_name"])
                except Exception as error:
                    print("L1:EXCEPTION OCCURED L1 bakup to incoming-file moving failed.")
                    print("L1: EXCEPTION OCCURED ", error)
            except Exception as error:
                print("L1: EXCEPTION OCCURED ", error)
                msg = "Data upload failed."
                count = 0
                exist_conn_closed(conn)
            flag_trigger_update = False
        else:
            msg = "Rejected - File is emtpy"
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", str(error))
        msg = "Data upload failed."
        count = 0
        exist_conn_closed(conn)
    return flag_trigger_update, msg, count
