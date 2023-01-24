'''
#Reading the configuration file
'''
from __future__ import print_function
import os
import logging
import json
import yaml
import boto3

LOGGER = logging.getLogger('EWB-L1')

#Called from lambda_function.py
#Reading the config file from s3 bucket
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
        s3_object.download_file(bucket, default_config_path, temp_path)
        with open(temp_path, "r") as data:
            file_dict = json.load(data)
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", str(error))
    return file_dict
