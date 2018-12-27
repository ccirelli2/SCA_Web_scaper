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



'''PURPOSE

The purpose of this script is to create the functions that will automate the 
scraping of the SCA Web Page

'''

def exec_gen_sql_command(mydb, sql_command):
    '''Input
    mydb:           database instance
    sql_command:    string of general sql command     
    '''
    mycursor = mydb.cursor()
    mycursor.execute(sql_command)
    myresult = mycursor.fetchall()
    return myresult


def type_of_scraper_run(run_type, mydb):
    '''
    Purpose:        The purpose of this function is to control the way the scraper runs. 
    Functionality:  If run_type = True, the scraper will start from the beginning and delete
                    all existing data in the database. 
                    If run_type = False, the scraper will start from the last page scraped.
    '''
    if run_type == 'Reset':
        mycursor    = mydb.cursor()
        sql         = "DELETE FROM SCA_data WHERE page_number > 0"
        mycursor.execute(sql)
        mydb.commit()
    
    elif Delete_prior_run == 'Start_from_last_page':
        # Reset Last_count object (last page scraped) to the max value.    
        '''
        Last_Count:     Equals the max page value in the database.
        Beginning_page: Equals our last page + 1, i.e. the next page.
        End_page:       Equals our beginning page +1.  
                        The obj is to scrape the next page.'''
        Beginning_page  = Last_count + 1
        End_page        = Beginning_page + 1

        # Check to see if this page is blank.
        '''
        Before starting our scraper, lets check to see if this next page is blank.  If blank,
        then lets assume that the administrator of the web page has not added added a new lawsuit
        and there is no need to try to scrape it
        '''
        # Create Beautiful Soup Object per article
        html = urlopen(Url + str(Beginning_page))
        bsObj = BeautifulSoup(html.read(), 'lxml')
        Tags = bsObj.find('section', {'id':'company'})
        if bool(Tags) == False:
            Next_page_null = True
            print('Warning:  The next page was blank.  Scraping is stopping.  Try again later')
            
            
        
        return None




def get_last_page_scraped(mydb, table):
    '''
    Myresult = [('http://securities.stanford.edu/filings-case.html?id=103165',)]
               Therefore, our first index returns the string within this list. 
               The second splits the string on = and returns the second value of that
               list, which should be our page number that coincides with the actual
               url. 
    '''
    # Get last page number scraped
    mycursor        = mydb.cursor()
    sql             = "SELECT max(page_number) FROM {}".format(table)
    mycursor.execute(sql)
    myresult        = mycursor.fetchall()
    last_page       = myresult[0][0].split('=')[1]
    
    return last_page


def check_page_blank(Url, beginning_page):
    html = urlopen(Url + str(beginning_page))
    bsObj = BeautifulSoup(html.read(), 'lxml')
    Tags = bsObj.find('section', {'id':'company'})
    Defendant = Tags.find('h4').get_text().split(':')[1]
    regex_exp = re.compile(' *[A-Z]+')
    search = re.search(regex_exp, Defendant)
    return search

