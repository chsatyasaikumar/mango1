'''
#Starting file of the project.The execution begins from here
#Default function - lambda_handler
'''
from __future__ import print_function
import datetime
import logging
from urllib.parse import unquote_plus
import traceback
import boto3
import json
import os
from comman_module.levelonevalidation import validate_file_format, validate_auto_manual_filnaming
from comman_module.save_data import get_load_id, upload_file_details, upload_file_details_with_conn
from comman_module.configuration import UPLOAD_DATA_DICT_DATA, BUCKET_CONFIG_FILENAME
from comman_module.function import get_config_dict_from_cache, get_master_config_dict_from_cache,\
get_gstin_status_config_dict_from_cache, is_key_exist, Properties

from sap_module.sap_mapping import mapping_data
# from sap_module.sap_configuration import SAP_MAPPING_CONFIG_PATH
from sap_module.sap_validation import sap_validate_csv_header

from oracle_module.oracle_mapping import oracle_ewb_format_mapping
# from oracle_module.oracle_configuration import ORACLE_MAPPING_CONFIG_PATH
from oracle_module.oracle_validation import oracle_validate_csv_header

from custom_module.custom_validation import custom_validate_csv_header
from custom_module.custom_mapping import transform_dataframe

from partb_module.partb_validation import partb_validate_csv_header
from partb_module.partb_mapping import partb_mapping_data

from purchase_register_module.purchase_register_mapping import purchase_register_mapping_data
from purchase_register_module.purchase_register_validation import \
        purchase_register_validate_csv_header

from grn_module.grn_validation import grn_validate_csv_header
from grn_module.grn_mapping import grn_mapping_data


from gstin_module.gstin_validation import gstin_validate_csv_header
from gstin_module.gstin_mapping import gstin_mapping_data

from irn_ewb.irn_ewb_process import IrnEwbProcess

LOGGER = logging.getLogger('EWB-L1')
LOGGER.setLevel(logging.INFO)

S3_OBJECT = boto3.client('s3')

#Helper function
#Splitting the necessary field with the specified sign
def split_data(filename, sign):
    '''
     Input  -
        params: filename - The record that needs splitting
        params: sign - The sign from which the data is to be split
     Output - The data is splitted with respect to the sign
    '''
    return filename.split(sign)

# This method using for sap/oracle file uploading and inserting upload table operation
def sap_oracle_upload_insert(data, database, upload_data_dict, s3_object, key, download_location,\
    status, l1_bucket, b_filename):
    # pylint: disable-msg=R0913
    '''
    Input -
        params: data - it is load id
        params: database - database configuration dictionary
        params: upload_data_dict - upload table dicionary
        params: s3_object - object of boto3 s3 client
        params: download_location - after transformation file for uploading
        params: key - file name of L2 process
        params: bucket - bucket name of L1
        params: status - status of L1 Process
        params: l1_bucket - L1 bucket name
        params: b_filename - backup file name from L1 bucket
    '''
    upload_trigger_flag = False
    # if process_bucket:
    upload_data_dict["status"] = status
    flag_upload = True
    # uplaoding file to L2 process and inserting data to upload table
    upload_file_details(data, database, upload_data_dict, b_filename,\
        l1_bucket, s3_object, key, download_location, flag_upload)
    # else:
    #     upload_trigger_flag = True
    #     status = "Level two bucket name does not found from config file"
    return upload_trigger_flag, status

#Helper function
#Reading the configuration file from s3 bucket and mapped data to sap, oracle and tally
def unique_validation(bucket, validation_key, func, download_location,\
    data, status, created_by_user, source_type, transform_config, master_config):
    # pylint: disable-msg=R0913
    '''
     Input  -
        params: bucket - The name of the s3 bucket
        params: s3_object - The s3 in aws
        params: validation_key - The source type
        params: func - The mapping of data
        params: config_file_path_local - The configuration set for local use
        params: config_file_path_bucket - The configuration read from s3 bucket
        params: download_location - The csv file location
        params: data - The sequence id from the upload table
        params: key - The csv file
        params: created_by_user - The user who have created the csv file
        params: source_type - The source type that is mentioned during uploading the csv file
     Output - The configuration file is read and datas are mapped to sap, oracle and tally
    '''
    flag_file_moving = False
    # Reading the configuration file from s3 bucket
    mapping_dict = transform_config
    # Checking the status of above line
    if mapping_dict and master_config:
        #Calling the parsing function of sap, oracle, tally
        flag_file_moving, remark = func(download_location, data, mapping_dict,\
            created_by_user, source_type, bucket, master_config)
        status = "Data extracted from file and getting loaded" if flag_file_moving else remark
    else:
        status = "Rejected - " + validation_key + "mapping dict does not found/master_config does not found"
        LOGGER.info(f"L1: STATUS {status}")
    return flag_file_moving, status

def send_email_sqs(sqs_message, email_sqs_url):
    '''
    Summery Line.
        Sqs send
    Parameters:
        sqs_message: sqs message
        customer_id(str): client id
    Return:
        None
    '''
    try:
        queue_client = boto3.client('sqs', region_name='ap-south-1')
        print(f'sqs client -> {str(queue_client)}')
        # LOGGER.info(f'sqs message -> {json.dumps(sqs_message)}')
        response = queue_client.send_message(\
            QueueUrl=email_sqs_url,\
            MessageBody=json.dumps(sqs_message))
        print("Message Send in Queue")
        print(f"{response}")
    except Exception as error:
        print(f"SQS Exception -> {error}")

def send_email_for_rejected_file(customer_id, bucket, file_name, status, load_id, email_sqs_url, default_headers_list=None):
    try:
        #sqs payload
        email_sqs_payload = {}
        email_sqs_payload['customer_id'] = customer_id
        email_sqs_payload['template'] = 'EWB File Rejection'
        email_sqs_payload['status'] = status
        email_sqs_payload['bucket'] = bucket
        email_sqs_payload['file_name'] = file_name
        email_sqs_payload['load_id'] = load_id
        if default_headers_list:
            email_sqs_payload['default_headers'] = json.dumps(default_headers_list)
        else:
            email_sqs_payload['default_headers'] = None
        send_email_sqs(email_sqs_payload, email_sqs_url)
    except Exception as error:
        LOGGER.error(f"error while sending sqs payload to email sqs")

#Main function from where the execution begins
#Downloading the files from s3 bucket and moving the file from incoming folder to backup folder.
#Time is calculated for the entire process and an email is sent
def lambda_handler(event, context):
    # pylint: disable-msg=W0703
    '''
    Input
       params: event   - This parameter to pass in event data to the handler.
                         This parameter is usually of the Python dict type.
                         It can also be list, str, int, float, or NoneType type.
    Output - Email is sent and time taken is being recorded
    '''
    LOGGER.info("L1:lambda_handler() FUNCTION CALL STARTED........................")
    LOGGER.info("Start Properties setup")
    load_id = ""
    prop_flag = Properties.set(serverless=True)
    LOGGER.info("End Properties setup")
    if not prop_flag:
        LOGGER.info("Properties file setup failed")
        return
    data = None
    database = None
    flag_trigger_upload = True
    upload_data_dict = UPLOAD_DATA_DICT_DATA.copy()
    l1_bucket, b_filename = "", ""
    # config_dict = get_config_dict(S3_OBJECT)
    #START READING CONFIGURATION
    LOGGER.info("L1: Start Reading Configurations")
    config_dict = get_config_dict_from_cache()
    master_config_dict = get_master_config_dict_from_cache()
    gstin_status_config_dict = get_gstin_status_config_dict_from_cache()
    #Adding gstin_status_config_dict into master_config_dict
    master_config_dict['gstin_status'] = gstin_status_config_dict
    if not config_dict:
        LOGGER.info("L1: Error: redis cache configuration is missing.")
        return
    #database = get_database(config_dict)
    database = config_dict.get("database")
    if not database:
        LOGGER.info("L1: Error: database configuration is missing.")
        return
    LOGGER.info("L1: End Reading Configurations")
    #END READING CONFIGURATIONS
    oracle_source_type = list(map(str.upper, json.loads(config_dict["etl_json"].get(\
        "ORACLE_SOURCE_TYPE", "[]"))))
    sap_source_type = list(map(str.upper, json.loads(config_dict["etl_json"].get(\
        "SAP_SOURCE_TYPE", "[]"))))
    tally_source_type = list(map(str.upper, json.loads(config_dict["etl_json"].get(\
        "TALLY_SOURCE_TYPE", "[]"))))
    custom_source_type = list(map(str.upper, json.loads(config_dict["etl_json"].get(\
        "CUSTOM_SOURCE_TYPE", "[]"))))
    try:
        for record in event['Records']:
            status = ""
            # Getting the bucket name
            bucket = record['s3']['bucket'].get('name')
            l1_bucket = bucket
            # Getting the file name
            key = unquote_plus(record['s3']['object'].get('key'))
            # Splitting the file name
            orig_key = key.split("/")
            json_csv_flag, json_csf_file_name = False, ""
            if orig_key[0] == "irn-ewb-process" and key.endswith('.json'):
                json_csv_flag, json_csf_file_name = IrnEwbProcess.transform(bucket, key, \
                    config_dict)
                if not json_csv_flag:
                    return
                orig_key[1] = json_csf_file_name
                key = f"incoming-file/{json_csf_file_name}"
            download_location = '/tmp/' + orig_key[-1]
            # Downloading the file from s3 bucket
            repo_split = orig_key[-1].split("@")
            repo_flag = bool(repo_split[0].lower() == "repository")
            if not repo_flag and "repository" not in orig_key[:-1]:
                if not json_csv_flag:
                    LOGGER.info("L1: DOWNLOADING FILE FROM S3 BUCKET")
                    S3_OBJECT.download_file(bucket, str(key), download_location)
                    LOGGER.info("L1: DOWNLOADED FILE FROM S3 BUCKET")
                    # Deleting the file from s3 bucket
                    LOGGER.info("L1: DELETING FILE FROM S3 BUCKET")
                    S3_OBJECT.delete_object(Bucket=bucket, Key=key)
                    LOGGER.info("L1: DELETED FILE FROM S3 BUCKET")
                else:
                    LOGGER.info("L1: DOWNLOADING IS NOT REQUIRED FILE COMING FROM JSON-TO-CSV PROCESS")
                # Getting the datetime stamp
                date_obj = datetime.datetime.now()
                unique_name = date_obj.strftime("%Y%m%d%H%M%S")
                date_folder = date_obj.strftime("%Y%m%d")
                # Backup file location
                unique_name = "backup" + f"/{date_folder}/" + orig_key[-1][:-4] + unique_name + ".csv"
                b_filename = unique_name
                # Checking if bill of entry is present in the data_type for
                # creating pdf file location
                if "Bill_Of_Entry" in orig_key[-1]:
                    upload_data_dict["s3_file_name"] = "pdf-file" + f"/{date_folder}/" + orig_key[-1][:-4] + ".pdf"
                    flag_is_exist = is_key_exist(S3_OBJECT, upload_data_dict["s3_file_name"], bucket)
                    if not flag_is_exist:
                        upload_data_dict["s3_file_name"] = "boe-backup" + f"/{date_folder}/" + orig_key[-1][:-4] + \
                            ".txt"
                else:
                    upload_data_dict["s3_file_name"] = unique_name
                S3_OBJECT.upload_file(download_location, bucket, unique_name)
                LOGGER.info("L1: UPLOADED BACKUP FILE TO S3 BUCKET")
            # Getting the sequence id from upload table.Calling get_load_id() function
            data = get_load_id(database)
            load_id = data[0] if data else ""
            if not data:
                status = "Rejected - Load ID is missing."
                break
            # Checking if the source type exist in env or not
            if not sap_source_type or not tally_source_type or not oracle_source_type:
                status = "Rejected - Source type is missing."
                break
                # File name
            upload_data_dict["file_name"] = orig_key[-1]
            LOGGER.info("L1: VALIDATING OF FILE EXTENSION")
            # Checking if the file format is correct
            # Calling validate_file_format() function from level1_validation
            # in common_module folder
            LOGGER.info("L1: VALIDATED OF FILE EXTENSION")
            if not validate_file_format(key):
                status = "Rejected - Invalid file extension"
                break
            splitdot = key[0:len(key) - 4]
            splitfolder = split_data(splitdot, "/")
            # Splitting the file name
            splitfile = split_data(splitfolder[-1], "@") if len(splitfolder) > 1 else [""]
            # Checking if the file name is correct or not
            if not (len(splitfile) >= 2 and splitfolder[0] == "incoming-file"):
                status = "Rejected - Invalid file name"
                break
            LOGGER.info("L1: VALIDATING FILE NAMING FORMAT")
            # Checking the file name is correct or not.
            # Calling validate_auto_manual_filenaming from level1_validation
            # in common _module folder
            validate_data = validate_auto_manual_filnaming(splitfile, oracle_source_type,\
                sap_source_type, tally_source_type, custom_source_type)
            LOGGER.info("L1: VALIDATED FILE NAMING FORMAT")
            # Checking if the file format is correct or not
            if not validate_data[0]:
                status = "Rejected - Invalid file name"
                break
            upload_data_dict["created_by"], upload_data_dict["load_type"] = ("Admin",\
                validate_data[1]) if validate_data[1] == "Automatic" else (splitfile[3],\
                validate_data[1])
            upload_data_dict["original_file_name"] = orig_key[-1]
            upload_data_dict["source_system"] = splitfile[1]
            upload_data_dict["data_type"] = splitfile[0]
            header_flag = False
            upper_data_type = upload_data_dict["data_type"].upper()
            upper_source_system = upload_data_dict["source_system"].upper()
            sap_source_type.extend(tally_source_type)
            if upper_data_type in ["DOCUMENT_DETAILS"] and upper_source_system in custom_source_type:
                header_flag, status= custom_validate_csv_header(download_location,\
                    config_dict["mapping"]["custom_config"], bucket, unique_name)

            elif upper_data_type == "REPOSITORY":
                upload_data_dict["s3_file_name"] = key
                upload_data_dict["category"] = upload_data_dict["data_type"]
                upload_data_dict["status"] = "Data successfully loaded"
                upload_data_dict["sbu"] = splitfile[-3]
                upload_data_dict["bu"] = splitfile[-4]
                upload_data_dict["location"] = splitfile[-5]
                upload_data_dict["company_name"] = splitfile[-2]
                upload_data_dict["folder_name"] = splitfile[-1]
                upload_data_dict["data_type"] = upload_data_dict["data_type"].title()
                upload_file_details_with_conn(data, upload_data_dict, None, None,\
                    conn_flag=True, data_base=database)
                return
            # Checking the source type
            elif upper_data_type in ["DOCUMENT_DETAILS", "BILL_OF_ENTRY"] and \
                    upper_source_system in sap_source_type:
                LOGGER.info("L1: VALIDATING SAP HEADER")
                # Checking for the header in sap format
                # Calling sap_validate_csv_header() function from sap_validation
                # in sap_module folder
                header_flag, status = sap_validate_csv_header(download_location,\
                    bucket, unique_name)
                LOGGER.info("L1: VALIDATED SAP HEADER ")
            elif upper_source_system in oracle_source_type:
                LOGGER.info("VALIDATING ORACLE HEADER")
                # Checking for the header in oracle format
                # Calling oracle_validate_csv_header() function
                # from oracle_validation in oracle_module folder
                header_flag, status = oracle_validate_csv_header(download_location,\
                    bucket, unique_name)
                LOGGER.info("VALIDATED ORACLE HEADER")
            elif upper_data_type in ["PARTB_DETAILS", "EWB_CHANGESHIP"] and \
                    upper_source_system in sap_source_type:
                # Checking for the header in partb format
                # Calling partb_validate_csv_header() function from partb_validation
                # in partb_module folder
                header_flag, status = partb_validate_csv_header(download_location,\
                    bucket, unique_name)
            elif upper_data_type in ["DELIVERY_DETAILS"]\
                    and upper_source_system in sap_source_type:
                # Checking for the header in grn format
                # Calling grn_validate_csv_header() function
                # from grn__validation
                # in grn_module folder
                header_flag, status = grn_validate_csv_header(download_location,\
                    bucket, unique_name)
            elif upper_data_type in ["PURCHASE_REGISTER"] and \
                    upper_source_system in sap_source_type:
                # Checking for the header in purchase_register format
                # Calling purchase_register_validate_csv_header() function
                # from purchase_register__validation
                # in purchase_register_module folder
                header_flag, status = purchase_register_validate_csv_header(download_location,\
                    bucket, unique_name)
            elif upper_data_type in ["GSTIN"]:
                # Checking for the header in purchase_register format
                # Calling purchase_register_validate_csv_header() function
                # from purchase_register__validation
                # in purchase_register_module folder
                header_flag, status = gstin_validate_csv_header(download_location,\
                    bucket, unique_name)

            # Checking the status of header flag
            if not header_flag:
                LOGGER.info("L1 - Header is not in valid format.")
                break

            if upper_data_type in ["DOCUMENT_DETAILS", 'BILL_OF_ENTRY'] and \
                upper_source_system in custom_source_type :
                LOGGER.info("L1:PARSING CUSTOM FORMAT")
                # Calling unique_validation from the same file
                # to parse the CUSTOM format
                flag_failure_process, status = unique_validation(bucket,\
                    upper_source_system, transform_dataframe, download_location, data, status,\
                    upload_data_dict["created_by"], upload_data_dict["load_type"],
                    config_dict["mapping"], master_config_dict)
                LOGGER.info("L1: PARSED CUSTOM FORMAT")
                if flag_failure_process:
                    flag_trigger_upload, status = sap_oracle_upload_insert(data, database,\
                        upload_data_dict, S3_OBJECT, key, download_location, status, l1_bucket, b_filename)
            elif upper_data_type in ["DOCUMENT_DETAILS", "BILL_OF_ENTRY"] and \
                    upper_source_system in sap_source_type:
                LOGGER.info("L1:PARSING SAP FORMAT")
                # Calling unique_validation from the same file
                # to parse the sap format
                flag_failure_process, status = unique_validation(bucket,\
                    upper_source_system, mapping_data, download_location, data, status,\
                    upload_data_dict["created_by"], upload_data_dict["load_type"],
                    config_dict["mapping"]["sap_config"], master_config_dict)
                LOGGER.info("L1: PARSED SAP FORMAT")
                if flag_failure_process:
                    flag_trigger_upload, status = sap_oracle_upload_insert(data, database,\
                        upload_data_dict, S3_OBJECT, key, download_location, status, l1_bucket, b_filename)

            elif upper_source_system in oracle_source_type:
                LOGGER.info("L1: PARSING ORACLE FORMAT")
                # Calling unique_validation from the same file
                # to parse the oracle format
                flag_failure_process, status = unique_validation(bucket,\
                    upper_source_system, oracle_ewb_format_mapping, download_location, data, status,\
                    upload_data_dict["created_by"], upload_data_dict["load_type"],\
                    config_dict["mapping"]["oracle_config"], master_config_dict)
                if flag_failure_process:
                    flag_trigger_upload, status = sap_oracle_upload_insert(data, database,\
                        upload_data_dict, S3_OBJECT, key, download_location, status,\
                        l1_bucket, b_filename)
                LOGGER.info("L1: PARSED ORACLE FORMAT")
            elif upper_data_type in ["PARTB_DETAILS", "EWB_CHANGESHIP"] and \
                    upper_source_system in sap_source_type:
                # Checking if the csv file is empty or not
                # Calling parb_mapping_data function() from parb_mapping.py
                # in partb_module folder
                flag_trigger_upload, status = partb_mapping_data(download_location,\
                    upload_data_dict["created_by"], data, upload_data_dict["source_system"],\
                    upload_data_dict["load_type"], upload_data_dict, l1_bucket, b_filename,\
                    config_dict["etl_json"], database)
            elif upper_data_type in ["DELIVERY_DETAILS"] and\
                    upper_source_system in sap_source_type:
                # Checking if the csv file is empty or not
                # Calling grn_mapping_data function()
                # from grn_mapping.py
                # in grn_module folder
                flag_trigger_upload, status, upload_data_dict["import_from_file"] = \
                    grn_mapping_data(download_location, data, upload_data_dict["created_by"],\
                        upload_data_dict, l1_bucket, b_filename, config_dict["etl_json"], database)
            elif upper_data_type in ["PURCHASE_REGISTER"] and \
                    upper_source_system in sap_source_type:
                # Checking if the csv file is empty or not
                # Calling purchase_register_mapping_data function()
                # from purchase_register_mapping.py
                # in purchase_register_module folder
                flag_trigger_upload, status, upload_data_dict["import_from_file"] = \
                    purchase_register_mapping_data(download_location, data,\
                        upload_data_dict["created_by"], upload_data_dict, l1_bucket,\
                        b_filename, database)
            elif upper_data_type in ["GSTIN"]:
                # Checking if the csv file is empty or not
                # Calling purchase_register_mapping_data function()
                # from purchase_register_mapping.py
                # in purchase_register_module folder
                flag_trigger_upload, status, upload_data_dict["import_from_file"] = \
                    gstin_mapping_data(download_location, data,\
                        upload_data_dict["created_by"], upload_data_dict, l1_bucket,\
                        b_filename, database)
            else:
                status = "Currently tally is not defined"
        LOGGER.info(f"L1: STATUS {status}")
        upload_data_dict["status"] = status
        #file_rejection_email
        success_status_list = ['Data successfully loaded', 'Data extracted from file and getting loaded']
        email_sqs_url = config_dict["etl_json"].get("email_sqs_url", "")
        if email_sqs_url and status not in success_status_list:
            customer_id = os.environ.get("customer_id", "")
            file_name = file_name = orig_key[-1]
            send_email_for_rejected_file(customer_id, bucket, file_name, status, load_id, email_sqs_url)
        # Inserting the details of l1 into dattabase
        # Calling upload_file_details() function from save_data.py
        # in common_module folder
        if flag_trigger_upload:
            LOGGER.info("L1: INSERTING DATA INTO UPLOAD TABLE")
            upload_file_details(data, database, upload_data_dict, b_filename, l1_bucket)
            LOGGER.info("L1: INSERTED DATA INTO UPLOAD TABLE")
        LOGGER.info("L1: SENDING EMAIL TO USER")
        LOGGER.info("L1: SENT EMAIL TO USER")
    except Exception as error:
        LOGGER.info(f"L1:EXCEPTION OCCURED {error}", exc_info=True)
