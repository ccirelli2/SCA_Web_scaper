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


import os
import json
import logging
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
import mysql.connector
import Module_5_Scraper_Automation as m5
import Module_4_Main_Scraper_Function as m4
import Module_1_Scraper_DataPoints as m1
import Module_0_utility_functions as m0

with open('./config.json', 'r') as f:
    config = json.load(f)

stemmer = PorterStemmer()


# TARGET OUTPUT DIR
target_output_dir = config.get('target_output_dir', '/tmp')

mydb = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    passwd=os.environ['MYSQL_PASSWORD'],
    database=config['database']['database'])

# WEB PAGE OBJECTS____________________________________________________________
URL = config['webPageObjects']

def SCA_data_scraper(Url, add_pages, Run_type, report_output_type, password):
    '''
    INPUTS
    Url:    Stanford Law Web Page - Target of scraper
    Run_type:       Two options, Reset or Start_from_last_lage
    Url:            The web page from which we are scraping data
    add_pages:      Using the 'Start_from_last_page selection, pages_2_add is an additional
                    page to add to the 'Beginning_page' object.  Sometimes the webpage manager
                    choses to insert blank pages into the numerical sequence of pages, which
                    trips up the scraper.
    report_output   Type of output the user wants to generate.  Used only for the 'Start_from_last_page
                    selection (need to sync up with driver function for gen reports.
    password        email account password (omitt from base script)
    '''
    #table = 'SCA_data'
    table = 'SCA_DATA3_TEST'

    breakpoint()
    # RUN-TYPE - RESET
    if Run_type == 'Reset':
        # Reset count values
        Count = 0
        Beginning_page = 100600
        End_page = 106750

        # Clear Database
        print('Clearing data from table {}'.format(table))
        mycursor = mydb.cursor()
        sql = "DELETE FROM {} WHERE page_number IS NOT NULL".format(table)
        # This will not work since we changed the values to varchar()
        mycursor.execute(sql)
        mydb.commit()

        # Create Range for Loop
        upper_bound = End_page - Beginning_page
        range_value = range(0, upper_bound)

        # Enter For Loop & Scrape All Pages in Range.
        for _ in range_value:
            # Increment Count
            Count += 1

            # Progress Recorder - % Total Pages Scraped
            m1.progress_recorder(Count, upper_bound)

            # Create Beautiful Soup Object per article
            html = urlopen(Url + str(Beginning_page + Count))
            web_page_address = (Url + str(Beginning_page + Count))
            bsObj = BeautifulSoup(html.read(), 'lxml')

            # Check to See if Page is Blank
            # Blank Page:      Don't scrape page and most to next
            #    the range of pages from beginning until end.  This creates issues for the scraper.
            #    If we hit a blank page, the code will increment the count but skip scraping the page.
            Tags = bsObj.find('section', {'id': 'company'})
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
        Beginning_page = int(m5.get_last_page_scraped(mydb, table))
        End_page = Beginning_page + add_pages
        Count = 0

        # Status
        print('Scraper starting from count {}'.format(Beginning_page))

        # Create Range for Loop
        upper_bound = End_page - Beginning_page
        range_value = range(0, upper_bound)

        # Enter For Loop & Scrape All Pages in Range.
        for _ in range_value:

            # Count
            Count += 1

            # Progress Recorder - % Total Pages Scraped
            m0.progress_recorder(Count, upper_bound)

            # Create Beautiful Soup Object per article
            html = urlopen(Url + str(Beginning_page + Count))
            web_page_address = (Url + str(Beginning_page + Count))
            bsObj = BeautifulSoup(html.read(), 'lxml')

            # Check to See if Page is Blank
            Tags = bsObj.find('section', {'id': 'company'})
            Defendant = Tags.find('h4').get_text().split(':')[1]
            regex_exp = re.compile(' *[A-Z]+')
            search = re.search(regex_exp, Defendant)

            # If Page Is Not Blank - Scrape
            if bool(search) is True:
                # Load Main Scraper Function
                m4.main_scraper_function(mydb, table, bsObj, web_page_address)
            # Otherwise, go to next page
            else:
                pass

        # Generate Report (Email or Print)-----------------------------------------

        # Otherwise print results
        if report_output_type == 'print_results':
            m0.driver_function_post_run_scraper_report(mydb, Beginning_page,
                                                       End_page, 'print_results')

        if report_output_type == 'generate_email':
            # DataFrame w/ Results
            m0.driver_function_post_run_scraper_report(mydb, Beginning_page, End_page, 'dataframe_w_results')
            # Filename + Path for DataFrame as Excel File
            Excel_file = m0.driver_function_post_run_scraper_report(mydb, Beginning_page, End_page, 'dataframe_filename_plus_path')

            # Generate Text File - Body of Email
            #'''function returns str of filename + path'''
            email_body_filename = m0.driver_function_post_run_scraper_report(mydb, Beginning_page,
                                                                             End_page, 'email_text_body')

            # Generate Email
            m0.email_with_attachments(
                password=password,   # input for top lvl scraper function
                toaddr='chris.cirelli@starrcompanies.com',
                subject='Intellisurance Securities Class Action Scraper Update',
                body=open(email_body_filename).read(),
                attachment_filename=Excel_file
            )

SCA_data_scraper(URL, add_pages=20, Run_type=config['runType'], report_output_type='generate_email', password='Work4starr')

# Logging
print('\n Generating loggin file')
logging.basicConfig(
    filename=config.get('logFile', '/tmp/logs.txt'),
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s')
print('Log files saved to {}')
