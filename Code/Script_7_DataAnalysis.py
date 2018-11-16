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

def get_claim_count_groupby_year(mydb):
    df_claim_count_by_year = m7.sql_query(mydb, m7.query1_count_groupby_year())
    return df_claim_count_by_year       



## QUERY_2:     Num of LAWSUITS_CASE_STATUS______________________________________________________

# Create Dataframe - Case_status by Year, Dismissal % of Total Cases
def get_case_status_count_groupby_year(mydb):
    '''Documentation
    1.) Input:          Our Query2 dataframe limited by claim type.  These will form the basis
                        of the new columns. 
    2.) Output:         A new dataframe with the count of claim type and % dismissed 
                        by year. 
    '''
    # Get Count by Year, Case Status
    df_count_groupby_year_case_status = m7.sql_query(mydb, 
            m7.query2_count_groupby_year_case_status())
    # Limit Dataframe By Case Status Type
    df_dismissed = m7.limit_dataframe_casetype_year(df_count_groupby_year_case_status,
                                               'Dismissed', '2018')
    # Settled
    df_settled = m7.limit_dataframe_casetype_year(df_count_groupby_year_case_status,
                                              'Settled', '2018')
    # Ongoing
    df_ongoing = m7.limit_dataframe_casetype_year(df_count_groupby_year_case_status,
                                              'Ongoing', '2018')
    dict_new = {}
    df_new = pd.DataFrame(dict_new, index = ['2010', '2011', '2012', '2013', '2014', 
                                            '2015', '2016', '2017'])
    df_new['Dismissed'] = list(df_dismissed['Count'])
    df_new['Settled'] = list(df_settled['Count'])
    df_new['Ongoing'] = list(df_ongoing['Count'])
    df_new['Percent_Dismissed'] = round(df_new['Dismissed'] / 
                                (df_new['Dismissed'] + df_new['Settled'] + df_new['Ongoing']),2)
    return df_new



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



# QUERY-4:   DISMISSAL RATE BY CATEGORY (SECTOR, JUDGE, ETC)

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
    # GET COUNTS FOR EACH CASE_STATUS TYPE----------------------------------------
    Dismissed = m7.sql_query(mydb, 
            m7.get_dismissal_rate_by_claim_category(category, col_title, min_year, 
                                                    'Dismissed')).set_index(category)
    Settled =   m7.sql_query(mydb, 
            m7.get_dismissal_rate_by_claim_category(category, col_title, min_year, 
                                                    'Settled')).set_index(category)
    Ongoing =   m7.sql_query(mydb, 
            m7.get_dismissal_rate_by_claim_category(category, col_title, min_year, 
                                                    'Ongoing')).set_index(category)
    
    # SELECT WHICH RELATIONSHIP (Percentage Dismissed or Settled or Ongoing)-----        
    
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



## RUN CODE_____________________________________________________________________

Relationship = 'Plaintiff_firm'

dismissal_rate_by_category = get_dismissal_rate_by_category(mydb, 'Dismissed',  
            '%_Dismissal', 2010, Relationship)\
                    .sort_values(by = '%_Dismissal', ascending = False)

print(dismissal_rate_by_category)
m0.write_to_excel(dismissal_rate_by_category, Relationship, target_dir)


# WRITE RELATIONSHIPS TO EXCEL_________________________________________________________________
'''
# Write each category relationship to Excel.
List_categories = ['Sector', 'Industry, Status_2', 'Headquarters', 'Company_market', 
                    'Court', 'Judge', 'Plaintiff_firm']

# Run Loop:
for category in List_categories:
    print('Writing relationship for {} category to Excel at {}'.format(category, target_dir))
    rate_by_category = get_dismissal_rate_by_category(mydb, 'Dismissed', 
            '%_Dismissed', 2010, category)
    m0.write_to_excel(rate_by_category, category, target_dir)
'''

### NOTES ___________________________________________________________________
'''NOTES:
 We can create a matrix that shows which case types are best to bring in which jurisdictions to get a dismissal.

Note, once you get the dismissal rate for each year, may limit to years only with mininal
ongoing cases, then you can start indexing for specific claim types, limit to each claim type
and compare the dismissal rates to see if there are any interesting relationships. 
Then graph in descending order to show that are most likely to contribute to dismissal. 

or you can put together that table that shows year in the rows and each column is an 
attributed that was input into the dataframe like we just did above. 

'''







