#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 07:41:27 2018

@author: ccirelli2
"""

'''PURPOSE

The purpose of this script is to scrape data from the Stanford Law Securities
Class Action Web page and convert it to structured data for ML training. 
'''


'''NOTES

1.) Page Order:  It is not clear that the page order coincides with the dates, i.e. they are not chronological. 
                We should record the page number next to the date in order to test this idea. 
                We should also take the range of the first page to last in order to know where the scraper should stop. 
                Then we can convert this into a numerical representation of what our scraper has to trasverse in order to scrape
                the entirety of the side. 

'''

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
import SCA_Web_Scraper_Module_1_Scraper as scraper_module_1
import SCA_Web_Scraper_Module_2_Ngram_Generator as scraper_module_2
import SCA_Web_Scraper_Module_3_Claim_Category_Generator as scraper_module_3
import Module4_Scraper_SQL_functions as scraper_module_4


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

Beginning_page = 101000 
End_page =  106720
First_minus_one= 101473
Test_end_page = 101010       # Used for testing code, = 10 iterations




### SCRAPER_______________________________________________________________________

def SCA_data_scraper(Url, Start):  
    '''Inputs'''

    print('Starting up Scraper...VROOM!@...VROOM!@...', '\n')

    # DELETE ROWS IN SQL TABLE FROM LAST ITERATION
    mycursor = mydb.cursor()
    sql = "DELETE FROM SCA_data WHERE page_number > 0"
    mycursor.execute(sql)
    mydb.commit()
  

    # Article Counter
    Count = 0

    # START LOOP OVER ARTICLES_________________________________________________
    
    # Create a range over which to iterate the loop. 
    upper_bound = End_page - Beginning_page
    range_value = range(0, upper_bound)
    test_upper_bound = 1000
    test_range_value = range(0,test_upper_bound)

    # Start Loop 
    for x in range_value:
        
        # First Page to Start Iteration
        Start +=1
         
        # Progress Recorder
        Count +=1       
        scraper_module_1.progress_recorder(Count, test_upper_bound)          

        # Create Beautiful Soup Object per article
        html = urlopen(Url + str(Start))
        bsObj = BeautifulSoup(html.read(), 'lxml')


        # SUMMARY SECTION----------------------------------------------        

        # Scrape Defendant Value
        Defendant = scraper_module_1.get_defendant(bsObj)
        
        # Skip those pages for which the Defendant value == None       
        if Defendant != None and len(Defendant) > 1:

            # SQL Commit - Defendant Name
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
            Filing_date = scraper_module_1.get_filing_date(bsObj)
            Filing_date_date_obj = datetime.strptime(Filing_date, ' %B %d, %Y')    
            scraper_module_4.insert_function_2(mydb, action = 'update',row_number = Count,
                                            obj_name = 'filling_date', data_obj = Filing_date_date_obj)


            # SQL Commit - Close Date
            Close_date = scraper_module_1.get_close_date(bsObj)
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
            Date_filed_date_obj = datetime.strptime(Filing_date, ' %B %d, %Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Date_filed', data_obj = Date_filed_date_obj)

            # Class Period Start
            Class_period_start = scraper_module_1.get_first_complaint_data_points(bsObj, 
                                                                            'Class Period Start')
            Class_period_start_date_object = datetime.strptime(Filing_date, ' %B %d, %Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Class_Period_Start', 
                                            data_obj = Class_period_start_date_object) 
            # Class Period End
            Class_period_end = scraper_module_1.get_first_complaint_data_points(bsObj, 'Class Period End')
            Class_period_end_date_object = datetime.strptime(Filing_date, ' %B %d, %Y')
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
            Ref_class_period_end = scraper_module_1.get_referenced_complaint_data_points(bsObj, 
                                                                                    'Class Period End')
            Ref_class_period_end_date_obj = datetime.strptime(Filing_date, ' %B %d, %Y')
            scraper_module_4.insert_function_2(mydb, action='update',row_number=Count,
                                            obj_name ='Ref_class_period_end',
                                            data_obj = Ref_class_period_end_date_obj)

            # LAW FIRM SECTION---------------------------------------------------------
            '''At a later point add Defense counsel'''
            # Plaintiff Firm
            Plaintiff_firm = scraper_module_1.get_plaintiff_firm(bsObj)
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

            
    return None


# RUN FUNCTION

SCA_data_scraper(Url, Beginning_page)


















