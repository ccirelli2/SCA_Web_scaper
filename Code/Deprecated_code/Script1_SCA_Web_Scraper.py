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
End_page =  10672
First_minus_one= 101473
Test_end_page = 101010       # Used for testing code, = 10 iterations


## PETRI DISH SECTION___________________________________________________________
'''Test code before adding to scaper'''
# Get Titles From Range of Articles
def loop_over_artilces_test(Url, Start):  
    
    # Create Lists to Capture values
    Defendant_list = []

    # Loop over article range
    for x in range(0,1):
        Start +=1
    
        # Create Beautiful Soup Object per article
        html = urlopen(Url + str(Start))
        bsObj = BeautifulSoup(html.read(), 'lxml')
    
        # Scrape Data Points
        #data = scraper_module_1.get_plaintiff_firm(bsObj)
        data = 'shit_can'
        
        page_number = 6 
        
        scraper_module_4.insert_function_2(mydb, 
                                            action = 'update_value', 
                                            row_number = page_number, 
                                            obj_name = 'defendant_name', 
                                            data_obj = data)
                


    return None

#loop_over_artilces_test(Url, First_minus_one)



## SCRAPER_______________________________________________________________________

def SCA_data_scraper(Url, Start, Write_to_excel):  
    '''Inputs

    '''

    print('Starting up Scraper...VROOM!@...VROOM!@...', '\n')


    # DELETE ROWS IN SQL TABLE FROM LAST ITERATION

    mycursor = mydb.cursor()
    sql = "DELETE FROM SCA_data WHERE page_number > 0"
    mycursor.execute(sql)
    mydb.commit()



    # LISTS TO CAPTURE DATA POINTS-------------------------------------

    # Page Number
    Page_number_list = []
    # Summary Section
    Defendant_list = []
    Case_Status_list = []
    Filing_date_list = []
    Close_date_list = []
    Case_summary_list = []
    # Company Section
    Sector_list = []
    Industry_list = []
    Ticker_symbol_list = []
    Status_2_list = []
    Headquarters_list = []
    Company_market_list = []
    # First Filed Complaint
    First_court_list = []
    First_docket_list = []
    First_judge_list = []
    First_date_filed_list = []
    First_class_period_start_list = []
    First_class_period_end_list = []
    # Referenced Complaint
    Ref_court_list = []
    Ref_docket_list = []
    Ref_judget_list = []
    Ref_date_filed_list = []
    Ref_class_period_start_list = []
    Ref_class_period_end_list = []
    # Law Firms
    Plaintiff_firm_list = []
    Defendant_firm_list = []

    # Claims Summary list
    ClaimType_IPO_list = []  
    ClaimType_10b5_list = []  


    # Article Counter
    Count = 0

    # START LOOP OVER ARTICLES_________________________________________________
    
    # Create a range over which to iterate the loop. 
    upper_bound = End_page - Beginning_page
    range_value = range(0, upper_bound)
    test_upper_bound = 5
    test_range_value = range(0,test_upper_bound)

    # Start Loop 
    for x in test_range_value:
        
        # First Page to Start Iteration
        Start +=1
         
        # Progress Recorder
        Count +=1       
        scraper_module_1.progress_recorder(Count, test_upper_bound)          

        # Capture Page Number
        Page_number_list.append(Count)

        # Create Beautiful Soup Object per article
        html = urlopen(Url + str(Start))
        bsObj = BeautifulSoup(html.read(), 'lxml')

        # SUMMARY SECTION----------------------------------------------
        
            
        '''Note:  Here I add a conditional statement that if there is no defendant name, to 
                  essentially skip all the remaining code and go to the next page. 
                  The assumption is that the page is blank and this will speed up the scraping
                  process as well as alleviate issues with teh code.'''

        # Scrape Defendant Value
        Defendant = scraper_module_1.get_defendant(bsObj)
        
        '''Note:  Here I add a conditional statement that if there is no defendant name, to 
                  essentially skip all the remaining code and go to the next page. 
                  The assumption is that the page is blank and this will speed up the scraping
                  process as well as alleviate issues with teh code.'''

        if Defendant == None:
           Defendant_list.append(None) 
        else:
            Defendant_list.append(Defendant)
        


        # SQL Commit - Defendant Name
        if Defendant != None:
            scraper_module_4.insert_function_2(mydb, 
                                            action = 'create_row', 
                                            row_number = Count, 
                                            obj_name = 'defendant_name', 
                                            data_obj = Defendant)



        # Scrape Status
        Status = scraper_module_1.get_case_status(bsObj)
        
        if Status == None:
            Case_Status_list.append(None)
        elif 'DISMISSED' in Status:
            Case_Status_list.append('Dismissed')
        elif 'SETTLED' in Status:
            Case_Status_list.append('Settled')
        else:
            Case_Status_list.append('Unknown')

        # SQL Commit - Case Status
        
        if 'DISMISSED' in Status:
            scraper_module_4.insert_function_2(mydb, action = 'update',row_number = Count, 
                                            obj_name = 'case_status', data_obj = 'Dismissed')
        elif 'SETTLED' in Status:
            scraper_module_4.insert_function_2(mydb, action = 'update',row_number = Count,
                                            obj_name = 'case_status', data_obj = 'Settled')
                                            

        # Scrape Filing Date
        Filing_date = scraper_module_1.get_filing_date(bsObj)
        Filing_date_dt_obj = datetime.strptime(Filing_date, ' %B %d, %Y')
        if Filing_date == None:
            Filing_date.append(None)
        else:
            Filing_date_list.append(Filing_date)
     
        # SQL Commit - Filing Date
        if len(Filing_date) < 1:
            scraper_module_4.insert_function_2(mydb, action = 'update',row_number = Count,
                                            obj_name = 'filling_date', 
                                            data_obj = Filing_date_dt_obj)


        # Scrape Close Date
        Close_date = scraper_module_1.get_close_date(bsObj)
        if Close_date == None:
            Close_date_list.append(None)
        else:
            Close_date_list.append(Close_date)


        ### SCRAPE CASE SUMMARY - GENERATE CLAIMS CATEGORIES------------------------------
        
        # Scrape Case Summary
        Case_summary = scraper_module_1.get_case_summary(bsObj)
        Case_summary_list.append(Case_summary)

        # Generate Claim Categories From Case Summary
        '''
        > Clean & Tokenize text
        > Use a for loop to loop over tokens and identify values within categories. 
        > Once a match is found, the list object for a given category should be 
        updated and the function should go to the next category. 

        '''
    

        # Convert Text to Nograms
        Nograms_claims_text = scraper_module_2.get_Ngrams(Case_summary, 'Bigrams')


        '''
        The below code will loop over each key searching for matches in its values. 
        Each key constitutes a column in our dataframe and will therefore need to have
        a separate list object in our code.  For each key, after iterating the text
        our code will update the list with a 0/1 and then go to the next list. 

        So, the for loop is over each token in the text AND the embedded loop
            is over the dictionary.  So once we finish checking each token, 
            the code will need to progress to the next set of scraping instructions
            and ultimately to the next page to scrape. 

        '''
        # Import Claim Type Object
        Claim_type_dict = scraper_module_3.Claim_type_dictionary
        
        # Loop over ngrams
        #for gram in Nograms_claims_text:
           
        # Loop over dictionary keys
        for key in Claim_type_dict:
            
            #**** Think about create a function that creates lists using the key being
            #     looped over as opposed to creating static lists.  This way, everytime
            #     you create a new key value pair you don't need to update your list of lists
            #     in each one of these functions.  

            Inter_list_IPO = []
            Inter_list_10b5 = []
            
            # Find matches for each key and update inter lists. 
            scraper_module_3.determine_inter_list_to_append(key, Nograms_claims_text, 
                                                            Claim_type_dict, 
                                                            Inter_list_IPO, 
                                                            Inter_list_10b5)
        # Based on matches found, update our primary lists to be included in df. 
        scraper_module_3.determine_primary_list_to_append(Inter_list_IPO, 
                            Inter_list_10b5, ClaimType_IPO_list,                                                            ClaimType_10b5_list)
        
            
       
        # COMPANY SECTION-------------------------------------------------_
        
        # Sector
        Sector = scraper_module_1.get_company_data_points(bsObj, 'Sector')
        Sector_list.append(Sector)
        # Industry
        Industry = scraper_module_1.get_company_data_points(bsObj, 'Industry')
        Industry_list.append(Industry)
        # Symbol
        Ticker_symbol = scraper_module_1.get_company_data_points(bsObj, 'Symbol')
        Ticker_symbol_list.append(Ticker_symbol)
        # Status
        Status_2 = scraper_module_1.get_company_data_points(bsObj, 'Status')
        Status_2_list.append(Status_2)
        # Headquarters
        Headquarters = scraper_module_1.get_company_data_points(bsObj, 'Headquarters')
        Headquarters_list.append(Headquarters)
        # Company Market
        Company_market = scraper_module_1.get_company_data_points(bsObj, 'Company Market')
        Company_market_list.append(Company_market)


        # FIRST FILED COMPLAINT SECTION------------------------------------
        
        # Court
        Court = scraper_module_1.get_first_complaint_data_points(bsObj, 'Court')
        First_court_list.append(Court)
        # Docket
        Docket = scraper_module_1.get_first_complaint_data_points(bsObj, 'Docket')
        First_docket_list.append(Docket)
        # Judge
        Judge = scraper_module_1.get_first_complaint_data_points(bsObj, 'Judge')
        First_judge_list.append(Judge)
        # Date Filed
        Date_filed = scraper_module_1.get_first_complaint_data_points(bsObj, 'Date Filed')
        First_date_filed_list.append(Date_filed)
        # Class Period Start
        Class_period_start = scraper_module_1.get_first_complaint_data_points(bsObj, 'Class Period Start')
        First_class_period_start_list.append(Class_period_start)
        # Class Period End
        Class_period_end = scraper_module_1.get_first_complaint_data_points(bsObj, 'Class Period End')
        First_class_period_end_list.append(Class_period_end)

        
        # REFERENCED FILED COMPLAINT SECTION---------------------------------------

        # Court
        Ref_court = scraper_module_1.get_referenced_complaint_data_points(bsObj, 'Court')
        Ref_court_list.append(Ref_court)
        # Docket
        Ref_docket = scraper_module_1.get_referenced_complaint_data_points(bsObj, 'Docket')
        Ref_docket_list.append(Ref_docket)
        # Judge
        Ref_judge = scraper_module_1.get_referenced_complaint_data_points(bsObj, 'Judge')
        Ref_judget_list.append(Ref_judge)
        # Date Filed
        Ref_date_filed = scraper_module_1.get_referenced_complaint_data_points(bsObj, 'Date Filed')
        Ref_date_filed_list.append(Ref_date_filed)
        # Class Period Start
        Ref_class_period_start = scraper_module_1.get_referenced_complaint_data_points(bsObj, 'Class Period Start')
        Ref_class_period_start_list.append(Ref_class_period_start)
        # Class Period End
        Ref_class_period_end = scraper_module_1.get_referenced_complaint_data_points(bsObj, 'Class Period End')
        Ref_class_period_end_list.append(Ref_class_period_end)

        # LAW FIRM SECTION---------------------------------------------------------

        # Plaintiff Firm
        Plaintiff_firm = scraper_module_1.get_plaintiff_firm(bsObj)
        Plaintiff_firm_list.append(Plaintiff_firm)
        # Defense Counsel
        # TBD

    # Combined Metrics
    '''Add duration from filing - close date'''

    # Print Len Lists 
    #print('Length of Page Number List    => ', len(Page_number_list), '\n')
    #print('Length of ClaimType_IPO_list  => ', len(ClaimType_IPO_list), '\n')
    #print('Length of ClaimType_10b5_list => ', len(ClaimType_10b5_list))
    

    # DATA ORGANIZATION SECTION----------------------------------------------------

    # Create DataFrame to House Values
    df = pd.DataFrame({})
    df['Page_number'] = Page_number_list
    df['Defendant'] = Defendant_list
    df['Case_Status'] = Case_Status_list 
    df['Filing_date'] = Filing_date_list
    df['Close_date'] = Close_date_list
    df['Case_summary'] = Case_summary_list
    df['Sector'] = Sector_list
    df['Industry'] = Industry_list
    df['Ticker_symbol'] = Ticker_symbol_list
    df['Status_2'] = Status_2_list
    df['Headquarters'] = Headquarters_list
    df['Company_Market'] = Company_market_list
    df['First_Court'] = First_court_list
    df['First_Docket'] = First_docket_list
    df['First_Judge'] = First_judge_list
    df['First_Date_Filed'] = First_date_filed_list
    df['First_Class_Period_Start'] = First_class_period_start_list
    df['First_Class_Period_End'] = First_class_period_end_list
    df['Ref_Court'] = Ref_court_list
    df['Ref_Docket'] = Ref_docket_list
    df['Ref_Judge'] = Ref_judget_list
    df['Ref_Date_Filed'] = Ref_date_filed_list
    df['Ref_Class_Period_Start'] = Ref_class_period_start_list
    df['Ref_Class_Period_End'] = Ref_class_period_end_list
    df['Plaintiff_Firm'] = Plaintiff_firm_list
    df['ClaimType_IPO'] =  ClaimType_IPO_list
    df['ClaimType_10b5'] = ClaimType_10b5_list

    # CLEAN UP DATAFRAME
    '''Because there are many pages that include none values, a quick way of getting rid of them
    is to sort the date in descending order'''

    df_final = df.sort_values('Filing_date', ascending = False) 

    # Generate Today's Date
    Todays_date_time = datetime.today().strftime('%Y%m%d_%H%M')
    

    # Write to Excel
    if Write_to_excel == True:
        os.chdir('/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Scraper_output')
        scraper_module_1.write_to_excel(df_final, 'SCA_scraper_data_export_'+ Todays_date_time)
    else:
        print(df_final)
    
    return None



# Execute Code
SCA_data_scraper(Url, Beginning_page, False)  
























