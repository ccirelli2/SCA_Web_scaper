'''DOCUMENTATION

Script:     This script contains the functions that will be used to prepare the dataset
            our dataset for the machine learning model
'''

## Import Packages
import pandas as pd
from sklearn import preprocessing

## Import Project Modules
import Module_7_DataAnalysis as m7



def sql_query_machine_learning_data_set(year):
    '''Purpose:  Initial query of db to retrieve data for ML application'''
    Query = '''SELECT *
               FROM SCA_data
               WHERE case_status IS NOT NULL
               AND YEAR_FILED > {}
               AND case_status != 'ongoing'
               AND Plaintiff_firm != 'Error'
               AND Judge != 'None'
               AND CHAR_LENGTH(Judge) > 2
               ;'''.format(year)
    return Query



def transform_target_binary(df):
    '''Purpose:  Convert the column with our target value to 1/0.
    1         Dismissed
    0         Settled
    '''
    # Create List to Capture Binary Values
    List_case_status_binary = []
    # Isolate the Case_status column
    Series_case_status = df['case_status']
    # Iterate the series and append values to our the list_case_status object
    for x in Series_case_status:
        if x == 'Dismissed':
            List_case_status_binary.append(1)
        elif x == 'Settled':
            List_case_status_binary.append(0)
        else:
            print('values other than dismissed and settled found in case_summary column')
    # Create a new column with binary representations
    df['Target_case_status_binary'] = List_case_status_binary
    # Drop old column
    df_final= df.drop(labels = 'case_status', axis = 1)

    return df_final


def transform_plaintiff_firm(df):
    '''Purpose is to shorten the name of the plaintiff firm in order to aviod issues differences
    that could arise with punctuation or text variations with a longer name, thereby avoiding
    a situation in which the same plaintiff firm comes up twice.
    '''
    List_plaintiff_firm_modified = []
    series_plaintiff_firm = df['Plaintiff_firm']
    for x in series_plaintiff_firm:
        List_plaintiff_firm_modified.append(x[:25])
    df['Plaintiff_firm_modified'] = List_plaintiff_firm_modified
    df_final = df.drop(labels = 'Plaintiff_firm', axis = 1)
    return df_final

def get_list_attributes_by_type(Type):

    if Type == 'categorical':
        return ['Sector', 'Industry', 'Headquarters', 'Company_market', 'Court',
       'Judge', 'Plaintiff_firm_modified']
    elif Type == 'numerical':
        return ['Breach_Fiduciary_Duties', 'Merger', 'Proxy_violation',
       'Related_parties', 'Stock_Drop', 'Cash_Flow', 'Revenue_Rec',
       'Net_Income', 'Customers', 'Fourth_Quarter', 'Third_Quarter',
       'Second_Quarter', 'Press_Release', '10K_Filling', '10Q_Filling',
       'Corporate_Governance', 'Conflicts_Interest', 'Accounting', 'Fees',
       'Failed_disclose', 'False_misleading', 'Commissions', 'Bankruptcy',
       'Secondary_Offering', 'IPO', '1934_Exchange_Act', 'Derivative', '10b5',
       '1933_Act', 'Heavy_trading', 'Sexual_Misconduct', 'class_action',
       'ERISA', 'FCPA', 'SEC_Investigation', 'Data_breach', 'Proxy',
       'Class_Duration']


### ONE HOT ENCODING PREPARATION____________________________________________________
def Encode_categorical_data(df, List_attributes_by_type):
    le = preprocessing.LabelEncoder()
    Attributes_categorical = df[List_attributes_by_type]
    Attributes_encoded = Attributes_categorical.apply(le.fit_transform)
    return Attributes_encoded


### Driver Function - Prepare Data Set
'''Includes all the above functions to prepare dataset'''
def prepare_dataset(conn, year):
    '''
    Purpose:    Prepare the dataset that we will use for our machine learning model
    Conn:       mysql connection
    Year:       Min year to be used to limit dataset to years > than this value
    Output:     Dataset prepared for ML algorithm
    '''

    # 1.) Import SCA_data
    '''Input:  Year_Filed to exclude'''
    df_SCA_data_table = m7.sql_query_executor(conn, sql_query_machine_learning_data_set(year))

    # 2.) Drop Columns - Defendant_address, case_summary, page_number
    '''Based on our preliminary analysis, these two columns were not propertly scraped and contain
    too many null values to be included in our final dataset. Therefore, they will be dropped
    '''
    df_drop_columns = df_SCA_data_table.drop(labels = ['defendant_address', 'case_summary',
                                                        'page_number', 'Ref_court', 'Ref_docket',
                                                        'Ref_judge', 'Ref_date_filed',
                                                        'Ref_class_period_start',
                                                        'Ref_class_period_end',
                                                        'filling_date', 'defendant_name',
                                                        'close_date', 'Date_Filed', 'Docket',
                                                        'Class_Period_Start', 'Class_Period_End',
                                                        'Symbol', 'YEAR_FILED', 'Status_2'], axis = 1)

    # 3.) Convert case_status to binary, where 1 = 'dimissed', 0 = 'settled'
    df_transform_case_status = transform_target_binary(df_drop_columns)

    # 4.) Transform Plaintiff Firm - Limit to first 25 Characters
    df_transform_plaintiff_firm = transform_plaintiff_firm(df_transform_case_status)



    # Return Transformed Dataset
    return df_transform_plaintiff_firm
