### DRIVER FUNCTION

'''
The purpose of this Script is to develop the machine learning driver function that will direct
the components of our ML algorithm data prep and result generation. 
'''



### IMPORT LIBRARIES____________________________________________________________________
import pandas as pd
import mysql.connector
import os
import matplotlib.pyplot as plt
from sklearn import preprocessing


### DIRECTORY OBJECTS_________________________________________________________________
code_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Code'
output_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Scraper_output'

### IMPORT MODULES_____________________________________________________________________
os.chdir(code_dir)
import Module_0_utility_functions as m0
import Module_7_DataAnalysis as m7
import Module_8_Machine_Learning_functions as m8


### Directory object(s)
target_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Scraper_output'

### SQL INSTANCIATION__________________________________________________________________
mydb = mysql.connector.connect(
        host="localhost",
        user="ccirelli2",
        passwd="Work4starr",
        database='SCA_SCRAPER')

### PREPARE DATASET_____________________________________________________________________

def prepare_dataset(conn, year):
    '''
    Purpose:    Prepare the dataset that we will use for our machine learning model
    Conn:       mysql connection
    Year:       Min year to be used to limit dataset to years > than this value
    Output:     Dataset prepared for ML algorithm
    '''

    # 1.) Import SCA_data 
    '''Input:  Year_Filed to exclude'''
    df_SCA_data_table = m7.sql_query_executor(conn, m8.sql_query_machine_learning_data_set(year))

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
    df_transform_case_status = m8.transform_target_binary(df_drop_columns)

    # 4.) Transform Plaintiff Firm - Limit to first 25 Characters
    df_transform_plaintiff_firm = m8.transform_plaintiff_firm(df_transform_case_status)
        


    # Return Transformed Dataset
    return df_transform_plaintiff_firm

ML_data_set = prepare_dataset(mydb, 2000)


print(ML_data_set.shape)


### MACHINE LEARNING PIPELINE___________________________________________________________

# Step1:  OneHotEncode DataFrame
df_encoded = pd.get_dummies(ML_data_set)

# Step2:  Separate X & Y Variables
'''Target column = 'Target_case_status_binary'''
X = df_encoded.drop('Target_case_status_binary', axis = 1)
Y = df_encoded['Target_case_status_binary']











# Scikit Learn - Decision Tree-------------------------------------------------------



# 



































