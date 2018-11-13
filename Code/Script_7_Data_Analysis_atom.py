# SCA DATA ANALYSIS

# Import libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

# File Objects
Dir_file = '/home/ccirelli2/Desktop/Programming/SCA_Web_scaper'
Data_file = '/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/SCA_data_export_11.08.2018.csv'
# Create dataframe
os.chdir(Dir_file)
df = pd.read_csv(Data_file)
df_fill_na = df.fillna(0)
columns = df_fill_na.columns
#print(columns)


group_by_case_status = df_fill_na.groupby(['case_status']).sum()

group_by_case_status_count = df_fill_na.groupby(['case_status']).sum()

print(group_by_case_status_sum.loc['Dismissed'])
 
