'''
#Validating sap headers
'''
from __future__ import print_function
import pandas as pd
import logging
import boto3
S3_OBJECT = boto3.client('s3')
from comman_module.function import csv_injection_handling

#Validating sap headers
def custom_validate_csv_header(filename, mapping_json, bucket, unique_name):
    # pylint: disable-msg=W0703
    '''
        Input  -
           params: filename - The file name for which the oracle _header is to be validated
        Output - The sap header is validated
    '''
    flag, message = False, "Rejected - Invalid file format"
    
    try:
        dframe = pd.read_csv(filename, encoding="ISO-8859-1", dtype=object)
        header = list(dframe.columns.values)
        # Checking the header of csv file with that of Custom header format
        if header == mapping_json.get('default_header'):
            print("L1: HEADER VALIDATED SUCCESSFULLY - CUSTOM")
            flag, message = True, ""
        else:
            print("L1: MESSAGE Header is not in valid format.")
            print("L1: HEADER ", header)
        #csv_injection_handling
        dframe = csv_injection_handling(header, dframe)
        #saving file in local after transformation
        dframe.to_csv(filename, columns=header, index=False)
        #replacing file in backup
        S3_OBJECT.upload_file(filename, bucket, unique_name)
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", str(error))
        print("L1: HEADER VALIDATION FAILED")
    return flag, message

