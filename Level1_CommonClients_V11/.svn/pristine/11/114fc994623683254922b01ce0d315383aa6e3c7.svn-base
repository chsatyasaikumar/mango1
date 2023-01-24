import pandas as pd
import numpy as np
import logging
from sap_module.sap_configuration import DEFAULT_HEADER_3 as final_header
from sap_module.sap_mapping import mapping_data
from comman_module.configuration import STATE_CODE_CONFIG

# final_header = DEFAULT_HEADER_2

def transform_dataframe(filepath, data, mapping_dict, created_by_user, source_type, bucket, master_config):
    dframe = pd.read_csv(filepath,encoding="ISO-8859-1", dtype=object)
    dframe = dframe.fillna("")
    sap_mapping_dict = mapping_dict["sap_config"]
    mapping_dict = mapping_dict["custom_config"]
    try:
        incoming_renamed_headers = list(dframe.columns.values)
        if mapping_dict.get("rename_headers"):
            #headers renaming as per standard format
            dframe.rename(columns=mapping_dict.get("rename_headers"), inplace=True)
        for header in final_header:
            if header not in incoming_renamed_headers:
                dframe[header] = ""
        # column exchange
        if mapping_dict.get("exchange_col"):
            set_excahnge_col(dframe, mapping_dict.get("exchange_col"))
        
        # default col value map
        if mapping_dict.get("default_value"):
            set_default_value(dframe, mapping_dict.get("default_value"))
        # conditonal transform
        if mapping_dict.get("conditonal_change"):
            set_condtional_change(dframe, mapping_dict.get("conditonal_change"))

        # multiple conditional transform
        if mapping_dict.get("two_condition"):
            if mapping_dict.get("two_condition")["or_condition"]:
                two_or_condition(dframe,mapping_dict.get("two_condition")["or_condition"])

        # convert to postive
        if mapping_dict.get("convert_to_positive") and \
        len(mapping_dict.get("convert_to_positive")) > 0:
            mapping_dict(dframe,mapping_dict['convert_to_positive'])

        logging.info(f"length of final headers -> {len(list(dframe.columns.values))}")
        dframe = dframe.fillna("")
        if mapping_dict.get("client_condition") and mapping_dict["client_condition"].get(\
            "function_name"):
            func = eval(mapping_dict["client_condition"].get("function_name"))
            dframe = func(dframe,master_config)

        new_dframe = pd.DataFrame()
        for column in final_header:
            if column in dframe:
                new_dframe[column] = dframe[column]
            else:
                new_dframe[column] = ''
        # new_dframe.to_csv(r'C:\Users\Bansal\Desktop\output3.csv', index=False)
        # exit(0)
        print("CUSTOM Mapping Done")
    except Exception as error:
        logging.error(f"Exception Occured {str(error)}", exc_info=True)
        logging.info("Transformation STANLEY Step-1 Failed")
        logging.error('Custom Mapping',exc_info=True)
    
    return mapping_data(filepath, data, sap_mapping_dict, created_by_user, source_type, bucket, master_config, custom_frame = new_dframe)


def set_condtional_change(dframe, condition_list):
    '''
    Summery line.
        Here we are transformming the conditionl value
    Parameters:
        dframe(pd): pandas data frame
        condition_list(list): contain multiple condition change condition
    '''
    for raw in condition_list:
        dframe[raw["target_col"]] = np.where(\
            dframe[raw['source_col']].str.upper() == raw["source_value"], \
            raw["target_value"], dframe[raw["else_col"]])

def set_excahnge_col(dframe, exchange_dict):
    '''
    Summery Line
        Here we are exchanging the col value
    Parameters:
        dframe(pd): dataframe
        exchange_dict(dict): excahnge col details
    '''
    for key, value in exchange_dict.items():
        dframe[key] = dframe[value]

def set_default_value(dframe, default_dict):
    '''
    Summery Line
        Here we are mapping the default value
    Parameters:
        dframe(pd): dataframe
        default_dict(dict): defult value configuration
    '''
    for key, value in default_dict.items():
        dframe[key] = value


def convert_float(data):
    try:
        x=0.0
        x = float(str(data).replace(' ','').replace(',',''))
    except Exception as error:
        print(f'Error -> {error}')
    finally:
        return x

def convert_int(data):
    try:
        x=0
        x = int(float(str(data).replace(' ','').replace(',','')))
    except Exception as error:
        print(f'Error -> {error}')
    finally:
        return x

def two_or_condition(dframe, condition_list):
    '''
    Summery line.
        Here we are transformming the conditionl value
    Parameters:
        dframe(pd): pandas data frame
        condition_list(list): contain multiple or condition change condition
    '''
    for raw in condition_list:
        dframe[raw['target_column']] = np.where(\
            (dframe[raw['source_one_col']] == raw['source_one_val']) \
            | (dframe[raw['source_two_col']] == raw['source_two_val']), \
            raw['target_val'], dframe[raw['else_col']])


def transform_description(data):
    try:
        result = data.strip()
        if "Alere G1 Strips" in result and "100 pack" in result:
            result = "Alere G1 Strips - 100 pack"
    except Exception as error:
        print(f"unable to transform description: {data}")
        result = data
    finally:
        return result


def alere_medical(dframe,master_config):
    location_code_master = master_config.get('location_code_master',{})
    location_code_mapping_master = master_config.get('location_code_mapping_master',{})
    customer_code_mapping_master = master_config.get('customer_code_mapping_master',{})

    def map_data(row):
        try:
            if row['From_Address1']:
                add = location_code_master.get(row['From_Address1'].strip(),'')
                add = location_code_mapping_master.get(add)
                if add:
                    row['From_Address1'] = add.get('address1','')
                    row['From_Address2'] = add.get('address2','')
                    row['From_Pin Code'] = add.get('pincode','')
                    # row['From_State'] = add.get('state','')
                    row['From_Place'] = add.get('place','')
            #description
            if row['Description']:
                row['Description'] = transform_description(row['Description'])


            if row['Bill To_State']:
                code = customer_code_mapping_master.get(row['Bill To_State'].strip(),{})
                if code:
                    row['Bill To_State'] = code.get('state','')
                    row['To_Address1'] = code.get('address1','')
                    row['To_Address2'] = code.get('address2','')
                    row['To_Place'] = code.get('place','')
                    row['To_Pin Code'] = code.get('pincode','')
                    row['To_State'] = code.get('state','')

            if row['Bill From_State'] :
                row['Bill From_State'] = STATE_CODE_CONFIG.get(row['Bill From_State'][:2],'')
                row['From_State'] = row['Bill From_State']
            else:
                row['Bill From_State'] =''
                row['From_State'] = ''

            #To_GSTIN
            if not row['To_GSTIN']:
                row['To_GSTIN'] = 'URP'
            #Unit
            if row['Unit'] and row['Unit'].upper() in ["EA","NOS"]:
                row['Unit'] = 'NUMBERS'
            
            #Calculate CGST Rate, SGST Rate, IGST Rate
            try:
                if row.get('GST','').upper() == 'JOIG':
                    row['IGST Rate'] = convert_int(row['GST %'])
                    row['SGST Rate'] = 0
                    row['CGST Rate'] = 0
                elif (row.get('GST','').upper() in ['JOCG,JOSG']):
                    row['CGST Rate'] = convert_float(row.get('GST %'))/2
                    row['SGST Rate'] = convert_float(row.get('GST %'))/2
                    row['IGST Rate'] = 0
                else:
                    row['CGST Rate'] = 0
                    row['SGST Rate'] = 0
                    row['IGST Rate'] = 0
            except Exception as error:
                print(f"Error->{error}")
                row['CGST Rate'] = 0
                row['SGST Rate'] = 0
                row['IGST Rate'] = 0

            row['Taxable value'] = convert_float(row.get('Taxable value'))
            row['Quantity'] = str(convert_int(row['Quantity']))

            # # converting taxable value into float
            row['CGST Amount'] = '%.2f' % ((row['CGST Rate'] * row['Taxable value']) / 100)
            row['SGST Amount'] = '%.2f' % ((row['SGST Rate'] * row['Taxable value']) / 100)
            row['IGST Amount'] = '%.2f' % ((row['IGST Rate'] * row['Taxable value']) / 100)
            #logic for exclusion
            row['is_ewaybill_exclude'] = ''
            hsn = str(row['HSN'].strip())
            if hsn and hsn[:2] == '99':
                row['is_ewaybill_exclude'] = 'Y'
            return pd.Series([row['From_Address1'],row['From_Address2'],\
                row['From_Pin Code'],row['From_State'],row['From_Place'],
                row['Bill To_State'],row['To_Address1'],row['To_Address2'],\
                row['To_Place'],row['To_Pin Code'],row['To_State'], row['Bill From_State'],\
                row['CGST Rate'], row['SGST Rate'],row['IGST Rate'],\
                row['CGST Amount'], row['SGST Amount'], row['IGST Amount'], row['Taxable value'], row['To_GSTIN'],\
                row['Unit'], row['is_ewaybill_exclude'], row['Description']])
        except:
            logging.error('alere_madical_function',exc_info=True)

    dframe[['From_Address1','From_Address2','From_Pin Code','From_State','From_Place',\
        'Bill To_State','To_Address1','To_Address2','To_Place','To_Pin Code','To_State',\
        'Bill From_State', 'CGST Rate','SGST Rate','IGST Rate',\
        'CGST Amount', 'SGST Amount', 'IGST Amount', 'Taxable value', 'To_GSTIN','Unit', 'is_ewaybill_exclude','Description']]= dframe.apply(map_data, axis=1)
    return dframe