'''
#Mapping the datas
'''
from __future__ import print_function
import boto3
import os
import traceback
import pandas as pd
from sap_module.client_transformation import ClientTransform
from .sap_configuration import DEFAULT_HEADER, DEFAULT_HEADER_2, RENAME_HEADER,\
    MASTER_CONFIG_PATH, GEN_HEADER, OPTIONAL_HEADER, OPTIONAL_HEADER_2
from .sap_date_parse import sap_dateparsing, parse_timestamp
#Mapping the headers
def exchange_map(test_data, mapping_dict):
    '''
    Input  -
       params: test_data - The csv file read
       params: mapping_dict - Configuration file of sap
    Output - Mapping the headers
    '''
    exchange = mapping_dict["exchange"]
    for key in exchange.keys():
        test_data[key] = test_data[exchange[key]]

#Mapping the blank or null fields
def map_blank_field(test_data, header):
    '''
    Input  -
       params: test_data - The csv file read
       params: header - The header for sap format
    Output - The null fields are mapped
    '''
    for value in header:
        test_data[value] = ""

#Mapping the fields like distance, user_gstin, bu, sbu_id, location, user
def map_master_data(row, master_obj, unit_transformation_dict, distance_transformation, \
    load_id, created_by_user, source_type):
    '''
    Input  -
       params: row - Each row in a csv file
       params: master_obj - The master data in the master table
    Output - The fields like distance, user_gstin, bu, sbu_id, location, user are mapped
    '''
    unit = row["unit"].strip().upper()
    if unit_transformation_dict and unit and unit in unit_transformation_dict:
        unit = unit_transformation_dict[unit]
    #Initialization of variables
    alert_validation_remark = ""
    upper_to_gstin = row["to_gstin"].strip().upper()
    upper_supply_type = row["supply_type"].strip().upper()
    upper_transporter_id = row["transporter_id"].strip().upper()
    upper_from_gstin = row["from_gstin"].strip().upper()
    #Mapping the distance
    distance_km = row["distance_km"]
    key = row["from_pin_code"] + row["to_pin_code"]
    #Checking if distance_km is null and equal to 0
    if distance_transformation == "Y":
        if row["from_pin_code"] == "999999" or row["to_pin_code"] == "999999" or \
            row["from_pin_code"] == row["to_pin_code"]:
            pass
        else:
            distance_km = "0"
    elif (not distance_km or distance_km == "0") and \
        key in master_obj.master_data["logistics_master"]:
        distance_km = master_obj.master_data["logistics_master"][key]
    validation_remark = ""

    #Mapping company_name and company_id
    upper_user_gstin = (row["user_gstin"].strip()).upper()
    company_name = ""
    #Checking if the user_gstin is present in master_data
    flag_user_gstin = upper_user_gstin in master_obj.master_data["company_master"]
    #Checking if user_gstin is null or not
    blank_check_user_gstin = row["user_gstin"] if row["user_gstin"] else "BLANK"
    #Checking the status of user_gstin in master_data
    if flag_user_gstin:
        company_id = str(master_obj.master_data["company_master"][upper_user_gstin][0])
        company_name = master_obj.master_data["company_master"][upper_user_gstin][1]
        gstin_id = master_obj.master_data["company_master"][upper_user_gstin][2]
    else:
        validation_remark = validation_remark + "\"" + "User GSTIN" + \
                            "\" \"" + blank_check_user_gstin +\
                            "\" is not available in master table<br>"
        gstin_id = "-1"
        company_id = "-1"

    #Mapping bu
    upper_bu = (row["bu"].strip()).upper()
    bu_id = "0"
    key_bu = company_id + ":" + upper_bu
    #Checking if the bu concatenated with company_id is present in master data
    flag_bu = key_bu in master_obj.master_data["bu_master"]
    #Checking the status of above line
    if flag_bu:
        bu_id = master_obj.master_data["bu_master"][key_bu]
    #Checking if bu exist
    #and the status of bu concatenated with company_id is present in master data
    if upper_bu and not flag_bu:
        validation_remark = validation_remark + "\"" + "BU" + "\" \"" \
                            + row["bu"] + "\" is not available in master table<br>"
        bu_id = "-1"

    #Mapping sbu_id
    upper_sbu = (row["sbu"].strip()).upper()
    sbu_id = "0"
    key_sbu = company_id + ":" + upper_sbu + ":" + upper_bu
    # Checking if the sbu concatenated with company_id and bu is present in master data
    flag_sbu = key_sbu in master_obj.master_data["sbu_master"]
    #Checking the status of above line
    if flag_sbu:
        sbu_id = master_obj.master_data["sbu_master"][key_sbu]
    # Checking if sbu exist
    # and the status of sbu concatenated with company_id and bu is present in master data
    if upper_sbu and not flag_sbu:
        validation_remark = validation_remark + "\"" + "SBU" + "\" \"" + \
                            row["sbu"] + "\" is not available in master table<br>"
        sbu_id = "-1"
    #Mapping the location
    upper_location = (row["location"].strip()).upper()
    key_location = company_id + ":" + upper_location
    location_id = "0"
    # Checking if the location concatenated with company_id is present in master data
    flag_location = key_location in master_obj.master_data["location_master"]
    #Checking the status of above line
    if flag_location:
        location_id = master_obj.master_data["location_master"][key_location]
    # Checking if location exist
    # and the status of location concatenated with company_id is present in master data
    if upper_location and not flag_location:
        validation_remark = validation_remark + "\"" + "Location" + "\" \"" \
                            + row["location"] + "\" is not available in master table<br>"
        location_id = "-1"

    #Mapping the user
    upper_user = (row["user"].strip()).upper()
    #Checking if the user exist and is present in master table
    if upper_user and master_obj.master_data["user_master"] \
            and upper_user not in master_obj.master_data["user_master"]:
        validation_remark = validation_remark + "\"" + "User" + "\" \"" + \
        row["user"] + "\" is not available in master table<br>"


    #Transporter email logic for TML Client
    fu_30 = row["fu_30"]
    fu_29 = row["fu_29"]
    trans_flag = False
    upper_transporter_id = str(row["transporter_id"]).upper() if row["transporter_id"] else ""
    upper_location = str(row["location"]).upper() if row["location"] else ""
    upper_mis_8 = str(row["mis_8"]).upper() if row["mis_8"] else ""
    if str(os.environ.get("customer_id", "")) == "402":
        tml_transporter_master_email_key  = upper_transporter_id + ":" + upper_location + ":" + upper_mis_8
        if tml_transporter_master_email_key in master_obj.master_data["tml_transporter_master_email"]:
            fu_30 = master_obj.master_data["tml_transporter_master_email"][tml_transporter_master_email_key]
            trans_flag = True
        if upper_supply_type == "OUTWARD":
            if upper_to_gstin in master_obj.master_data["customer_master_email"]:
                fu_29 = master_obj.master_data["customer_master_email"][upper_to_gstin] if trans_flag else \
                master_obj.master_data["customer_master_email"][upper_to_gstin]
    else:
        if upper_transporter_id in master_obj.master_data["transporter_master_email"]:
            fu_30 = master_obj.master_data["transporter_master_email"][upper_transporter_id]
            trans_flag = True
        if upper_supply_type == "OUTWARD":
            if upper_to_gstin in master_obj.master_data["customer_master_email"]:
                fu_30 = fu_30 + "," + \
                master_obj.master_data["customer_master_email"][upper_to_gstin] if trans_flag else \
                master_obj.master_data["customer_master_email"][upper_to_gstin]
    # nic is not using the block validation now we are commenting the code 22/03/2022
    #Appending alert_validation_remark for blocked gstin [transporter_id, from_gstin, to_gstin]
    #transporter_id
    # if upper_transporter_id:
    #     if upper_transporter_id in master_obj.master_data["gstin_status"]:
    #         if master_obj.master_data["gstin_status"][upper_transporter_id][\
    #             "nic_block_status"] == "BLOCKED":
    #             alert_validation_remark = alert_validation_remark + "\"" +\
    #             "Transporter Id" + "\" \"" +\
    #             upper_transporter_id + "\" of transporter appears to be blocked (Alert)<br>"
    # #to_gstin in case of "OUTWARD" supply type
    # if upper_to_gstin and upper_supply_type == "OUTWARD":
    #     if upper_to_gstin in master_obj.master_data["gstin_status"]:
    #         if master_obj.master_data["gstin_status"][upper_to_gstin][\
    #             "nic_block_status"] == "BLOCKED":
    #             alert_validation_remark = alert_validation_remark + "\"" +\
    #             "To GSTIN" + "\" \"" +\
    #             upper_to_gstin + "\"  of consignee appears to be blocked (Alert)<br>"
    # #from_gstin in case of "INWARD" supply type
    # if upper_from_gstin and upper_supply_type == "INWARD":
    #     if upper_from_gstin in master_obj.master_data["gstin_status"]:
    #         if master_obj.master_data["gstin_status"][upper_from_gstin][\
    #             "nic_block_status"] == "BLOCKED":
    #             alert_validation_remark = alert_validation_remark + "\"" +\
    #             "From GSTIN" + "\" \"" +\
    #             upper_from_gstin + "\"  of supplier appears to be blocked (Alert)<br>"
    # transforming ackdt
    if row["ackdt"]:
        row["ackdt"] = parse_timestamp(row["ackdt"])
    document_status = "Loaded"
    validation_status = "Loaded"
    load_id = load_id
    created_by_user = created_by_user
    source_type = source_type
    return pd.Series([bu_id, sbu_id, location_id, company_id, company_name,
        validation_remark, distance_km, gstin_id, fu_29, fu_30, \
        alert_validation_remark, row["ackdt"], unit, document_status, \
        validation_status, load_id, created_by_user, source_type])

class MasterData:
    '''
    add master_config
    '''
    def __init__(self, dict_obj):
        self.master_data = dict_obj

#Mapping the sap format
def mapping_data(filepath, data, mapping_dict, created_by_user, source_type, bucket, master_config, custom_frame=None):
    # pylint: disable-msg=W0703
    # pylint: disable-msg=R0913
    print("SAP FORMAT MAPPING")
    '''
    Input  -
       params: file_path - The location of the file
       params: data - The csv file read
       params: mapping_dict - Configuration file of sap
       params: created_by_user - The user who have uploaded the file
       params: source_type - The source_type present in update_data_dict_data in configuration.py
                             from common_module
    Output - Mapping done with respect to sap format
    '''
    flag, message = False, "Rejected - Empty file."
    try:
        #Reading the file by using pandas
        if isinstance(custom_frame, pd.DataFrame):
            test_data = custom_frame
        else:
            test_data = pd.read_csv(filepath,encoding="ISO-8859-1", dtype=object)
            
        #Getting the size of data
        size = test_data.shape
        test_data = test_data.fillna("")
        #Checking the config json file exist or not
        if not test_data.empty:
            # test_data["document_status"] = "Loaded"
            # test_data["validation_status"] = "Loaded"
            # #Setting the load_id
            # test_data["id"] = str(data[0]) if data else ""
            # #Setting the user_name who uploaded the file
            # test_data["created_by_user"] = created_by_user
            # #Setting the source_type of the file name
            # test_data["source_type"] = source_type
            #Mapping the columns
            exchange_map(test_data, mapping_dict)
            #Parsing the date
            sap_dateparsing(test_data, mapping_dict, size[0])
            #Renaming the columns to bd format
            if size[1] == len(DEFAULT_HEADER):
                map_blank_field(test_data, OPTIONAL_HEADER)
            elif size[1] == len(DEFAULT_HEADER_2):
                map_blank_field(test_data, OPTIONAL_HEADER_2)
            # client level transformation
            if mapping_dict.get("client_condition"):
                test_data = ClientTransform.client_process(test_data, \
                    mapping_dict.get("client_condition"))
            if mapping_dict.get("client_condition_v2"):
                test_data = ClientTransform.client_process_v2(test_data, \
                    mapping_dict)
            test_data.rename(columns=RENAME_HEADER, inplace=True)
            master_data = master_config
            master_obj = MasterData(master_data)
            unit_transformation_dict = mapping_dict.get("unit_transformation", {})
            distance_transformation = mapping_dict.get("distance_transformation")
            # load id
            load_id = str(data[0]) if data else ""
            if not distance_transformation:
                distance_transformation = ""
            test_data[["bu_id", "sbu_id", "location_id", "company_id", "company_name",\
                "validation_remark", "distance_km", "gstin_id", "fu_29", "fu_30",\
                "alert_validation_remark", "ackdt", "unit", "document_status", \
                "validation_status", "id", "created_by_user", "source_type"]] = \
                test_data.apply(map_master_data, args=(master_obj, unit_transformation_dict, \
                    distance_transformation, load_id, created_by_user, source_type), axis=1)
            #Saving the file to l2 format
            test_data.to_csv(filepath, columns=GEN_HEADER, index=False)
            flag, message = True, ""
        else:
            print("L1 - Empty File")
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", error)
        traceback.print_exc()
        message = str(error)

    return flag, message
