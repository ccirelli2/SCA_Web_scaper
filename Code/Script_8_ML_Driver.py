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
import numpy as np

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

# Year Range
min_year_value = 2000
max_year_value = 2018

# Generate Dataset
ML_data_set = m8.prepare_dataset(mydb, min_year = min_year_value, 
                                       max_year = max_year_value).fillna(0)



### DATA ENCODING & SPLIT___________________________________________________________

# Step1:  OneHotEncode DataFrame
df_encoded = pd.get_dummies(ML_data_set)

# Step2:  Separate X & Y Variables
'''Target column = 'Target_case_status_binary'''
X = df_encoded.drop('Target_case_status_binary', axis = 1)
Y = df_encoded['Target_case_status_binary']


### NEAREST NEIGHBOR________________________________________________________________
# Test Different Number of Nearest Neighbors
'''
KNN_results = m8.train_KNN_predictor(X,Y, 62, min_year_value, max_year_value, 
                                    plot = True)'''
# Test Unique Select Num Neighbor, Generate Confusion Matrix
'''
knn_result = m8.train_KNN_single_neighbor_classifier(X, Y, NN = 2,
                                            random_state_value = 62, 
                                            result = 'precision_score')'''

### LOGISTIC REGRESSION___________________________________________________________
'''
log_reg = m8.train_log_regressor_classifier(X, Y, 62, 'precision_score')
print(log_reg)
'''

### NAIVE BAYES__________________________________________________________________
'''
Naive_bayes = m8.train_NaiveBayes_classifier(X,Y, 62, 'Multinomial', 'precision_score')
print(Naive_bayes) '''

### RANDOM FOREST__________________________________________________________________
'''
RF_classifier =  m8.train_RandomForecast_classifier(X,Y, 62, 'precision_score')
print(RF_classifier)'''



### CLASSIFIER PIPELINE (NAIVE BAYES, RANDOM FOREST, LOGISTIC REGRESSION, KNN)_____________

def generate_ml_pipeline(X, Y, random_state_input, result_input, output):

    # Capture Classifier Results
    KNN_score_list = []
    Log_reg_score_list = []
    NB_score_list = []
    RandomForest_score_list = []

    # Generate Predictions
    KNN_result = m8.train_KNN_single_neighbor_classifier(X, Y, 5, random_state_input, result_input)
    Log_reg_result = m8.train_log_regressor_classifier(X, Y, random_state_input, result_input)   
    Naive_bayes_result = m8.train_NaiveBayes_classifier(X,Y, random_state_input, 'Multinomial', 
                                                        result_input)
    RandomForest_result =  m8.train_RandomForecast_classifier(X,Y, random_state_input, 
                                                        result_input)
    # Append Predictions to List
    KNN_score_list.append(         round(KNN_result,2))
    Log_reg_score_list.append(     round(Log_reg_result,2))
    NB_score_list.append(          round(Naive_bayes_result,2))
    RandomForest_score_list.append(round(RandomForest_result,2))

    # Generate DataFrame
    df_results = pd.DataFrame({}, index = [result_input])
    df_results['KNN'] = KNN_score_list
    df_results['Logistic_Reg'] = Log_reg_score_list
    df_results['Naive_Bayes'] = NB_score_list
    df_results['Random_Forest'] = RandomForest_score_list

    # Output
    if output == 'write2excel':
        # Write to Excel
        m0.write_to_excel(df_results, 'MachineLearning_Pipeline_Output: {}'.format(result_input), 
                          target_dir)
     
    elif output == 'plot':
        # Plot Results
        x_labels = ['KNN', 'Logistic_Regression', 'Naive_Bayes', 'Random_Forest']
        
        y_values = [df_results['KNN'][0], df_results['Logistic_Reg'][0], 
                    df_results['Naive_Bayes'][0], df_results['Random_Forest'][0]
                    ]
        plt.bar(x_labels, y_values, align = 'center', alpha = 0.5) 
        plt.xlabel('Algorithms', fontsize = 15)
        plt.ylabel(result_input, fontsize = 15)
        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)
        plt.title('''Machine Learning Algorithm Comparison
                     Years:  From {} To {}
                     Score:  {}'''.format(min_year_value, max_year_value, result_input), 
                     fontsize = 20)
        plt.show()
       

    elif output == 'print':
        print(df_results.transpose())

# RUN PIPELINE______________________________________________________________________

generate_ml_pipeline(X, Y, random_state_input = 62, result_input = 'recall_score', 
                    output = 'plot')


    
























# Graph Comparison - Average Performance All Features vs Dropping Derived Values____________
'''
m8.graph_comparison_performance_features()
'''



# Group Feature Importance by Major Cateogry________________________________________________

def gen_feature_groups():
    target_file = r'Feature_Importance_2018-12-03 17:29:11.854574.xlsx'
    target_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/ML_Algorithm_Results'

    Feature_importance_results = m8.record_feature_importance_ungrouped_categories(df, 
                                    generate_sum_importance_ungrouped_features, 
                                                     target_dir, target_file)
    m0.write_to_excel(Feature_importance_results, 'Feature_importance_results_manual_generate', 
            target_dir)
    
    return None





















