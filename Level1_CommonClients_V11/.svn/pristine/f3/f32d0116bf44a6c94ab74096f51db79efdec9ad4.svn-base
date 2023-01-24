'''
#Validating the date fields
'''
from __future__ import print_function
import datetime
#Helper function
#Parsing string date to date object
def sap_parse_string_to_datetime(date_format, date_string):
    # pylint: disable-msg=W0703
    '''
    Input  -
       params: date_format - The allowed date format
       params: date_string - The date to be parsed to datetime
    Output - The date string parsed to date object
    '''
    try:
        date_string = datetime.datetime.strptime(date_string, date_format).strftime("%Y-%m-%d")
    except Exception as error:
        pass
    return date_string

#Helper function
#Reading date config from json and parsing date to db format
def sap_dateparsing(data, mapping_dict, size):
    '''
        Input  -
           params: data - The csv file read
           params: mapping_dict - Configuration file of oracle
           params: size - The size of the csv file
        Output - The date is read from json file and converted to db storable format
    '''
    date_details = mapping_dict["date_details"]
    # can be multiple date format in date_format
    date_format = date_details["date_format"]
    # if date_format is string then add to list
    date_format = [date_format] if isinstance(date_format, str) else date_format
    date_field_columns = date_details["date_field_columns"]
    # loop iteration on date format
    for custom_date in date_format:
        # loop iteration on date column
        for date_field_name in date_field_columns:
            temp_list = data[date_field_name]
            # Checking for list type
            if not isinstance(data[date_field_name], list):
                temp_list = data[date_field_name].tolist()
            # loop iteration on data
            for i in range(size):
                # Converting the string to date object.
                # Calling sap_parse_string_to_datetime() function in the same file
                temp_list[i] = sap_parse_string_to_datetime(custom_date, temp_list[i])
            data[date_field_name] = temp_list

# ackdt pasrse

def parse_timestamp(data):
    '''
    Summery Line.
        Here we are transforming ackdt to %Y-%m-%d %H:%M:%S format
    Parameters:
        data(str): ackdt
    Return:
        data(str) after transform
    '''
    try: 
        data = datetime.datetime.strptime(data, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    except Exception as error:
        pass
    return data
