'''
#Validating the date fields and defining the headers
'''
from __future__ import print_function
import datetime

#Defining the headers
DEFAULT_HEADER = ['GSTIN', 'Year', 'Month', 'Document Type', 'Document Number', 'Document Date',\
    'GSTIN of Supplier', 'Name of Supplier', 'Line Item', 'HSN', 'Product/Service Description',\
    'Taxable value', 'GST Rate', 'CGST (Amt)', 'SGST (Amt)', 'IGST (Amt)', 'Cess (Amt)',\
    'MIS 1', 'MIS 2', 'MIS 3', 'MIS 4', 'MIS 5', 'MIS 6', 'MIS 7', 'MIS 8', 'MIS 9', 'MIS 10']
# Rename COL
RENEAME_COL_DICT = {"GSTIN": "user_gstin", "Year": "year", "Month": "month",\
    "Document Type": "document_type", "Document Number": "document_no",\
    "Document Date": "document_date", "GSTIN of Supplier": "gstin_of_supplier",\
    "Name of Supplier": "name_of_supplier", "Line Item": "line_item", "HSN": "hsn",\
    "Product/Service Description": "product_service_description",\
    "Taxable value": "taxable_value", "GST Rate": "gst_rate", "CGST (Amt)": "cgst_amount",\
    "SGST (Amt)": "sgst_amount", "IGST (Amt)": "igst_amount", "Cess (Amt)": "cess_amount",\
    "MIS 1": "mis_1", "MIS 2": "mis_2", "MIS 3": "mis_3", "MIS 4": "mis_4", "MIS 5": "mis_5",\
    "MIS 6": "mis_6", "MIS 7": "mis_7", "MIS 8": "mis_8", "MIS 9": "mis_9", "MIS 10": "mis_10"}
# Default Document Type List
DOCUMENT_TYPE_DEFAULT = ['TAX INVOICE', 'BILL OF SUPPLY', 'BILL OF ENTRY', 'DELIVERY CHALLAN',\
    'CREDIT NOTE', 'OTHERS']

#Validating the date format
def grn_validate_date(str_date, d_format, p_format):
    # pylint: disable-msg=W0703
    '''
    Input  -
       params: str_date - The date present in csv file that is to be validated
       params: d_format - The allowed date format
       params: p_format - The allowed date format
    Output - The date format is validated successfully
    '''
    date_string = None
    try:
        #Parsing the date object to string.Calling parse_datetime_to_string() function
        date_string = datetime.datetime.strptime(str_date, d_format).strftime(p_format)
    except Exception as error:
       pass
    return date_string
