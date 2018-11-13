#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 21:11:48 2018

@author: ccirelli2
"""

'''Note:
    
    We should really only create one bsObj per artcile and then scrape all of the
    data from that one artcile.  The below code creates a new bsObj per object
    which will be very taxing as the number of objects and articles grows. 


'''

# Import Libraries
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


# UTILITY FUNCTIONS---------------------------------------------

def write_to_excel(dataframe, filename):
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, 'Data')
    writer.save()

def progress_recorder(Count_obj, range_value_obj):
    '''
    Inputs      
        Count_obj:  This is the current count of the for loop, i.e. the current count of the number of pages scraped.  
        range_value_obj: This represents the integer value of the last page of the web page minus the first, so the total number of pages to scrape.       
    '''
    if Count_obj == 1:
        print('Scraper started')
    elif Count_obj == round(range_value_obj * 0.01, 0):
        print('1% Complete')
    elif Count_obj == round(range_value_obj * 0.05, 0):
        print('5% Complete')
    elif Count_obj == round(range_value_obj * 0.1,0):
        print('10% Complete')
    elif Count_obj == round(range_value_obj * 0.15,0):
        print('15% Completed')
    elif Count_obj == round(range_value_obj * 0.20,0):
        print('20% Complete')
    elif Count_obj == round(range_value_obj * 0.25,0):
        print('25% Completed')
    elif Count_obj == round(range_value_obj * 0.3,0):
        print('30% Completed')
    elif Count_obj == round(range_value_obj * 0.35,0):
        print('35% Completed')
    elif Count_obj == round(range_value_obj * 0.4,0):
        print('40% Completed')
    elif Count_obj == round(range_value_obj * 0.5,0):
        print('50% Completed')
    elif Count_obj == round(range_value_obj * 0.6,0):
        print('60% Completed')
    elif Count_obj == round(range_value_obj * 0.7,0):
        print('70% Completed')
    elif Count_obj == round(range_value_obj * 0.8,0):
        print('80% Completed')
    elif Count_obj == round(range_value_obj * 0.9,0):
        print('90% Completed')
    elif Count_obj == round(range_value_obj * 1.0,0):
        print('RRRRRR!!!!!!.......Scraping 100% Complete!!')
        print('Ok to proceed to the next job!')
    return None        


def pre_run_scraper_status_report(Run_type, End_page):
    
    if Run_type == 'Start_from_last_page':
        print('Scraper starting from the last page scraped, which is {}'.format(End_page))
    elif Run_type == 'Reset':
        print('''The user has selected the reset run-option.  The scraper will 
                proceed to delete all prior data and start to scrape from page 0''')

    return None


# CASE SUMMARY----------------------------------------------------

def get_title(Url):
    # Create Bs4
    html = urlopen(Url)
    bsObj = BeautifulSoup(html.read(), 'lxml')   
    return bsObj.find() 

def get_case_status(Obj):   
    # Scrape Only News Article Links
    Tags = Obj.find('section', {'id':'summary'})
    if Tags != None:
        Status = Tags.find('p').get_text()
        return Status
    else:
        return 'Status Not Found'

def get_defendant(Obj):
    # Scrape Only News Article Links
    Tags = Obj.find('section', {'id':'company'})
    # Check if tag text is blank. 
    H4 = Tags.find('h4').get_text()
    Defendant = H4.split(':')[1]
    if Defendant != None:
        return Defendant
    else:
        return 'No Defendant Found'

def get_filing_date(Obj):
    # Limit to the summary section
    Section_summary = Obj.find('section', {'id':'summary'})
    # From the summary section, limit to the filing date
    Section_p = Section_summary.find('p', {'class':'lead'}).get_text()
    # Split string 'Filing Date: Month Day, Year, to just the date'
    Filing_date = Section_p.split(':')[1]
    # Return Filing Date
    return Filing_date

def get_close_date(Obj):
    # Limit to the summary section
    Section_summary = Obj.find('section', {'id':'summary'})
    Paragraph = Section_summary.find('p').get_text()
    regex = re.compile('[0-9][0-9]*/[0-9][0-9]*/[0-9]*')
    search = re.search(regex, Paragraph)
    # Check to see if the search returns a nul value. 
    if search == None:
        return None
    # If positive, return the date value. 
    else:
        date_value = search.group()
        return date_value

def get_case_summary(Obj):
    # Limit to the summary section
    Section_summary = Obj.find('section', {'id':'summary'})
    Description = Section_summary.find('div', {'class':'span12'}).get_text()
    return Description


# COMPANY INFORMATION-------------------------------------------------------


def get_company_data_points(Obj, data_point):
    '''data_point choices
        Sector, Industry, Symbol, Status, Headquarters, Company Market'''

    # Limit to the summary section
    Section_summary = Obj.find('section', {'id':'company'})
    Description = Section_summary.findAll('div', {'class':'span4'})
    for data in Description:
        if data_point == 'Sector':
            if 'Sector' in data.get_text():
                bs_sector_obj = data.get_text().split(':')[1]
                return bs_sector_obj
        elif data_point == 'Industry': 
            if 'Industry' in data.get_text():
                bs_industry_obj = data.get_text().split(':')[1]
                return bs_industry_obj
        elif data_point == 'Symbol':
            if 'Symbol' in data.get_text():
                bs_symbol_obj = data.get_text().split(':')[1]
                return bs_symbol_obj
        elif data_point == 'Status':
            if 'Status' in data.get_text():
                bs_status_obj = data.get_text().split(':')[1]
                return bs_status_obj
        elif data_point == 'Headquarters':
            if 'Headquarters' in data.get_text():
                bs_headquarters_obj = data.get_text().split(':')[1]
                return bs_headquarters_obj
        elif data_point == 'Company Market':
            if 'Company Market' in data.get_text():
                bs_co_market_obj = data.get_text().split(':')[1]
                return bs_co_market_obj
        else:
            return None


# FIRST IDENTIFIED COMPLAINT------------------------------------------------

def get_first_complaint_data_points(Obj,data_point):
    '''Data point options:
        Court, Docket, Judge, Date Filed, Class Period Start, Class Period End'''

    First_identified_complaint = Obj.find('section', {'id':'fic'})
    # Check to see if search came up with a null value. 
    if First_identified_complaint == None:
        return None
    # Otherwise, proceed with scraping. 
    else:
        Complaint_data_points = First_identified_complaint.findAll('div', {'class':'span4'})
    # Once you obtain the list of values, iterate over the list to identify each data point. 
    for data in Complaint_data_points:
        if data_point == 'Court':
            if 'COURT' in data.get_text():
                return data.get_text().split(':')[1]
        elif data_point == 'Docket':
            if 'DOCKET' in data.get_text():
                return data.get_text().split(':')[1]
        elif data_point == 'Judge':
            if 'JUDGE' in data.get_text():
                return data.get_text().split(':')[1]
        elif data_point == 'Date Filed':
            if 'DATE' in data.get_text():
                return data.get_text().split(':')[1]
        elif data_point == 'Class Period Start':
            if 'START' in data.get_text():
                return data.get_text().split(':')[1]
        elif data_point == 'Class Period End':
            if 'END' in data.get_text():
                return data.get_text().split(':')[1]
        else:
            return None


def get_referenced_complaint_data_points(Obj,data_point):
    '''Data point options:
        Court, Docket, Judge, Date Filed, Class Period Start, Class Period End'''

    First_identified_complaint = Obj.find('section', {'id':'ref'})

    if First_identified_complaint != None:
        Complaint_data_points = First_identified_complaint.findAll('div', {'class':'span4'})
        # Once you obtain the list of values, iterate over the list to identify each data point.
        for data in Complaint_data_points:
            if data_point == 'Court':
                if 'COURT' in data.get_text():
                    return data.get_text().split(':')[1]
            elif data_point == 'Docket':
                if 'DOCKET' in data.get_text():
                    return data.get_text().split(':')[1]
            elif data_point == 'Judge':
                if 'JUDGE' in data.get_text():
                    return data.get_text().split(':')[1]
            elif data_point == 'Date Filed':
                if 'DATE' in data.get_text():
                    return data.get_text().split(':')[1]
            elif data_point == 'Class Period Start':
                if 'START' in data.get_text():
                    return data.get_text().split(':')[1]
            elif data_point == 'Class Period End':
                if 'END' in data.get_text():
                    return data.get_text().split(':')[1]


# DEFENSE COUNSEL AND PLAINTIFF FIRM-------------------------------------------

def get_plaintiff_firm(Obj):
    Ref_complaint = Obj.find('section', {'id':'fic'})
    if Ref_complaint != None:
        Container = Ref_complaint.find('ol', {'class':'styled'})
        if Container == None:
            return None
        else:
            try:
                Firms = Container.find('li').get_text()
                return Firms
            except AttributeError:
                return None
       

# Defense Counsel (TBD)



# DOCUMENTS AVAILABLE ON WEB PAGE---------------------------------------------

def get_titles_first_complaint_docs(Obj):
    First_identified_complaint_section = Obj.find('section', {'id':'fic'})
    
    Docs = First_identified_complaint_section.find('table', {'class':'table table-bordered table-striped table-hover'}).get_text()
    if 'No\nDocument Title' in Docs:
        return 'No Documents Found'
    else:
        return Docs

def get_titles_referenced_complaint_docs(Obj):
    Referenced_complaint_section = Obj.find('section', {'id':'ref'})
    Table = Referenced_complaint_section.find('table', {'class':'table table-bordered table-striped table-hover'})
    Entries = Table.findAll('tr', {'class':'table-link'})
    print(len(Entries))
    # Table for later















