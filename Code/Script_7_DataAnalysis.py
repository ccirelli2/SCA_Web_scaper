# Preliminary Data Analysis



### IMPORT LIBRARIES____________________________________________________________________
import pandas as pd
import mysql.connector
import os
import matplotlib.pyplot as plt

### IMPORT MODULES
import Module_7_DataAnalysis as m7
import Module_0_utility_functions as m0

### Directory object(s)
target_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Scraper_output'

### SQL INSTANCIATION__________________________________________________________________
mydb = mysql.connector.connect(
        host="localhost",
        user="ccirelli2",
        passwd="Work4starr",
        database='SCA_SCRAPER')


## Relationships to investigate
'''
1.) Number of lawsuits by year
2.) Number of lawsuit types (dismissed, settled, ongoing) by year
3.) Dismissal rate by year
4.) Dismissal rate by type by year
5.) Dimissal rate grouped by Industry, Judge, Plaintiff firm, Headquarters (state),
    Court,

'''


## QUERY_1: GET NULL VALUES BY COLUMN___________________________________________________

def get_count_null_values_by_attribute(mydb):
    # Retrieve entire table
    df_entire_table = m7.sql_query_executor(mydb, m7.sql_query_entire_table())

    # List Non-Binary Attributes
    List_nonbinary_attributes = df_entire_table.columns[:27]

    # Function:  Get Null Values By Column
    Count_null_values_SCA_data_table = m7.get_count_null_values_by_column(df_entire_table, List_nonbinary_attributes)
    
    # Return results
    return Count_null_values_SCA_data_table


## QUERY_1: CLAIM COUNT BY YEAR__________________________________________________________
'''
Function:  Returns the claim count grouped by year

'''
def get_claim_count_groupby_year(mydb):
    df_claim_count_by_year = m7.sql_query_executor(mydb, m7.query1_count_groupby_year())
    return df_claim_count_by_year

#claim_count_by_year = get_claim_count_groupby_year(mydb)
#plt.bar(claim_count_by_year)



## QUERY_2: Num of LAWSUITS_CASE_STATUS__________________________________________________


# Create Dataframe - Case_status by Year, Dismissal % of Total Cases

def get_case_status_count_groupby_year(mydb):
    '''Documentation
    1.) Input:          Our Query2 dataframe limited by claim type.  These will form the basis
                        of the new columns.
    2.) Output:         A new dataframe with the count of claim type and % dismissed
                        by year.
    '''
    # Get Count by Year, Case Status
    df_count_groupby_year_case_status = m7.sql_query_executor(mydb,
            m7.query2_count_groupby_year_case_status(year_min = 2000, year_max = 2018))

    # Limit Dataframe By Case Status Type
    df_dismissed = m7.limit_dataframe_casetype(df_count_groupby_year_case_status,
                                                   'Dismissed')

    # Settled
    df_settled = m7.limit_dataframe_casetype(df_count_groupby_year_case_status,
                                                  'Settled')

    # Ongoing
    df_ongoing = m7.limit_dataframe_casetype(df_count_groupby_year_case_status,
                                                  'Ongoing')

    #print(df_dismissed)
    #print(df_settled)
    #print(df_ongoing)

    df_new = pd.DataFrame({}, index = df_dismissed['YEAR_FILED'])
    df_new['Dismissed'] = list(df_dismissed['Count'])
    df_new['Settled'] = list(df_settled['Count'])
    #df_new['Ongoing'] = list(df_ongoing['Count'])
    df_new['Percent_Dismissed'] = round(df_new['Dismissed'] /
                            (df_new['Dismissed'] + df_new['Settled']),2)
    return df_new


test = get_case_status_count_groupby_year(mydb)

print('Data Range:  From 2001 to 2017')
print('Sum Dismissed => {}'.format(sum(test['Dismissed'])))
print('Sum Settled =>   {}'.format(sum(test['Settled'])))



# QUERY-3:    INVESTIGATE DISMISSAL RATE BY CASE ALLEGATION______________________________________
'''Documentation:
    Count_dimissal:     Create a dataframe with the rows organized by year and columns by
                        allegation type.  Then we limit the Count_dimissal dataframe to only
                        those cases that were dismissed and the
    Count_all:          Count of all cases.
    Dismissal_rate:     We divide the Count_dimissal data frame by the Count_all dataframe

'''
def get_dismissal_rate_groupby_year_case_types(mydb):
    Count_dismissal = m7.sql_query(mydb,
                   m7.get_count_all_allegations_by_year_for_dismissed()).set_index('YEAR_FILED')
    Count_all = m7.sql_query(mydb,
            m7.get_count_all_allegations_all_years()).set_index('YEAR_FILED')
    dismissal_rate =  Count_dismissal.div(Count_all)
    return dismissal_rate


# QUERY-4:   DISMISSAL RATE BY CATEGORY (SECTOR, JUDGE, ETC)___________________________________

def get_dismissal_rate_by_category(mydb, relationship, col_title, min_year, category):
    '''INPUTS
    mydb:           Mysql connection
    relationship:   The relationship that you want to output, eg. dismissal rate, settle rate, etc.
    col_title:      The title of your column, i.e. Dismissal_rate, Settlement_rate, etc.
    min_year:       The minimum year from which you want to pull the data.  Ex min_year = 2010, the
                    function will only include data from 2011 to 2018.
    category:       The category you want to select to group you data.

    Permissible options for category include:
                    Sector, Industry, Status_2, Headquarters, Company_market,
                    Court, Judge, Plaintiff_firm.
    Note:           We need to include state of domicile of the company,
                    buckets for the class period,
                    potentially buckets for the stock drop, and defense counsel.
    '''
    # Get Counts For Each Case_Status Type------------------------------------------
    Dismissed = m7.sql_query(mydb,
            m7.get_dismissal_rate_by_claim_category(category, col_title, min_year,
                                                    'Dismissed')).set_index(category)
    Settled =   m7.sql_query(mydb,
            m7.get_dismissal_rate_by_claim_category(category, col_title, min_year,
                                                    'Settled')).set_index(category)
    Ongoing =   m7.sql_query(mydb,
            m7.get_dismissal_rate_by_claim_category(category, col_title, min_year,
                                                    'Ongoing')).set_index(category)

    # Select Which Relationship (Percentage Dimissed / Settled / Ongoing)-----------

    if relationship == 'Dismissed':
        # Get Dismissal Rate
        Dismissal_rate = round(Dismissed.div(Dismissed + Settled + Ongoing),2)
        # Return New Dataframe
        return Dismissal_rate.dropna()

    elif relationship == 'Settled':
        # Get Dismissal Rate
        Settlement_rate = round(Settled.div(Dismissed + Settled + Ongoing),2)
        # Return New Dataframe
        return Settlement_rate.dropna()

    elif relationship == 'Ongoing':
        # Get Dismissal Rate
        Ongoing_rate = round(Settled.div(Dismissed + Settled + Ongoing),2)
        # Return New Dataframe
        return Ongoing_rate.dropna()

    return None



## GENERATE RELATIONSHIPS_____________________________________________________________________

'''INPUTS

Category:           The relationship for which we are looking to generate the dismissal rate and graph.
Return_value:       The dataframe with the dismissal rate for this category.
Relationship.index: We use the index of our dataframe as the labels for our x legend of our chart.
Subtitle:           Is the title of the chart
'''


# Get Relationship
'''
Return_value_dismissal_rate = m7.get_dismissal_rate_by_category(mydb, 'Dismissed',
        '%_Dismissal', 2010, Category).sort_values(by = '%_Dismissal', ascending = False)
'''

# Plot Relationship
'''
get_plot_dismissal_rate(Return_value_dismissal_rate, 'Dismissal_Rate_{}'.format(Category), Category)
'''





