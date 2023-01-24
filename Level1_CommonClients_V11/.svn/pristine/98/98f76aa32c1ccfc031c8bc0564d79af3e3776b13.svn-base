'''
#Validating the header for purchase_register module
'''
from __future__ import print_function
import csv
import pandas as pd
import boto3
s3_obj = boto3.client('s3')
from .gstin_configuration import DEFAULT_HEADER
from comman_module.function import csv_injection_handling

#Validating purchase_register columns
def gstin_validate_csv_header(filename, bucket, unique_name):
    # pylint: disable-msg=W0703
    '''
    Input  -
       param: filename - The filename whose header is to be validated
    Output - The gstin module header is validated successfully
    '''
    message = "Rejected - Invalid file format"
    flag = False
    try:
        with open(filename, encoding="ISO-8859-1") as csv_read:
            csv_data = csv.reader(csv_read, delimiter=',')
            header = next(csv_data)
            #header uppercase
            header = list(map(lambda x: x.upper(), header))
            #Checking if the header in csv file is the same as the header defined for
            if header == DEFAULT_HEADER:
                print("L1: HEADER VALIDATED SUCCESSFULLY")
                flag, message = True, ""
            else:
                print("L1: MESSAGE Header is not in valid format for gstin")
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
        print("L1: EXCEPTION OCCURED ", error)
        print("L1: CSV HEADER VALIDATION FAILED")
    return flag, message
