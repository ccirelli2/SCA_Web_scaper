### DOCUMENTATION
'''
Purpose:    The purpose of this module is to house functions relative to grouping 
            claims into categories. 

Functions   Below are the functions found in this module

            Dictionary
            
'''



Claim_type_dictionary = {'IPO': ['ipo', 'prospectus']}




def createper_claim_violation_category_cols(Claim_text, Violation_dictionary, Ngram_type):

    Count_col_completion = 0

    # Iterate over each key of the violation dictionary
    for key in violation_dictionary:

        # Create a list of values that will represent if a match was found between the tokens in the text and the
        # values associated with the key.  It should be 1 value per key, either 1 or 0.
        List_matches_key_violation = []

        # Iterate over each row in our dataframe
        for row in dataframe['LOSS_DESCRIPTION.1']:

            # Tokenize and clean the text.
            tokenize_claims_text = text_cleaning_pipeline(row)

            # Create an intermediary list to capture the matches from the
            token_list_matches = []

            # A. Check to see if the tokenized row is a list (it may have 0 values after the text clearning):
            if isinstance(tokenize_claims_text, list):

                # Iterate over each token in the tokenized row
                for token in tokenize_claims_text:

                    # Check to see if the token is in the key values
                    if token in violation_dictionary[key]:
                        # If we have a match, append 1 to the token_list_matches list.
                        token_list_matches.append(1)
                        # If we found a match, break the current for loop as we are done with this row.
                        break
                    else:
                        # If we haven't appended a 0 to our list yet (as a 1 would have already broken the for loop)
                        if len(token_list_matches) == 0:
                            token_list_matches.append(0)

                # Once finished iterating over the tokens of the row, check to see what is in our list
                if sum(token_list_matches) > 0:
                    # If the sum of the list is greater than zero, then we found at least one match.
                    List_matches_key_violation.append(1)
                else:
                    # If no, then we found no matches and appended a 0.
                    List_matches_key_violation.append(0)

            # B. If the tokenized row was not a list, simply append 0 to the List of matches
            else:
                List_matches_key_violation.append(0)





