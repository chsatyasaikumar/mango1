'''
ewb configuration details
'''
EWB_CSV_HEADER = ['User GSTIN', 'Supply Type', 'Sub Type', 'Document Type', 'Document No',\
    'Document Date', 'From_Name', 'From_GSTIN', 'Bill From_State', 'From_Address1',\
    'From_Address2', 'From_Place', 'From_Pin Code', 'From_State', 'To_Name', 'To_GSTIN',\
    'Bill To_State', 'To_Address1', 'To_Address2', 'To_Place', 'To_Pin Code', 'To_State',\
    'Line Item', 'Item code', 'Product Name', 'Description', 'HSN', 'Unit', 'Quantity',\
    'Taxable value', 'CGST Rate', 'CGST Amount', 'SGST Rate', 'SGST Amount', 'IGST Rate',\
    'IGST Amount', 'Cess Rate', 'Cess Amount', 'Trans Mode', 'Distance (Km)', 'Transporter Name',\
    'Transporter ID', 'Trans Doc No', 'Trans Doc Date', 'Vehicle No', 'Vehicle Type', 'BU',\
    'SBU', 'Location', 'User', 'Tracking Number', 'Accounting Doc No', 'Accounting Doc Date',\
    'PO No', 'PO Date', 'SO No', 'SO Date', 'Original Document No.', 'Original Document Date',\
    'MIS 1', 'MIS 2', 'MIS 3', 'MIS 4', 'MIS 5', 'MIS 6', 'MIS 7', 'MIS 8', 'MIS 9', 'MIS 10',\
    'FU 1', 'FU 2', 'FU 3', 'FU 4', 'FU 5', 'FU 6', 'FU 7', 'FU 8', 'FU 9', 'FU 10', 'FU 11',\
    'FU 12', 'FU 13', 'FU 14', 'FU 15', 'FU 16', 'FU 17', 'FU 18', 'FU 19', 'FU 20', 'FU 21',\
    'FU 22', 'FU 23', 'FU 24', 'FU 25', 'FU 26', 'FU 27', 'FU 28', 'FU 29', 'FU 30',\
    'is_ewaybill', 'is_irn', 'irn', 'ackno', 'ackdt', 'irn_load_id', 'update_history',\
    'irn_status', 'is_ewaybill_exclude']
# EWB_STRUCTURE
EWB_STRUCTURE_PAYLOAD = {"User GSTIN": "", "Supply Type": "", "Sub Type": "",\
    "Document Type": "", "Document No": "", "Document Date": "",\
    "From_Name": "", "From_GSTIN": "", "Bill From_State": "", \
    "From_Address1": "", "From_Address2": "", "From_Place" : "",\
    "From_Pin Code": "", "From_State": "", "To_Name": "",\
    "To_GSTIN": "", "Bill To_State": "", "To_Address1": "", "To_Address2": "",\
    "To_Place": "", "To_Pin Code": "", "To_State": "", "Line Item":"", "Item code": "",\
    "Product Name": "", "Description": "", "HSN": "", "Unit": "", "Quantity": "",\
    "Taxable value": "", "CGST Rate": "", "CGST Amount": "", "SGST Rate": "",\
    "SGST Amount": "", "IGST Rate": "", "IGST Amount": "", "Cess Rate":"",\
    "Cess Amount":"", "Trans Mode":"", "Distance (Km)": "", "Transporter Name": "",\
    "Transporter ID": "", "Trans Doc No": "", "Trans Doc Date": "", "Vehicle No": "",\
    "Vehicle Type": "", "BU": "", "SBU": "", "Location": "", "User": "",\
    "Tracking Number": "", "Accounting Doc No": "", "Accounting Doc Date": "", "PO No": "",\
    "PO Date": "", "SO No": "", "SO Date": "", "Original Document No.": "",\
    "Original Document Date": "", "MIS 1": "", "MIS 2":"", "MIS 3": "", "MIS 4": "",\
    "MIS 5": "", "MIS 6": "", "MIS 7": "", "MIS 8": "", "MIS 9": "", "MIS 10": "",\
    "FU 1": "", "FU 2": "", "FU 3": "", "FU 4": "", "FU 5": "", "FU 6": "", "FU 7": "",\
    "FU 8": "", "FU 9": "", "FU 10": "", "FU 11": "", "FU 12": "", "FU 13": "",\
    "FU 14": "", "FU 15": "", "FU 16": "", "FU 17": "", "FU 18": "", "FU 19": "",\
    "FU 20": "", "FU 21": "", "FU 22": "", "FU 23": "", "FU 24": "", "FU 25": "",\
    "FU 26": "", "FU 27": "", "FU 28": "", "FU 29": "", "FU 30": "", "is_ewaybill": "",\
    "is_irn": "", "irn": "", "ackno": "", "ackdt": "", "irn_load_id": "",\
    "update_history": "", "irn_status": "", "is_ewaybill_exclude": ""}
# INVOICE LEVEL DATA MAPPING
# first index=json key
# second index = ewb field name
# third index = default value
MAND_DATA_MAPPING = {
    "TranDtls": [\
        ("OutwardInward", "Supply Type", "Outward"),\
        ("SubType", "Sub Type", "Supply"),\
        ("SubTypeDescription", "FU 1", ""),\
    ],
    "DocDtls": [\
        ("No", "Document No", ""),\
        ("Dt", "Document Date", ""),\
        ("Typ", "Document Type", ""),\
    ],\
    "SellerDtls": [\
        ("TrdNm", "From_Name", ""),\
        ("Gstin", "From_GSTIN", ""),\
        ("Stcd", "Bill From_State", ""),\
    ],\
    "DispDtls": [\
        ("Pin", "From_Pin Code", ""),\
        ("Stcd", "From_State", ""),\
        ("Pin", "From_Pin Code", ""),\
        ("Addr1", "From_Address1", ""),\
        ("Addr2", "From_Address2", ""),\
        ("Loc", "From_Place", ""),\
    ],\
    "BuyerDtls": [\
        ("TrdNm", "To_Name", ""),\
        ("Gstin", "To_GSTIN", ""),\
        ("Stcd", "Bill To_State", ""),\
    ],\
    "ShipDtls": [\
        ("Pin", "To_Pin Code", ""),\
        ("Stcd", "To_State", ""),\
        ("Pin", "To_Pin Code", ""),\
        ("Addr1", "To_Address1", ""),\
        ("Addr2", "To_Address2", ""),\
        ("Loc", "To_Place", ""),\
    ],\
    "ValDtls": [\
        ("TotInvVal", "FU 4", ""),\
        ("OthChrg", "FU 7", ""),\
    ],\
    "RefDtls": [\
        ("AccountingDocNo", "Accounting Doc No", ""),\
        ("AccountingDocDt", "Accounting Doc Date", ""),\
        ("SoNo", "SO No", ""),\
        ("SoDt", "SO Date", ""),\
    ],\
    "EwbDtls": [\
        ("TransId", "Transporter ID", ""),\
        ("Distance", "Distance (Km)", ""),\
        ("TransName", "Transporter Name", ""),\
        ("TransMode", "Trans Mode", ""),\
        ("TransDocNo", "Trans Doc No", ""),\
        ("TransDocDt", "Trans Doc Date", ""),\
        ("VehNo", "Vehicle No", ""),\
        ("VehType", "Vehicle Type", ""),\
    ],\
    "MisColumns": [\
        ("Bu", "BU", ""),\
        ("Sbu", "SBU", ""),\
        ("Location", "Location", ""),\
        ("User", "User", ""),\
        ("TrackingNo", "Tracking Number", ""),\
        ("EwbNo", "FU 2", ""),\
    ]
}


# ITEM LEVEL DATA MAPPING
# first index=json key
# second index = ewb field name
# third index = default value
MAND_ITM_LVL_MAPPING = [\
    ("SlNo", "Line Item", ""),\
    ("ItemCode", "Item code", ""),\
    ("PrdNm", "Product Name", ""),\
    ("HsnCd", "HSN", ""),\
    ("Unit", "Unit", ""),\
    ("Qty", "Quantity", ""),\
    ("PrdDesc", "Description", ""),\
    ("AssAmt", "Taxable value", ""),\
    ("CgstRt", "CGST Rate", ""),\
    ("SgstRt", "SGST Rate", ""),\
    ("IgstRt", "IGST Rate", ""),\
    ("CesRt", "Cess Rate", ""),\
    ("CesNonAdvolRt", "FU 8", ""),\
    ("CesNonAdvlAmt", "FU 9", ""),\
    ("IgstAmt", "IGST Amount", ""),\
    ("CgstAmt", "CGST Amount", ""),\
    ("SgstAmt", "SGST Amount", ""),\
    ("CesAmt", "Cess Amount", ""),\
    ("Mis1", "MIS 1", ""),\
]
# UNIT TRANSFORMATION CONFIGURATION
UNIT_CONFIG = {'BAG': 'BAGS', 'BAL': 'BALE', 'BDL': 'BUNDLES', 'BKL': 'BUCKLES',\
    'BOU': 'BILLION OF UNITS', 'BOX': 'BOX', 'BTL': 'BOTTLES', 'BUN': 'BUNCHES',\
    'CAN': 'CANS', 'CBM': 'CUBIC METERS', 'CCM': 'CUBIC CENTIMETERS', 'CMS': 'CENTI METERS',\
    'CTN': 'CARTONS', 'DOZ': 'DOZENS', 'DRM': 'DRUMS', 'GGK': 'GREAT GROSS', 'GMS': 'GRAMMES',\
    'GRS': 'GROSS', 'GYD': 'GROSS YARDS', 'KGS': 'KILOGRAMS', 'KLR': 'KILOLITRE',\
    'KME': 'KILOMETRE', 'MLT': 'MILILITRE', 'MTR': 'METERS', 'MTS': 'METRIC TON',\
    'NOS': 'NUMBERS', 'OTH': 'OTHERS', 'PAC': 'PACKS', 'PCS': 'PIECES', 'PRS': 'PAIRS',\
    'QTL': 'QUINTAL', 'ROL': 'ROLLS', 'SET': 'SETS', 'SQF': 'SQUARE FEET',\
    'SQM': 'SQUARE METERS', 'SQY': 'SQUARE YARDS', 'TBS': 'TABLETS', 'TGM': 'TEN GROSS',\
    'THD': 'THOUSANDS', 'TON': 'TONNES', 'TUB': 'TUBES', 'UGS': 'US GALLONS',\
    'UNT': 'UNITS', 'YDS': 'YARDS', 'BGS': 'BAGS', 'BND': 'BUNDLES', 'CMT': 'CUBIC METERS', \
    'DZN': 'DOZENS', 'KMS': 'KILO METERS', 'MLS': 'MILLI LITRES', 'PAR': 'PAIRS', \
    'QTS': 'QUINTALS', 'SFT': 'SQUARE FEET', 'SMT': 'SQUARE METERS', \
    'SNO': 'THOUSAND NUMBERS/UNITS', 'LTR': 'LITRES'}
# STATE TRANSFORMATION CONFIGURATION
STATE_CONFIG = {"96": "OTHER COUNTRIES", "1": "JAMMU AND KASHMIR",\
    "2": "HIMACHAL PRADESH", "3": "PUNJAB", "4": "CHANDIGARH", "5": "UTTARAKHAND",\
    "6": "HARYANA", "7": "DELHI", "8": "RAJASTHAN", "9": "UTTAR PRADESH",\
    "01": "JAMMU AND KASHMIR", "02": "HIMACHAL PRADESH", "03": "PUNJAB",\
    "04": "CHANDIGARH", "05": "UTTARAKHAND", "06": "HARYANA", "07": "DELHI",\
    "08": "RAJASTHAN", "09": "UTTAR PRADESH", "10": "BIHAR", "11": "SIKKIM",\
    "12": "ARUNACHAL PRADESH", "13": "NAGALAND", "14": "MANIPUR", "15": "MIZORAM",\
    "16": "TRIPURA", "17": "MEGHALAYA", "18": "ASSAM", "19": "WEST BENGAL",\
    "20": "JHARKHAND", "21": "ODISHA", "22": "CHHATTISGARH", "23": "MADHYA PRADESH",\
    "24": "GUJARAT", "25": "DAMAN AND DIU", "26": "DADRA AND NAGAR HAVELI", "27": "MAHARASHTRA",\
    "29": "KARNATAKA", "30": "GOA", "31": "LAKSHADWEEP", "32": "KERALA", "33": "TAMIL NADU",\
    "34": "PUDUCHERRY", "35": "ANDAMAN AND NICOBAR ISLANDS", "36": "TELANGANA",\
    "37": "ANDHRA PRADESH", "38": "LADAKH", "97": "OTHER TERRITORY",\
    "99": "OTHER COUNTRIES"}

# STATE NAME TRANSFORM NAME DICT
STATE_NAME_TRANS_DICT = {\
    "ANDAMAN AND NICOBAR": "ANDAMAN AND NICOBAR ISLANDS",\
    "DADAR AND NAGAR HAVELI": "DADRA AND NAGAR HAVELI",\
    "OTHER COUNTRY": "OTHER COUNTRIES",\
    "MAHARASTRA": "MAHARASHTRA",\
    "ORISSA": "ODISHA",\
}
# STATE CONFIG ID
STATE_CONFIG_ID = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,\
    22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 99, 97]
# STATE CONFIG ID IGN
STATE_CONFIG_ID_IGNORE = [99, 97]

# STATE TRANSFORMATION LIST
STATE_TRANSFORMATION_LIST = ("From_State", "To_State", "Bill From_State", "Bill To_State")
# STATE NAME TRANSFORMATION COLUMNS LIST
STATE_NAME_TRANS_LIST = ("Bill From_State", "Bill To_State")
# TRANS_MOD_DICT
TRANS_MODE_TRANSFORM_DICT = {"1": "ROAD", "2": "RAIL", "3": "AIR", "4": "SHIP"}
# VEHICLE TYPE DICT
VEHICLE_TYP_TRANSFORM_DICT = {"O": "OVER DIMENSIONAL CARGO", "R": "REGULAR"}
# DOCUMENT TYPE TRANSFORMATIOn
DOC_TYPE_CONFIG = {\
    "INV": "TAX INVOICE",\
    "DBN": "Debit Note",\
    "CRN": "Credit Note",\
    "CHL": "Delivery Challan",\
    "BOE": "Bill of Entry",\
    "BIL": "Bill of supply",\
    "OTH": "Others",\
    "RCV": "Receipt Voucher",\
    "RFV": "Refund Voucher",\
    "PMV": "Payment Voucher",\
}
# Transaction type transformation config
TRAN_TYPE_CONFIG = {\
    "REG": "Address Same as Seller and Buyer (By default)",\
    "DIS": "Dispatch Address different from Seller Address",\
    "SHP": "Ship To Address is different from Buyer Address",\
    "CMB": "Both Dispatch and Shipping Address is different from Seller and Buyer respectively",\
}
# Default_value_map
# first index=json key
# second index = ewb field name
# third index = default value
DFLT_VAL_MAP = [\
    ("is_ewb", "is_ewaybill", ""),\
    ("irn", "irn", ""),\
    ("load_id", "irn_load_id", ""),\
    ("update_history", "update_history", "Data inserted through IRN API"),\
    ("irn_status", "irn_status", ""),\
    ("is_irn", "is_irn", ""),\
    ("email", "FU 30", ""),\
    ("is_ewaybill_exclude", "is_ewaybill_exclude", ""),\
    ("ackno", "ackno", ""),\
    ("ackdt", "ackdt", ""),\
]
# DATE TRANSFROM LIST
DATE_COL_LIST = [\
    "Document Date",\
    "Trans Doc Date",\
    "Accounting Doc Date",\
    "PO Date",\
    "SO Date",\
    "Original Document Date",\
]
# TranDtls Typ Transform Dict
TRANS_TYPE_TRANSFORM = {\
    "REG": "REGULAR",\
    "DIS": "BILL FROM- DISPATCH FROM",\
    "SHP": "BILL TO- SHIP TO",\
    "CMB": "COMBINATION OF 2 AND 3",\
}
