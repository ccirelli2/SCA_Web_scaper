### DOCUMENTATION
'''
Purpose:    The purpose of this module is to house functions relative to grouping 
            claims into categories. 

Functions   Below are the functions found in this module

            Dictionary
            
'''



Claim_type_dictionary = {
        # Statutes Referenced
        '1934_Exchange_Act':[('1934', 'rule'), ('1934', 'exchange'), ('exchange', 'act'), 
                             ('act', '1934')],
        '1933_Act':         [('act', '1933'), ('1933', 'section')],
        '10b5':             [('rule', '10b-5'), ('10b-5', 'promulgated')],
        'Derivative':       [('shareholder', 'derivative'), ('derivative', 'action')],
        'class_action':   [('class', 'action'), ('class', 'period'), 
                             ('class', 'certification')],
        'ERISA':         [('erisa', 'breach'), ('erisa', 'complaint'), 
                             ('erisa', 'lawsuit'), ('erisa', 'cases')],
        'FCPA':          [('act', 'fcpa'), ('fcpa', 'company'), ('violation', 'fcpa')],
        'SEC_Investigation': [('exchange', 'commission'), ('commission', 'sec')],
        # Transaction Referenced
        'IPO':              [('initial', 'public'), ('public', 'offering'), 
                             ('registration', 'statement'), ('alleges', 'prospectus'), 
                             ('ipo', 'exchange'), ('prospectus', 'materially'), 
                             ('prospectus', 'prospectus'), ('prospectus', 'sec'),
                             ('incorporated', 'prospectus'), ('ipo', 'connection'), 
                             ('regarding', 'ipos')], 
        'Secondary_Offering':[('secondary', 'offering')],
        'Bankruptcy':       [('bankruptcy', 'court'), ('bankruptcy', 'code'), 
                             ('states', 'bankruptcy'), ('filed', 'bankruptcy')],
        'Merger':           [('plan', 'merger'), ('merger', 'consideration')],
        # Allegations Mentioned
        'False_misleading': [('false', 'misleading'), ('misleading', 'statements'), 
                             ('artificially', 'inflated'), ('misleading', 'failed'), 
                             ('material', 'misrepresentations'), ('artificially', 'inflating'), 
                             ('misrepresentations', 'market'), ('misrepresented', 'following'), 
                             ('materially', 'overstated'), ('materially', 'false')],
        'Failed_disclose':  [('failed', 'disclose'), ('disclose', 'material')], 
        'Commissions':      [('undisclosed', 'commissions'), ('commissions', 'certain')],
        'Fees':             [('fees', 'reimbursement'), ('fees', 'expenses')],
        'Accounting':       [('accounting', 'principles'), ('improper', 'accounting'), 
                             ('restate', 'financial'), ('accepted', 'accounting'),
                             ('principles', 'gaap'), ('violation', 'gaap'), 
                             ('accordance', 'gaap'), ('accounting', 'issues'), 
                             ('violated', 'gaap'), ('non-gaap', 'financial')],
        'Conflicts_Interest':[('conflicts', 'interest')], 
        'Corporate_Governance':    [('corporate', 'governance')],
        'Related_parties':  [('related', 'parties'), ('related', 'party')],
        'Sexual_Misconduct':[('sexual', 'misconduct'), ('sexual', 'harrassment'),
                            ('claim', 'sexual'), ('sexual', 'abuse'), ('sexual', 'assault')],
        'Proxy_violation':  [('misleading', 'proxy')],
        'Breach_Fiduciary_Duties':[('breach', 'fiduciary'), ('fiduciary', 'duties')],
        'Data_breach':      [('data', 'breach'), ('data', 'privacy')],
        # Fillings Referenced
        '10Q_Filling':      [('form', '10-q'), ('10-q', 'quarterly')], 
        '10K_Filling':      [('form', '10-k'), ('10-k', 'fiscal')],
        'Press_Release':    [('issued', 'press')],
        'Proxy':         [('proxy', 'statement'), ('statement', 'proxy'), 
                             ('alleges', 'proxy'), ('definitive', 'proxy'), 
                             ('14a', 'proxy'), ('misleading', 'proxy'), ('filed', 'proxy'),
                             ('proxy', 'filed')],   
        # Quarter Referenced
        'Second_Quarter':   [('second', 'quarter')],
        'Third_Quarter':    [('third', 'quarter')],
        'Fourth_Quarter':   [('fourth', 'quarter')], 
        # Mention of Counterparties
        'Customers':        [('customers', 'agree'), ('agreement', 'customers')], 
        # Financial Metrics Mentioned
        'Net_Income':       [('net', 'income'), ('income', 'earnings')], 
        'Revenue_Rec':      [('revenue', 'recognition')],
        'Cash_Flow':        [('cash', 'flow')],
        # Consequences Mentioned
        'Stock_Drop':       [('stock', 'dropped')],
        'Heavy_trading':     [('heavy', 'trading')]
        
        
                            }




                        
def get_match(key, text, dict_obj):
    '''Purpose
    The purpose of this script is to determine which is to be updated based on the 
    key with which we are currently checking to see if there is a match.
    Inputs =        key:
                    dict_obj:
                    List1-n match is whether or not there was a match found, which determines if
                    we appenda 0 or 1. 
    '''
    
    Inter_list = []
    match = ''

    # Iterate the list of ngrams    
    for Ngram in text:
    
    # Search for a match between the gram and the values
        if Ngram in dict_obj[key]:
        # If a match, append 1 to the list associated w/ our key and break
            Inter_list.append(1)
    
    
    if sum(Inter_list) > 0:
        match = 1
    else:
        match = 0
    
    return match     



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


