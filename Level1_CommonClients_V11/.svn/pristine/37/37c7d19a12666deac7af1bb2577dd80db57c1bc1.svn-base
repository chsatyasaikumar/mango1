'''
#Defining queries
'''
#Helper function
#Updating transporter_name in document_details table
# Creating update query for document_details update table
T_UPDATE_QUERY = ("UPDATE demo.document_details SET transporter_name= %s, "\
    "transporter_id=%s, updated_by =%s , update_history=CONCAT(update_history, "\
    "%s), updated_date = %s WHERE udid = %s")
#Defining the insert query for transporter_update_history table
INSERT_QUERY = ("INSERT INTO DEMO.transporter_update_history(document_no, transporter_name, "\
    "transporter_id, mis_3, udid, created_by, created_date, load_id, source_type, load_type) "\
    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
#Helper function
#Updating transporter_name and transporter_id in ewb_details table
T_EWB_DTLS_UDT_QUERY = ("UPDATE demo.ewb_details SET transporter_name=%s, transporter_id=%s, "\
    "updated_by=%s, updated_date=%s, comments=CONCAT(comments, %s) WHERE udid=%s")
#Helper function
#Selecting the unique load_id from ewb_details table
EWB_LOAD_ID_QUERY = ("SELECT DISTINCT load_id, load_id, eway_bill_no, user_gstin FROM demo.ewb_details " \
    "WHERE udid =%s AND active = 'Y' AND is_expired = 'N' AND is_cancel = 'N' "\
    "AND is_countery_party_rejected = 'N'")
    