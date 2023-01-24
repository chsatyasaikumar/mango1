'''
#This file has database and bucket configurations
'''
import datetime

INDIAN_CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
DB_CONFIG_FILENAME = "database_config.json"
BUCKET_CONFIG_FILENAME = "bucket_config.json"
UPLOAD_DATA_DICT_DATA = {"source_system": "", "category": "", "data_type": "", "company_id": 1,\
    "company_name": "", "state": "", "file_name": "", "load_type": "", "mapping": "",\
    "status": "Pending", "import_from_file": 0, "failed_quality": 0,\
    "updated_date": INDIAN_CURRENT_DATE, "created_date": INDIAN_CURRENT_DATE, "updated_by": "",\
    "created_by": "", "active": "Y", "comments": "", "original_file_name": "",\
    "s3_file_name": "", "bu": "", "sbu": "", "location": "", "folder_name": ""}

UP_INSERT_QUERY = ("INSERT INTO demo.upload(id, load_id, source_system, category, data_type, "\
    "company_id, company_name, state, file_name, load_type, mapping, status, "\
    "import_from_file, failed_quality, created_date, created_by, updated_date, updated_by, "\
    "active, comments, original_file_name, s3_file_name, bu, sbu, location, folder_name) "\
    "VALUES(%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "\
    "%s, %s, %s, %s, %s, %s, %s)")

UP_D_INSERT_QUERY = "INSERT INTO demo.upload(id, load_id, source_system, category, data_type, "\
    "company_id, company_name, state, file_name, load_type, mapping, status, "\
    "import_from_file, failed_quality, created_date, created_by, updated_date, updated_by, "\
    "active, comments, original_file_name, s3_file_name, bu, sbu, location, folder_name) "\
    "VALUES(%(id)s, %(load_id)s, %(source_system)s, %(category)s, %(data_type)s, "\
    "%(company_id)s, %(company_name)s, %(state)s, %(file_name)s, %(load_type)s, %(mapping)s, "\
    "%(status)s, %(import_from_file)s, %(failed_quality)s, %(created_date)s, %(created_by)s, "\
    "%(updated_date)s, %(updated_by)s, %(active)s, %(comments)s, %(original_file_name)s, "\
    "%(s3_file_name)s, %(bu)s, %(sbu)s, %(location)s, %(folder_name)s)"
# GSTIN REGEX WITH URP
GSTIN_REGEX_WITH_URP = r"^([0-9]{2}[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}" \
    r"[1-9A-Za-z]{1}[Zz1-9A-Ja-j]{1}[0-9a-zA-Z]{1}|[Uu][rR][pP]|[0-9]{2}[0-9|A-Z]{13})$"
# DOCUMENT NUMBER REGULAR EXPRESSION
DOC_NO_REGEX = r"^[a-zA-Z0-9\-\/]{1,16}$"
# GSTIN REGEX
GSTIN_REGEX = r"^([0-9]{2}[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}[1-9A-Za-z]{1}" \
    r"[Zz1-9A-Ja-j]{1}[0-9a-zA-Z]{1})$"
# Year Regex
YEAR_REGEX = r"^([0-9]{4})$"
# Month Regex
MONTH_REGEX = r"^([0-9]{2})$"
# HSN REGEX
HSN_REGEX = r"^([0-9]{1,8})$"
# GST REGEX
GST_RATE_REGEX = r"^-?[0-9]{1,4}(\.\d{0,3})?$"
# TAXABLE VALUE REGEX
TAXABLE_VALUE_VAL_REGEX = r"^-?[0-9]\d{0,13}(\.\d{0,10})?$"
# CGST RATE REGEX
CGST_AMOUNT_REGEX = r"^-?[0-9]\d{0,13}(\.\d{0,10})?$"

#mapping state acc to statecode
STATE_CODE_CONFIG = {"99": "OTHER COUNTRIES", "01": "JAMMU AND KASHMIR", "02": "HIMACHAL PRADESH",\
        "03": "PUNJAB", "04": "CHANDIGARH", "05": "UTTARAKHAND", "06": "HARYANA", "07": "DELHI",\
        "08": "RAJASTHAN", "09": "UTTAR PRADESH", "10": "BIHAR", "11": "SIKKIM",\
        "12": "ARUNACHAL PRADESH", "13": "NAGALAND", "14": "MANIPUR", "15": "MIZORAM",\
        "16": "TRIPURA", "17": "MEGHALAYA", "18": "ASSAM", "19": "WEST BENGAL", "20": "JHARKHAND",\
        "21": "ODISHA", "22": "CHHATTISGARH", "23": "MADHYA PRADESH", "24": "GUJARAT",\
        "25": "DAMAN AND DIU", "26": "DADAR AND NAGAR HAVELI", "27": "MAHARASHTRA",\
        "29": "KARNATAKA", "30": "GOA", "31": "LAKSHADWEEP", "32": "KERALA", "33": "TAMIL NADU",\
        "34": "PUDUCHERRY", "35": "ANDAMAN AND NICOBAR", "36": "TELANGANA", "37": "ANDHRA PRADESH",\
        "38": "LADAKH", "97": "OTHER TERRITORY"
        }