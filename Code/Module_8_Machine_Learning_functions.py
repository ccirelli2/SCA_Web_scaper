### PURPOSE: 
'''
To house the functions to prepare our dataset for the ML Functions
'''

## Import Packages
import pandas as pd
from sklearn import preprocessing





def sql_query_machine_learning_data_set(year):
    '''Purpose:  Initial query of db to retrieve data for ML application'''
    Query = '''SELECT * 
               FROM SCA_data
               WHERE case_status IS NOT NULL
               AND YEAR_FILED > {}
               AND case_status != 'ongoing';'''.format(year)
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















