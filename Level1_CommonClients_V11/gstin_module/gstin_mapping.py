'''
#Validating the columns in purchase_register module
'''
from __future__ import print_function
import datetime
import traceback
import pandas as pd
from comman_module.db_config import make_connection, get_dict_cursor, exist_cur_conn_closed,\
execute_query, exist_conn_closed, execute_selectquery, fetchall_select_query, execute_many_query
from comman_module.save_data import upload_file_details_with_conn
from comman_module.function import validate_expression, error_upload_file
from comman_module.configuration import GSTIN_REGEX
from .gstin_configuration import RENEAME_COL_DICT
from .gstin_query import INSERT_QUERY_FOR_NEW_GSTIN, SELECT_QUERY_FOR_EXISTING_GSTIN,\
UPDATE_QUERY_FOR_EXISTING_GSTIN
import psycopg2
import psycopg2.extras
import json


#Helper function
#Truncating the length of the data if it exceeds the size
def truncate(data, length):
    '''
    Input  -
       params: data - The data whose length is to be truncated
       params: length - The length to be truncated
    Output - The data with the truncated length
    '''
    return data if len(data) <= length else data[:length]

def rowvalidation(row):
    # pylint: disable-msg=R0912
    '''
    Iteration on pandas df
    Input -
        params: row: dict of file row
    Output - Returning Pandas series
    '''
    validation_remark = "Valid GSTIN"
    row["status"] = "Initiated"
    #stripping the gstin
    row["gstin"] = row["gstin"].strip()
    #Validating user_gstin
    # Checking if the user_gstin matches the corresponding regex.
    if not validate_expression(GSTIN_REGEX, row["gstin"]):
        validation_remark = ""
        row["status"] = ""
        #Truncating length of gstin as per gstin column size in database
        row["gstin"] = truncate(row["gstin"], 20)
    row["gstin"] = row["gstin"].upper()
    return pd.Series([row["gstin"], validation_remark, row["status"]])

#Called from lambda_function.py
#Validating the columns
def gstin_mapping_data(filepath, data, created_by_user, upload_data_dict,\
    l1_bucket, b_filename, database):
    # pylint: disable-msg=W0703
    # pylint: disable-msg=R0913
    '''
     Input  -
        params: filepath - The location of the file path
        params: data - The data in csv file
        params: created_by_user - The user who have uploaded the file
        params: l1_bucket - bucket name of L1
        params: b_filename - file name from backup
        params: config_dict: configuration of database
     Output - The fields are validated
    '''
    msg, count = "", 0
    flag_trigger_update = True
    conn = None
    try:
        #Reading data from CSV
        test_data = pd.read_csv(filepath, encoding="ISO-8859-1", dtype=object)
        #Rename Column
        test_data.rename(columns=RENEAME_COL_DICT, inplace=True)
        #filling blank 
        test_data = test_data.fillna("")
        #filtering empty value from series
        test_data['gstin'] = list(filter(lambda x: True if x else False,test_data['gstin']))
        #uppercase of gstin
        test_data['gstin'] = list(map(lambda x: x.upper(),test_data['gstin']))
        #dropping duplicate entries
        count = test_data.shape[0]
        print("L1: Total Count OF GSTIN (In Uploaded File) = ", test_data.shape[0])
        test_data.drop_duplicates(subset="gstin", keep="first", inplace=True)
        print("L1: Non-Duplicate Count OF GSTIN (In Uploaded File) = ", test_data.shape[0])
        if test_data.shape[0]:
            #convertin gstin into list data
            gstin_join = ",".join([ f"'{x}'" for x in test_data['gstin']])
            #getting data from dataabse for the existing gstin
            final_select_query = SELECT_QUERY_FOR_EXISTING_GSTIN.format(gstin_join=gstin_join)
            print(f"select query -> {final_select_query}")
            conn = make_connection(database)
            cursor = get_dict_cursor(conn)
            final_select_query_data = fetchall_select_query(final_select_query, cursor)
            print(f"NUMBER OF NON INITIATED EXISTING GSTIN -> {len(final_select_query_data)}")
            #preparing list of data
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_history = "Data inserted through csv by {0} on {1}".format(created_by_user, current_date)
            existing_gstin_update_list = []
            existing_gstin_insert_list = []
            print(test_data)
            if final_select_query_data:
                #Preparing insert data and update data for existing gstind
                for row in final_select_query_data:
                    #Preparing insert and update data for existing gstins if status!="Initiated"
                    #update data for exising gstin entry
                    update_data={}
                    update_data['active'] = 'N'
                    update_data['updated_by'] = created_by_user
                    update_data['updated_date'] = current_date
                    update_data['update_history'] = update_history
                    update_data['id'] = row['id']
                    existing_gstin_update_list.append(update_data)
                    #insert data for existing gstin new entry
                    del row['id']
                    row['status'] = "Initiated"
                    row['created_by'] = created_by_user
                    row['updated_by'] = created_by_user
                    row['created_date'] = current_date
                    row['updated_date'] = current_date
                    row['load_id'] = str(data[0])
                    row['update_history'] = row['update_history'] + "<br>" + update_history
                    row['gstin_adadr'] = json.dumps(row['gstin_adadr']) if row['gstin_adadr']!=None else row['gstin_adadr']
                    existing_gstin_insert_list.append(row)

                #inserting and updating data in database for exsting gstins
                if existing_gstin_update_list and existing_gstin_insert_list:
                    insert_column_list = existing_gstin_insert_list[0].keys()
                    INSERT_QUERY_FOR_EXISTING_GSTIN = (f"INSERT INTO demo.gstin_status({', '.join(insert_column_list)}) VALUES("\
                        f"{', '.join([f'%({x})s' for x in insert_column_list])})")
                    print(f"INSERT QUERY -> {INSERT_QUERY_FOR_EXISTING_GSTIN}")
                    cursor.executemany(UPDATE_QUERY_FOR_EXISTING_GSTIN, existing_gstin_update_list)
                    cursor.executemany(INSERT_QUERY_FOR_EXISTING_GSTIN,existing_gstin_insert_list)
                    conn.commit()

            #INSERTING NEW GSTIN IN DATABASE
            # validating file and GSTIN and Setting nic status
            test_data[["gstin", "validation_remark", "status"]] = \
            test_data.apply(rowvalidation, axis=1)
            # default value key
            default_value = {"created_by": created_by_user, "created_date": current_date, \
            "updated_by": created_by_user, "updated_date": current_date, "load_id": str(data[0]),\
            "update_history": update_history}
            #Appending default values in test_data
            for key in default_value:
                test_data[key] = default_value[key]
            all_list = test_data.T.to_dict().values()
            cursor.executemany(INSERT_QUERY_FOR_NEW_GSTIN, tuple(all_list))
            conn.commit()
            print("L1: New GSTIN added to the database = ", cursor.rowcount)
            #UPDATING UPLOAD TABLE
            upload_data_dict["import_from_file"] = count
            msg = "Data successfully loaded"
            upload_data_dict["status"] = msg
            try:
                print("L1: INSERTING DATA INTO UPLOAD TABLE")
                upload_file_details_with_conn(data, upload_data_dict, conn, cursor)
                print("L1: INSERTED DATA INTO UPLOAD TABLE")
            except Exception as error:
                print("L1 EXCEPTION OCCURED Getting insertion error on upload table")
                print("L1: EXCEPTION OCCURED ", error)
                msg = "Data upload failed."
                count = 0
                # uploading file to error folder
                error_upload_file(l1_bucket, b_filename, upload_data_dict["original_file_name"])
            exist_cur_conn_closed(conn, cursor)
            flag_trigger_update = False
        else:
            msg = "Rejected - File is emtpy"
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", error)
        print("L1: SOMETHING IS WRONG")
        msg = "Data upload failed."
        count = 0
        exist_conn_closed(conn)
        traceback.print_exc()
    return flag_trigger_update, msg, count
