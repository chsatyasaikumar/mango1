'''
Here we are transforming the client level data
'''
import traceback
import pandas as pd

class ClientTransform:
    '''
    Summery Line
        Client Transform
    '''
    def __str__(self):
        '''
        Summery Line
            object representation
        '''
        return "ClientTransform object"

    @staticmethod
    def tml_apply(row):
        '''
        Summery Line
            tml apply function
        Parameters
            row(dict): row data
        '''
        copy_row = row.copy()
        fu_3 = copy_row["FU 3"]
        if copy_row["Document No"]:
            if copy_row["Document No"].startswith("3"):
                fu_3 = "PV"
            elif len(copy_row["Document No"]) > 2 and copy_row["Document No"][2] == "5":
                fu_3 = "PV"
            else:
                fu_3 = "CV"
        else:
            fu_3 = "CV"
        return pd.Series([fu_3])

    @staticmethod
    def tml_transform(dframe):
        '''
        Summery Line
            Tml Transformation
        Parameters:
            dframe(dataframe)
        '''
        dframe[["FU 3"]] = dframe.apply(ClientTransform.tml_apply, axis=1)

    @staticmethod
    def whirlpool_transform(dframe, custom_config):
        '''
        Summery Line.
            whirlpool transformation
        '''
        master_config = custom_config.get("address_config", {})
        def map_data(copy_row):
            row = copy_row.copy()
            try:
                master_data_by_mis_6 = master_config.get(row['MIS 6'].upper().strip(), '')
                if master_data_by_mis_6:
                    row['To_Address1'] = master_data_by_mis_6.get('Address Line 1', '')
                    row['To_Address2'] = master_data_by_mis_6.get('Address Line 2','')
                    row['To_Place'] = master_data_by_mis_6.get('Place', '')
                    row['To_Pin Code'] = master_data_by_mis_6.get('Pincode', '')
                    row['To_State'] = master_data_by_mis_6.get('State', '')
            except Exception as error:
                print(f"Exception Occured {str(error)}")
                traceback.print_exc()
            # return row
            return pd.Series([row["To_Address1"], row["To_Address2"], row["To_Place"], \
                row["To_Pin Code"], row["To_State"]])
        
        dframe[["To_Address1", "To_Address2", "To_Place", "To_Pin Code", \
            "To_State"]] = dframe.apply(map_data, axis=1)
        return dframe

    @staticmethod
    def client_process(dframe, config):
        '''
        Summery Line
            Client transformation process
        Parameters:
            dframe: data frame
            config(dict): client transformation
        '''
        for key, value in config.items():
            func = eval(value)
            func(dframe)
        return dframe

    @staticmethod
    def client_process_v2(dframe, config):
        '''
        Summery Line
            Client transformation process
        Parameters:
            dframe: data frame
            config(dict): client transformation
        '''
        try:
            print("v2 client transformation starts")
            func = eval(config.get("client_condition_v2"))
            dframe = func(dframe, config)
        except Exception as error:
            print("client transformation has been failed")
            traceback.print_exc()
        print("v2 client transformation end")
        return dframe
