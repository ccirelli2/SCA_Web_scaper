#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''FIXING RUN ON NEXT PAGE


1.) Page Count:         Is off.  Our the last defendant name in our database is FCP Financial Holdings w/ a page number of 6259 
                        where as the actual page number is 106759.  I think we need to fix the count and add a primary key to our db
                        so that we can properly refer to the correct page on the web that coincides with the case. 
                        Note:  In fact, we may just want to save the entire URL, this way we can use it in our code without any modifications. 
                        Solution:  You can see the solution in the below script.  the html object is the web page address.  So we would
                                   replace the input of 'Count' in our mainscraper function (import from module 4) w/ a similar html
                                   object that we passed to access the page.  This way what we scrape and record as the page in our db
                                   should be the same (obviously we'll need to double check as the count seems to be skipping the blank
                                   pages). 

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
import Module_1_Scraper_DataPoints as m1
import Module_2_Scraper_CaseSummary as m2
import Module_3_Dict_Derived_Values as m3
import Module_4_Main_Scraper_Function as m4
import Module_5_Scraper_Automation as m5


### SQL INSTANTIATIONS_________________________________________________________
mydb = mysql.connector.connect(
        host="localhost",
        user="ccirelli2",
        passwd="Work4starr",
        database='SCA_SCRAPER')


### WEB PAGE OBJECTS____________________________________________________________ 
Url = 'http://securities.stanford.edu/filings-case.html?id='



### SCRAPER_______________________________________________________________________

def SCA_data_scraper(Url, add_pages, Run_type = 'Start_from_last_page'):  
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

    # Count Objects
    '''Establishes the values for where the scraper starts and ends'''
    Last_count      = m5.get_last_page_scraped(mydb)
    Beginning_page  = 0
    End_page        = 0
    Count           = 0  
   
    # Next Page Null Check 
    '''This object is used to control the flow of the code when Delete prior to run is set to True.  
    Next_page_null = True:      The default value for this object is False.
                   Action:      The value is changed to True when the function "type_of_scraper"'''
    Next_page_null = False
     
    # Check Run-Type:
    '''
    Function:       "type_of_scraper_run"
    Purpose:        The purpose of this function is to control how the scraper runs. 
    Run_type        May be Reset or run_from_last_count.
                    If "Reset" the scraper will delete all prior data and start from page 0. 
                    If "Start_from_last_page", the scraper checks whether the next page is blank, and if not, 
                    it will proceed to scrape the page. For every iteration of the code in the While loop, 
                    so long as the next page is not null it will continue to scrape subsequent pages.
    '''
    
 

    # SCRAPER_______________________________________________________________________________________
    
    # RUN-TYPE - RESET
    if Run_type == 'Reset':
        # Reset count values
        Last_count = 0
        Count = 0
        Beginning_page = 100600
        End_page = 106750
        # Clear Database
        mycursor    = mydb.cursor()
        sql         = "DELETE FROM SCA_data WHERE page_number > 0"     # This will not work since we changed the values to varchar()
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
                m4.main_scraper_function(mydb, table, bsObj, Count)
            # Elif Blank - Just increase count & move to the next page
                # do nothing

    

    # RUN-TYPE - START FROM LAST PAGE
    elif Run_type == 'Start_from_last_page':

        # Assume next page equals True
        Next_page_null == True
        
        # Set Count Objects - Add One Page
        '''Inputs:
        First_run_beginning_page:   The first page we started scraping when run_type was set to reset. 
        Last_page:                  Count of last page scraped in our database. 
        Beginning_page:             Summation of First run + Last count in our db + 1 + add_pages'''
        First_run_beginning_page =  100600 
        Beginning_page  =           First_run_beginning_page + Last_count + 1 + add_pages
        End_page        =           Beginning_page + 1
        Count           =           Beginning_page - First_run_beginning_page
  
        # Status
        print('Scraper starting from count {}'.format(Beginning_page))

        # Create Beautiful Soup Object
        search = m5.check_page_blank(Url, Beginning_page)

        # Check to see if page Tag is blank
        if bool(search) == False:
            # If blank, set Next_page_null to True so that the while loop will not start. 
            Next_page_null = True
            print('Attention:  The next page was blank.  Scraping is stopping.  Try again later')

        # If Next Page Not Null - Enter While Loop 
        while Next_page_null == False:                

            # Create Range for Loop
            upper_bound = End_page - Beginning_page
            range_value = range(0, upper_bound)

            # Once we've confirmed that the Last_page_null = False, we can let the loop run its course. 
            for x in range_value:
                                 
                # Increment Page Count
                Count += 1
                
                # Progress Recorder      
                m1.progress_recorder(Count, upper_bound)          

                # Create Beautiful Soup Object per article
                html = urlopen(Url + str(Beginning_page + Count))
                bsObj = BeautifulSoup(html.read(), 'lxml')
            
                # Load Main Scraper    
                m4.main_scraper_function(mydb, table, bsObj, Count)
            
                # Check to see if next page is null. Used to Exit While Loop
                search = m5.check_page_blank(Url, Beginning_page)
                
                # Check to see if page Tage is blank
                if bool(search) == False:
                # If blank, set Next_page_null to True so that the while loop will not start. 
                    Next_page_null = True

        # Once While Loop Breaks
        '''Add a progress report that updates the user on the new SCA filling and runs the ML piece.''' 


    return None


# RUN FUNCTION
SCA_data_scraper(Url, 0, 'Reset')




