'''
Lambda event
'''
import logging
from irn_ewb.module.util.mis_function import S3Read
from irn_ewb.module.ewb.ewb_parse import EwbParse, upload_csv

LOGGER = logging.getLogger('irn-ewb-process')
LOGGER.setLevel(logging.INFO)

class IrnEwbProcess:
    '''
    '''
    def transform(bucket_name, f_path, config_dict):
        '''
        Summery Line.
            here we processing irn payload for ewb process and creating
            csv file and uploading to EWB ETL L1 bucket
        Parameters:
            event(dict): contain event structure
                bucket_name(str): bucket name
                json_file_name(str): json file path
                customer_id(str): customer id
                load_id(int): irn load id
                email_ids(str): email id
        Return:
            return None
        '''
        filename = ""
        flag = False
        try:
            LOGGER.info(f"File name is {f_path}")
            ewb_list = []
            ewb_data = S3Read.read_file_from_bucket(bucket_name,\
                f_path)
            csv_format = ewb_data.get('csv_format')
            payload_list = ewb_data.get('ewb_list')
            if payload_list:
                for payload in payload_list:
                    EwbParse.ewb_json_csv_parse(payload, ewb_list, config_dict)

                if ewb_list:
                    flag, filename = upload_csv(ewb_list, bucket_name, csv_format)
            else:
                LOGGER.error("payload is missing")
        except Exception as error:
            LOGGER.error(f"Exception {error}", exc_info=True)

        return flag, filename
