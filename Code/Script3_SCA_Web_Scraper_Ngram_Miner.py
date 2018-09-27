# PURPOSE
'''
The purpose of this script + module is to create a function that will identify key attributes about the SCA that are not currently captured on the Securities Class Action Web Page. 

The soure of this data will come from the case summary provided on the web page and being scraped by our scraper.   

'''



def get_SCA_categories(claim_summary_text):
    '''
    Purpose     This function needs to fit within the process of our code. 
                Once the data is scraped from a single page, and before progressing to the next, 
                we need this function to generate the 
    Input       raw text from claims summary
    Output      

    Process     > Driver function queries the web page and obtains the claims data. 
                > Tokenizer tokenizes and cleans text and generates ngrams. 
                > get_SCA_categories receives list of ngrams, checks to see if any of the ngrams
                are present in our key word dictionary (object needs to be created) and appends 
                values to a set of lists created to capture/represent these categories. 


                get_SCA_categories should not be a stand alone function as it will need to update
                many list objects that will exist outside of this function. 

                so the function will get written into the body of our scraper and then it will
                source functions for the tokenization and the dictionary object. 


    '''












