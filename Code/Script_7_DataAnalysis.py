# Preliminary Data Analysis



### IMPORT LIBRARIES
import pandas as pd
import mysql.connector
import os


### IMPORT MODULES
import Module_7_DataAnalysis as m7
import Module_0_utility_functions as m0

### Directory object(s)
target_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Scraper_output'

### SQL INSTANCIATION
mydb = mysql.connector.connect(
        host="localhost",
        user="ccirelli2",
        passwd="Work4starr",
        database='SCA_SCRAPER')


## Relationships
'''
1.) Number of lawsuits by year
2.) Number of lawsuit types (dismissed, settled, ongoing) by year
3.) Dismissal rate by year
4.) Dismissal rate by type by year
5.) Dimissal rate grouped by Industry, Judge, Plaintiff firm, Headquarters (state), 
    Court, 

'''

## QUERY_1:     NUMBER LAWSUITS BY YEAR__________________________________________________________
df_claim_count_by_year = m7.sql_query(mydb, m7.query1_count_groupby_year())
#print(df_claim_count_by_year)
#m0.write_to_excel(df_claim_count_by_year, 'Claim_count_by_year', target_dir)



## QUERY_4:     Num of LAWSUITS_CASE_STATUS______________________________________________________
df_count_groupby_year_case_status = m7.sql_query(mydb, m7.query2_count_groupby_year_case_status())

# Limit Dataframe By Case Status Type
df_dismissed = m7.limit_dataframe_casetype_year(df_count_groupby_year_case_status, 
                                               'Dismissed', '2018')
# Settled
df_settled = m7.limit_dataframe_casetype_year(df_count_groupby_year_case_status, 
                                              'Settled', '2018')
# Ongoing
df_ongoing = m7.limit_dataframe_casetype_year(df_count_groupby_year_case_status,
                                              'Ongoing', '2018')

# Create Dataframe - Case_status by Year, Dismissal % of Total Cases
def get_new_df(df_dismissed, df_settled, df_ongoing):
    '''Documentation
    1.) Input:          Our Query2 dataframe limited by claim type.  These will form the basis
                        of the new columns. 
    2.) Output:         A new dataframe with the count of claim type and % dismissed 
                        by year. 
    '''
    dict_new = {}
    df_new = pd.DataFrame(dict_new, index = ['2010', '2011', '2012', '2013', '2014', 
                                            '2015', '2016', '2017'])
    df_new['Dismissed'] = list(df_dismissed['Count'])
    df_new['Settled'] = list(df_settled['Count'])
    df_new['Ongoing'] = list(df_ongoing['Count'])
    df_new['Percent_Dismissed'] = round(df_new['Dismissed'] / 
                                (df_new['Dismissed'] + df_new['Settled'] + df_new['Ongoing']),2)
    return df_new




# QUERY_3 - INVESTIGATE DISMISSAL RATE BY CASE ALLEGATION______________________________________

Count_dismissal = m7.sql_query(mydb, m7.get_count_all_allegations_by_year_for_dismissed()).set_index('YEAR_FILED')
'''Approach:  Create three dataframes and filter by case_status
'''
Count_all = m7.sql_query(mydb, m7.get_total_count_all_cases_by_year()).set_index('YEAR_FILED')
dismissal_rate =  Count_dismissal.div(Count_all)


print(Count_all.head())


# WRITE RELATIONSHIPS TO EXCEL_________________________________________________________________

## Dismissal Rate
#m0.write_to_excel(dismissal_rate, 'Dismissal_rate_by_case_type', target_dir)

## Case Status by Year
#m0.write_to_excel(get_new_df(df_dismissed, df_settled, df_ongoing), 'Case_status_by_year', target_dir)

## Claims Count By Year
#m0.write_to_excel(df_claim_count_by_year, 'Claim_count_by_year', target_dir)





'''
Note, once you get the dismissal rate for each year, may limit to years only with mininal
ongoing cases, then you can start indexing for specific claim types, limit to each claim type
and compare the dismissal rates to see if there are any interesting relationships. 
Then graph in descending order to show that are most likely to contribute to dismissal. 

or you can put together that table that shows year in the rows and each column is an 
attributed that was input into the dataframe like we just did above. 

'''







