#!/usr/bin/env python3
# -*- coding: utf-8 -*-




'''FIXING RUN ON NEXT PAGE

1.) Page Count:         Is off.  Our the last defendant name in our database 
                        is FCP Financial Holdings w/ a page number of 6259 
                        where as the actual page number is 106759.  
                        I think we need to fix the count and add a primary key to our db
                        so that we can properly refer to the correct page on 
                        the web that coincides with the case. 
                        Note:  In fact, we may just want to save the entire URL, 
                        this way we can use it in our code without any modifications. 
    Solution:           You can see the solution in the below script.  the html object 
                        is the web page address.  So we would
                        replace the input of 'Count' in our mainscraper function 
                        (import from module 4) w/ a similar html
                        object that we passed to access the page.  This way what 
                        we scrape and record as the page in our db
                        should be the same (obviously we'll need to double check 
                        as the count seems to be skipping the blank pages). 
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
import Module_0_utility_functions as m0
import Module_1_Scraper_DataPoints as m1
import Module_2_Scraper_Scrape_CaseSummary as m2
import Module_3_Dict_Derived_Values as m3
import Module_4_Main_Scraper_Function as m4
import Module_5_Scraper_Automation as m5


### TARGET OUTPUT DIR
target_output_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Scraper_output'

### SQL INSTANTIATIONS_________________________________________________________
mydb = mysql.connector.connect(
        host="localhost",
        user="ccirelli2",
        passwd="Work4starr",
        database='SCA_SCRAPER')


### WEB PAGE OBJECTS____________________________________________________________ 
Url = 'http://securities.stanford.edu/filings-case.html?id='


### SCRAPER_______________________________________________________________________

def SCA_data_scraper(Url, add_pages = 20, Run_type = 'Start_from_last_page', email_report = True):  
    '''Input:
    Run_type:       Two options, Reset or Start_from_last_lage
    Url:            The web page from which we are scraping data
    add_pages:    Using the 'Start_from_last_page selection, pages_2_add is an additional
                    page to add to the 'Beginning_page' object.  Sometimes the webpage manager
                    choses to insert blank pages into the numerical sequence of pages, which
                    trips up the scraper. 
        
    
    '''
    # Table Object
    table = 'SCA_DATA3_TEST'
  
    # SCRAPER______________________________________________________________________________________
    
    # RUN-TYPE - RESET
    if Run_type == 'Reset':
        # Reset count values
        Count = 0
        Beginning_page = 100600
        End_page = 106750

        # Clear Database
        print('Clearing data from table {}'.format(table))
        mycursor    = mydb.cursor()
        sql         = "DELETE FROM {} WHERE page_number IS NOT NULL".format(table)     
        # This will not work since we changed the values to varchar()
        mycursor.execute(sql)
        mydb.commit()
        
        # Create Range for Loop
        upper_bound = End_page - Beginning_page
        range_value = range(0, upper_bound)
        
        # Enter For Loop & Scrape All Pages in Range.  
        for x in range_value:
        
            # Increment Count
            Count += 1

            # Progress Recorder - % Total Pages Scraped      
            m1.progress_recorder(Count, upper_bound)

            # Create Beautiful Soup Object per article
            html = urlopen(Url + str(Beginning_page + Count))
            web_page_address = (Url + str(Beginning_page + Count))
            bsObj = BeautifulSoup(html.read(), 'lxml')
            
            # Check to See if Page is Blank
            '''Blank Page:      Don't scrape page and most to next 
               the range of pages from beginning until end.  This creates issues for the scraper.  
               If we hit a blank page, the code will increment the count but skip scraping the page. 
            '''
            Tags = bsObj.find('section', {'id':'company'})
            Defendant = Tags.find('h4').get_text().split(':')[1]
            regex_exp = re.compile(' *[A-Z]+')
            search = re.search(regex_exp, Defendant)

            # If Page Is Not Blank - Scrape
            if bool(search) is True:
                # Load Main Scraper Function
                m4.main_scraper_function(mydb, table, bsObj, web_page_address)
            # Elif Blank - Just increase count & move to the next page
                # do nothing

    

    # RUN-TYPE - START FROM LAST PAGE
    elif Run_type == 'Start_from_last_page':
        
        # Set Count Objects - Add One Page
        Beginning_page  =           int(m5.get_last_page_scraped(mydb, table))
        End_page        =           Beginning_page + add_pages
        Count           =           0        

        # Status
        print('Scraper starting from count {}'.format(Beginning_page))

        # Create Range for Loop
        upper_bound = End_page - Beginning_page
        range_value = range(0, upper_bound)

        # Enter For Loop & Scrape All Pages in Range.  
        for x in range_value:

            # Count
            Count += 1

            # Progress Recorder - % Total Pages Scraped      
            m0.progress_recorder(Count, upper_bound)

            # Create Beautiful Soup Object per article
            html = urlopen(Url + str(Beginning_page + Count))
            web_page_address = (Url + str(Beginning_page + Count))
            bsObj = BeautifulSoup(html.read(), 'lxml')

            # Check to See if Page is Blank
            '''Blank Page:      Don't scrape page and most to next 
               the range of pages from beginning until end.  This creates issues for the scraper.  
               If we hit a blank page, the code will increment the count but skip scraping the page. 
            '''
            Tags = bsObj.find('section', {'id':'company'})
            Defendant = Tags.find('h4').get_text().split(':')[1]
            regex_exp = re.compile(' *[A-Z]+')
            search = re.search(regex_exp, Defendant)

            # If Page Is Not Blank - Scrape
            if bool(search) is True:
                # Load Main Scraper Function
                m4.main_scraper_function(mydb, table, bsObj, web_page_address)
                
            # Elif Blank - Just increase count & move to the next page
                # do nothing
        
        # Print Summary Report Upon Completion 
        m0.driver_function_post_run_scraper_status_report(mydb, 'Start_from_last_page', 
                                        Beginning_page, End_page)

        # Email Report

        if email_report = True:
            m0.send_email(
                    from_address = 'intellisurance@gmail.com', 
                    to_address   = 'intellisurance@gmail.com', 
                    timeout_sec  = 5, 
                    password     = 'Work4*****', 
                    message      = 'test message from python script')


    # Function Returns Nothing
    return None
    # ---------------------------------------------------------------------------------------





# RUN SCRAPER FUNCTION_____________________________________________________________________


#SCA_data_scraper(Url, add_pages = 20, Run_type = 'Start_from_last_page', email_report = True)


















