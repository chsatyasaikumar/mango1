'''
# common function
'''
import os
import re
import logging
import traceback
import boto3
import base64
from base64 import b64decode
from botocore.exceptions import ClientError
import redis
import json
import yaml
from retry import retry
import requests
import pandas as pd
from Crypto.Cipher import AES

QUEUE_CLIENT = boto3.client('sqs', region_name='ap-south-1')
LOGGER = logging.getLogger('EWB-L1')

def csv_injection_handling(headers, dframe):
    '''
    Summery line
        Here we are handling the csv injection data
    Parameters:
        headers(list): column names
        dframe(df): pandas dframe
    '''
    dframe = dframe.fillna("")
    dframe = dframe.applymap(str)
    for col in headers:
        try:
            dframe[col] = dframe[col].apply(lambda x : f"'{x}'" if \
                x.startswith("+") or x.startswith("@") or x.startswith("=") else x)
        except Exception as error:
            print("Getting exception in csv-injection verification and exception "\
                f"is {error}")
    return dframe

@retry((Exception,), tries=2, delay=10)
def get_config_dict(s3_object):
    '''
        Getting etl.json config data for processing
        PARAM - s3_object: boto3 s3 client object
    '''
    config_dict = {}
    customer_id = os.environ.get("customer_id", "")
    try:
    # getting env data from lambda
        bucket_name = os.environ.get("config_bucket", "")
        file_path = os.environ.get("etl_config_file_path", "")
        # checking env data is exist or not
        if bucket_name and file_path and customer_id:
            # customer_config_file_name
            config_file_name = customer_id + "_etl_ewb_config.json"
            # full path of customer_config_file
            full_path = "{0}/".format(file_path) + config_file_name
            # Where download configfile path
            local_path = "/tmp/" + config_file_name
            # downloading the file and converting to json
            print("L1: Start reading {0} config file from s3 bucket from path {1}".format(\
                config_file_name, full_path))
            # s3_clientobj = s3_object.get_object(Bucket=bucket_name, Key=full_path)
            # s3_clientdata = s3_clientobj['Body'].read().decode('utf-8')
            # s3_clientdata = FileEncryption.decrypt_message(s3_clientdata)
            pass_data = {}
            ReadYmlConfig.common_s3_read(bucket_name, full_path, pass_data)
            s3_clientdata = pass_data.get("s3_data")
            config_dict = json.loads(s3_clientdata)
            if not config_dict:
                print("L1: Error - {0} file is missing.".format(config_file_name))
            # else:
            #     print("L1: {0} config file data is from s3 bucket is -> {1}".format(\
            #         config_file_name, config_dict))
        else:
            print("Error:- Env confiuration is missing.")
    except Exception as error:
        print("L2: configuration is not found in s3 bucket now trying to set configuration cache")
        token = os.environ.get("token", "")
        url = os.environ.get("pull_api_url", "")
        if token and url:
            print(f"L2: Pull API url is {url} and token is {token}")
            header = {"Content-Type": "application/json",\
                "token": token,\
                "customerid": customer_id,\
            }
            body = { \
                "case":"100", \
                "module":"ewb", \
                "param":[ \
                    { \
                        "key":"", \
                        "action":"set", \
                    }, \
                ], \
            }
            call = False
            try:
                resp = requests.post(url, headers=header, data=json.dumps(body))
                print(f"L1: Pull API response status code is {resp.status_code} and content is " \
                    f"{resp.content}")
                call = True
            except Exception:
                traceback.print_exc()
            if call:
                raise Exception(error)
        else:
            print("L2: token/Pull API url is missing")
            traceback.print_exc()
    return config_dict

def get_config_dict_from_cache():
    # pylint: disable-msg=W0703
    '''
    Here we are get cache from redis cache
    '''
    config_dict = {}
    redis_url = os.environ.get("spring.redis.host", "")
    redis_port = os.environ.get("spring.redis.port", "6379")
    if os.environ.get("redis_flag", "").strip().lower() == "true":
        customer_id = os.environ.get("customer_id", "")
        if not customer_id:
            print("L1 Error - customer_id is missing in env")
            return config_dict
        if not redis_url:
            print("L1 Error - redis_url is missing in env")
            return config_dict
        try:
            key = customer_id + "_etl_ewb_config"
            print("L1: Making connection with redis cache")
            client = redis.Redis(host=redis_url, port=redis_port, db=0, ssl=True)
            print("redis connectivity is:",client.ping())
            print("L1: Reading {0} key data from Redis Cache".format(key))
            redis_data = client.get(key)
            if redis_data:
                config_dict = json.loads(redis_data)
                # print("L1: {0} key data from redis cache -> {1}".format(key, config_dict))
            else:
                print("L1 - Error - " + key + " key does not exist in redis")
        except Exception as error:
            print("L1 Exception - redis")
            print(error)
    if not config_dict:
        s3_object = boto3.client('s3')
        config_dict = get_config_dict(s3_object)
    return config_dict


def get_master_config_dict_from_cache():
    # pylint: disable-msg=W0703
    '''
    Here we are get cache from redis cache
    '''
    master_config_dict = {}
    redis_url = os.environ.get("spring.redis.host", "")
    redis_port = os.environ.get("spring.redis.port", "6379")
    if os.environ.get("redis_flag", "").strip().lower() == "true":
        customer_id = os.environ.get("customer_id", "")
        if not customer_id:
            print("L1 Error - customer_id is missing in env")
            return master_config_dict
        if not redis_url:
            print("L1 Error - redis_url is missing in env")
            return master_config_dict
        try:
            key = customer_id + "_etl_master_config"
            print("L1: Start making connection from redis cache")
            client = redis.Redis(host=redis_url, port=redis_port, db=0, ssl=True)
            print("L1: redis connectivity is:",client.ping())
            print("L1: Reading {0} key data from redis cache".format(key))
            redis_data = client.get(key)
            if redis_data:
                master_config_dict = json.loads(redis_data)
                # print("L1: {0} key data from redis cache is -> {1}".format(key, master_config_dict))
            else:
                print("L1 - Error - " + key + " key is not exist in redis")
        except Exception as error:
            print("L1 Exception - redis")
            print(error)
    if not master_config_dict:
        s3_object = boto3.client('s3')
        master_config_dict = get_master_config_dict(s3_object)
    return master_config_dict


def get_gstin_status_config_dict_from_cache():
    # pylint: disable-msg=W0703
    '''
    Here we are get cache from redis cache
    '''
    gstin_status_config_dict = {}
    redis_url = os.environ.get("spring.redis.host", "")
    redis_port = os.environ.get("spring.redis.port", "6379")
    if os.environ.get("redis_flag", "").strip().lower() == "true":
        customer_id = os.environ.get("customer_id", "")
        if not customer_id:
            print("L1 Error - customer_id is missing in env")
            return gstin_status_config_dict
        if not redis_url:
            print("L1 Error - redis_url is missing in env")
            return gstin_status_config_dict
        try:
            key = customer_id + "_etl_gstin_status"
            print("L1: Making connection with redis cache")
            client = redis.Redis(host=redis_url, port=redis_port, db=0, ssl=True)
            print("L1: Redis connectivity is:",client.ping())
            print("L1: Start reading {0} key data from redis cache".format(key))
            redis_data = client.get(key)
            if redis_data:
                gstin_status_config_dict = json.loads(redis_data)
                # print("L1: {0} key data from redis cache is -> {1}".format(key, gstin_status_config_dict))
            else:
                print("L1 - Error - " + key + " key is not exist in redis")
        except Exception as error:
            print("L1 Exception - redis")
            print(error)
    if not gstin_status_config_dict:
        s3_object = boto3.client('s3')
        gstin_status_config_dict = get_gstin_status_config_dict(s3_object)
    return gstin_status_config_dict
    
def get_gstin_status_config_dict(s3_object):
    '''
        Getting etl.json config data for processing
        PARAM - s3_object: boto3 s3 client object
    '''
    # getting env data from lambda
    bucket_name = os.environ.get("config_bucket", "")
    file_path = os.environ.get("etl_config_file_path", "")
    customer_id = os.environ.get("customer_id", "")
    gstin_status_config_dict = {}
    # checking env data is exist or not
    if bucket_name and file_path and customer_id:
        # customer_config_file_name
        config_file_name = customer_id + "_etl_gstin_status.json"
        # full path of customer_config_file
        full_path = "{0}/".format(file_path) + config_file_name
        print("ETL Config File path -> {0}".format(full_path))
        # Where download configfile path
        local_path = "/tmp/" + config_file_name
        # downloading the file and converting to json
        print("L1: Reading {0} config file from path -> {1}".format(config_file_name, full_path))
        gstin_status_config_dict = read_config_file_from_bucket(bucket_name, s3_object, local_path, full_path)
        if not gstin_status_config_dict:
            print("L1: Error - {0} file is empty".format(config_file_name))
        # else:
        #     print("L1: {0} config file data from S3 bucket is -> {1}".format(config_file_name, gstin_status_config_dict))
    else:
        print("Error:- Env confiuration is missing.")
    return gstin_status_config_dict

def get_master_config_dict(s3_object):
    '''
        Getting etl.json config data for processing
        PARAM - s3_object: boto3 s3 client object
    '''
    # getting env data from lambda
    bucket_name = os.environ.get("config_bucket", "")
    file_path = os.environ.get("etl_config_file_path", "")
    customer_id = os.environ.get("customer_id", "")
    master_config_dict = {}
    # checking env data is exist or not
    if bucket_name and file_path and customer_id:
        # customer_config_file_name
        config_file_name = customer_id + "_etl_master_config.json"
        # full path of customer_config_file
        full_path = "{0}/".format(file_path) + config_file_name
        # Where download configfile path
        local_path = "/tmp/" + config_file_name
        # downloading the file and converting to json
        print("L1: Start reading {0} config file from path -> {1}".format(config_file_name, full_path))
        master_config_dict = read_config_file_from_bucket(bucket_name, s3_object, local_path, full_path)
        if not master_config_dict:
            print("L1: Error - {0} file is missing.".format(config_file_name))
        # else:
        #     print("L1: {1} config file data from S3 is -> {1}".format(config_file_name, master_config_dict))
    else:
        print("Error:- Env confiuration is missing.")
    return master_config_dict


def is_exist_key(key, config_dict):
    '''
        Checking key is exist or not in dictionary
        PARAM - key: a string/int
        PARAM - config_dict - a dictionary
    '''
    return bool(key in config_dict)

def get_database(config_dict):
    '''
        getting database configuration from config_dict
        PARAM - config_dict: a dictionary
    '''
    # database key names list
    database_list = ["database_name", "host", "port", "user", "password"]
    # checking database keys exist or not in config_dict
    flag = all(is_exist_key(key, config_dict['database']) for key in database_list)
    database = {}
    if flag:
        # creating database dictionary
        for key in database_list:
            database[key] = config_dict['database'][key]
    print("CUSTOMER DB DETAILS:")
    print(database)
    return database

def get_common_dict(s3_object):
    '''
        Getting pincode and hsn configuration
        PARAM - s3_object: boto3 s3 client object
    '''
    bucket_name = os.environ.get("config_bucket", "")
    file_path = os.environ.get("etl_config_file_path", "")
    common_dict = {}
    # checking env data is exist or not
    if bucket_name and file_path:
        # creating key for etl.json
        full_path = "{0}/{1}".format(file_path, ETL_COMMON_CONFIG_FILE)
        # Where download configfile path
        local_path = "/tmp/" + ETL_COMMON_CONFIG_FILE
        # downloading the file and converting to json
        common_dict = read_config_file_from_bucket(bucket_name, s3_object, local_path, full_path)
        if not common_dict:
            print("L2: Error - ETL COMMON CONFIG JSON file is missing.")
    else:
        print("Error:- Env confiuration is missing.")
    return common_dict

def is_key_exist(s3_object, key, bill_of_entry_bucket):
    # pylint: disable-msg=W0703
    '''
        checking s3 key is exist or not in bill-of-entry bucket
        PARAM - s3_object: s3 boto3 client object
        PARAM - key: s3 object key
        PARAM - bill_of_entry_bucket: bill-of-entry bucket name
    '''
    flag = False
    try:
        s3_object.head_object(Bucket=bill_of_entry_bucket, Key=key)
        flag = True
    except Exception as error:
        pass
    return flag

def validate_expression(expression, data):
    '''
     Input  -
        params: expression - The regex for data to be checked for the pattern matching
        params: data - The data that needs to be checked for its corresponding regex
     Output - The status of regex pattern matching
    '''
    regex = re.compile(expression)
    return bool(regex.match(data))

def error_upload_file(l1_bucket, b_filename, original_file_name):
    # pylint: disable-msg=W0703
    '''
        copy error file from backup to Error folder
        Input -
            params: l1_bucket: L1 bucket Name
            params: b_filename: Backup file path
            params: original_file_name: original file name
    '''
    # creating s3 resource
    s3_resource = boto3.resource('s3')
    copy_source = {"Bucket" : l1_bucket, "Key": b_filename}
    try:
        # copying file from backup to Error
        s3_resource.meta.client.copy(copy_source, l1_bucket, "error/" + original_file_name)
    except Exception as error:
        print("L1:EXCEPTION OCCURED L1 bakup to incoming-file moving failed.")
        print("L1: EXCEPTION OCCURED ", error)

def send_sqs(sqs_message, sqs_url):
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
        print(f'sqs client -> {str(QUEUE_CLIENT)}')
        print(f'sqs message -> {json.dumps(sqs_message)}')
        response = QUEUE_CLIENT.send_message(\
            QueueUrl=sqs_url,\
            MessageBody=json.dumps(sqs_message))
        print("Message Send in Queue")
        print(response)
    except Exception as error:
        traceback.print_exc()

class ReadYmlConfig:
    '''
    Summery Line.
        Reading Yml File
    '''
    def __str__(self):
        '''
        Summery Line.
            object representation
        '''
        return "ReadYmlConfig object"

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
    def read_yml_s3(f_path):
        '''
        Summery Line.
            reading properties file from s3 bucket
        Parameters:
            f_path: file path
        Return:
            properties(dict): Properties configuration
        '''
        proptes = None
        # s3_object = boto3.client('s3')
        bucket_name = os.environ.get("config_bucket", "")
        LOGGER.info(f"config_bucket is > {bucket_name}")
        if bucket_name:
            # s3_clientobj = s3_object.get_object(Bucket=bucket_name, Key=f_path)
            # s3_clientdata = s3_clientobj['Body'].read().decode('utf-8')
            # s3_clientdata = FileEncryption.decrypt_application(s3_clientdata)
            pass_data = {}
            ReadYmlConfig.common_s3_read(bucket_name, f_path, pass_data)
            s3_clientdata = pass_data.get("s3_data")
            proptes = yaml.safe_load(s3_clientdata)
        else:
            LOGGER.info("config_bucket is missing.....")
        return proptes


def read_config_file_from_bucket(bucket, s3_object, temp_path, default_config_path):
    # pylint: disable-msg=W0703
    '''
    Input  -
       params: bucket - The s3 bucket
       params: s3_object - s3 object to connect with boto3
       param: temp_path - The file path
       param: default_config_path - The configuration file path
    Output -  The config file is read from s3 bucket
    '''
    file_dict = {}
    try:
        # s3_clientobj = s3_object.get_object(Bucket=bucket, Key=default_config_path)
        # s3_clientdata = s3_clientobj['Body'].read().decode('utf-8')
        # s3_clientdata = FileEncryption.decrypt_message(s3_clientdata)
        pass_data = {}
        ReadYmlConfig.common_s3_read(bucket, default_config_path, pass_data)
        s3_clientdata = pass_data.get("s3_data")
        file_dict = json.loads(s3_clientdata)
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", str(error))
    return file_dict

class ReadYml:
    '''
    Summery Line.
        Here we are reading yml file
    '''
    def __str__(self):
        '''
        Summery Line.
            object representation
        '''
        return "ReadYml object"

    @staticmethod
    def read_yml(f_path):
        '''
        Summery Line.
            Here we are reading yml file from directory
        Parameters:
            f_path: file path
        Return:
            properties(dict): Properties configuration
        '''
        proptes = {}
        with open(f_path) as pfile:
            readlines = pfile.readlines()
            text = "".join(readlines)
            decrypt_text = FileEncryption.decrypt_application(text)
            proptes = yaml.safe_load(decrypt_text)
        return proptes

class Properties:
    '''
    Summery Line.
        here we are set environemnt for properties data
    '''    
    def __str__(self):
        '''
        Summery Line.
            Properties object representation
        '''

        return "Properties Object"

    @staticmethod
    def set(serverless=False):
        '''
        Summery Line.
            reading properties files and set to environemnt
        Parameters:
            serverless(bool): severless variable identify where from
                this function is called (if serverless=True means serverless)
                otherwise server
        Return:
            setting the properties to environment.
            Returning None
        '''
        flag = False
        try:
            path = os.environ.get('properties_path', '')
            if path:
                f_name = 'application.yml'
                f_path = f"{path}{f_name}"
                # reading properties path
                proptes = {}
                if not serverless:
                    # redading yml file for server
                    proptes = ReadYml.read_yml(f_path)
                else:
                    # reading yml file for serverless
                    proptes = ReadYmlConfig.read_yml_s3(f_path)
                if proptes:
                    # SET REDIS CREDENTIAL
                    os.environ['spring.redis.host'] = proptes.get('spring.redis.host', '')
                    os.environ['spring.redis.port'] = str(proptes.get('spring.redis.port', ''))
                    os.environ['spring.redis.password'] = proptes.get('spring.redis.password', '')
                    # PULL API URL
                    os.environ['pull_api_url'] = proptes.get('pull_api_url', '')
                    os.environ["FILE_PUBLIC_KEY"] = proptes.get("FILE_PUBLIC_KEY", "")
                    os.environ["FILE_PRIVATE_KEY"] = proptes.get("FILE_PRIVATE_KEY", "")
                    flag = True
                else:
                    LOGGER.error("Properties Configuration is missing")
            else:
                LOGGER.error("Properties file path is missing from environment variable")
        except Exception as error:
            LOGGER.error("EXCEPTION OCCURED on properties reading %s", str(error), exc_info=True)
        return flag

class SecretKeyReader:
    '''
    Read the configurations from secret key manager
    for aws environment
    '''
    @staticmethod
    def get_secret_value(secretkey):
        '''
        Read data from secret manager
        '''
        client = boto3.client('secretsmanager')
        data = None
        if secretkey:
            try:
                # kwargs = {'SecretId': secretKey}
                response = client.get_secret_value(SecretId=secretkey)
                data = json.loads(response["SecretString"])
            except Exception as error:
                LOGGER.error(str(error), exc_info=True)
        else:
            LOGGER.error("Secret Key is not found in application yml")
        return data


class FileEncryption:
    """
    File Encryption and Decryption Methods
    """
    @staticmethod
    def get_private_key():
        '''
        Summary Line
            Get private key from aws secret manager
        Params:
            None
        Returns:
            None
        '''
        prikey = SecretKeyReader.get_secret_value(os.environ.get("FILE_PRIVATE_KEY", ""))["key"]
        return prikey

    @staticmethod
    def get_application_key():
        '''
        Summary Line
            Get private key from aws secret manager
        Params:
            None
        Returns:
            None
        '''
        prikey = SecretKeyReader.get_secret_value(os.environ.get("FILE_APP_KEY", ""))["key"]
        return prikey

    @staticmethod
    def get_public_key():
        '''
        Summary Line
            Get Public key from aws secret manager
        Params:
            None
        Returns:
            None
        '''
        pubkey = SecretKeyReader.get_secret_value(os.environ.get("FILE_PUBLIC_KEY", ""))["key"]
        return pubkey

    @staticmethod
    def encrypt_message(raw):
        '''
        Summery line.
            Here we are encrypting data
        Parameters:
            raw(str)
        Return:
            encrypted data
        '''
        encoded_encrypted_msg = None
        try:
            bs = 16
            pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
            private_key = FileEncryption.get_private_key()
            key = base64.b64decode(private_key.encode('utf-8'))
            raw = pad(raw).encode("utf-8")
            cipher = AES.new(key, AES.MODE_ECB)
            encoded_encrypted_msg = base64.b64encode(cipher.encrypt(raw)).decode()
        except Exception as error:
            LOGGER.error(f"Exception in Encrypting data -> {error}", exc_info=True)
        return encoded_encrypted_msg

    @staticmethod
    def decrypt_message(enc):
        '''
        Summery line.
            Here we are encrypting data
        Parameters:
            raw(str)
        Return:
            encrypted data
        '''
        decrypted_string = None
        try:
            bs = 16
            unpad = lambda s: s[0:-ord(s[-1:])]
            private_key = FileEncryption.get_private_key()
            key = base64.b64decode(private_key.encode('utf-8'))
            enc = base64.b64decode(enc)
            cipher = AES.new(key, AES.MODE_ECB)
            decrypted_string = cipher.decrypt(enc)
            decrypted_string = unpad(decrypted_string)
        except Exception as error:
            LOGGER.error(f"Exception in Decrypting data -> {error}", exc_info=True)
        return decrypted_string

    @staticmethod
    def decrypt_application(enc):
        '''
        Summery line.
            Here we are encrypting data
        Parameters:
            raw(str)
        Return:
            encrypted data
        '''
        decrypted_string = None
        try:
            bs = 16
            unpad = lambda s: s[0:-ord(s[-1:])]
            private_key = FileEncryption.get_application_key()
            key = base64.b64decode(private_key.encode('utf-8'))
            enc = base64.b64decode(enc)
            cipher = AES.new(key, AES.MODE_ECB)
            decrypted_string = cipher.decrypt(enc)
            decrypted_string = unpad(decrypted_string)
        except Exception as error:
            LOGGER.error(f"Exception in Decrypting data -> {error}", exc_info=True)
        return decrypted_string
