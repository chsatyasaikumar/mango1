'''
#Validating grn_module header
'''
from __future__ import print_function
import csv
import datetime
from .grn_configuration import DEFAULT_HEADER
from comman_module.function import csv_injection_handling
import pandas as pd
import boto3
s3_obj = boto3.client('s3')

#Validating the grn_module header
def grn_validate_csv_header(filename, bucket, unique_name):
    # pylint: disable-msg=W0703
    '''
    Input  -
       param: filename - The filename whose header is to be validated
    Output - The grn module header is validated successfully
    '''
    flag = False
    header = None
    message = "Rejected - Invalid file format"
    try:
        with open(filename, encoding="ISO-8859-1") as csv_read:
            csv_data = csv.reader(csv_read, delimiter=',')
            header = next(csv_data)
            # Checking if the header in csv file is the same as the header defined for
            # grn module
            if header != DEFAULT_HEADER:
                print("L1: MESSAGE - Header is not in valid format - grn module")
                print("L1: HEADER ", header)
            else:
                print("L1: HEADER VALIDATED SUCCESSFULLY")
                flag = True
                message = ""
            #dframe
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

#Validating the date format
def grn_validate_date(str_date, d_format, p_format):
    # pylint: disable-msg=W0703
    '''
        Input  -
           params: str_date - The date present in csv file that is to be validated
           params: d_format - The allowed date format
           params: p_format - The allowed date format
        Output - The date format is validated successfully
    '''
    flag, date_string = False, None
    try:
        # Parsing the date object to string.Calling parse_datetime_to_string() function
        date_string = datetime.datetime.strptime(str_date, d_format).strftime(p_format)
        flag = True
    except Exception as error:
        pass
    return flag, date_string
