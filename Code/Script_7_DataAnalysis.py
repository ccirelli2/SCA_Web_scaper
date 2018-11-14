# Preliminary Data Analysis



### IMPORT LIBRARIES
import pandas as pd
import mysql.connector

### IMPORT MODULES
import Module_7_DataAnalysis as m7


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

## Query 1:     Num Lawsuits By Year
df_claim_count_by_year = m7.sql_query(mydb, m7.query1_count_groupby_year())
#print(df_claim_count_by_year)


## Query 2:     Num of Lawsuits By Type By Year
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


# Create New Dataframe
def get_new_df(df_dismissed, df_settled):
    dict_new = {}
    df_new = pd.DataFrame(dict_new, index = ['2010', '2011', '2012', '2013', '2014', 
                                            '2015', '2016', '2017'])
    df_new['Dismissed'] = list(df_dismissed['Count'])
    df_new['Settled'] = list(df_settled['Count'])
    df_new['Ongoing'] = list(df_ongoing['Count'])
    
    return df_new

print(get_new_df(df_dismissed, df_settled))



'''
Note, once you get the dismissal rate for each year, may limit to years only with mininal
ongoing cases, then you can start indexing for specific claim types, limit to each claim type
and compare the dismissal rates to see if there are any interesting relationships. 
Then graph in descending order to show that are most likely to contribute to dismissal. 

or you can put together that table that shows year in the rows and each column is an 
attributed that was input into the dataframe like we just did above. 

'''







