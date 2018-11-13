#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 07:41:27 2018

@author: ccirelli2
"""

'''PURPOSE

The purpose of this script is to scrape data from the Stanford Law Securities
Class Action Web page and convert it to structured data for ML training. 

Structure Web Page List of Cases
Root =              http://securities.stanford.edu/
Specific Cases =    filings-case.html?id=106716
?id =               Specific case Id.  Need to identify range.  These are the 
                    pages that we would iterate over. You could also look into
                    downloading each page to your laptop maybe using bash curl. 


NEXT STEPS:

1.)                 In order to build out your classification dictionary, use the X number of cases
                    that GSU provided in Text.  Concat file and create a set of ngrmas. 
                    Then use these and the allegations combinations to build out the dictionary. 

2.)                 A lot of None values are showing up in the database. 



3.)                 We have three instances of determining if the pages are blank or not. 
                    This needs to get fixed. 


4.)                 We need to add an input value for the table at the function lvl. 
                    This way we can toggle between SCA_data and SCA_DATA_2.
                    It looks like this will need to be updated in the modules as well to update the
                    Insert functions. 

5.)                 SCA Type Dictionary:  Should be refined to ensure that we are capturing the correct
                    data points and that the categories at minimum match those being used by other
                    sources, including Standaford Law & ...


6.)               Test that the Scraper functions when updating the database once a new SCA has been filed,                     that it stops correctly and sends an email with an update. 

4.)                 Add a time object such that the function runs once a week. 


5.)                 Create a new module for the ML piece.  Ideally you will want to run the ML algorithm 
                    each time the database is updated. 

6.)                 Check the page counter.  There appeared to be issues with this with the prior run. 
                    Maybe you can add the URL to the database to ensure that the count is correct. 


7.)                 Automatic email blast:  Will need to include a cross reference with the Starr database
                    :to see if we write the account. 

8.)                 Lawsuit Status:  We need to accurately capture these fields.  Types:  'ONGOING', 
                    'DISMISSED', 'SETTLED', 'DISMISSED'....

9.)                 At a later date it would be nice to pull the stock drop that preceeded the filling of the
                    lawsuit and add that to the dataset.   Equally, we could integrate the last earnings
                    call and mine that for sentiment and or key phrases. 

10.)                Replace "Count" object with actually page number.  

'''


'''GUIDE TO SCRAPER


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
        sql         = "DELETE FROM SCA_data WHERE page_number > 0"
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
                m4.main_scraper_function(bsObj, mydb, Count)
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
                m4.main_scraper_function(bsObj, mydb, Count)
            
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




