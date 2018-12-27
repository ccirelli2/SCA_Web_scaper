from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd 
import re
import os
import string
from nltk.stem import *
stemmer = PorterStemmer() 
from nltk import corpus
import nltk
from datetime import datetime
import mysql.connector

import Module_1_Scraper_DataPoints as m1
import Module_2_Scraper_Scrape_CaseSummary as m2
import Module_3_Dict_Derived_Values as m3




def insert_function_2(mydb, table, action, row_number, obj_name, data_obj):
    '''
    action:         can either be create row or update_value.
    page_number:    Will be required everytime for this function
    data_obj_name   Name of data object we are looking to update. Type string. 
    data_obj:       The column for which we are looking to update. 
    '''
    
    # Specify MySQL Table to Insert Data To

    mycursor = mydb.cursor()

    if action == 'create_row':

        sql_command = "INSERT INTO {} (page_number, defendant_name) VALUES (%s,%s)".format(table)
        val = (row_number, data_obj)
        mycursor.execute(sql_command, val)
        mydb.commit()

    else:
        sql_command = '''UPDATE {}
                            SET {} = '{}'
                            WHERE page_number = '{}' '''.format(table, obj_name, 
                                                         data_obj, row_number)
        
        mycursor.execute(sql_command)
        mydb.commit()
    
    return None


def main_scraper_function(mydb, table, bsObj, Count):

    # SUMMARY SECTION____________________________________________________________________        

    # Define Count As the Page Number for Our Database
    '''At the end of the loop we'll need to increment Beginning_page by 1'''


    # SQL Commit - Defendant Name
    Defendant = m1.get_defendant(bsObj)
    insert_function_2(mydb, table, action = 'create_row', row_number = Count,
                      obj_name = 'defendant_name', data_obj = Defendant)

    # SQL Commit - Case Status
    Status = m1.get_case_status(bsObj)
    if 'DISMISSED' in Status:
        insert_function_2(mydb, table, action = 'update',row_number = Count,
                          obj_name = 'case_status', data_obj = 'Dismissed')
    elif 'SETTLED' in Status:
        insert_function_2(mydb, table, action = 'update',row_number = Count,
                          obj_name = 'case_status', data_obj = 'Settled')

    elif 'ONGOING' in Status:
        insert_function_2(mydb, table, action = 'update',row_number = Count,
                      obj_name = 'case_status', data_obj = 'Ongoing')

    # SQL Commit - Filing Date
    try:
        Filing_date = m1.get_filing_date(bsObj)
        Filing_date_date_obj = datetime.strptime(Filing_date, ' %B %d, %Y')
        insert_function_2(mydb, table, action = 'update',row_number = Count,
                                            obj_name = 'filling_date', data_obj = Filing_date_date_obj)
    except ValueError:
        Filing_date = 'January 01, 1900'
        Filing_date_date_obj = datetime.strptime(Filing_date, '%B %d, %Y')
        insert_function_2(mydb, table, action = 'update',row_number = Count,
                          obj_name = 'filling_date', data_obj = Filing_date_date_obj)

    # SQL Commit - Close Date
    try:
        Close_date = m1.get_close_date(bsObj)
        Close_date_date_obj = datetime.strptime(Close_date, '%m/%d/%Y')
        insert_function_2(mydb, table, action = 'update',row_number = Count,
                                          obj_name = 'close_date', data_obj = Close_date_date_obj)
    except TypeError:
        Close_date = '01/01/1900'
        Close_date_date_obj = datetime.strptime(Close_date, '%m/%d/%Y')
        insert_function_2(mydb, table, action = 'update',row_number = Count,
                          obj_name = 'close_date', data_obj = Close_date_date_obj)


    # Year Filed

    try:
        Filing_date = m1.get_filing_date(bsObj)
        Filing_date_date_obj = datetime.strptime(Filing_date, ' %B %d, %Y')
        year_filed = Filing_date_date_obj.year
        insert_function_2(mydb, table, action = 'update',row_number = Count,
                                            obj_name = 'YEAR_FILED', data_obj = year_filed)
    except ValueError:
        Filing_date = '1900'
        year_filed = Filing_date
        insert_function_2(mydb, table, action = 'update',row_number = Count,
                          obj_name = 'YEAR_FILED', data_obj = year_filed)



    # COMPANY SECTION______________________________________________________________________

    # Sector
    Sector = m1.get_company_data_points(bsObj, 'Sector')
    insert_function_2(mydb, table, action='update',row_number=Count,
                      obj_name ='Sector', data_obj = Sector)
    
    # Case Summary
    import string
    Punct_list = string.punctuation
    Case_summary = m1.get_case_summary(bsObj)
    case_summary_clean = ('').join(list(filter(lambda x: (x not in Punct_list), Case_summary)))

    insert_function_2(mydb, table, action = 'update', row_number = Count, 
                      obj_name = 'case_summary', data_obj = str(case_summary_clean))

    # Industry
    Industry = m1.get_company_data_points(bsObj, 'Industry')
    insert_function_2(mydb, table, action='update',row_number=Count,
                      obj_name ='Industry', data_obj = Industry)
    # Symbol
    Ticker_symbol = m1.get_company_data_points(bsObj, 'Symbol')
    insert_function_2(mydb, table, action='update',row_number=Count,
                      obj_name ='Symbol', data_obj = Ticker_symbol)
    # Status
    Status_2 = m1.get_company_data_points(bsObj, 'Status')
    insert_function_2(mydb, table, action='update',row_number=Count,
                      obj_name ='Status_2', data_obj = Status_2)
    # Headquarters
    Headquarters = m1.get_company_data_points(bsObj, 'Headquarters')
    insert_function_2(mydb, table, action='update',row_number=Count,
                      obj_name ='Headquarters', data_obj = Headquarters)
    # Company Market
    Company_market = m1.get_company_data_points(bsObj, 'Company Market')
    insert_function_2(mydb, table, action='update',row_number=Count,
                      obj_name ='Company_market', data_obj = Company_market)


    # FIRST FILED COMPLAINT SECTION________________________________________________________

    # Court
    Court = m1.get_first_complaint_data_points(bsObj, 'Court')
    insert_function_2(mydb, table, action='update',row_number=Count,
                      obj_name ='Court', data_obj = Court)
    # Docket
    Docket = m1.get_first_complaint_data_points(bsObj, 'Docket')
    insert_function_2(mydb, table, action='update',row_number=Count,
                      obj_name ='Docket', data_obj = Docket)
    # Judge
    try:
        Judge = m1.get_first_complaint_data_points(bsObj, 'Judge')
        insert_function_2(mydb, table, action='update',row_number=Count,
                obj_name ='Judge', data_obj = Judge) 
    except mysql.connector.Error as err:
        Judge = 'None'
        insert_function_2(mydb, table, action='update',row_number=Count,
                obj_name ='Judge', data_obj = Judge)

    # Date Filed
    Date_filed = m1.get_first_complaint_data_points(bsObj, 'Date Filed')
    Date_filed_date_obj = datetime.strptime(Date_filed, ' %m/%d/%Y')
    insert_function_2(mydb, table, action='update',row_number=Count,
                      obj_name ='Date_filed', data_obj = Date_filed_date_obj)

    # Class Period Start
    try:
        Class_period_start = m1.get_first_complaint_data_points(bsObj,'Class Period Start')
        Class_period_start_date_object = datetime.strptime(Class_period_start, ' %m/%d/%Y')
        insert_function_2(mydb, table, action='update',row_number=Count,
                          obj_name ='Class_Period_Start',
                          data_obj = Class_period_start_date_object)
    except ValueError:
        Class_period_start = ' 01/01/1900'
        Class_period_start_date_object = datetime.strptime(Class_period_start, ' %m/%d/%Y')
        insert_function_2(mydb, table, action='update',row_number=Count,
                          obj_name ='Class_Period_Start',
                          data_obj = Class_period_start_date_object)

    # Class Period End
    try:
        Class_period_end = m1.get_first_complaint_data_points(bsObj, 'Class Period End')
        Class_period_end_date_object = datetime.strptime(Class_period_end, ' %m/%d/%Y')
        insert_function_2(mydb, table, action='update',row_number=Count,
                          obj_name ='Class_Period_End',
                          data_obj = Class_period_end_date_object)
    except ValueError:
        Class_period_end = ' 01/01/1900'
        Class_period_end_date_object = datetime.strptime(Class_period_end, ' %m/%d/%Y')
        insert_function_2(mydb, table, action='update',row_number=Count,
                          obj_name ='Class_Period_End',
                          data_obj = Class_period_end_date_object)


    # REFERENCED FILED COMPLAINT SECTION_____________________________________________________

    # Court
    Ref_court = m1.get_referenced_complaint_data_points(bsObj, 'Court')
    insert_function_2(mydb, table, action='update',row_number=Count,
                      obj_name ='Ref_court',
                      data_obj = Ref_court)
    # Docket
    Ref_docket = m1.get_referenced_complaint_data_points(bsObj, 'Docket')
    insert_function_2(mydb, table, action='update',row_number=Count,
                      obj_name ='Ref_docket',
                      data_obj = Ref_docket)
    # Judge
    try:
        Ref_judge = m1.get_referenced_complaint_data_points(bsObj, 'Judge')
        insert_function_2(mydb, table, action='update',row_number=Count,
                          obj_name ='Ref_judge',
                          data_obj = Ref_judge)
    except mysql.connector.errors.ProgrammingError:
        insert_function_2(mydb, table, action='update',row_number=Count,
                          obj_name ='Ref_judge',
                          data_obj = 'No_judge_found')

    # Date Filed
    try:
        Ref_date_filed = m1.get_referenced_complaint_data_points(bsObj, 'Date Filed')
        Ref_date_filed_date_obj = datetime.strptime(Ref_date_filed, ' %m/%d/%Y')
        insert_function_2(mydb, table, action='update',row_number=Count,
                          obj_name ='Ref_date_filed',
                          data_obj = Ref_date_filed_date_obj)
    except TypeError:
        Ref_date_filed = ' 01/01/1900'
        Ref_date_filed_date_obj = datetime.strptime(Ref_date_filed, ' %m/%d/%Y')
        insert_function_2(mydb, table, action='update',row_number=Count,
                          obj_name ='Ref_date_filed',
                          data_obj = Ref_date_filed_date_obj)

    # Class Period Start
    try:
        Ref_class_period_start = m1.get_referenced_complaint_data_points(bsObj,
                                                                                    'Class Period Start')
        Ref_class_period_start_date_obj = datetime.strptime(Ref_class_period_start, ' %m/%d/%Y')
        insert_function_2(mydb, table, action='update',row_number=Count,
        obj_name ='Ref_class_period_start', data_obj = Ref_class_period_start_date_obj)
    except TypeError:
        Ref_class_period_start = ' 01/01/1900'
        Ref_class_period_start_date_obj = datetime.strptime(Ref_class_period_start, ' %m/%d/%Y')
        insert_function_2(mydb, table, action='update',row_number=Count, obj_name ='Ref_class_period_start',
                          data_obj = Ref_class_period_start_date_obj)
    except ValueError:
        Ref_class_period_start = ' 01/01/1900'
        Ref_class_period_start_date_obj = datetime.strptime(Ref_class_period_start, ' %m/%d/%Y')
        insert_function_2(mydb, table, action='update',row_number=Count, obj_name ='Ref_class_period_start',
                          data_obj = Ref_class_period_start_date_obj)

    # Class Period End
    try:
        Ref_class_period_end = m1.get_referenced_complaint_data_points(bsObj,
                                                                                    'Class Period End')
        Ref_class_period_end_date_obj = datetime.strptime(Ref_class_period_end, ' %m/%d/%Y')
        insert_function_2(mydb, table, action='update',row_number=Count, obj_name ='Ref_class_period_end',
                          data_obj = Ref_class_period_end_date_obj)
    except TypeError:
        Ref_class_period_end = ' January 01, 1900'
        Ref_class_period_end_date_obj = datetime.strptime(Ref_class_period_end, ' %B %d, %Y')
        insert_function_2(mydb, table, action='update',row_number=Count, 
                                           obj_name ='Ref_class_period_end',
                                           data_obj = Ref_class_period_end_date_obj)
    except ValueError:
        Ref_class_period_end = ' January 01, 1900'
        Ref_class_period_end_date_obj = datetime.strptime(Ref_class_period_end, ' %B %d, %Y')
        insert_function_2(mydb, table, action='update',row_number=Count,
                          obj_name ='Ref_class_period_end', data_obj = Ref_class_period_end_date_obj)

    # LAW FIRM SECTION__________________________________________________________________________
    '''At a later point add Defense counsel'''
    
    # Plaintiff Firm
    try:
        Plaintiff_firm = m1.get_plaintiff_firm(bsObj)
        insert_function_2(mydb, table, action='update',row_number=Count,
                          obj_name ='Plaintiff_firm', data_obj = Plaintiff_firm)
    except mysql.connector.errors.ProgrammingError:
        Plaintiff_firm = 'Error'
        insert_function_2(mydb, table, action='update',row_number=Count, obj_name ='Plaintiff_firm',
                          data_obj = Plaintiff_firm)

    # CASE SUMMARY SECTION - DERIVED VALUES_____________________________________________________
    '''
    Description:        In this section we mine the case summary on the web page in order to derive
                        additional attributes about the case that are not provided by the owner
                        of the web page and have not been converted to structured data. 
    Process:            1.) For each web page we scrape the case summary.
                        2.) We then tokenize and clean the text. 
                        3.) We iterate over that cleaned text and compare each token with a dictionary of 
                            key attributes.  If a match is found with one of those key attributes, we return 
                            a one and update the row in our data frame with that value.  
                            Note:  we iterate through the entire dictionary and use the key to update the 
                                   mysql database where the column name is the same as the key in our dict. 

    '''
    # SQL Commit - Case Summary
    '''Note, presently we are unable to store the entire text summary'''

    Case_summary = m1.get_case_summary(bsObj)
    '''
    insert_function_2(mydb, action = 'update',row_number = Count,
                                            obj_name = 'case_summary', data_obj = Case_summary)'''
    # Tokenize Text
    Tokenized_text = m2.clean_and_tokenize_text(Case_summary)

    # Convert Text to Nograms
    Ngrams_claims_text = m2.get_Ngrams(Tokenized_text, 'Bigrams')

    # Import Claim Type Object
    Claim_type_dict = m3.Claim_type_dictionary

    # Loop over dictionary keys
    for key in Claim_type_dict:
    # Find matches for each key and update inter lists. 
        Match = m3.get_match(key, Ngrams_claims_text, Claim_type_dict)
        if Match == 1:
            insert_function_2(mydb, table, action = 'update',row_number = Count,
            obj_name = key, data_obj = 1)
        
        else:
            insert_function_2(mydb, table, action = 'update', row_number = Count, 
            obj_name = key, data_obj = 0)
        

    # END FUNCTION

    return None


















