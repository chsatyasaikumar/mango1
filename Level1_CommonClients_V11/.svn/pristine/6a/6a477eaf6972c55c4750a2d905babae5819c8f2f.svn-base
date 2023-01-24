#Validating the oracle header
from __future__ import print_function
import csv
import pandas as pd
import boto3
s3_obj = boto3.client('s3')
from comman_module.function import csv_injection_handling
from .oracle_configuration import ORACLE_FORMAT_HEADER

#Validating the oracle header
def oracle_validate_csv_header(filename, bucket, unique_name):
    '''
    Input  -
       params: filename - The file name for which the oracle _header is to be validated
    Output - The oracle header is validated
    '''
    try:
        with open(filename, encoding="ISO-8859-1") as csv_read:
            csv_data = csv.reader(csv_read, delimiter=',')
            header = next(csv_data)
            #Checking the header of csv file with that of oracle header format
            if header != ORACLE_FORMAT_HEADER:
                message = "Header is not in valid format - oracle"
                print("L1: MESSAGE IS ", str(message))
                print("L1: HEADER IS ", str(header))
                return False, "Rejected - Invalid file format"
            else:
                print("L1: VALIDATED HEADER SUCCESSFULLY")
                return True, ""
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
        print("L1: CSV HEADER VALIDATION FAIL FOR ORACLE")
        return False, "Rejected - Invalid file format"
