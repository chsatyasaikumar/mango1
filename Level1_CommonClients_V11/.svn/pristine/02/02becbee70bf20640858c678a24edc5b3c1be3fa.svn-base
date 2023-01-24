'''
#Validating sap headers
'''
from __future__ import print_function
import csv
import pandas as pd
import boto3
s3_obj = boto3.client('s3')
from comman_module.function import csv_injection_handling
from .sap_configuration import DEFAULT_HEADER, DEFAULT_HEADER_2, DEFAULT_HEADER_3

#Validating sap headers
def sap_validate_csv_header(filename, bucket, unique_name):
    # pylint: disable-msg=W0703
    '''
        Input  -
           params: filename - The file name for which the oracle _header is to be validated
        Output - The sap header is validated
    '''
    flag, message = False, "Rejected - Invalid file format"
    try:
        with open(filename, encoding="ISO-8859-1") as csv_read:
            csv_data = csv.reader(csv_read, delimiter=',')
            header = next(csv_data)
            # Checking the header of csv file with that of sap header format
            if header == DEFAULT_HEADER or header == DEFAULT_HEADER_2 or \
                header == DEFAULT_HEADER_3:
                print("L1: HEADER VALIDATED SUCCESSFULLY - SAP")
                flag, message = True, ""
            else:
                print("L1: MESSAGE Header is not in valid format.")
                print("L1: HEADER ", header)
            #reading File
            dframe = pd.read_csv(filename, encoding="ISO-8859-1", dtype=object)
            #csv_injection_handling
            dframe = csv_injection_handling(header, dframe)
            #saving file in local after transformation
            dframe.to_csv(filename, columns=header, index=False)
            #replacing file in backup
            s3_obj.upload_file(filename, bucket, unique_name)
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", str(error))
        print("L1: HEADER VALIDATION FAILED")
    return flag, message
        