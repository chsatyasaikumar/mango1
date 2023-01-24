#Parsing date objects to string and vice versa
from __future__ import print_function
import datetime

#Helper function
#Parsing the date object to string
def parse_datetime_to_string(date_string):
    '''
     Input  -
        params: date_string - The date to be parsed to string
     Output - The date object parsed to string
    '''
    return date_string.strftime("%Y-%m-%d")

#Helper function
#Parsing string date to date object
def sap_parse_string_to_datetime(date_format, date_string):
    '''
     Input  -
        params: date_string - The date to be parsed to datetime
        params: key - The remark to be added
    Output - The date string parsed to date object
    '''
    try:
        date_string = parse_datetime_to_string(datetime.datetime.strptime(date_string, date_format))
    except Exception:
        pass
    return date_string

#Helper function
#Reading date config from json and parsing date to db format
def oracle_dateparsing(data, mapping_dict, size):
    '''
    Input  -
       params: data - The csv file read
       params: mapping_dict - Configuration file of oracle
       params: size - The size of the csv file
    Output - The date is read from json file and converted to db storable format
    '''
    date_details = mapping_dict["date_details"]
    date_format = date_details["date_format"]
    date_field_columns = date_details["date_field_columns"]
    for date_field_name in date_field_columns:
        temp_list = data[date_field_name]
        #Checking for list type
        if not isinstance(data[date_field_name], list):
            temp_list = data[date_field_name].fillna("").tolist()
        for i in range(size):
            #Converting the string to date object.
            #Calling sap_parse_string_to_datetime() function in the same file
            temp_list[i] = sap_parse_string_to_datetime(date_format, temp_list[i])
        data[date_field_name] = temp_list
