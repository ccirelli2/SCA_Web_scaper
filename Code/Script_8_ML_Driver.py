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

# KNN
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# Logistic Regression
from sklearn.linear_model import LogisticRegression


### DIRECTORY OBJECTS_________________________________________________________________
code_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Code'
output_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/ML_Algorithm_Results'

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
ML_data_set = m8.prepare_dataset(mydb, 2015).fillna(0)

### DATA ENCODING & SPLIT___________________________________________________________

# Step1:  OneHotEncode DataFrame
df_encoded = pd.get_dummies(ML_data_set)

# Step2:  Separate X & Y Variables
'''Target column = 'Target_case_status_binary'''
X = df_encoded.drop('Target_case_status_binary', axis = 1)
Y = df_encoded['Target_case_status_binary']


m8.train_RandomForecast_predictor_pipeline_version(X,Y, 42)



### NEAREST NEIGHBOR________________________________________________________________
'''
m8.train_KNN_predictor(X,Y)
'''

### KNN - ITERATE YEAR FILED TOWARD PRESENT_____________________________________
'''
range_object = range(2000, 2017)
m8.train_KNN_predictor_iterate_over_range_years(mydb, range_object, 3)
'''



### MACHINE LEARNING PIPELINE_________________________________________________________

def create_ml_pipeline(range_object, random_state_value, C_value, write2excel, num_neighbors,
                        limit_col_list, feature_selection_limits):
    '''KNN & Logistic Regression algorithms'''

    # Capture Prediction Values
    KNN_score_list = []
    Log_reg_score_list = []
    BernoulliNB_score_list = []
    RandomForest_score_list = []

    # Capture min-year filed
    min_year_filed = []

    # Iterate over range object
    for year in range_object:
        # Append min year
        min_year_filed.append(year)
        # Prepare Data Set
        ML_data_set = m8.prepare_dataset(mydb, year).fillna(0)
        # Limit Features 2 Include In Algorithm
        ML_data_set = m8.limit_feature_selection(ML_data_set, feature_selection_limits)
        # OneHotEncode DataFrame
        df_encoded = pd.get_dummies(ML_data_set)
        # Step2:  Separate X & Y Variables
        X = df_encoded.drop('Target_case_status_binary', axis = 1)
        Y = df_encoded['Target_case_status_binary']

        # Generate Predictions
        KNN_score_list.append(m8.train_KNN_predictor_pipeline_version(X, Y, 60, num_neighbors))
        Log_reg_score_list.append(m8.train_log_regressor_pipeline_version(X, Y, 60, 1))
        BernoulliNB_score_list.append(m8.train_NaiveBayes_predictor_pipeline_version(X,Y, random_state_value,
                                                                                    'Bernoulli'))
        RandomForest_score_list.append(m8.train_RandomForecast_predictor_pipeline_version(X,Y, random_state_value))

    # Write Results To Excel
    if write2excel == True:
        df = pd.DataFrame({}, index = [[x for x in range_object]])
        df['KNN_test_score'] = KNN_score_list
        df['LogReg_test_score'] = Log_reg_score_list
        df['BernoulliNB_score'] = BernoulliNB_score_list
        df['RandomForest_score'] = RandomForest_score_list
        m0.write_to_excel(df, 'KNN_LogReg_NB_output', output_dir)

    # Plotting
    x_label_range_year = [x for x in range_object]
    plt.plot(x_label_range_year, KNN_score_list, label = 'KNN_test_score')
    plt.plot(x_label_range_year, Log_reg_score_list, label = 'Log_reg_test_score')
    plt.plot(x_label_range_year, BernoulliNB_score_list, label = 'Bernoulli_NB_test_score')
    plt.plot(x_label_range_year, RandomForest_score_list, label = 'RandomForest_test_score')
    plt.ylabel('Accuracy', fontsize = 20)
    plt.xlabel('Range of Years Case Was Filed' , fontsize = 20)
    plt.title('''Comparison: KNN, Log_Reg, NaiveBayes, Random_Forest
                 Year Range => {}
                 Number of Neighbors => {}
                 Features_dropped = {}'''.format('2000-2018', str(num_neighbors),
                                                 feature_selection_limits)
                 , fontsize = 30)
    plt.legend(fontsize = 15)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(b=None, which='major')
    plt.show()

# Run Pipeline:
'''
range_object = range(2000, 2017)
create_ml_pipeline(range_object, random_state_value = 42, C_value = 1, write2excel = True,
                   num_neighbors = 3, limit_col_list = m8.list_categorical_features,
                   feature_selection_limits = 'Drop_merger_value')
'''



# Graph Comparison - Average Performance All Features vs Dropping Derived Values
'''
m8.graph_comparison_performance_features()
'''
