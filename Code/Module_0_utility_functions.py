### PURPOSE
'''
The purpose of this script is to house certain utility functions that are applicable to a wide
range of functions and different scripts. 

'''

# Import Libraries
import os
from datetime import datetime
import pandas as pd
import smtplib                  # to send emails




# OUTPUT FUNCTIONS____________________________________________________________________

def write_to_excel(dataframe, filename, target_dir):
    '''Inputs:  dataframe, filename, target_dir'''
    os.chdir(target_dir)
    filename = filename + '_' + str(datetime.today())
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, 'Data')
    print('Dataframe {} has been written to {}'.format(filename, target_dir))
    writer.save()

# REPORT FUNCTIONS___________________________________________________________________


def progress_recorder(Count_obj, range_value_obj):
    '''
    Inputs      
        Count_obj:  This is the current count of the for loop, i.e. 
        the current count of the number of pages scraped.  
        range_value_obj: This represents the integer value of the last 
        page of the web page minus the first, so the total number of pages to scrape.       
    '''
    if Count_obj == 1:
        print('Scraper started')
    elif Count_obj == round(range_value_obj * 0.01, 0):
        print('1% Complete')
    elif Count_obj == round(range_value_obj * 0.05, 0):
        print('5% Complete')
    elif Count_obj == round(range_value_obj * 0.1,0):
        print('10% Complete')
    elif Count_obj == round(range_value_obj * 0.15,0):
        print('15% Completed')
    elif Count_obj == round(range_value_obj * 0.20,0):
        print('20% Complete')
    elif Count_obj == round(range_value_obj * 0.25,0):
        print('25% Completed')
    elif Count_obj == round(range_value_obj * 0.3,0):
        print('30% Completed')
    elif Count_obj == round(range_value_obj * 0.35,0):
        print('35% Completed')
    elif Count_obj == round(range_value_obj * 0.4,0):
        print('40% Completed')
    elif Count_obj == round(range_value_obj * 0.5,0):
        print('50% Completed')
    elif Count_obj == round(range_value_obj * 0.6,0):
        print('60% Completed')
    elif Count_obj == round(range_value_obj * 0.7,0):
        print('70% Completed')
    elif Count_obj == round(range_value_obj * 0.8,0):
        print('80% Completed')
    elif Count_obj == round(range_value_obj * 0.9,0):
        print('90% Completed')
    elif Count_obj == round(range_value_obj * 1.0,0):
        print('RRRRRR!!!!!!.......Scraping 100% Complete!!')
        print('Ok to proceed to the next job!')
    return None

 
# PROGRESS REPORT - Page numbers on first run----------------------------------------------

def pre_run_scraper_status_report(Run_type, End_page):
    '''Input:  Run_type, End_page'''
    if Run_type == 'Start_from_last_page':
        print('Scraper starting from the last page scraped, which is {}'.format(End_page))
    elif Run_type == 'Reset':
        print('''The user has selected the reset run-option.  The scraper will 
                proceed to delete all prior data and start to scrape from page 0''')

    return None


# PROGRESS REPORT - Information After Run--------------------------------------------------

def get_num_pages_scraped(mydb, Beginning_page):
    '''
    Function:           Get count of rows in table where page_number is great than our start
                        page.  This will tell us how many pages were scraped
    Substring_index:    https://dev.mysql.com/doc/refman/8.0/en/
                        string-functions.html#function_substring-index
    Sql command:        Iterate dictionary, return value associated with key "Count(*)"'''
    mycursor = mydb.cursor(dictionary = True)
    sql_command = ''' 
        SELECT  COUNT(*)
        FROM SCA_DATA3_TEST 
        WHERE SUBSTRING_INDEX(page_number, '=', -1) > {}'''.format(Beginning_page)   
    mycursor.execute(sql_command)
    for x in mycursor:
        return x['COUNT(*)']   


def get_summary_data_companies_sued(mydb, Beginning_page):

    mycursor = mydb.cursor(dictionary = True)
    sql_command = '''
        SELECT  page_number, defendant_name, filling_date, case_summary
        FROM SCA_DATA3_TEST
        WHERE SUBSTRING_INDEX(page_number, '=', -1) > {}'''.format(Beginning_page)
    
    df = pd.read_sql_query(sql_command, mydb)
    
    return df


def driver_function_post_run_scraper_status_report(mydb, Run_type, Beginning_page, End_page):
    '''Input:   Run_type, End_page
       Output:  Excel (for now)
    
    Functions:
                1.) Define first and last pages scraped
                2.) Define cases scraped - return dataframe
                    Derived values:  try to create a key of the attributes
                3.) If Starr is on the account
                4.) Prediction
                5.) Similar cases
    '''
    
    # Number of pages scraped
    num_pages_scraped = get_num_pages_scraped(mydb, Beginning_page)

    # Dataframe - Companies Sued, Case Summary
    df_companies_sued = get_summary_data_companies_sued(mydb, Beginning_page)

    # For now lets just print the results
    print('Number of pages scraped {}\n'.format(num_pages_scraped))
    print('The following companies where sued:\n {}'.format(
          [x.split("\n")[0] for x in df_companies_sued['defendant_name']]))

    

def send_email(from_address, to_address, timeout_sec, password, message):
    '''Should probably add each of these objects as inputs'''

    # Objects:
    gmail_server = 'smtp.gmail.com'
    port         = 465
    message      = 'Test message from python script'

    # Create Secure Connection to Gmail Server
    server = smtplib.SMTP_SSL(gmail_server, port ,timeout = timeout_sec)
    print('Connection Created to Gmail Server \n')
    server.login(from_address, password)
    print('Log-on successful to gmail address {}'.format(from_address)
    server.sendmail(
        from_address,
        to_address,                  
        message)
    server.quit()
 










