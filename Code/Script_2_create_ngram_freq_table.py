## WEB SCRAPER - SCRIPT 2____________________________________________________

'''Purpose
The purpose of this script is to design a series of functions to analyze the 
text from the case summary. 

1.) Clean & tokenize text
2.) Ngram frequency table
3.) Dictionary major categories and values
4.) Functions to develop new value columns in our main scraper function. 

'''

## Import Libraries
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

## Import Modules
import SCA_Web_Scraper_Module_2 as scraper_module_2

## FILES
target_directory = '/home/ccirelli2/Desktop/Programming/SCA_Web_scaper'
# Scraper Output
scraper_out_put_file = 'SCA_scraper_data_export.xlsx'
# Concatenated Text
file_concat_case_text = '/concat_text_scraped_09082018.txt'



## CONCAT CASE SUMMARIES______________________________________________

#scraper_module_2.concat_text_from_case_summary(target_directory, 
 #                                       scraper_out_put_file, 
  #                                      'concat_text_scraped_09222018')



## CREATE KEY WORD FREQUENCY TABLE___________________________________

def get_word_freq_case_summary(directory, File, write_2_excel, Ngram_type, New_file_name):
    '''
    Refine your progress function to either act as a len of list or single value
    '''
    # Import File
    Case_summary_text = open(directory + '/' + File).read()
    
    # Clean and tokenize text
    Clean_tokenized_text = scraper_module_2.clean_and_tokenize_text(Case_summary_text)
    
    # Create NGRAMS
    Ngrams = scraper_module_2.get_Ngrams(Clean_tokenized_text, Ngram_type) 
    # Create Dictionary Object
    Dictionary = {}
    
    # Create Word Frequency Table
    for token in Ngrams:
        Dictionary[token] = Dictionary.get(token, 0) + 1
    
    # Create dataframe
    df = pd.DataFrame(Dictionary, index = [0]).transpose()
    
    # Create Ngram Column
    df_with_ngram_column = scraper_module_2.create_Ngram_column(df, Ngram_type)
    if write_2_excel == True:
        scraper_module_2.write_to_excel(df_with_ngram_column, New_file_name + '_' + Ngram_type)
        print('Frequency table written to +>' , print(directory + '/'))
    else:
        print(df.head())
    return df_with_ngram_column


test = get_word_freq_case_summary(  target_directory, 
                                    file_concat_case_text, 
                                    True, 
                                    'Bigrams', 
                                    'Ngram_freq_tabled')







