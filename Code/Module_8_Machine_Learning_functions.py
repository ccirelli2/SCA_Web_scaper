'''DOCUMENTATION

Script:     This script contains the functions that will be used to prepare the dataset
            our dataset for the machine learning model
'''

## Import Packages
import pandas as pd
import sklearn
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

## Import Project Modules
import Module_7_DataAnalysis as m7
import Module_0_utility_functions as m0


## Directory Object
output_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/ML_Algorithm_Results'

'''We need to modify the first function below to allow the user to limit the data by min
and max year as we did in Module 7.  This will ensure that we choose a data set with
an equivalent number of dismissed and settled cases'''



### DATA RETREIVAL & TRANSFORMATION___________________________________________________________

def sql_query_machine_learning_data_set(min_year, max_year):
    '''Purpose:  Initial query of db to retrieve data for ML application'''
    Query = '''SELECT *
               FROM SCA_data
               WHERE case_status IS NOT NULL
               AND YEAR_FILED > {}
               AND YEAR_FILED < {}
               AND case_status != 'ongoing'
               AND Plaintiff_firm != 'Error'
               AND Judge != 'None'
               AND CHAR_LENGTH(Judge) > 2
               ;'''.format(min_year, max_year)
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



### One Hot Encode Data------------------------------------------------------------------
def Encode_categorical_data(df, List_attributes_by_type):
    le = preprocessing.LabelEncoder()
    Attributes_categorical = df[List_attributes_by_type]
    Attributes_encoded = Attributes_categorical.apply(le.fit_transform)
    return Attributes_encoded



### DRIVER FUNCTION - PREPARE DATA SET FOR ML ALGORITHM----------------------------------
'''Includes all the above functions to prepare dataset'''

def prepare_dataset(conn, min_year, max_year):
    '''
    Purpose:    Prepare the dataset that we will use for our machine learning model
    Conn:       mysql connection
    Year:       Min year to be used to limit dataset to years > than this value
    Output:     Dataset prepared for ML algorithm
    '''

    # 1.) Import SCA_data
    '''Input:  Year_Filed to exclude'''
    df_SCA_data_table = m7.sql_query_executor(conn, 
                        sql_query_machine_learning_data_set(min_year, max_year))

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




##########################           ALGORITHMS                 ###############################



### KNN____________________________________________________________________________________


# Test Number of Neighbors-----------------------------------------------------------------

def train_KNN_predictor(X, Y, random_state_value, min_year, max_year, write_2_excel = False, 
                        plot = False, results = 'DataFrame'):
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
                                        random_state = random_state_value, 
                                        test_size = .15)

    # Ratio Dissmissed to Settled;
    Dismissal_percentage = round(sum(Y) / len(Y), 2)

    # Case Count
    Case_count = len(Y)

    # Lists to Capture Predictions
    accuracy_training_list = []
    accuracy_test_list = []
    dismissal_percentage_list = [Dismissal_percentage for x in range(1,10)]

    # Range of Nearest Neighbors
    num_range_neighbors = range(1,10)
    # Run Loop
    for num in num_range_neighbors:
        # Instantiate KNN Algorithm
        knn = KNeighborsClassifier(n_neighbors = num)
        # Fit algorithm to training data
        knn.fit(x_train, y_train)
        y_predict = knn.predict
        accuracy_training_list.append(knn.score(x_train, y_train))
        accuracy_test_list.append(knn.score(x_test, y_test))


    # Create DataFrame for scores
    df = pd.DataFrame({}, index = [2,3,4,5,6,7,8,9,10])
    df['Accuracy_Training'] = accuracy_training_list
    df['Accuracy_Test'] = accuracy_test_list
    df['Dismissal_Percentage'] = dismissal_percentage_list


    # Write Results To Excel
    if write_2_excel == True:
        m0.write_to_excel(df, 'KNN_output', output_dir)

    # Plotting
    if plot == True:
        plt.plot(num_range_neighbors, accuracy_training_list, label = 'Accuracy of training')
        plt.plot(num_range_neighbors, accuracy_test_list, label = 'Accuracy of test')
        plt.plot(num_range_neighbors, dismissal_percentage_list, label = 'Dismissal Percentage')
        plt.ylabel('Accuracy', fontsize = 20)
        plt.xlabel('Number of Neighbors' , fontsize = 20)
        plt.title('''Performance KNN Algorithm SCA Dataset
                 For Years: {} to {}
                 Case Count => {}
                 Ratio Dismissed to Total Cases => {}'''.format(min_year, max_year, Case_count, 
                 Dismissal_percentage), fontsize = 25)
        plt.legend(fontsize = 15)
        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)
        plt.grid(b=None, which='major')
        plt.show()

    # Confusion Matrix
    if results == 'Confusion_matrix':
        clf_predict_y_test = knn.predict(y_test)
        clf_confusion_matrix = confusion_matrix(y_test, clf_predict_y_test)
        return clf_confusion_matrix 
    
    # Results in Dataframe
    if results == 'DataFrame':
        return df
    #-------------------------------------------------------------------------------




## KNN - Single Neighbor - Generate Classification Report------------------------------------------

def train_KNN_single_neighbor_classifier(X, Y, NN, random_state_value, result):
    '''
    x_tain , y_train:  This represents the training data for our algorithm.  x_train is our
                       features and y_train the target. 
    y_pred_class:      Once trained, we input the x_test data, which our model has not yet seen, 
                       from which the model generates a prediction.  That prediction is saved to
                       y_pred_class object.  We then compare this prediction to the actual y_values
                       which are saved in y_test.  Its important to remember that x_test is the 'test'
                       data that our model has not yet seen. Hence the word 'test'.  
    '''
    # Split Data Into Training & Test Sets:
    x_train, x_test, y_train, y_test = train_test_split(
                                        X, Y,
                                        stratify = Y,
                                        random_state = random_state_value,
                                        test_size = .15)

    # Instantiate KNN Algorithm
    knn = KNeighborsClassifier(n_neighbors = NN)

    # Fit algorithm to training data
    knn.fit(x_train, y_train)
    
    # Predict for Test Data
    '''Feed our model the x_test data (features) and make a prediction for our y-variable'''
    y_predict = knn.predict(x_test)

    # Generate Results
    if result == 'Classification_report':
        '''We now compare our y-prediction to the actual y saved in the y_test object'''
        knn_class_report_train = sklearn.metrics.classification_report(y_test, y_predict)
        return knn_class_report_train
    elif result == 'f1_score':
        knn_f1_score = sklearn.metrics.f1_score(y_test, y_predict)
        return knn_f1_score
    elif result == 'precision_score':
        knn_precision_score = sklearn.metrics.precision_score(y_test, y_predict)
        return knn_precision_score
    elif result == 'recall_score':
        knn_recall_score = sklearn.metrics.recall_score(y_test, y_predict)
        return knn_recall_score

    
    #-------------------------------------------------------------------------------


## LOGISTIC REGRESSION________________________________________________________________


def train_log_regressor_classifier(X, Y, random_state_value, result):
    x_train, x_test, y_train, y_test = train_test_split(X, Y,
                                                    stratify = Y,
                                                    random_state = random_state_value)
    # Standardize Data
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    
    #x_train_sc = sc.fit_transform(x_train)
    #x_test_sc = sc.fit_transform(x_test)

    # Instantiate Model & Generate Prediction
    log_reg = LogisticRegression()
    log_reg.fit(x_train, y_train)
    y_predict = log_reg.predict(x_test)

    # Generate Results
    if result == 'Classification_report':
        log_reg_class_report = sklearn.metrics.classification_report(y_test, y_predict)
        return log_reg_class_report
    elif result == 'f1_score':
        log_reg_f1_score = sklearn.metrics.f1_score(y_test, y_predict)
        return log_reg_f1_score
    elif result == 'precision_score':
        log_reg_precision_score = sklearn.metrics.precision_score(y_test, y_predict)
        return log_reg_precision_score
    elif result == 'recall_score':
        log_reg_recall_score = sklearn.metrics.recall_score(y_test, y_predict)
        return log_reg_recall_score

    


    #-------------------------------------------------------------------------------


## NAIVE BAYES______________________________________________________________________

'''DOCUMENTATION:
Bernoulli Naive Bayes:  The binomial model is useful if your feature vectors 
                        are binary (i.e., 0s and 1s). One application would be text 
                        classification with a bag of words model where the 0s 1s are 
                        "word occurs in the document" and "word does not occur 
                        in the document"

Multinomial Naive:      Bayes The multinomial naive Bayes model is typically used for discrete counts.                         E.g., if we have a text classification problem, we can take the idea 
                        of bernoulli trials one step further and instead of "word occurs in the 
                        document" we have "count how often word occurs in the document", 
                        you can think of it as "number of times outcome number x_i is observed 
                        over the n trials"

Gaussian Naive Bayes:    Here, we assume that the features follow a normal distribution. 
                         Instead of discrete counts, we have continuous features (e.g., 
                         the popular Iris dataset where the features are sepal width, petal 
                         width, sepal length, petal length).
Source:                  http://users.sussex.ac.uk/~christ/crs/ml/lec02b.html
'''


def train_NaiveBayes_classifier(X,Y, random_state_value, NB_type, result):

    x_train, x_test, y_train, y_test = train_test_split(X, Y, 
                                                        stratify = Y, 
                                                        random_state = random_state_value)
    # Multinomial Model:-------------------------
    if NB_type == 'Multinomial':
        NB_multi = MultinomialNB(alpha = 1)
        NB_multi.fit(x_train, y_train)
        y_predict = NB_multi.predict(x_test)
        
        # Generate Results
        if result == 'Classification_report':
            NB_class_report = sklearn.metrics.classification_report(y_test, y_predict)
            return NB_class_report
        elif result == 'f1_score':
            NB_f1_score = sklearn.metrics.f1_score(y_test, y_predict)
            return NB_f1_score
        elif result == 'precision_score':
            NB_precision_score = sklearn.metrics.precision_score(y_test, y_predict)
            return NB_precision_score
        elif result == 'recall_score':
            NB_recall_score = sklearn.metrics.recall_score(y_test, y_predict)
            return NB_recall_score

    # Bernoulli Model----------------------------
    elif NB_type == 'Bernoulli':
        NB_bern = BernoulliNB()
        NB_bern.fit(x_train, y_train)
        y_predict = NB_bern.predict(x_test)

        # Generate Results
        if result == 'Classification_report':
            NB_class_report = sklearn.metrics.classification_report(y_test, y_predict)
            return NB_class_report
        elif result == 'f1_score':
            NB_f1_score = sklearn.metrics.f1_score(y_test, y_predict)
            return NB_f1_score
        elif result == 'precision_score':
            NB_precision_score = sklearn.metrics.precision_score(y_test, y_predict)
            return NB_precision_score
        elif result == 'recall_score':
            NB_recall_score = sklearn.metrics.recall_score(y_test, y_predict)
            return NB_recall_score

    #-------------------------------------------------------------------------------
        

# RANDOM FOREST_______________________________________________________________________________


def train_RandomForecast_classifier(X,Y, random_state_value, result):

    x_train, x_test, y_train, y_test = train_test_split(X, Y, 
                                                        stratify = Y)
    
    # Generate Prediction
    clf_RF = RandomForestClassifier(n_estimators = 100)
    clf_RF.fit(x_train, y_train)
    y_predict = clf_RF.predict(x_test)

    # Generate Results
    if result == 'Classification_report':
        NB_class_report = sklearn.metrics.classification_report(y_test, y_predict)
        return NB_class_report
    elif result == 'f1_score':
        NB_f1_score = sklearn.metrics.f1_score(y_test, y_predict)
        return NB_f1_score
    elif result == 'precision_score':
        NB_precision_score = sklearn.metrics.precision_score(y_test, y_predict)
        return NB_precision_score
    elif result == 'recall_score':
        NB_recall_score = sklearn.metrics.recall_score(y_test, y_predict)
        return NB_recall_score
    elif result == 'feature_importance':
        Feature_important = clf_RF.feature_importances_
        df = pd.DataFrame({}, index = X.columns)
        df['Feature Importance'] = Feature_important
        m0.write_to_excel(df, 'Feature_Importance', output_dir)
        return clf_RF.score(x_test, y_test)
    #-------------------------------------------------------------------------------











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



# Feature Importance - Un-groupped Categories
'''
Because of the one-hot-encoding certain features where broken into their subgroups.
Example the feature judge has a column for every single judge.  The below functions 
rever these columns back to the single lvl features and then sum the feature importance
exported from our model. 
'''

def generate_sum_importance_ungrouped_features(df, Feature):
    Feature_importance_list = []

    for x in df['Category']:
        if Feature in x:
            Feature_importance_list.append(1)
        else:
            Feature_importance_list.append(0)
    df[Feature + '_Importance'] = Feature_importance_list
    df_limit_feature = df[Feature +'_Importance'] == 1
    df_final = df[df_limit_feature]

    Feature_importance_sum = sum(df_final['Feature Importance'])

    return Feature_importance_sum

def record_feature_importance_ungrouped_categories(df, grouping_function, target_dir, target_file):

    # Load File
    os.chdir(target_dir)
    df = pd.read_excel(target_file)


    Dict_feature_importance = {}
    Ungrouped_feature_list = ['Judge', 'Court', 'Plaintiff_firm', 
                              'Headquarters', 'Sector', 'Industry']
    
    
    for feature in Ungrouped_feature_list:
        feature_importance = round(grouping_function(df, feature), 4)
        Dict_feature_importance[feature] = feature_importance

    df = pd.DataFrame(Dict_feature_importance, index = ['Feature_importance']).transpose()

    return df
























