'''
#Defining the insert query
'''
update_history = ""

INSERT_QUERY_FOR_NEW_GSTIN = '''INSERT INTO demo.gstin_status(nic_gstin, created_by, created_date, updated_by,\
updated_date, status, validation_remark, load_id, active, update_history) \
SELECT %(gstin)s, %(created_by)s, %(created_date)s, %(updated_by)s, %(updated_date)s, %(status)s,\
%(validation_remark)s, %(load_id)s, 'Y', %(update_history)s \
WHERE NOT EXISTS(\
SELECT nic_gstin from demo.gstin_status where nic_gstin = %(gstin)s and active='Y'\
)'''

SELECT_QUERY_FOR_EXISTING_GSTIN = "SELECT * from demo.gstin_status "\
"WHERE active='Y' and status!='Initiated' and nic_gstin in ({gstin_join})"

UPDATE_QUERY_FOR_EXISTING_GSTIN = "UPDATE demo.gstin_status SET active=%(active)s, "\
    "updated_by=%(updated_by)s, updated_date=%(updated_date)s, "\
    "update_history=CONCAT(update_history, '<br>', %(update_history)s) WHERE id=%(id)s"