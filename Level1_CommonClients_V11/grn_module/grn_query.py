'''
#Defining the queries
'''
EWB_DETAILS_QUERY_1 = ("SELECT * FROM demo.ewb_details "\
    "WHERE udid = %s AND document_date = DATE(%s) AND "\
    "ewb_generation_status NOT IN ('Cancelled', 'Sent for cancellation', "\
    "'Sent For vehicle update', 'Sent for Extension', 'Sent For transporter update', "\
    "'Sent For Consolidation' ,'Sent for Regeneration') AND active = 'Y' "\
    "AND nic_eway_bill_date <= %s AND document_date <= %s "\
    "AND eway_bill_no IS NOT NULL AND is_countery_party_rejected =  'N' "\
    "AND is_cancel =  'N' AND (movement_status !=  'Delivered' OR movement_status IS NULL) "\
    "ORDER BY load_id DESC, document_no DESC, udid DESC")

EWB_DETAILS_QUERY = ("SELECT * FROM demo.ewb_details e WHERE "\
    "EXISTS(SELECT * FROM (VALUES(%s, %s)) v(udid, document_date) "\
    "WHERE e.udid = v.udid AND e.document_date = DATE(v.document_date)) "\
    "AND ewb_generation_status NOT IN ('Cancelled', 'Sent for cancellation', "\
    "'Sent For vehicle update', 'Sent for Extension', 'Sent For transporter update', "\
    "'Sent For Consolidation' ,'Sent for Regeneration') AND active = 'Y' "\
    "AND nic_eway_bill_date <= %s AND document_date <= %s "\
    "AND eway_bill_no IS NOT NULL AND is_countery_party_rejected =  'N' "\
    "AND is_cancel =  'N' AND (movement_status !=  'Delivered' OR movement_status IS NULL) "\
    "ORDER BY load_id DESC, document_no DESC, udid DESC")

INSERT_QUERY = "INSERT INTO demo.grn_details(user_gstin, supply_type, document_no, "\
    "document_date, delivery_document_no, delivery_document_date, place, mis_1, mis_2, mis_3, "\
    "mis_4, mis_5, mis_6, mis_7, mis_8, mis_9, mis_10, created_by, created_date, updated_by, "\
    "updated_date, remarks, status, load_id, udid) VALUES(%(user_gstin)s, %(supply_type)s, "\
    "%(document_no)s, %(document_date)s, %(delivery_document_no)s, %(delivery_document_date)s, "\
    "%(place)s, %(mis_1)s, %(mis_2)s, %(mis_3)s, %(mis_4)s, %(mis_5)s,%(mis_6)s, %(mis_7)s, "\
    "%(mis_8)s, %(mis_9)s, %(mis_10)s, %(created_by)s, %(created_date)s, %(updated_by)s, "\
    "%(updated_date)s, %(remarks)s, %(status)s, %(load_id)s, %(udid)s)"
