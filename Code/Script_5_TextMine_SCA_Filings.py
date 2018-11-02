# PURPOSE
'''
Mine the actual SCA fillings for key words and phrases to include in our attribute dictionary. 
'''

# Import Libraries
import os
os.chdir('/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Code')
import Module_2_Scraper_CaseSummary as m2

# Objects
dir_data = r'/home/ccirelli2/Desktop/Programming/Data_sets/filings_text_legal_team'
list_files = os.listdir(dir_data)
target_dir = r'/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Code/SCA_concat_txt_output'



# Concatenate Text Files

def create_concat_file(list_files, file_name, dir_data, target_dir):
    with open(str(file_name), 'w') as f:
        for doc in list_files:
            text = open(dir_data + '/' + doc).read()
            f.write(text)

    return None
    

# Create Clean Tokenized Text

concat_text = open('/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Code/SCA_concat_txt_output/Concat_SCA.txt').read()

clean_tokenized_text = m2.clean_and_tokenize_text(concat_text)


ngrams = m2.get_Ngrams(clean_tokenized_text, 'Bigrams')

#ngram_column = m2.create_Ngram_column(ngrams, 'Bigrams')

print(ngrams[:100])


'''@@@@@@@@@@  Need to import create_freq_dist_table or db'''

#m2.write_to_excel(ngram_column, 'ngrams')

