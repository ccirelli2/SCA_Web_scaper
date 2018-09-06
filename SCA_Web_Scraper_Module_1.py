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


def write_to_excel(dataframe, filename):
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, 'Data')
    writer.save()

# CASE SUMMARY----------------------------------------------------

def get_title(Url):
    # Create Bs4
    html = urlopen(Url)
    bsObj = BeautifulSoup(html.read(), 'lxml')   
    return bsObj.find() 

def get_case_status(Obj):   
    # Scrape Only News Article Links
    Tags = Obj.find('section', {'id':'summary'})
    Status = Tags.find('p').get_text()
    return Status

def get_defendant(Obj):
    # Scrape Only News Article Links
    Tags = Obj.find('section', {'id':'summary'})
    Defendant = Tags.find('h4').get_text().replace('Securities Litigation', '')
    return Defendant

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


# DEFENSE COUNSEL AND PLAINTIFF FIRM-------------------------------------------

def get_plaintiff_firm(Obj):
    Ref_complaint = Obj.find('section', {'id':'ref'})
    if Ref_complaint != None:
        Container = Ref_complaint.find('ol', {'class':'styled'})
        if Container != None:
            Firms = Container.find('li').get_text()
            return Firms
        else:
            return None
    else:
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




# MINE CASE SUMMARY-----------------------------------------------------------
'''Values to min
1.) Statutes referenced:  Ex 1934 Act, ERISA, etc. 
2.) Violations
3.) Type of lawsuit:  Probably need to create categories.  Ex involving a merger. 
4.) Allegations:  ex:  false and misleading statements. 
5.) Earnings
6.) Stock drop %. 
'''

def concat_text_from_case_summary(new_file_name):

    # Identify Excel File
    target_dir = '/home/ccirelli2/Desktop/Programming/SCA_Web_scaper'
    File = 'SCA_scraper_data_export.xlsx'
    df = pd.read_excel(target_dir+'/'+File)
    # Limit datafrmae to Case Summary Text
    df_case_summary = df['Case_summary']
    
    # Create new write file
    New_File = open(str(new_file_name) + '.txt','w')

    # Create Loop Through List of Directories
    for row in df_case_summary:

        # Write files to new file
        New_File.write(str(row))
        New_File.write('\n')

    # Close File
    New_File.close()
    print('Case study text concatenated\n')
    return None


def clean_andTokenize_text(Text_file):
    '''
    Input      = Text File
    Operations = Tokenize, lowercase, strip punctuation/stopwords/nonAlpha
    Return     = Object = Set; Set = cleaned, isalpha only tokens
    '''
    # Strip Lists
    Punct_list = set((punct for punct in string.punctuation))
    Stopwords = nltk.corpus.stopwords.words('english')
    Set_names = get_set_human_names()
    # Tokenize Text
    Text_tokenized = nltk.word_tokenize(Text_file)
    # Convert tokens to lowercase
    Text_lowercase = (token.lower() for token in Text_tokenized)
    # Strip Punctuation
    Text_tok_stripPunct = filter(lambda x: (x not in Punct_list), Text_lowercase)
    # Strip Stopwords
    Text_strip_stopWords = filter(lambda x: (x not in Stopwords), Text_tok_stripPunct)
    # Strip Non-Alpha
    Text_strip_nonAlpha = filter(lambda x: x.isalpha(), Text_strip_stopWords)
    # Strip 2 letter words
    Text_strip_2letter_words = filter(lambda x: len(x)>3, Text_strip_nonAlpha)
    # Strip names
    Text_strip_names_2 = filter(lambda x: x not in Set_names, Text_strip_2letter_words)
    # Take Stem of Each Token 
    Text_stem = [stemmer.stem(x) for x in Text_strip_names_2]
    # Note that we are not returning a set here as with Ngrams we are looking for patters which could be altered materially by using
    # a set function, which is better used outside the function if need be. 
    return Text_stem




















