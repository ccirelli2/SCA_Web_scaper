# PURPOSE
'''
Mine the actual SCA fillings for key words and phrases to include in our attribute dictionary. 
'''

# Import Libraries
import os
import Module_2_Scraper_CaseSummary as m2
import pandas as pd


# Text Objects
dir_data = r'/home/ccirelli2/Desktop/Programming/Data_sets/filings_text_legal_team'
target_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Concat_txt_page_case_summary'
os.chdir(target_dir)
concatenated_txt_file = open('concat_text_scraped_09222018.txt').read()


'''How would you get the average representation of each 
token in each document?

1.) After we have our list of tokens, loop back through each document. 
    - Loop through each document and add a one to a new dictionary every time
      the word is found. 
    - Break once found. 
    - At the end, divide your values by the total number of documents. 
    - That will give you the average appearance of those words. 

'''


def pipeline_get_bigram_freq(concatenated_txt_file, ngram_type):
    # Tokenize & Clean Text
    print('Cleaning & tokenizing text', '\n')
    clean_tokenized_text = m2.clean_and_tokenize_text(concatenated_txt_file)

    # Generate Ngrams
    print('Generating Ngrams List Object', '\n')
    ngrams = m2.get_Ngrams(clean_tokenized_text, ngram_type)

    # Generate Fequency of Ngrams
    print('Generating frequency of Ngrams', '\n')
    freq_ngrams = m2.get_freq_ngrams(ngrams)
    test = freq_ngrams.transpose()
    ngram_column = m2.create_Ngram_column(test, ngram_type)
    m2.write_to_excel(ngram_column, str(ngram_type))

    return None



pipeline_get_bigram_freq(concatenated_txt_file, 'Bigrams')

#ngram_freq_file = (r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Code/SCA_concat_txt_output/ngrams.xlsx')

#df_ngrams = pd.read_excel(ngram_freq_file)

#print(df_ngrams.loc('Ngrmas'))

