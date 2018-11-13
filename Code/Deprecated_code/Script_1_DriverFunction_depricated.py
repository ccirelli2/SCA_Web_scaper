#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 07:41:27 2018

@author: ccirelli2
"""
### IMPORT LIBRARIES___________________________________________________________
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


### IMPORT MODULES_____________________________________________________________
import Module_1_Scrape_DataPoints as scraper_module_1
import Module_2_Scrape_CaseSummary as scraper_module_2
import Module_3_Scraper_Dict as scraper_module_3
import Module_4_SQL_InsertFunction as scraper_module_4
import Module_5_Scraper_Automation as m5

### SQL INSTANTIATIONS
mydb = mysql.connector.connect(
        host="localhost",
        user="ccirelli2",
        passwd="Work4starr",
        database='SCA_SCRAPER'
        )


### WEB PAGE OBJECTS____________________________________________________________ 
'''Structure Web Page List of Cases
Root =              http://securities.stanford.edu/
Specific Cases =    filings-case.html?id=106716
?id =               Specific case Id.  Need to identify range.  These are the 
                    pages that we would iterate over. You could also look into
                    downloading each page to your laptop maybe using bash curl. 
'''
Url = 'http://securities.stanford.edu/filings-case.html?id='


### SCRAPER STATUS REPORT_______________________________________________________

# Get Last Page From Database
sql_query_last_page = 'SELECT max(page_number) FROM SCA_data'
db_last_page = m5.exec_gen_sql_command(mydb, sql_query_last_page)[0][0]
print('Last page in database {}'.format(db_last_page))



# SCRAPER_______________________________________________________________________

def SCA_data_scraper(Url, last_pg_scraped):  
           
    # COUNT    
    Count = 1 

    # Create Bs4 Object & Increment Count by 1
    html = urlopen(Url + str(last_pg_scraped + Count))
    bsObj = BeautifulSoup(html.read(), 'lxml')

    # Check to See if Page is Blank       
    Tags = bsObj.find('section', {'id':'company'})
    Defendant = Tags.find('h4').get_text().split(':')[1]
    regex_exp = re.compile(' *[A-Z]+')
    search = re.search(regex_exp, Defendant)
    print(Tags)
    
    # If the subsequent page is not blank, start scraper & add 1 to Count.  
    if bool(search) is True:
        print('Match found')

        # SUMMARY SECTION----------------------------------------------        
       
        # SQL Commit - Defendant Name
        Defendant = scraper_module_1.get_defendant(bsObj)
        scraper_module_4.insert_function_2(mydb, action = 'create_row', row_number = Count,
                                            obj_name = 'defendant_name', data_obj = Defendant)
     
        # SQL Commit - Case Status
        Status = scraper_module_1.get_case_status(bsObj)
        if 'DISMISSED' in Status:
            scraper_module_4.insert_function_2(mydb, action = 'update',row_number = Count, 
                                            obj_name = 'case_status', data_obj = 'Dismissed')
        elif 'SETTLED' in Status:
            scraper_module_4.insert_function_2(mydb, action = 'update',row_number = Count,
                                            obj_name = 'case_status', data_obj = 'Settled')
                                            
        # SQL Commit - Filing Date
        try:
            Filing_date = scraper_module_1.get_filing_date(bsObj)
            Filing_date_date_obj = datetime.strptime(Filing_date, ' %B %d, %Y')    
            scraper_module_4.insert_function_2(mydb, action = 'update',row_number = Count,
                                            obj_name = 'filling_date', data_obj = Filing_date_date_obj)
        except ValueError:
            Filing_date = 'January 01, 1900'
            Filing_date_date_obj = datetime.strptime(Filing_date, '%B %d, %Y')
            scraper_module_4.insert_function_2(mydb, action = 'update',row_number = Count,
                                            obj_name = 'filling_date', data_obj = Filing_date_date_obj)


        # SQL Commit - Close Date
        try:
            Close_date = scraper_module_1.get_close_date(bsObj)
            Close_date_date_obj = datetime.strptime(Close_date, '%m/%d/%Y')    
            scraper_module_4.insert_function_2(mydb, action = 'update',row_number = Count,
                                          obj_name = 'close_date', data_obj = Close_date_date_obj)
        except TypeError:
            Close_date = '01/01/1900'
            Close_date_date_obj = datetime.strptime(Close_date, '%m/%d/%Y')
            scraper_module_4.insert_function_2(mydb, action = 'update',row_number = Count,
                                           obj_name = 'close_date', data_obj = Close_date_date_obj)

       
        # COMPANY SECTION-------------------------------------------------_
        
        # Sector
        Sector = scraper_module_1.get_company_data_points(bsObj, 'Sector')
        Case_summary = scraper_module_1.get_case_summary(bsObj)
        scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Sector', data_obj = Sector)
        # Industry
        Industry = scraper_module_1.get_company_data_points(bsObj, 'Industry')
        scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Industry', data_obj = Industry)
        # Symbol
        Ticker_symbol = scraper_module_1.get_company_data_points(bsObj, 'Symbol')
        scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Symbol', data_obj = Ticker_symbol)
        # Status
        Status_2 = scraper_module_1.get_company_data_points(bsObj, 'Status')
        scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Status_2', data_obj = Status_2)
        # Headquarters
        Headquarters = scraper_module_1.get_company_data_points(bsObj, 'Headquarters')
        scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Headquarters', data_obj = Headquarters)
        # Company Market
        Company_market = scraper_module_1.get_company_data_points(bsObj, 'Company Market')
        scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Company_market', data_obj = Company_market)

        # FIRST FILED COMPLAINT SECTION------------------------------------
        
        # Court
        Court = scraper_module_1.get_first_complaint_data_points(bsObj, 'Court')
        scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Court', data_obj = Court)
        # Docket
        Docket = scraper_module_1.get_first_complaint_data_points(bsObj, 'Docket')
        scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Docket', data_obj = Docket)
        # Judge
        Judge = scraper_module_1.get_first_complaint_data_points(bsObj, 'Judge')
        scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                    obj_name ='Judge', data_obj = Judge[:10])
        # Date Filed
        Date_filed = scraper_module_1.get_first_complaint_data_points(bsObj, 'Date Filed')
        Date_filed_date_obj = datetime.strptime(Date_filed, ' %m/%d/%Y')
        scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Date_filed', data_obj = Date_filed_date_obj)

        # Class Period Start
        try:
            Class_period_start = scraper_module_1.get_first_complaint_data_points(bsObj, 
                                                                            'Class Period Start')
            Class_period_start_date_object = datetime.strptime(Class_period_start, ' %m/%d/%Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Class_Period_Start', 
                                            data_obj = Class_period_start_date_object)
        except ValueError:
            Class_period_start = ' 01/01/1900'
            Class_period_start_date_object = datetime.strptime(Class_period_start, ' %m/%d/%Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                             obj_name ='Class_Period_Start',
                                             data_obj = Class_period_start_date_object)



        # Class Period End
        try:
            Class_period_end = scraper_module_1.get_first_complaint_data_points(bsObj, 'Class Period End')
            Class_period_end_date_object = datetime.strptime(Class_period_end, ' %m/%d/%Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Class_Period_End',
                                            data_obj = Class_period_end_date_object)
        except ValueError:
            Class_period_end = ' 01/01/1900'
            Class_period_end_date_object = datetime.strptime(Class_period_end, ' %m/%d/%Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                             obj_name ='Class_Period_End',
                                             data_obj = Class_period_end_date_object)

        
        # REFERENCED FILED COMPLAINT SECTION---------------------------------------

        # Court
        Ref_court = scraper_module_1.get_referenced_complaint_data_points(bsObj, 'Court')
        scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_court',
                                            data_obj = Ref_court)
        # Docket
        Ref_docket = scraper_module_1.get_referenced_complaint_data_points(bsObj, 'Docket')
        scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_docket',
                                            data_obj = Ref_docket)
        # Judge
        try:
            Ref_judge = scraper_module_1.get_referenced_complaint_data_points(bsObj, 'Judge')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_judge',
                                            data_obj = Ref_judge)
        except mysql.connector.errors.ProgrammingError:
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_judge',
                                            data_obj = 'No_judge_found')
                
                
        # Date Filed
        try:
            Ref_date_filed = scraper_module_1.get_referenced_complaint_data_points(bsObj, 'Date Filed')
            Ref_date_filed_date_obj = datetime.strptime(Ref_date_filed, ' %m/%d/%Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_date_filed',
                                            data_obj = Ref_date_filed_date_obj)
        except TypeError:
            Ref_date_filed = ' 01/01/1900'
            Ref_date_filed_date_obj = datetime.strptime(Ref_date_filed, ' %m/%d/%Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_date_filed',
                                            data_obj = Ref_date_filed_date_obj)
        # Class Period Start
        try:
            Ref_class_period_start = scraper_module_1.get_referenced_complaint_data_points(bsObj, 
                                                                                    'Class Period Start')
            Ref_class_period_start_date_obj = datetime.strptime(Ref_class_period_start, ' %m/%d/%Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_class_period_start',
                                            data_obj = Ref_class_period_start_date_obj)            
        except TypeError:
            Ref_class_period_start = ' 01/01/1900'
            Ref_class_period_start_date_obj = datetime.strptime(Ref_class_period_start, ' %m/%d/%Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_class_period_start',
                                            data_obj = Ref_class_period_start_date_obj)
        except ValueError:
            Ref_class_period_start = ' 01/01/1900'
            Ref_class_period_start_date_obj = datetime.strptime(Ref_class_period_start, ' %m/%d/%Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_class_period_start',
                                            data_obj = Ref_class_period_start_date_obj)


        # Class Period End
        try:
            Ref_class_period_end = scraper_module_1.get_referenced_complaint_data_points(bsObj, 
                                                                                    'Class Period End')
            Ref_class_period_end_date_obj = datetime.strptime(Ref_class_period_end, ' %m/%d/%Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_class_period_end',
                                            data_obj = Ref_class_period_end_date_obj)
        except TypeError:
            Ref_class_period_end = ' January 01, 1900'
            Ref_class_period_end_date_obj = datetime.strptime(Ref_class_period_end, ' %B %d, %Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_class_period_end',
                                            data_obj = Ref_class_period_end_date_obj)
           
        except ValueError:
            Ref_class_period_end = ' January 01, 1900'
            Ref_class_period_end_date_obj = datetime.strptime(Ref_class_period_end, ' %B %d, %Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_class_period_end',
                                            data_obj = Ref_class_period_end_date_obj)
            
        # LAW FIRM SECTION---------------------------------------------------------
        '''At a later point add Defense counsel'''
        # Plaintiff Firm
        try:
            Plaintiff_firm = scraper_module_1.get_plaintiff_firm(bsObj)
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Plaintiff_firm',
                                            data_obj = Plaintiff_firm)
        except mysql.connector.errors.ProgrammingError:
            Plaintiff_firm = 'Error'
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Plaintiff_firm',
                                            data_obj = Plaintiff_firm)


        # CASE SUMMARY SECTION- MINE CLAIMS SUMMARY - GENERATE CLAIMS CATEGORIES------------------

        # SQL Commit - Case Summary
        '''Note, presently we are unable to store the entire text summary'''
            
                        
        Case_summary = scraper_module_1.get_case_summary(bsObj)
        '''
        scraper_module_4.insert_function_2(mydb, action = 'update',row_number = Count,
                                            obj_name = 'case_summary', data_obj = Case_summary)
        '''
        # Tokenize Text
        Tokenized_text = scraper_module_2.clean_and_tokenize_text(Case_summary)
            
        # Convert Text to Nograms
        Ngrams_claims_text = scraper_module_2.get_Ngrams(Tokenized_text, 'Bigrams')
            
        # Import Claim Type Object
        Claim_type_dict = scraper_module_3.Claim_type_dictionary
            
        # Loop over dictionary keys
        for key in Claim_type_dict:
                        
            # Find matches for each key and update inter lists. 
            Match = scraper_module_3.get_match(key, Ngrams_claims_text, Claim_type_dict)
                
            if Match == 1:
                    
                scraper_module_4.insert_function_2(mydb, action = 'update',row_number = Count,
                                obj_name = key, data_obj = 1)

        
        # Send Email W/ Progress Report
        print('New SCA Identified')
        page = (db_last_page + Count)
        sql_command = 'SELECT * FROM SCA_data WHERE page_number = {}'.format(page)
        print(m5.exec_gen_sql_command(mqdb, d + Count)) 
    

    return None


# RUN FUNCTION
SCA_data_scraper(Url, db_last_page)




