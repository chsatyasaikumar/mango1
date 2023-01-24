'''
#Validating partb columns
'''
from __future__ import print_function
import csv
import pandas as pd
import boto3
s3_obj = boto3.client('s3')
from comman_module.function import csv_injection_handling
from .partb_config import PARTB_HEADER

#Called from lambda_function.py
#Validating partb columns
def partb_validate_csv_header(filename, bucket, unique_name):
    # pylint: disable-msg=W0703
    '''
    Input  -
       params: filename - The file for which columns are to be validated
    Output - The sap column are validated
    '''
    flag = False
    message = "Rejected - Invalid file format"
    try:
        with open(filename, encoding="ISO-8859-1") as csv_read:
            csv_data = csv.reader(csv_read, delimiter=',')
            header = next(csv_data)
            #Comparing the csv file header and partb header
            if header != PARTB_HEADER:
                message = "Header is not in valid format - partb."
                print("L1: THE MESSAGE IS Header is not in valid format - partb.")
                print("L1: THE HEADER IS ", header)
            else:
                print("L1: VALIDATED HEADER SUCCESSFULLY - PARTB")
                flag, message = True, ""
            #reading File
            dframe = pd.read_csv(filename, encoding="ISO-8859-1", dtype=object)
            #csv_injection_handling
            dframe = csv_injection_handling(header, dframe)
            #saving file in local after transformation
            dframe.to_csv(filename, columns=header, index=False)
            #replacing file in backup
            s3_obj.upload_file(filename, bucket, unique_name)
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", error)
        print("L1: CSV HEADER VALIDATION FAILED")
    return flag, message
