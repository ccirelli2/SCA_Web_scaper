### PURPOSE
'''
The purpose of this script is to house certain utility functions that are applicable to a wide
range of functions and different scripts. 

'''

# Import Libraries
import os
from datetime import datetime
import pandas as pd


def write_to_excel(dataframe, filename, target_dir):
    os.chdir(target_dir)
    filename = filename + '_' + str(datetime.today())
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, 'Data')
    print('Dataframe {} has been written to {}'.format(filename, target_dir))
    writer.save()


# Note:  Add a generalized counter object that can be used for 


