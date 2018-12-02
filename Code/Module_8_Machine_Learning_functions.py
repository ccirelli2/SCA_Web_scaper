'''DOCUMENTATION

Script:     This script contains the functions that will be used to prepare the dataset
            our dataset for the machine learning model
'''

## Import Packages
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

## Import Project Modules
import Module_7_DataAnalysis as m7
import Module_0_utility_functions as m0

## Directory Object
output_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/ML_Algorithm_Results'





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




### ALGORITHMS_______________________________________________________________



## Nearest Neighbor----------------------------------------------------------

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
    plt.grid(b=None, which='major')
    plt.show()

    # Return Results in df object
    return df



def train_KNN_predictor_iterate_over_range_years(mydb, range_object, num_neighbors):

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

    # Lists objects to capture results
    year_list = []
    accuracy_train_score_list = []
    accuracy_test_score_list = []

    # Iterate over each year in range
    for year in range_object:

        # Append to list year
        year_list.append(year)

        # Prepare Data Set
        ML_data_set = prepare_dataset(mydb, year).fillna(0)
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
    plt.grid(b=None, which='major')
    plt.show()

    # Return Results in df object
    return df



## Pipeline Setup------------------------------------------------------------------

def train_log_regressor_pipeline_version(X, Y, random_state_value,  C_value):
    # Split Data
    x_train, x_test, y_train, y_test = train_test_split(X, Y,
                                                    stratify = Y,
                                                    random_state = random_state_value)
    # Instantiate Model
    log_reg = LogisticRegression(C = C_value)
    log_reg.fit(x_train, y_train)

    # Return Test Score
    return log_reg.score(x_test, y_test)


def train_KNN_predictor_pipeline_version(X, Y, random_state_value, num_neighbors):
    # Split dataset
    x_train, x_test, y_train, y_test = train_test_split(
                                        X, Y,
                                        stratify = Y,
                                        random_state = random_state_value)
    # Instantiate KNN Algorithm
    knn = KNeighborsClassifier(n_neighbors = num_neighbors)
    # Fit algorithm to training data
    knn.fit(x_train, y_train)
    
    # Return prediction
    return knn.score(x_test, y_test)
    


def train_NaiveBayes_predictor_pipeline_version(X,Y, random_state_value, NB_type):

    x_train, x_test, y_train, y_test = train_test_split(X, Y, 
                                                        stratify = Y, 
                                                        random_state = random_state_value)
    if NB_type == 'Gaussian':
        clf_NB = GaussianNB()
        clf_NB.fit(x_train, y_train)
        return clf_NB.score(x_test, y_test)

    elif NB_type == 'Bernoulli':
        clf_NB = BernoulliNB()
        clf_NB.fit(x_train, y_train)
        return clf_NB.score(x_test, y_test)


def train_RandomForecast_predictor_pipeline_version(X,Y, random_state_value):

    x_train, x_test, y_train, y_test = train_test_split(X, Y, 
                                                        stratify = Y)
                 
    clf_RF = RandomForestClassifier(n_estimators = 100)
    clf_RF.fit(x_train, y_train)
    Feature_important = list(map(lambda x: round(x,2), clf_RF.feature_importances_))
    df = pd.DataFrame({}, index = X.columns)
    df['Feature Importance'] = Feature_important
    m0.write_to_excel(df, 'Feature_Importance', output_dir)
    
    # Return Prediction
    return clf_RF.score(x_test, y_test)



# ELIMINATE ATTRIBUTES & RUN MODEL
'''Documentation

Purpose:        The purpose of this section is to generate lists in order to 


'''


list_categorical_features = ['Sector', 'Industry', 'Company_market',
                             'Court', 'Judge', 'Plaintiff_firm_modified',
                             'Target_case_status_binary']


def limit_feature_selection(df, limit_selection):
    if limit_selection == 'Drop_derived_values':
        return df[['Sector', 'Industry', 'Company_market',
                             'Court', 'Judge', 'Plaintiff_firm_modified',
                             'Target_case_status_binary']]
    elif limit_selection == 'Use_all':
        return df

    elif limit_selection == 'Drop_merger_value':
        return df.drop(['Derivative', 'Merger', 'Proxy'], axis = 1)







# Graph Comparison - Average Performance All Features vs Dropping Derived Values

def graph_comparison_performance_features():
    year = [x for x in range(2000, 2017)]
    All_features = [.7, .689, .693, .689, .68, .693, .699, .704, .688, .726, .706,
                    .711, .705, .740, .822, .889, .954]
    Categorical_features_only = [.628, .595, .595, .612, .624, .617, .631, .655, .661,
                                 .680, .674, .696, .716, .757, .834, .876, .954]

    df = pd.DataFrame({}, index = year)
    df['Average_Performance_All_Features'] = All_features
    df['Categorical_features_only'] = Categorical_features_only

    plt.plot(year, df['Average_Performance_All_Features'], label = 'All_Features')
    plt.plot(year, df['Categorical_features_only'], label = 'Categorical_Features_Only')
    plt.ylabel('Average_Score', fontsize = 20)
    plt.xlabel('Range of Years Case Was Filed' , fontsize = 20)
    plt.title('Comparison: All Features vs Categorical Features Only', fontsize = 30)
    plt.legend(fontsize = 15)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(b=None, which='major')
    plt.show()
    return df
















