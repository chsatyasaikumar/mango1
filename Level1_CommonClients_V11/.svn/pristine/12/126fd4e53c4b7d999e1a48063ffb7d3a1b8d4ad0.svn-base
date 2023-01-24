'''
#Validating the file name and file format
'''
from __future__ import print_function
from itertools import chain
#Called from lambda_function.py
#Validating the file format
def validate_file_format(filename):
    '''
    Input  -
       params: filename - The file for which the format is to be validated
    Output - The file name is validated
    '''
    #Checking if it is a csv file
    return bool(len(filename) > 3 and filename[-4:] in ['.csv', '.pdf'])

#Called from lambda_function.py
#Validating the file name
def validate_auto_manual_filnaming(filename, oracle_type, sap_type, tally_type, custom_type):
    '''
    Input  -
       params: filename - The file for which the name is to be validated
    Output - The file name is validated
    '''
    #Getting the source type from env
    source_type = list(chain(oracle_type, sap_type, tally_type, custom_type))

    #Category format
    auto_cat_format = ["document_details", "customer_master", "supplier_master", "product_master",
                       "transporter_master", "logistics_master", "bill_of_entry", "partb_details",
                       "ewb_changeship", "purchase_register", "delivery_details", "repository","gstin"]
    validate_data = (False, "Automatic")
    if len(filename) >= 5:
        #Checking the source type for web
        comman_flag = filename[0].lower() in auto_cat_format and\
                      filename[1].upper() in source_type
        # Checking if the file is uploaded from web or not
        validate_data = (False, filename[2])
        #Checking the status of above line
        if comman_flag:
            validate_data = (True, filename[2])
        #Checking if the file is uploaded from web or not
    elif len(filename) >= 2:
        #Checking the source type for automatic
        validate_data = (False, "Automatic")
        if filename[0].lower() in auto_cat_format and \
                filename[1].upper() in source_type:
            validate_data = (True, "Automatic")
    return validate_data
