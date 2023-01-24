# pylint: disable-msg=W1202
'''
Here we are parsing json to csv for ewb
'''
# Builtin imports
import os
from io import StringIO
import time
import datetime
import operator
from operator import itemgetter
import uuid
import random
import secrets
import copy
import csv
import logging
import json
# External imports
import boto3
# Internal imports
from irn_ewb.module.util.mis_function import parse_date
from irn_ewb.settings.configuration import RESPONSE_MESSAGE
from irn_ewb.module.ewb.configuration import EWB_STRUCTURE_PAYLOAD, MAND_DATA_MAPPING, \
    MAND_ITM_LVL_MAPPING, UNIT_CONFIG, STATE_CONFIG, STATE_TRANSFORMATION_LIST, \
    DOC_TYPE_CONFIG, TRAN_TYPE_CONFIG, DFLT_VAL_MAP, EWB_CSV_HEADER, DATE_COL_LIST, \
    TRANS_MODE_TRANSFORM_DICT, VEHICLE_TYP_TRANSFORM_DICT, \
    TRANS_TYPE_TRANSFORM, STATE_NAME_TRANS_DICT, STATE_NAME_TRANS_LIST
LOGGER = logging.getLogger("irn-ewb-process")


class EwbParse:
    '''
    Summery Line.
        Here we are transforming einvoice data into ewb data
    '''
    def __str__(self):
        '''
        Summery Line.
            obect representation
        '''
        return "EwbParse object"

    @staticmethod
    def orignal_invoice_no_dt_map(payload, ewb_data):
        '''
        Summery Line.
            Here we are mapping original invoice number and date
        Parameters:
            payload(dict): request payload
            ewb_data(dict): document details data
        Return:
            modify ewb_data
        '''
        if isinstance(payload.get("RefDtls"), dict) and payload["RefDtls"].get("PrecDocDtls") and \
            isinstance(payload["RefDtls"].get("PrecDocDtls"), list):
            inv_no = ''
            inv_dt = ''
            inv_no_list = []
            inv_dt_list = []
            for data in payload["RefDtls"].get("PrecDocDtls"):
                if data and isinstance(data, dict):
                    if "InvNo" in data and data["InvNo"]:
                        inv_no_list.append(data['InvNo'])
                    if "InvDt" in data and data['InvDt']:
                        inv_dt_list.append(data['InvDt'])

            inv_no = ', '.join(inv_no_list)
            inv_dt = ', '.join(inv_dt_list)

            ewb_data["Original Document No."] = inv_no
            ewb_data["Original Document Date"] = inv_dt

    @staticmethod
    def po_no_dt_map(payload, ewb_data):
        '''
        Summery Line.
            Here we are po no and po date
        Parameters:
            payload(dict): request payload
            ewb_data(dict): document details data
        Return:
            modify ewb_data
        '''
        if isinstance(payload.get("RefDtls"), dict) and payload["RefDtls"].get("ContrDtls") and \
            isinstance(payload["RefDtls"].get("ContrDtls"), list):
            po_no = ''
            po_dt = ''
            po_no_list = []
            po_dt_list = []
            for data in payload["RefDtls"].get("ContrDtls"):
                if data and isinstance(data, dict):
                    if data.get("PORefr"):
                        po_no_list.append(data['PORefr'])
                    if data.get('PORefDt'):
                        po_dt_list.append(data['PORefDt'])

            po_no = ', '.join(po_no_list)
            po_dt = ', '.join(po_dt_list)

            ewb_data["PO No"] = po_no
            ewb_data["PO Date"] = po_dt

    @staticmethod
    def trans_type_transform(payload, ewb_data):
        '''
        Summery Line.
            Here Transforming TranDtls_Typ
        Parameters:
            payload(dict): request payload
            ewb_data(dict): document details data
        Return:
            modify ewb_data
        '''
        if "TranDtls" in payload and isinstance(payload["TranDtls"], dict) and \
            payload["TranDtls"].get("Typ") and isinstance(payload["TranDtls"]["Typ"], str):
            upper_trans_type = payload["TranDtls"]["Typ"].upper()
            if upper_trans_type in TRANS_TYPE_TRANSFORM:
                ewb_data["FU 6"] = TRANS_TYPE_TRANSFORM[upper_trans_type]

    @staticmethod
    def default_transform(ewb_data):
        '''
        Summery Line.
            Here we are transforming default value
        Parameters:
            ewb_data(dict): document details data
        Return:
            None
        '''
        if not ewb_data["Supply Type"]:
            ewb_data["Supply Type"] = "Outward"
        if not ewb_data["FU 1"] and isinstance(ewb_data["Sub Type"], str) and \
            ewb_data["Sub Type"].upper() == "OTHERS":
            ewb_data["FU 1"] = "OTHERS"

    @staticmethod
    def version_103_transform(ewb_data, payload, config_dict):
        '''
        Summery Line.
            Here we are transforming the version 1.03 changes
        Parameters:
            ewb_data(dict): ewb data
            payload(dict): irn payload
        Return:
            None
        '''
        # Sub Typ Transform
        if not ewb_data["Sub Type"]:
            if isinstance(payload.get("TranDtls"), dict) and isinstance(\
                payload["TranDtls"].get("SupTyp"), str) and \
                payload["TranDtls"].get("SupTyp").upper() in ["EXPWOP", "EXPWP"]:
                ewb_data["Sub Type"] = "Export"
            else:
                ewb_data["Sub Type"] = "Supply"

        # From Details Transform
        if not ewb_data["From_Address1"] and not ewb_data["From_Address2"] and \
            not ewb_data["From_Place"] and not ewb_data["From_Pin Code"] and \
            not ewb_data["From_State"]:
            if isinstance(payload.get("SellerDtls"), dict):
                ewb_data["From_Address1"] = payload["SellerDtls"].get("Addr1", "")
                ewb_data["From_Address2"] = payload["SellerDtls"].get("Addr2", "")
                ewb_data["From_Place"] = payload["SellerDtls"].get("Loc", "")
                ewb_data["From_Pin Code"] = payload["SellerDtls"].get("Pin", "")
                ewb_data["From_State"] = payload["SellerDtls"].get("Stcd", "")

        # To Details Transform
        if not ewb_data["To_Address1"] and not ewb_data["To_Address2"] and \
            not ewb_data["To_Place"] and not ewb_data["To_Pin Code"] and \
            not ewb_data["To_State"]:
            if isinstance(payload.get("BuyerDtls"), dict):
                ewb_data["To_Address1"] = payload["BuyerDtls"].get("Addr1", "")
                ewb_data["To_Address2"] = payload["BuyerDtls"].get("Addr2", "")
                ewb_data["To_Place"] = payload["BuyerDtls"].get("Loc", "")
                ewb_data["To_Pin Code"] = payload["BuyerDtls"].get("Pin", "")
                ewb_data["To_State"] = payload["BuyerDtls"].get("Stcd", "")

        # TRANSACTION TYEPE TRANSFORMATION
        disp_flag = isinstance(payload.get("DispDtls"), dict) and \
            not payload["DispDtls"].get("Nm") and not payload["DispDtls"].get("Addr1") and \
            not payload["DispDtls"].get("Addr2") and not payload["DispDtls"].get("Loc") and \
            not payload["DispDtls"].get("Pin") and not payload["DispDtls"].get("Stcd")

        ship_flag = isinstance(payload.get("ShipDtls"), dict) and \
            not payload["ShipDtls"].get("Gstin") and not payload["ShipDtls"].get("LglNm") and \
            not payload["ShipDtls"].get("TrdNm") and not payload["ShipDtls"].get("Addr1") and \
            not payload["ShipDtls"].get("Addr2") and not payload["ShipDtls"].get("Loc") and \
            not payload["ShipDtls"].get("Pin") and not payload["ShipDtls"].get("Stcd")

        if not ewb_data["FU 6"]:
            if "SellerDtls" in payload and "BuyerDtls" in payload and isinstance(\
                payload.get("ShipDtls"), dict) and not ship_flag and isinstance(\
                payload.get("DispDtls"), dict) and not disp_flag:
                ewb_data["FU 6"] = TRANS_TYPE_TRANSFORM["CMB"]
            elif "SellerDtls" in payload and "BuyerDtls" in payload and isinstance(\
                payload.get("ShipDtls"), dict) and not ship_flag:
                ewb_data["FU 6"] = TRANS_TYPE_TRANSFORM["SHP"]
            elif "SellerDtls" in payload and "BuyerDtls" in payload and isinstance(\
                payload.get("DispDtls"), dict) and not disp_flag:
                ewb_data["FU 6"] = TRANS_TYPE_TRANSFORM["DIS"]
            elif (not payload.get("DispDtls") and not payload.get("ShipDtls")) or (\
                disp_flag and ship_flag):
                ewb_data["FU 6"] = TRANS_TYPE_TRANSFORM["REG"]
            else:
                ewb_data["FU 6"] = TRANS_TYPE_TRANSFORM["REG"]

        # other charge FU 7 transformation
        if isinstance(payload.get("ValDtls"), dict) and isinstance(\
            payload["ValDtls"].get("OthChrg", 0), (int, float)) and isinstance(\
            payload["ValDtls"].get("StCesVal", 0), (int, float)) and isinstance(\
            payload["ValDtls"].get("Discount", 0), (int, float)) and isinstance(\
            payload["ValDtls"].get("RndOffAmt", 0), (int, float)):

            item_othchrg = 0
            try:
                if isinstance(payload.get("ItemList"), list):
                    item_othchrg = sum(map(itemgetter('OthChrg'), payload.get("ItemList")))
            except Exception:
                pass
            amount = item_othchrg + payload["ValDtls"].get("OthChrg", 0) + \
                payload["ValDtls"].get("StCesVal", 0) + \
                payload["ValDtls"].get("RndOffAmt", 0) - \
                payload["ValDtls"].get("Discount", 0)

            ewb_data["FU 7"] = round(amount, 8)
        else:
            ewb_data["FU 7"] = ""
        if not ewb_data["FU 7"] and config_dict.get("etl_json") and \
            config_dict["etl_json"].get("fu7_transformation") and \
            config_dict["etl_json"].get("fu7_transformation") == "Y":
            if payload.get("ItemList") and isinstance(payload.get("ItemList"), list):
                fu_amount = 0
                for row in payload.get("ItemList"):
                    if row and isinstance(row, dict):
                        if row.get("Fu7"):
                            if isinstance(row.get("Fu7"), (int, float)):
                                fu_amount += row.get("Fu7")
                            else:
                                try:
                                    fu_amount += round(float(row.get("Fu7").strip()), 8)
                                except Exception:
                                    pass
                if fu_amount:
                    ewb_data["FU 7"] = round(fu_amount, 8)

    @staticmethod
    def ewb_json_csv_parse(payload, ewb_list, config_dict):
        '''
        Summery Line.
            Here we are parsing einvoice json to ewb_details structure and
            create csv
        Parameters:
            payload(dict): request payload
            ewb_list(list): appending transform data(dict) to ewb_list
        Return:
            modifying ewb_list
            returning None
        '''
        start_time = time.time()
        LOGGER.info(f"Load ID: {payload['load_id']} |UDID: {payload['udid']} "\
            f"EWB CSV DATA Creation Start")
        ewb_data = copy.deepcopy(EWB_STRUCTURE_PAYLOAD)

        # get user gstin
        ewb_data['User GSTIN'] = payload.get('User_GSTIN', "")
        # Here we are mapping invoice level data
        for key in MAND_DATA_MAPPING:
            if key in payload and isinstance(payload[key], dict):
                for einvoice_key, ewb_key, dflt_val in MAND_DATA_MAPPING[key]:
                    ewb_data[ewb_key] = payload[key].get(einvoice_key, dflt_val)
        # einvoice data map
        for ei_key, ew_key, ew_dflt_val in DFLT_VAL_MAP:
            ewb_data[ew_key] = payload.get(ei_key, ew_dflt_val)
        if os.environ.get("customer_id", "") and os.environ.get("customer_id", "") == "435":
            ewb_data["is_ewaybill"] = "N"
        # version 1.03 changes
        EwbParse.version_103_transform(ewb_data, payload, config_dict)
        # default transformation
        EwbParse.default_transform(ewb_data)
        # Document Type Transformation
        upr_doc_type = ewb_data["Document Type"].upper()
        ewb_data["Document Type"] = DOC_TYPE_CONFIG[upr_doc_type] if \
            upr_doc_type in DOC_TYPE_CONFIG else ewb_data["Document Type"]
        # Transaction Type Transformation
        if payload.get("ewb_details") and "EwbNo" in payload['ewb_details']:
            if isinstance(payload['ewb_details'], str):
                payload['ewb_details'] = json.loads(payload['ewb_details'])
            ewbno = payload['ewb_details']['EwbNo']
            ewbdt = payload['ewb_details']['EwbDt']
            ewbvalidtill = payload['ewb_details']['EwbValidTill']
            ewb_data["FU 2"] = f"{ewbno}|"\
                f"{ewbdt if ewbdt else ''}|{ewbvalidtill if ewbvalidtill else ''}"
        upr_fu6 = ewb_data["FU 6"].upper()
        ewb_data["FU 6"] = TRAN_TYPE_CONFIG[upr_fu6] if \
            upr_fu6 in TRAN_TYPE_CONFIG else ewb_data["FU 6"]
        # STATE TRANSFROMATION
        for state in STATE_TRANSFORMATION_LIST:
            ewb_data[state] = STATE_CONFIG[ewb_data[state]] if \
                ewb_data[state] in STATE_CONFIG else ewb_data[state]
        # STATE NAME TRANSFORMATION
        for state_name in STATE_NAME_TRANS_LIST:
            if isinstance(ewb_data[state_name], str):
                upper_state = ewb_data[state_name].upper()
                ewb_data[state_name] = STATE_NAME_TRANS_DICT[upper_state] if \
                    upper_state in STATE_NAME_TRANS_DICT else ewb_data[state_name]

        # trans mode transform
        if ewb_data["Trans Mode"] in TRANS_MODE_TRANSFORM_DICT:
            ewb_data["Trans Mode"] = TRANS_MODE_TRANSFORM_DICT[ewb_data["Trans Mode"]]
        # Vehicle Type Transform
        if ewb_data["Vehicle Type"] in VEHICLE_TYP_TRANSFORM_DICT:
            ewb_data["Vehicle Type"] = VEHICLE_TYP_TRANSFORM_DICT[ewb_data["Vehicle Type"]]
        # original invoice number map
        EwbParse.orignal_invoice_no_dt_map(payload, ewb_data)
        # po_no, po_date map
        EwbParse.po_no_dt_map(payload, ewb_data)
        # transforming TranDtls_Typ
        EwbParse.trans_type_transform(payload, ewb_data)
        # not required currently but in the future this code can be required
        # # DATE TRANSFORM
        # for date_col in DATE_COL_LIST:
        #     if ewb_data[date_col]:
        #         ewb_data[date_col] = parse_date(ewb_data[date_col], "%Y-%m-%d", "%d/%m/%Y")
        # irn status map
        if payload.get("irn_status", "") == RESPONSE_MESSAGE["IRN_SUCCESS"]:
            ewb_data["irn_status"] = RESPONSE_MESSAGE["IRN_SUCCESS"]
        if payload.get("InfoDtls") and isinstance(payload.get("InfoDtls"), list):
            infodtls_list = []
            for info_dtls in payload.get("InfoDtls"):
                if isinstance(info_dtls, dict) and isinstance(info_dtls.get("InfCd"), str) and \
                    info_dtls.get("InfCd") == "EWBERR":
                    if isinstance(info_dtls.get("Desc"), list):
                        tmp_infodtls = [x["ErrorMessage"] for x in info_dtls.get("Desc") if \
                            "ErrorMessage" in x]
                        if tmp_infodtls:
                            infodtls_list.extend(tmp_infodtls)
            if infodtls_list:
                ewb_error = "<br>".join(infodtls_list)
                ewb_data["irn_status"] += f"|{ewb_error}"
        # start mapping line item data
        count = 1
        if "ItemList" in payload and isinstance(payload["ItemList"], list):
            for line_item in payload["ItemList"]:
                cp_ewb_data = copy.deepcopy(ewb_data)
                if isinstance(line_item, dict):
                    for e_inv_itm_key, ewb_item_key, itm_dflt_val in MAND_ITM_LVL_MAPPING:
                        cp_ewb_data[ewb_item_key] = line_item.get(e_inv_itm_key, itm_dflt_val)
                    # UNIT Transformation
                    cp_ewb_data["Unit"] = UNIT_CONFIG[cp_ewb_data["Unit"].upper()] if \
                        cp_ewb_data["Unit"].upper() in UNIT_CONFIG else cp_ewb_data["Unit"]

                    if not line_item.get("CgstRt") and not line_item.get("SgstRt") and \
                        payload.get("system_inter_intra", "") == "INTRA":
                        if line_item.get("GstRt") and isinstance(line_item.get("GstRt"), \
                            (int, float)):
                            rate = round(line_item.get("GstRt")/2, 8)
                            cp_ewb_data["CGST Rate"] = rate
                            cp_ewb_data["SGST Rate"] = rate
                    elif not line_item.get("IgstRt") and payload.get(\
                        "system_inter_intra", "") == "INTER":
                        if line_item.get("GstRt") and isinstance(line_item.get("GstRt"), \
                            (int, float)):
                            cp_ewb_data["IGST Rate"] = line_item.get("GstRt")
                count += 1
                ewb_list.append(cp_ewb_data)
        LOGGER.info(f"Load ID: {payload['load_id']} |UDID: {payload['udid']} "\
            f"EWB CSV Data Creation"\
            f"End |Total Time Taken {format((time.time() - start_time) * 1000, '.2f')}")
        return None

# def upload_csv(ewb_list, bucket_name, csv_format):
#     # pylint: disable-msg=W0703
#     # pylint: disable=E1101
#     '''
#     Summery Line.
#         Here we are creating csv and uploading to client bucket
#     Parameters:
#         ewb_list(list): dict of list
#         bucket_name(str): bucket name of client
#     Return:
#         None
#     '''
#     try:
#         LOGGER.info("EWB CSV Uploading Start")
#         writefile = StringIO()
#         wrcsv = csv.DictWriter(writefile, delimiter=',', fieldnames=EWB_CSV_HEADER, \
#             lineterminator='\n')
#         wrcsv.writeheader()
#         wrcsv.writerows(ewb_list)
#         s3_object = boto3.resource('s3')
#         csv_file_name = ''
#         random_num = str(random.randrange(1, 10000))
#         time_stamp = f"{datetime.datetime.now().strftime('%s')}_{random_num}"
#         time_stamp = f"Load_id__{ewb_list[0]['irn_load_id']}@{time_stamp}"
#         if csv_format and isinstance(csv_format, dict) and \
#             csv_format.get('created_by') and csv_format.get('load_type'):
#             if csv_format.get('created_by') != "Admin" and \
#                 csv_format.get('load_type') != "Automatic":
#                 csv_file_name = f"Document_Details@SAP@{csv_format['load_type']}@"\
#                     f"{csv_format['created_by']}-System@{time_stamp}"
#             else:
#                 csv_file_name = f"Document_Details@SAP@{time_stamp}"
#         else:
#             csv_file_name = f"Document_Details@SAP@API@Admin@{time_stamp}"

#         file_name = f"incoming-file/{csv_file_name}.csv"
#         s3_object.Object(bucket_name, file_name).put(Body=writefile.getvalue())
#         LOGGER.info(f"EWB CSV File Successfully Uploaded To S3 Bucket")
#     except Exception as error:
#         LOGGER.error(f"EXCEPTION: CSV UPLOADING Exception -> {error}", exc_info=True)
#     return


def remove_special_characters(data):
    try:
        #initialization
        result = data if data else ''
        #remove special characters
        result = ''.join(ch for ch in data if ch.isalnum())
    except Exception as error:
        LOGGER.error(f"EXCEPTION: While removing special characters-> {error}", exc_info=True)
    finally:
        return result



def upload_csv(ewb_list, bucket_name, csv_format):
    # pylint: disable-msg=W0703
    # pylint: disable=E1101
    '''
    Summery Line.
        Here we are creating csv and uploading to client bucket
    Parameters:
        ewb_list(list): dict of list
        bucket_name(str): bucket name of client
    Return:
        None
    '''
    flag = False
    csv_file_name = ""
    try:
        LOGGER.info("EWB CSV Uploading Start")
        csv_file_name = ''
        document_no = ""
        if isinstance(ewb_list[0], dict) and isinstance(ewb_list[0].get("Document No"), str):
            document_no = remove_special_characters(ewb_list[0].get("Document No"))
        # random_num = str(random.randrange(1, 100000))
        random_num = str(secrets.SystemRandom().randrange(1, 100000))
        time_stamp = f"{datetime.datetime.now().strftime('%s')}_{random_num}"
        time_stamp = f"Load_id__{ewb_list[0]['irn_load_id']}@{time_stamp}"
        if csv_format and isinstance(csv_format, dict) and \
            csv_format.get('created_by') and csv_format.get('load_type'):
            if csv_format.get('created_by') != "Admin" and \
                csv_format.get('load_type') != "Automatic":
                csv_file_name = f"Document_Details@SAP@{csv_format['load_type']}@"\
                    f"{csv_format['created_by']}-System@{time_stamp}_{document_no}"
            else:
                csv_file_name = f"Document_Details@SAP@{time_stamp}_{document_no}"
        else:
            csv_file_name = f"Document_Details@SAP@API@Admin@{time_stamp}_{document_no}"
        csv_file_name = f"{csv_file_name}.csv"
        LOGGER.info(f"File name is {csv_file_name}")
        file_name = f"/tmp/{csv_file_name}"
        with open(file_name, "w") as wfile:
            wrcsv = csv.DictWriter(wfile, delimiter=',', fieldnames=EWB_CSV_HEADER, \
                lineterminator='\n')
            wrcsv.writeheader()
            wrcsv.writerows(ewb_list)
            flag = True
        LOGGER.info(f"EWB CSV File Successfully Uploaded To S3 Bucket")
    except Exception as error:
        LOGGER.error(f"EXCEPTION: CSV UPLOADING Exception -> {error}", exc_info=True)
    return flag, csv_file_name
