'''
Partb Mapping calling update transporter API
'''
from __future__ import print_function
import traceback
import pandas as pd
from .partb_update import update_document_details

#Called from lambda_function.py
#Updating the transporter_name and transporter_id in document_details table
#by calling function in another file
def partb_mapping_data(filepath, created_by_user, load_id, source_system, load_type,\
    upload_data_dict, l1_bucket, b_filename, config_dict, database):
    # pylint: disable-msg=R0913
    # pylint: disable-msg=W0703
    '''
    Input  -
       params: filepath -
       params: created_by_user - The user who have uploaded the csv file
       params: load_id - The load_id that is generated after inserting details to database
       params: source_system - The source system defined in configuration.py
                                in common module in update_data_dict
       params: load_type - The load type defined in configuration.py
                            in common module in update_data_dict
       params: config_dict: configuration of transporter update url
    Output - The transporter_name and transporter_id in document_details table
              is being uploaded
    '''
    flag_trigger_update = False
    status = "Rejected - File is emtpy"
    try:
        test_data = pd.read_csv(filepath, encoding="ISO-8859-1", dtype=object)
        test_data = test_data.fillna("")
        #Checking the size of a csv file
        if not test_data.empty:
            #Updating transporter_name and transporter_id in document_details table
            #Calling update_document_details() function
            flag, status = update_document_details(test_data, created_by_user, load_id,\
                source_system, load_type, upload_data_dict, l1_bucket, b_filename, config_dict, database)
            flag_trigger_update = not flag
        else:
            print("L1: EMPTY FILE")
            flag_trigger_update = True
    except Exception as error:
        status = str(error)
        print("L1: EXCEPTION OCCURED %s ", status)
        flag_trigger_update = True
        traceback.print_exc()
    return flag_trigger_update, status
