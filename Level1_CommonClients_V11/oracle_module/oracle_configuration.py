#Defining some constants
#Defining oracle header
ORACLE_FORMAT_HEADER = [
    "User GSTIN",
    "Supply Type",
    "Sub Type",
    "Document Type",
    "Doc No",
    "Doc Date",
    "From_Name",
    "From_GSTIN",
    "Bill From_State",
    "From_Address1",
    "From_Address2",
    "From_Place",
    "From_Pin Code",
    "From_State",
    "To_Name",
    "To_GSTIN",
    "Bill To_State",
    "To_Address1",
    "To_Address2",
    "To_Place",
    "To_Pin Code",
    "To_State",
    "Line Item",
    "Item code",
    "Product",
    "Desc",
    "HSN code",
    "Unit",
    "Quantity",
    "Taxable amount",
    "CGST %",
    "CGST Amount",
    "SGST %",
    "SGST Amount",
    "IGST %",
    "IGST Amount",
    "Cess Rate",
    "Cess Amount",
    "Trans Mode",
    "Distance (Km)",
    "Transporter",
    "Transporter ID",
    "Trans Doc No",
    "Trans Doc Date",
    "Vehicle No",
    "Type of vehicle",
    "BU",
    "SBU",
    "Location",
    "User",
    "Tracking id",
    "Acc Doc No",
    "Acc Doc Date",
    "PO No",
    "PO Date",
    "SO No",
    "SO Date",
    "Org Doc No.",
    "Org Doc Date"

]
#Defining oracle config file
ORACLE_MAPPING_CONFIG_PATH = "oracle_mapping_config.json"
#Defining rename header
RENAME_HEADER = {
    'User GSTIN': "user_gstin",
    'Supply Type': "supply_type",
    'Sub Type': "sub_type",
    'Document Type': "document_type",
    'Doc No': "document_no",
    'Doc Date': "document_date",
    'From_Name': "from_name",
    'From_GSTIN': "from_gstin",
    'Bill From_State': 'bill_from_state',
    'From_Address1': "from_address1",
    'From_Address2': "from_address2",
    'From_Place': "from_place",
    'From_Pin Code': "from_pin_code",
    'From_State': "from_state",
    'To_Name': "to_name",
    'To_GSTIN': "to_gstin",
    'Bill To_State': 'bill_to_state',
    'To_Address1': "to_address1",
    'To_Address2': "to_address2",
    'To_Place': "to_place",
    'To_Pin Code': "to_pin_code",
    'To_State': "to_state",
    'Line Item': "line_item",
    'Item code': "item_code",
    'Product': "product_name",
    'Desc': "description",
    'HSN code': "hsn",
    'Unit': "unit",
    'Quantity': "quantity",
    'Taxable amount': "taxable_value",
    'CGST %': "cgst_rate",
    'CGST Amount': "cgst_amount",
    'SGST %': "sgst_rate",
    'SGST Amount': "sgst_amount",
    'IGST %': "igst_rate",
    'IGST Amount': "igst_amount",
    'Cess Rate': "cess_rate",
    'Cess Amount': "cess_amount",
    'Trans Mode': "trans_mode",
    'Distance (Km)': "distance_km",
    'Transporter': "transporter_name",
    'Transporter ID': "transporter_id",
    'Trans Doc No': "trans_doc_no",
    'Trans Doc Date': "trans_doc_date",
    'Vehicle No': "vehicle_no",
    'Type of vehicle': 'vehicle_type',
    'BU': "bu",
    'SBU': "sbu",
    'Location': "location",
    'User': "user",
    'Tracking id': 'tracking_number',
    'Acc Doc No': "accounting_doc_no",
    'Acc Doc Date': "accounting_doc_date",
    'PO No': "po_no",
    'PO Date': "po_date",
    'SO No': "so_no",
    'SO Date': "so_date",
    "Org Doc No.": "original_document_no",
    'Org Doc Date': "original_document_date",
    'MIS 1': "mis_1",
    'MIS 2': "mis_2",
    'MIS 3': "mis_3",
    'MIS 4': "mis_4",
    'MIS 5': "mis_5",
    'MIS 6': "mis_6",
    'MIS 7': "mis_7",
    'MIS 8': "mis_8",
    'MIS 9': "mis_9",
    'MIS 10': "mis_10",
    'FU 1': "fu_1",
    'FU 2': "fu_2",
    'FU 3': "fu_3",
    'FU 4': "fu_4",
    'FU 5': "fu_5",
    'FU 6': 'fu_6',
    'FU 7': 'fu_7',
    'FU 8': 'fu_8',
    'FU 9': 'fu_9',
    'FU 10': 'fu_10'
}

#Defining header name for l2
DEFAULT_HEADER = ['user_gstin', 'supply_type', 'sub_type', 'document_type', 'document_no',
                  'document_date', 'from_name', 'from_gstin', 'bill_from_state', 'from_address1',
                  'from_address2', 'from_place', 'from_pin_code', 'from_state', 'to_name',
                  'to_gstin', 'bill_to_state', 'to_address1', 'to_address2', 'to_place',
                  'to_pin_code', 'to_state', 'line_item', 'item_code', 'product_name',
                  'description', 'hsn', 'unit', 'quantity', 'taxable_value', 'cgst_rate',
                  'cgst_amount', 'sgst_rate', 'sgst_amount', 'igst_rate', 'igst_amount',
                  'cess_rate', 'cess_amount', 'trans_mode', 'distance_km', 'transporter_name',
                  'transporter_id', 'trans_doc_no', 'trans_doc_date', 'vehicle_no',
                  'vehicle_type', 'bu', 'sbu', 'location', 'user', 'tracking_number',
                  'accounting_doc_no', 'accounting_doc_date', 'po_no', 'po_date',
                  'so_no', 'so_date', 'original_document_no', 'original_document_date',
                  'mis_1', 'mis_2', 'mis_3', 'mis_4', 'mis_5', 'mis_6', 'mis_7', 'mis_8',
                  'mis_9', 'mis_10', 'fu_1', 'fu_2', 'fu_3', 'fu_4', 'fu_5', 'fu_6', 'fu_7',
                  'fu_8', 'fu_9', 'fu_10', 'document_status', 'validation_status', 'id']
