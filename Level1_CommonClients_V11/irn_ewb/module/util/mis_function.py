# pylint: disable-msg=W1202
# pylint: disable-msg=W0703
# pylint: disable-msg=W0613
'''
function
'''
# Builtin imports
import datetime
import logging
import json
import boto3
LOGGER = logging.getLogger("irn-ewb-process")

def parse_date(data, s_dt_frmt, t_dt_frmt):
    # pylint: disable-msg=W0703
    '''
    Summery Line.
        Here we are converting date format to new date format for table.
    Parameters:
        data(str): date string
        s_dt_frmt(str): source date format
        t_dt_frmt(str): target date format
    Return:
        data(str)
    '''

    try:
        data = datetime.datetime.strptime(data, s_dt_frmt).strftime(t_dt_frmt)
    except Exception as error:
        LOGGER.warning(str(error))
    return data

class S3Read:
    '''
    Summery Line.
        All s3 related work are here
    '''
    def __str__(self):
        '''
        Summery Line.
            S3Read object Representation
        '''
        return "S3Read object"

    @staticmethod
    def common_s3_read(bucket_name, default_config_path, pass_data):
        '''
        Summery Line
            Here we are reading the configuration and file data from s3 bucket
        Parameters:

        '''
        s3_object = boto3.client('s3')
        s3_clientobj = s3_object.get_object(Bucket=bucket_name, Key=default_config_path)
        s3_clientdata = s3_clientobj['Body'].read().decode('utf-8')
        pass_data["s3_data"] = s3_clientdata

    @staticmethod
    def read_file_from_bucket(bucket_name, f_path):
        # pylint: disable-msg=W0703
        # pylint: disable-msg=W0613
        '''
        Summery Line.
            #Reading the json file from s3 bucket
        Parameters:
            bucket_name(str): The s3 bucket
            f_path(str): The json file path
        Return:
            payload_list(list): The json file is read from s3 bucket
        '''
        payload_list = []
        try:
            LOGGER.info("EWB JSON file reading Start")
            s3_object = boto3.client('s3')
            # s3_clientobj = s3_object.get_object(Bucket=bucket_name, Key=f_path)
            # s3_clientdata = s3_clientobj['Body'].read().decode('utf-8')
            pass_data = {}
            S3Read.common_s3_read(bucket_name, f_path, pass_data)
            s3_clientdata = pass_data.get("s3_data")
            LOGGER.info("EWB JSON file deleting start from s3 bucket")
            s3_object.delete_object(Bucket=bucket_name, Key=f_path)
            LOGGER.info("EWB JSON file deleting END from s3 bucket")
            s3_resource = boto3.resource('s3')
            file_name = "irn-ewb-process-backup/" + f_path.split('/')[1]
            LOGGER.info("EWB JSON file moving start to backup")
            s3_resource.Object(bucket_name, file_name).put(Body=s3_clientdata)
            LOGGER.info("EWB JSON file moving end to backup")
            payload_list = json.loads(s3_clientdata)
            LOGGER.info("EWB JSON file reading End")
        except Exception as error:
            LOGGER.error(f"EWB JSON file reading Exception {error}", exc_info=True)
        return payload_list
