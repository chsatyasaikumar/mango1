'''
#Defining the constants
'''
#Defining the default sap header
DEFAULT_HEADER = ['User GSTIN', 'Supply Type', 'Sub Type', 'Document Type', 'Document No',\
    'Document Date', 'From_Name', 'From_GSTIN', 'Bill From_State', 'From_Address1',\
    'From_Address2', 'From_Place', 'From_Pin Code', 'From_State', 'To_Name', 'To_GSTIN',\
    'Bill To_State', 'To_Address1', 'To_Address2', 'To_Place', 'To_Pin Code', 'To_State',\
    'Line Item', 'Item code', 'Product Name', 'Description', 'HSN', 'Unit', 'Quantity',\
    'Taxable value', 'CGST Rate', 'CGST Amount', 'SGST Rate', 'SGST Amount', 'IGST Rate',\
    'IGST Amount', 'Cess Rate', 'Cess Amount', 'Trans Mode', 'Distance (Km)', 'Transporter Name',\
    'Transporter ID', 'Trans Doc No', 'Trans Doc Date', 'Vehicle No', 'Vehicle Type', 'BU', 'SBU',\
    'Location', 'User', 'Tracking Number', 'Accounting Doc No', 'Accounting Doc Date', 'PO No',\
    'PO Date', 'SO No', 'SO Date', 'Original Document No.', 'Original Document Date', 'MIS 1',\
    'MIS 2', 'MIS 3', 'MIS 4', 'MIS 5', 'MIS 6', 'MIS 7', 'MIS 8', 'MIS 9', 'MIS 10', 'FU 1',\
    'FU 2', 'FU 3', 'FU 4', 'FU 5', 'FU 6', 'FU 7', 'FU 8', 'FU 9', 'FU 10']
# Default Header 2
DEFAULT_HEADER_2 = ['User GSTIN', 'Supply Type', 'Sub Type', 'Document Type', 'Document No',\
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
    'FU 22', 'FU 23', 'FU 24', 'FU 25', 'FU 26', 'FU 27', 'FU 28', 'FU 29', 'FU 30']
# Default Header 3
DEFAULT_HEADER_3 = ['User GSTIN', 'Supply Type', 'Sub Type', 'Document Type', 'Document No',\
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
    'FU 22', 'FU 23', 'FU 24', 'FU 25', 'FU 26', 'FU 27', 'FU 28', 'FU 29', 'FU 30', 'is_ewaybill',\
    "is_irn", "irn", "ackno", "ackdt", "irn_load_id", "update_history", "irn_status",\
    "is_ewaybill_exclude"]
#Renaming the header to L2 format
RENAME_HEADER = {'User GSTIN': "user_gstin", 'Supply Type': "supply_type", 'Sub Type': "sub_type",\
    'Document Type': "document_type", 'Document No': "document_no",\
    'Document Date': "document_date", 'From_Name': "from_name", 'From_GSTIN': "from_gstin",\
    'Bill From_State': 'bill_from_state', 'From_Address1': "from_address1",\
    'From_Address2': "from_address2", 'From_Place': "from_place",\
    'From_Pin Code': "from_pin_code", 'From_State': "from_state", 'To_Name': "to_name",\
    'To_GSTIN': "to_gstin", 'Bill To_State': 'bill_to_state', 'To_Address1': "to_address1",\
    'To_Address2': "to_address2", 'To_Place': "to_place", 'To_Pin Code': "to_pin_code",\
    'To_State': "to_state", 'Line Item': "line_item", 'Item code': "item_code",\
    'Product Name': "product_name", 'Description': "description", 'HSN': "hsn", 'Unit': "unit",\
    'Quantity': "quantity", 'Taxable value': "taxable_value", 'CGST Rate': "cgst_rate",\
    'CGST Amount': "cgst_amount", 'SGST Rate': "sgst_rate", 'SGST Amount': "sgst_amount",\
    'IGST Rate': "igst_rate", 'IGST Amount': "igst_amount", 'Cess Rate': "cess_rate",\
    'Cess Amount': "cess_amount", 'Trans Mode': "trans_mode", 'Distance (Km)': "distance_km",\
    'Transporter Name': "transporter_name", 'Transporter ID': "transporter_id",\
    'Trans Doc No': "trans_doc_no", 'Trans Doc Date': "trans_doc_date",\
    'Vehicle No': "vehicle_no", 'Vehicle Type': 'vehicle_type', 'BU': "bu", 'SBU': "sbu",\
    'Location': "location", 'User': "user", 'Tracking Number': 'tracking_number',\
    'Accounting Doc No': "accounting_doc_no", 'Accounting Doc Date': "accounting_doc_date",\
    'PO No': "po_no", 'PO Date': "po_date", 'SO No': "so_no", 'SO Date': "so_date",\
    "Original Document No.": "original_document_no",\
    'Original Document Date': "original_document_date", 'MIS 1': "mis_1", 'MIS 2': "mis_2",\
    'MIS 3': "mis_3", 'MIS 4': "mis_4", 'MIS 5': "mis_5", 'MIS 6': "mis_6", 'MIS 7': "mis_7",\
    'MIS 8': "mis_8", 'MIS 9': "mis_9", 'MIS 10': "mis_10", 'FU 1': "fu_1", 'FU 2': "fu_2",\
    'FU 3': "fu_3", 'FU 4': "fu_4", 'FU 5': "fu_5", 'FU 6': 'fu_6', 'FU 7': 'fu_7',\
    'FU 8': 'fu_8', 'FU 9': 'fu_9', 'FU 10': 'fu_10', 'FU 11': 'fu_11', 'FU 12': 'fu_12',\
    'FU 13': 'fu_13', 'FU 14': 'fu_14', 'FU 15': 'fu_15', 'FU 16': 'fu_16', 'FU 17': 'fu_17',\
    'FU 18': 'fu_18', 'FU 19': 'fu_19', 'FU 20': 'fu_20', 'FU 21': 'fu_21', 'FU 22': 'fu_22',\
    'FU 23': 'fu_23', 'FU 24': 'fu_24', 'FU 25': 'fu_25', 'FU 26': 'fu_26', 'FU 27': 'fu_27',\
    'FU 28': 'fu_28', 'FU 29': 'fu_29', 'FU 30' : 'fu_30'}
# OPTIONAL HEADER
OPTIONAL_HEADER = ['FU 11', 'FU 12', 'FU 13', 'FU 14', 'FU 15', 'FU 16', 'FU 17', 'FU 18',\
    'FU 19', 'FU 20', 'FU 21', 'FU 22', 'FU 23', 'FU 24', 'FU 25', 'FU 26', 'FU 27', 'FU 28',\
    'FU 29', 'FU 30', 'is_ewaybill', "is_irn", "irn", "ackno", "ackdt", "irn_load_id", \
    "update_history", "irn_status", "is_ewaybill_exclude"]
# optional Header 2
OPTIONAL_HEADER_2 = ['is_ewaybill', "is_irn", "irn", "ackno", "ackdt", "irn_load_id",\
    "update_history", "irn_status", "is_ewaybill_exclude"]
# L2 File Header after rename
GEN_HEADER = ['user_gstin', 'supply_type', 'sub_type', 'document_type', 'document_no',\
    'document_date', 'from_name', 'from_gstin', 'bill_from_state', 'from_address1',\
    'from_address2', 'from_place', 'from_pin_code', 'from_state', 'to_name', 'to_gstin',\
    'bill_to_state', 'to_address1', 'to_address2', 'to_place', 'to_pin_code', 'to_state',\
    'line_item', 'item_code', 'product_name', 'description', 'hsn', 'unit', 'quantity',\
    'taxable_value', 'cgst_rate', 'cgst_amount', 'sgst_rate', 'sgst_amount', 'igst_rate',\
    'igst_amount', 'cess_rate', 'cess_amount', 'trans_mode', 'distance_km',\
    'transporter_name', 'transporter_id', 'trans_doc_no', 'trans_doc_date', 'vehicle_no',\
    'vehicle_type', 'bu', 'sbu', 'location', 'user', 'tracking_number', 'accounting_doc_no',\
    'accounting_doc_date', 'po_no', 'po_date', 'so_no', 'so_date', 'original_document_no',\
    'original_document_date', 'mis_1', 'mis_2', 'mis_3', 'mis_4', 'mis_5', 'mis_6', 'mis_7',\
    'mis_8', 'mis_9', 'mis_10', 'fu_1', 'fu_2', 'fu_3', 'fu_4', 'fu_5', 'fu_6', 'fu_7', 'fu_8',\
    'fu_9', 'fu_10', 'document_status', 'validation_status', 'id', 'created_by_user',\
    'source_type', "bu_id", "sbu_id", "location_id", "company_id", "company_name", \
    "validation_remark", "gstin_id", "fu_11", "fu_12", "fu_13", "fu_14", "fu_15", "fu_16",\
    "fu_17", "fu_18", "fu_19", "fu_20", "fu_21", "fu_22", "fu_23", "fu_24", "fu_25", "fu_26",\
    "fu_27", "fu_28", "fu_29", "fu_30", 'is_ewaybill', "is_irn", "irn", "ackno", "ackdt",\
    "irn_load_id", "update_history", "irn_status", "alert_validation_remark",\
    "is_ewaybill_exclude"]

SAP_MAPPING_CONFIG_PATH = "sap_mapping_config.json"
MASTER_CONFIG_PATH = "master_config.json"
