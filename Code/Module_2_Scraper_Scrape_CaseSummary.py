## MODULE 2____________________________________________________________________

'''Purpose

The purpose of this module is to design functions that will be used to process
the text from the each case summary. 

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



# MINE CASE SUMMARY____________________________________________________
'''Values to min
1.) Statutes referenced:  Ex 1934 Act, ERISA, etc.
2.) Violations
3.) Type of lawsuit:  Probably need to create categories.  Ex involving a merger.
4.) Allegations:  ex:  false and misleading statements.
5.) Earnings
6.) Stock drop %.
'''

def concat_text_from_case_summary(target_dir, target_file, new_file_name):

    # Identify Excel File
    df = pd.read_excel(target_dir+'/'+ target_file)
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


def get_set_human_names():
    '''
    Purpose:  obtain a set of all human names
    Input:    none
    Output:   Set of of both female and male names
    '''
    # Create a list of Male names, convert to lower case, split on '\n' 
    # as the text reads in a string as unicode
    Male_names = corpus.names.open('male.txt').read().lower().split('\n')
    # Create a lise of female names, convert to lower case, split on '\n' 
    #as the text reads in a string as unicode
    Female_names = corpus.names.open('female.txt').read().lower().split('\n')
    # Return to the user a set of the concatenation of both lists. 
    return set(Male_names + Female_names)


def clean_and_tokenize_text(Text_file):
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
    #Text_strip_nonAlpha = filter(lambda x: x.isalpha(), Text_strip_stopWords)
    # Strip 2 letter words
    Text_strip_2_letter_words = filter(lambda x: len(x)>2, Text_strip_stopWords)
    # Strip names
    Text_strip_names = filter(lambda x: x not in Set_names, Text_strip_2_letter_words)
    # Take Stem of Words
    #Text_stem = [stemmer.stem(x) for x in Text_strip_names]
    return list(Text_strip_names)


def get_Ngrams(Clean_tokenized_text, Ngram_selection):
    # Create a list to capture Ngrams
    List_Ngrams = []
    
    # If Bigrams selected
    
    if Ngram_selection == 'Nograms':
        [List_Ngrams.append(x) for x in Clean_tokenized_text]
        
    elif Ngram_selection == 'Bigrams':
        [List_Ngrams.append((x,y)) for x,y in zip(Clean_tokenized_text, 
                                               Clean_tokenized_text[1:])]  
    # If Trigrams selected
    elif Ngram_selection == 'Trigrams':
        [List_Ngrams.append((x,y,z)) for x,y,z in zip(Clean_tokenized_text, 
                                                    Clean_tokenized_text[1:], 
                                                    Clean_tokenized_text[2:])]
    # If Quadgrams selected. 
    elif Ngram_selection == 'Quadgrams':
        [List_Ngrams.append((w,x,y,z)) for w,x,y,z in zip(Clean_tokenized_text, 
                                                    Clean_tokenized_text[1:], 
                                                    Clean_tokenized_text[2:], 
                                                    Clean_tokenized_text[3:])]
    # Return Ngrams list
    return List_Ngrams


# FUNCTION TO CREATE AN NGRAM COLUMN
    
def create_Ngram_column(dataframe, Ngrams):
    '''
    Purpose:    The purpose of this code is to:
                1.) to adjust our dataframe to account for the fact that the pandas multiindex merges the 
                cells that contain the same words.     
                2.) Create a single column that includes a tuple of the Ngrams.
                3.) Remove the old columns. 
                
    Input:      Output from our FreqDist function
    Output:     The same dataframe but without the individual word columns, which is replaced with a single column 
                representing our Ngrams. 
    '''
    
    # Create lists to capture each word in the target column. 
    List_level_0 = []
    List_level_1 = []
    List_level_2 = []
    
    # Create a list to capture our new column where the none values are converted to the last actual word.
    New_column_0 = []
    New_column_1 = []
    New_column_2 = []
    
    # Lists to capture tuples
    List_tuple_bigrams = []
    List_tuple_trigrams = []
    List_tuple_quadgrams = []
    
    # Reset the index
    dataframe_reset_index = dataframe.reset_index()
   

    # For each word in the target column
    
    if Ngrams == 'Nograms':
        dataframe_reset_index = dataframe_reset_index.rename(index = str, columns = {'index': 0})  
        
    # BIGRAMS
    
    elif Ngrams == 'Bigrams':
        for word in dataframe_reset_index['level_0']:
        # Append each word to the list. 
            if isinstance(word, str):
                List_level_0.append(word)
        
        # And if present row in the column == None
            if isinstance(word, float):
                New_column_0.append(List_level_0[-1])
            else:
                # If the last word is not == to None, then append the present word. 
                New_column_0.append(word)
    
        # Drop old column and append new columne to dataframe. 
        dataframe_reset_index.drop(['level_0'], axis = 1)
        dataframe_reset_index['level_0'] = New_column_0
        
        # Iterate over the new dataframe 
        for row in dataframe_reset_index.itertuples():
            # Create a tuple of the bigram
            Col_tuples = (row[1], row[2])
            # Append the bigram tuple to our List. 
            List_tuple_bigrams.append(Col_tuples)
        
        # Drop the individual columns. 
        dataframe_reset_index = dataframe_reset_index.drop(['level_0', 'level_1'], axis = 1)
        # Append the bigram column to the dataframe with a col name of 0. 
        dataframe_reset_index[int(1)] = List_tuple_bigrams
        # Rename Columns
        dataframe_reset_columns = dataframe_reset_index.rename(index = str, columns = {1: 'Ngrams', 0:'Frequency'})
        # Sort Columns
        dataframe_reset_index = dataframe_reset_columns.sort_index(ascending = True, axis = 1)
    
    
    # TRIGRAMS
    
    elif Ngrams == 'Trigrams':
        
        for word in dataframe_reset_index['level_0']:
        # Append each word to the list. 
            if isinstance(word, str):
                List_level_0.append(word)
        
        # And if present row in the column == None
            if isinstance(word, float):
                New_column_0.append(List_level_0[-1])
            else:
                # If the last word is not == to None, then append the present word. 
                New_column_0.append(word)
        
        # Append new column to the dataframe
        dataframe_reset_index.drop(['level_0'], axis = 1)
        dataframe_reset_index['level_0'] = New_column_0
        
        for word in dataframe_reset_index['level_1']:
            # Append each word to the list. 
                if isinstance(word, str):
                    List_level_1.append(word)
                    
            # And if present row in the column == None
                if isinstance(word, float):
                    New_column_1.append(List_level_1[-1])
                else:
                    # If the last word is not == to None, then append the present word. 
                    New_column_1.append(word)
        
        # Append new column to the dataframe
        dataframe_reset_index.drop(['level_1'], axis = 1)
        dataframe_reset_index['level_1'] = New_column_1
    
        # Creat a single column for the quadgram tuple and remove the old ones. 
        for row in dataframe_reset_index.itertuples():
            Col_tuples = (row[1], row[2], row[3])
            List_tuple_quadgrams.append(Col_tuples)
        
        # Drop old columns
        dataframe_reset_index = dataframe_reset_index.drop(['level_0', 'level_1', 'level_2'], axis = 1)
        dataframe_reset_index[int('1')] = List_tuple_quadgrams            
        # Rename Columns
        dataframe_reset_columns = dataframe_reset_index.rename(index = str, columns = {1: 'Ngrams', 0:'Frequency'})
        # Sort Frequency
        dataframe_reset_index = dataframe_reset_columns.sort_index(ascending = True, axis = 1)
    
    
    # QUADGRAMS
    
    elif Ngrams == 'Quadgrams':
        # Iterate over each row of the dataframe. 
        for word in dataframe_reset_index['level_0']:
        # Append each word to the list. 
            if isinstance(word, str):
                List_level_0.append(word)
        
        # And if present row in the column == None
            if isinstance(word, float):
                New_column_0.append(List_level_0[-1])
            else:
                # If the last word is not == to None, then append the present word. 
                New_column_0.append(word)
        
        # Append new column to the dataframe
        dataframe_reset_index.drop(['level_0'], axis = 1)
        dataframe_reset_index['level_0'] = New_column_0
        
        for word in dataframe_reset_index['level_1']:
            # Append each word to the list. 
                if isinstance(word, str):
                    List_level_1.append(word)
                    
            # And if present row in the column == None
                if isinstance(word, float):
                    New_column_1.append(List_level_1[-1])
                else:
                    # If the last word is not == to None, then append the present word. 
                    New_column_1.append(word)
        
        # Append new column to the dataframe
        dataframe_reset_index.drop(['level_1'], axis = 1)
        dataframe_reset_index['level_1'] = New_column_1

        for word in dataframe_reset_index['level_2']:
            # Append each word to the list. 
                if isinstance(word, str):
                    List_level_2.append(word)
                    
            # And if present row in the column == None
                if isinstance(word, float):
                    New_column_2.append(List_level_2[-1])
                else:
                    # If the last word is not == to None, then append the present word. 
                    New_column_2.append(word)
        
        # Append new column to the dataframe
        dataframe_reset_index.drop(['level_2'], axis = 1)
        dataframe_reset_index['level_2'] = New_column_2
        
        # Creat a single column for the quadgram tuple and remove the old ones. 
        for row in dataframe_reset_index.itertuples():
            Col_tuples = (row[1], row[2], row[3], row[4])
            List_tuple_quadgrams.append(Col_tuples)
                
        dataframe_reset_index = dataframe_reset_index.drop(['level_0', 'level_1', 'level_2', 'level_3'], axis = 1)
        dataframe_reset_index[int('1')] = List_tuple_quadgrams            
        # Rename Columns
        dataframe_reset_columns = dataframe_reset_index.rename(index = str, columns = {1: 'Ngrams', 0:'Frequency'})
        # Sort Frequency
        dataframe_reset_index = dataframe_reset_columns.sort_index(ascending = True, axis = 1)
    
    
    # Return the new column list to the user. 
    return dataframe_reset_index



# Concatenate Text Files
    def create_concat_file(list_files, file_name, dir_data, target_dir):
        with open(str(file_name), 'w') as f:
            for doc in list_files:
                text = open(dir_data + '/' + doc).read()
                f.write(text)

    return None


def get_freq_ngrams(list_ngrams):
    '''Purpose:  Get the frequency of ngrams'''
    dict_obj = {}
    for ngram in list_ngrams:
        dict_obj[ngram] = dict_obj.get(ngram, 0) +1  

    df = pd.DataFrame(dict_obj, index = ['Count'])

    return df








