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


### NEAREST NEIGHBOR________________________________________________________________
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

def train_KNN_predictor(X, Y):
    '''Documentation:
    random_state:      seed used by the random generator.
    stratify:          separation of data into homogenious groups before sampling.
    range:             range over which to iterate to generate predictions
    lists:             capture predictions

    '''
    # Split dataset
    x_train, x_test, y_train, y_test = train_test_split(
                                        X, Y,
                                        stratify = Y,
                                        random_state = 66)

    # Lists to Capture Predictions
    accuracy_training_list = []
    accuracy_test_list = []

    # Range of Nearest Neighbors
    num_range_neighbors = range(1,10)
    # Run Loop
    for num in num_range_neighbors:
        # Instantiate KNN Algorithm
        knn = KNeighborsClassifier(n_neighbors = num)
        # Fit algorithm to training data
        knn.fit(x_train, y_train)
        accuracy_training_list.append(knn.score(x_train, y_train))
        accuracy_test_list.append(knn.score(x_test, y_test))

    # Write Results To Excel
    df = pd.DataFrame({}, index = [2,3,4,5,6,7,8,9,10])
    df['Accuracy_Training'] = accuracy_training_list
    df['Accuracy_Test'] = accuracy_test_list
    m0.write_to_excel(df, 'KNN_output', output_dir)

    # Plotting
    plt.plot(num_range_neighbors, accuracy_training_list, label = 'Accuracy of training')
    plt.plot(num_range_neighbors, accuracy_test_list, label = 'Accuracy of test')
    plt.ylabel('Accuracy', fontsize = 20)
    plt.xlabel('Number of Neighbors' , fontsize = 20)
    plt.title('Performance KNN Algorithm SCA Dataset', fontsize = 30)
    plt.legend(fontsize = 15)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.show()

    # Return Results in df object
    return df

#train_KNN_predictor(X,Y)




### KNN - ITERATE YEAR FILED TOWARD PRESENT_____________________________________
'''Documentation
Objective:          The objective is to test the hypothesis that there will be a
                    positive relationship between the accuracy of our model and
                    using more recent data.  The underlying assumption is that due
                    to a plethora of reasons, including by not limited to changes
                    in jurisprudence and status, how the outcome of cases are decided
                    will be more homogeneous the nearer we are to the present.
range_object:       This object will determine which data we pull into our algorithm
                    organized by yearself.
prepare_dataset:    the 'year' input into this function will restrict the dataset
                    to years greater than this input.  For example, if the input is
                    2010, then the algorithm will only pull data for lawsuits that
                    were filed after this year.
num_neighbors:      The user may select the number of nearest neighbor nodes to use in the
                    algorithm.  Based on the above function where we iterated over a range
                    of 1-10 nearest neighbors, it appears that 3 provides for the best
                    prediction score.
ML_data_set         fillna:      Fill all None values with a 0. Should only apply to our
                    binary features.
'''


def train_KNN_predictor_iterate_over_range_years(mydb, range_object, num_neighbors):

    # Lists objects to capture results
    year_list = []
    accuracy_train_score_list = []
    accuracy_test_score_list = []

    # Iterate over each year in range
    for year in range_object:

        # Append to list year
        year_list.append(year)

        # Prepare Data Set
        ML_data_set = m8.prepare_dataset(mydb, year).fillna(0)
        # OneHotEncode DataFrame
        df_encoded = pd.get_dummies(ML_data_set)
        # Step2:  Separate X & Y Variables
        X = df_encoded.drop('Target_case_status_binary', axis = 1)
        Y = df_encoded['Target_case_status_binary']

        # Split Data into Train/Test
        x_train, x_test, y_train, y_test = train_test_split(
                                        X, Y,
                                        stratify = Y,
                                        random_state = 66)
        # Instantiate KNN Algorithm
        knn = KNeighborsClassifier(n_neighbors = num_neighbors)

        # Fit algorithm to training data
        knn.fit(x_train, y_train)
        accuracy_train_score_list.append(knn.score(x_train, y_train))
        accuracy_test_score_list.append(knn.score(x_test, y_test))

    # Write Results To Excel
    df = pd.DataFrame({}, index = [[x for x in range_object]])
    df['Accuracy_Training'] = accuracy_train_score_list
    df['Accuracy_Test'] = accuracy_test_score_list
    m0.write_to_excel(df, 'KNN_output', output_dir)

    # Plotting
    x_label_range_year = [x for x in range_object]
    plt.plot(x_label_range_year, accuracy_train_score_list, label = 'Accuracy of training')
    plt.plot(x_label_range_year, accuracy_test_score_list, label = 'Accuracy of test')
    plt.ylabel('Accuracy', fontsize = 20)
    plt.xlabel('Range of Years Case Was Filed' , fontsize = 20)
    plt.title('''Performance KNN Algorithm SCA Dataset
                 Year Range => {}
                 Number of Neighbors => {}'''.format('2000-2018', str(num_neighbors))
                 , fontsize = 30)
    plt.legend(fontsize = 15)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.show()

    # Return Results in df object
    return df

# Range Object

range_object = range(2000, 2017)

train_KNN_predictor_iterate_over_range_years(mydb, range_object, 3)
