###  PUPROSE IS TO HOUSE THE FUNCTIONS FOR THE DATA ANALYSIS SCRIPT


# Import Libraries
import pandas as pd


def sql_query(conn, Query):
    '''
    conn:       Mysql connection
    Query:      Query to pass to function as a string. 
    Purpose:  General function to turn an SQL query into pandas df
    '''
    Query = (Query)
    df = pd.read_sql_query(Query, conn)
    return df



def query1_count_groupby_year():
    '''Purpose:  Get number of lawsuits filled by year'''

    Query = '''SELECT
            YEAR_FILED
            ,COUNT(defendant_name)

            FROM SCA_data
            GROUP BY YEAR_FILED;
            '''
    return Query


def query2_count_groupby_year_case_status():
    '''Purpose:  Get number of lawsuits filled by year'''

    Query = '''
            SELECT
            case_status
            ,YEAR_FILED
            ,COUNT(defendant_name) AS 'Count'
            FROM SCA_data
            WHERE YEAR_FILED > 2009
            AND case_status IS NOT NULL
            GROUP BY case_status, YEAR_FILED;            

            '''
    return Query



def limit_dataframe_casetype_year(df, case_type, year):
    '''
    Purpose:    Index the original sql query to return only data for dismissed and < 2018 > 2010
    Input:      dataframe grouped by year and case status
                case_type: can be 'Dismissed', 'Settled', 'Ongoing'
                year:  Should be the year that you want to exclude. 
    return:     filtered dataframe for status and year. 
    '''
    limit_case_status = df.case_status == case_type
    limit_year = df.YEAR_FILED != year
    df_index_case_status = df[limit_case_status]
    df_dismissed_final = df_index_case_status[limit_year]
    return df_dismissed_final


def get_settled(df):
    Not_dismissed = df.case_status == 'Settled'
    Yr_2010_2017 = df.YEAR_FILED != '2018'
    df_index_not_dismissed = df[Not_dismissed]
    df_not_dismissed_final = df_index_not_dismissed[Yr_2010_2017]
    return df_not_dismissed_final

















