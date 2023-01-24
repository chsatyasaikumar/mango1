#Parsing the oracle format to l2
from __future__ import print_function
import pandas as pd

from .oracle_configuration import RENAME_HEADER
from .oracle_date_parse import oracle_dateparsing

#Helper function
#Mapping the blank field
def blank_field_map(data, size, mapping_dict):
    '''
    Input  -
       params: data - The csv file that is being read
       params: size - The size of the field
       params: mapping_dict - The environment variable of oracle
    Output - The empty fields are mapped
    '''
    blank_value_field = mapping_dict["blank_value_field"]
    for blank_column in blank_value_field:
        data[blank_column] = [""] * size

#Called from lambda_function.py
#Parsing the oracle format to l2
def oracle_ewb_format_mapping(filename, data_id, mapping_dict, created_by_user, source_type, bucket, master_config):
    '''
    Input  -
       params: filename - The name of csv file
       params: mapping_dict - The environment variable of oracle
       params: created_by_user - The user who created the csv file
       params: source_type - Source_type for csv file
    Output - The oracle format is parsed according to l2
    '''
    try:
        test_data = pd.read_csv(filename, encoding="ISO-8859-1", dtype=object)
        size = test_data.shape
        if size[0] > 0:
            blank_field_map(test_data, size[0], mapping_dict)
            oracle_dateparsing(test_data, mapping_dict, size[0])
            test_data.rename(columns=RENAME_HEADER, inplace=True)
            test_data["document_status"] = "Loaded"
            test_data["validation_status"] = "Loaded"
            #Setting the load_id
            test_data["id"] = str(data_id[0]) if data_id else ""
            #Setting the user name who uploaded the file
            test_data["created_by_user"] = created_by_user
            #Setting source type of file name
            test_data["source_type"] = source_type
            #Saving file to level 2 format
            test_data.to_csv(filename, sep=",", index=False)
            print("L1: MAPPING COMPLETED")
            flag = True
            remark = ""
        else:
            flag = False
            remark = "Rejected - Empty file."
    except Exception as error:
        flag = False
        remark = str(error)
        print("L1: EXCEPTION OCCURED ", str(error))
    return flag, remark
