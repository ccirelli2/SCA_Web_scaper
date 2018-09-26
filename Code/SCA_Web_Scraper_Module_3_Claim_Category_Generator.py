### DOCUMENTATION
'''
Purpose:    The purpose of this module is to house functions relative to grouping 
            claims into categories. 

Functions   Below are the functions found in this module

            Dictionary
            
'''



Claim_type_dictionary = {
        # Statutes Referenced
        '1934_Exchange_Act':[('1934', 'rule'), ('1934', 'exchange')],
        '1933_Act':         [('act', '1933'), ('1933', 'section')],
        '10b5':             [('rule', '10b-5'), ('10b-5', 'promulgated')],
        'Derivative':       [('shareholder', 'derivative'), ('derivative', 'action')],
        # Transaction Referenced
        'IPO':              [('initial', 'public'), ('public', 'offering'), 
                             ('registration', 'statement'), ('alleges', 'prospectus'), 
                             ('ipo', 'exchange'), ('prospectus', 'materially'), 
                             ('prospectus', 'prospectus'), ('prospectus', 'sec')
                             ('incorporated', 'prospectus'), ('ipo', 'connection'), 
                             ('regarding', 'ipos')], 
        'Secondary_offering':[('secondary', 'offering')],
        'Bankruptcy':       [('bankruptcy', 'court'), ('bankruptcy', 'code'), 
                             ('states', 'bankruptcy'), ('filed', 'bankruptcy')],
        # Allegations Mentioned
        'False_misleading': [('false', 'misleading'), ('misleading', 'statements'), 
                             ('artificially', 'inflated'), ('misleading', 'failed'), 
                             ('material', 'misrepresentations'), ('artificially', 'inflating'), 
                             ('misrepresentations', 'market'), ('misrepresented', 'following'), 
                             ('materially', 'overstated')],
        'Failed_disclose':  [('failed', 'disclose'), ('disclose', 'material')], 
        'Commissions':      [('undisclosed', 'commissions'), ('commissions', 'certain')],
        'Fees':             [('fees', 'reimbursement'), ('fees', 'expenses')],
        'Accounting':       [('accounting', 'principles'), ('improper', 'accounting'), 
                             ('restate', 'financial')],
        'Conflicts_Interest':[('conflicts', 'interest')], 
        'Corporate_Gov':    [('corporate', 'governance')],
        # Fillings Referenced
        '10Q_Filling':      [('form', '10-q'), ('10-q', 'quarterly')], 
        '10K_Filling':      [('form', '10-k'), ('10-k', 'fiscal')],
        'Press_Release':    [('issued', 'press')],
        # Quarter Referenced
        'Second_Quarter':   [('second', 'quarter')],
        'Third_Quarter':    [('third', 'quarter')],
        'Fourth_Quarter':   [('fourth', 'quarter')], 
        # Mention of Counterparties
        'Customers':        [('customers', 'agree'), ('agreement', 'customers')], 
        # Financial Metrics Mentioned
        'Net_Income':       [('net', 'income'), ('income', 'earnings')], 
        'Revenue_Rec':      [('revenue', 'recognition')]
        'Cash_Flow':        [('cash', 'flow')],,
        # Consequences Mentioned
        'Stock_Drop':       [('stock', 'dropped')],
        'Heavy_traing':     [('heavy', 'trading')],
        
        
                            }
                        
                        
                        
def determine_inter_list_to_append(key, text, dict_obj, List1, List2):
    '''Purpose
    The purpose of this script is to determine which is to be updated based on the 
    key with which we are currently checking to see if there is a match.
    Inputs =        key:
                    dict_obj:
                    List1-n match is whether or not there was a match found, which determines if
                    we appenda 0 or 1. 
    '''
    # Iterate the list of ngrams    
    for gram in text:
    # Search for a match between the gram and the values
        if gram in dict_obj[key]:
        # If a match, append 1 to the list associated w/ our key and break
            if key == 'IPO':
                List1.append(1)
            elif key == '10b5':
                List2.append(1)
        # If no match was found, append a 0
        else:
            if key == 'IPO':
                List1.append(0)
            elif key == '10b5':
                List2.append(0)
    return None       


def determine_primary_list_to_append(Inter_list_1, Inter_list_2, Primary_list_1, Primary_list_2):
   '''
    All we are doing with this function is determining whether any matches were found for 
    each key by taking the length of our inter lists.  Since many matches could be found, 
    we append an intermediary list with all matches and then convert that to a binary value 
    at the primary list level, which is the single claim or page level. 

   '''

   if sum(Inter_list_1) > 0:
        Primary_list_1.append(1)
   else:
        Primary_list_1.append(0)
   if sum(Inter_list_2) > 0:
        Primary_list_2.append(1)
   else:
        Primary_list_2.append(0)
    
   return None


