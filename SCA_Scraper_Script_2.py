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
import SCA_Web_Scraper_Module_1 as scraper_1


## CONCAT CASE SUMMARIES______________________________________________

#scraper_1.concat_text_from_case_summary('concat_text_scraped_09082018')



## CREATE KEY WORD FREQUENCY TABLE___________________________________

def get_word_freq_case_summary(Excel):
    # Import File
    directory = '/home/ccirelli2/Desktop/Programming/SCA_Web_scaper'
    File = '/concat_text_scraped_09082018.txt'
    Case_summary_text = open(directory+File).read()

    # Clean and tokenize text
    Clean_tokenized_text = scraper_1.clean_and_tokenize_text(Case_summary_text)

    # Create Dictionary Object
    Dictionary = {}

    # Create Word Frequency Table
    for token in Clean_tokenized_text:
        Dictionary[token] = Dictionary.get(token, 0)+1

    # Create dataframe
    df = pd.DataFrame(Dictionary, index = [x for x in range(0, len(Dictionary))]).transpose()
    
    if Excel == True:
        scraper_1.write_to_excel(df, 'Word Frequency Table')
    else:
        print(df.head())
    
    return df 


word_freq = get_word_freq_case_summary(False)

print(word_freq.head())









