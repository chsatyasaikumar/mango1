'''
#Validating the columns in purchase_register module
'''
from __future__ import print_function
import datetime
import traceback
import pandas as pd
from comman_module.db_config import make_connection, get_dict_cursor, exist_cur_conn_closed,\
                        exist_conn_closed
from comman_module.save_data import upload_file_details_with_conn
from comman_module.function import validate_expression, error_upload_file
from comman_module.configuration import GSTIN_REGEX, YEAR_REGEX, MONTH_REGEX, DOC_NO_REGEX,\
                        HSN_REGEX, GST_RATE_REGEX, TAXABLE_VALUE_VAL_REGEX,\
                        CGST_AMOUNT_REGEX
from .purchase_register_configuration import DOCUMENT_TYPE_DEFAULT,\
    grn_validate_date, RENEAME_COL_DICT
from .purchase_register_query import INSERT_QUERY

#Helper function
#Truncating the length of the data if it exceeds the size
def truncate(data, length):
    '''
    Input  -
       params: data - The data whose length is to be truncated
       params: length - The length to be truncated
    Output - The data with the truncated length
    '''
    return data if len(data) <= length else data[:length]

def truncate_int(data, length):
    # pylint: disable-msg=W0703
    '''
    truncating int data
    Input -
        params: data - string value
        params: length - length for truncating
    Output - Returning truncate data
    '''
    try:
        int(data)
        # Truncating the length of data
        data = truncate(data, length)
    except Exception as error:
        data = 0
    return data

def clean_number(data):
    '''
    cleaning numeric data
    Input -
        params: data - removing , space and replacing - empty to 0
    Output - Return Clean data
    '''
    data = data.replace(",", "")
    data = data.replace(" ", "")
    data = "0" if data == "-" else data
    data = "0" if not data else data
    return data

def rowvalidation(row):
    # pylint: disable-msg=R0912
    '''
    Iteration on pandas df
    Input -
        params: row: dict of file row
    Output - Returning Pandas series
    '''
    validation_remark = ''
    #Validating user_gstin
    # Checking if the user_gstin matches the corresponding regex.
    if not validate_expression(GSTIN_REGEX, row["user_gstin"]):
        validation_remark = "Full length of gstin"
        row["user_gstin"] = truncate(row["user_gstin"], 512)
    # Truncating the length of user_gstin
    row["user_gstin"] = row["user_gstin"].upper()
        #Validating Year
        # Checking if the year matches the corresponding regex.
    if not validate_expression(YEAR_REGEX, row["year"]):
        validation_remark = validation_remark + "Full length of Year"
        row["year"] = truncate_int(row["year"], 4)
    #Validating month
    # Checking if the month matches the corresponding regex.
    if not validate_expression(MONTH_REGEX, row["month"]):
        validation_remark = validation_remark + "Full length of Month"
        row["month"] = truncate_int(row["month"], 2)

    #Validating document_type
    row["document_type"] = row["document_type"].upper()
    #Checking if the document_type is present in one of its allowed values
    if row["document_type"] not in DOCUMENT_TYPE_DEFAULT:
        validation_remark = validation_remark + "Full length of document_type"
        # Truncating the length of document_type
        row["document_type"] = truncate(row["document_type"], 100)

    #Validating document_number
    # Checking if the document_number matches the corresponding regex.
    if not validate_expression(DOC_NO_REGEX, row["document_no"]):
        validation_remark = validation_remark + "Full length of document"
        # Truncating the length of document_number
        row["document_no"] = truncate(row["document_no"], 16)
    row["document_no"] = row["document_no"].upper()

    #Validating HSN
    # Checking if the hsn matches the corresponding regex.
    if not validate_expression(HSN_REGEX, row["hsn"]):
        validation_remark = validation_remark + "Full length of HSN"
        # Truncating the length of hsn
        row["hsn"] = truncate(row["hsn"], 8)
    #Validating Document Date
    row["document_date"] = grn_validate_date(
        row["document_date"], "%d/%m/%Y", "%Y-%m-%d")
    if not row["document_date"]:
        validation_remark = validation_remark + "Document date is invalid/blank<br>"

    #Validating Product or Service Description
    product_service_description_regex = r"^([a-zA-Z0-9\.]{1,100})$"
    # Checking if the product_service-description matches the corresponding regex.
    if not validate_expression(product_service_description_regex,\
        row["product_service_description"]):
        validation_remark = validation_remark + "Full length of product_service_description"
        # Truncating the length of product_service_description
        row["product_service_description"] = truncate(row["product_service_description"], 100)

    # Truncating the length of name_of_supplier
    row["name_of_supplier"] = truncate(row["name_of_supplier"], 512)

    # Truncating the length of gstin_of_supplier
    row["gstin_of_supplier"] = truncate(row["gstin_of_supplier"], 512)
    row["gstin_of_supplier"] = row["gstin_of_supplier"].upper()

    #Validating gst_rate
    row["gst_rate"] = clean_number(row["gst_rate"])
    # Checking if the gst_rate matches the corresponding regex.
    if not validate_expression(GST_RATE_REGEX, row["gst_rate"]):
        validation_remark = validation_remark + "\"GST Rate\" \"" + row[
            "gst_rate"] + "\" is invalid/missing<br>"
        row["gst_rate"] = "0"
    else:
        # Truncating the decimal_part of gst_rate
        row["gst_rate"] = format(float(row["gst_rate"]), '.2f')

    #Validating line_item
    line_item_regex = r"^[0-9]{0,6}$"
    #Checking if line_item field is null or not
    row["line_item"] = "0" if not row["line_item"] else row["line_item"]
    # Checking if the line_item matches the corresponding regex.
    if not validate_expression(line_item_regex, row["line_item"]):
        validation_remark = validation_remark + "\"Line item\" \"" +\
                            row["line_item"] + "\" is invalid<br>"
        row["line_item"] = "0"

    #Validating taxable_value
    row["taxable_value"] = clean_number(row["taxable_value"])
    # Checking if the taxable_value matches the corresponding regex.
    if not validate_expression(TAXABLE_VALUE_VAL_REGEX, row["taxable_value"]):
        validation_remark = validation_remark + "\"Taxable value\" \"" + \
                            row["taxable_value"] + "\" is invalid/missing<br>"
        row["taxable_value"] = "0"
    else:
        # Truncating the decimal_part of taxable_value
        row["taxable_value"] = format(float(row["taxable_value"]), '.2f')

    #Validating cgst amount
    #Removing the space and comma
    row["cgst_amount"] = clean_number(row["cgst_amount"])
    # Checking if the cgst_amount matches the corresponding regex.
    if not validate_expression(CGST_AMOUNT_REGEX, row["cgst_amount"]):
        validation_remark = validation_remark + "\"Cgst amount\" \"" + \
                            row["cgst_amount"] + "\" is invalid/missing<br>"
        row["cgst_amount"] = "0"
    # Truncating the decimal_part of cgst_amount
    else:
        row["cgst_amount"] = format(float(row["cgst_amount"]), '.2f')

    #Validating sgst amount
    # Removing the space and comma
    row["sgst_amount"] = clean_number(row["sgst_amount"])
    # Checking if the sgst_amount matches the corresponding regex.
    if not validate_expression(CGST_AMOUNT_REGEX, row["sgst_amount"]):
        validation_remark = validation_remark + "\"Sgst amount\" \"" + \
                            row["sgst_amount"] + "\" is invalid/missing<br>"
        row["sgst_amount"] = "0"
    # Truncating the decimal_part of sgst_amount
    else:
        row["sgst_amount"] = format(float(row["sgst_amount"]), '.2f')

    #Validating igst amount
    # Removing the space and comma
    row["igst_amount"] = clean_number(row["igst_amount"])
    # Checking if the igst_amount matches the corresponding regex.
    if not validate_expression(CGST_AMOUNT_REGEX, row["igst_amount"]):
        validation_remark = validation_remark + "\"Igst amount\" \"" +\
                            row["igst_amount"] + "\" is invalid/missing<br>"
        row["igst_amount"] = "0"
    # Truncating the decimal_part of igst_amount
    else:
        row["igst_amount"] = format(float(row["igst_amount"]), '.2f')

    #Validating cess amount
    # Removing the space and comma
    row["cess_amount"] = clean_number(row["cess_amount"])
    # Checking if the cess_amount matches the corresponding regex.
    if not validate_expression(CGST_AMOUNT_REGEX, row["cess_amount"]):
        validation_remark = validation_remark + "\"Cess amount\" \"" + \
                            row["cess_amount"] + "\" is invalid/missing<br>"
        row["cess_amount"] = "0"
    else:
        # Truncating the decimal_part of cess_amount
        row["cess_amount"] = format(float(row["cess_amount"]), '.2f')

    return pd.Series([row["user_gstin"], row["year"], row["month"], row["document_type"],\
        row["document_no"], row["hsn"], row["document_date"], row["product_service_description"],\
        row["name_of_supplier"], row["gstin_of_supplier"], row["gstin_of_supplier"],\
        row["gst_rate"], row["line_item"], row["taxable_value"], row["cgst_amount"],\
        row["sgst_amount"], row["igst_amount"], row["cess_amount"], validation_remark])

#Called from lambda_function.py
#Validating the columns
def purchase_register_mapping_data(filepath, data, created_by_user, upload_data_dict,\
    l1_bucket, b_filename, database):
    # pylint: disable-msg=W0703
    # pylint: disable-msg=R0913
    '''
     Input  -
        params: filepath - The location of the file path
        params: data - The data in csv file
        params: created_by_user - The user who have uploaded the file
        params: l1_bucket - bucket name of L1
        params: b_filename - file name from backup
        params: config_dict: configuration of database
     Output - The fields are validated
    '''
    msg, count = "", 0
    flag_trigger_update = True
    conn = None
    try:
        test_data = pd.read_csv(filepath, encoding="ISO-8859-1", dtype=object)
        test_data.rename(columns=RENEAME_COL_DICT, inplace=True)
        test_data = test_data.fillna("")
        size = test_data.shape[0]
        #Checking the file is empty or not
        if not test_data.empty:
            # validating file
            test_data[["user_gstin", "year", "month", "document_type", "document_no",\
                "hsn", "document_date", "product_service_description", "name_of_supplier",\
                "gstin_of_supplier", "gstin_of_supplier", "gst_rate", "line_item",\
                "taxable_value", "cgst_amount", "sgst_amount", "igst_amount", "cess_amount",\
                "validation_remark"]] = test_data.apply(rowvalidation, axis=1)
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           # default value key
            default_value = {"company_id": 0, "company_name": "", "state": "", "bu_id": 0,\
                "bu_name": "", "sbu_id": 0, "sbu_name": "", "location_id": 0, "location_name": "",\
                "gstin_id": 0, "active": "Y", "created_by": created_by_user,\
                "updated_by": created_by_user, "created_date": current_date,\
                "updated_date": current_date, "comments": " ", "load_id": str(data[0])}
            for key in default_value:
                test_data[key] = default_value[key]
            conn = make_connection(database)
            cursor = get_dict_cursor(conn)
            all_list = test_data.T.to_dict().values()
            cursor.executemany(INSERT_QUERY, tuple(all_list))
            count = size
            msg = "Data successfully loaded"
            upload_data_dict["status"] = msg
            upload_data_dict["import_from_file"] = count
            try:
                print("L1: INSERTING DATA INTO UPLOAD TABLE")
                upload_file_details_with_conn(data, upload_data_dict, conn, cursor)
                print("L1: INSERTED DATA INTO UPLOAD TABLE")
            except Exception as error:
                print("L1 EXCEPTION OCCURED Getting insertion error on upload table")
                print("L1: EXCEPTION OCCURED ", error)
                msg = "Data upload failed."
                count = 0
                # uploading file to error folder
                error_upload_file(l1_bucket, b_filename, upload_data_dict["original_file_name"])
            exist_cur_conn_closed(conn, cursor)
            flag_trigger_update = False
        else:
            msg = "Rejected - File is emtpy"
    except Exception as error:
        print("L1: EXCEPTION OCCURED ", error)
        print("L1: SOMETHING IS WRONG")
        msg = "Data upload failed."
        count = 0
        exist_conn_closed(conn)
        traceback.print_exc()
    return flag_trigger_update, msg, count
