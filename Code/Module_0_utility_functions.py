### PURPOSE
'''
The purpose of this script is to house certain utility functions that are applicable to a wide
range of functions and different scripts. 

'''

# Import Libraries
import os
from datetime import datetime
import pandas as pd

# Modules For Sending Emails
import smtplib
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders





# OUTPUT FUNCTIONS____________________________________________________________________

def write_to_excel(dataframe, filename, target_dir, add_datetime):
    '''Inputs:  dataframe, filename, target_dir'''
    os.chdir(target_dir)

    # Add datetime to filename or not
    if add_datetime == True:
        filename = filename + '_' + str(datetime.today())
    else:
        filename = filename

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
        print('Scraping started')
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
        print('Ok to proceed to the next job!\n')
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


def get_df_data_companies_sued(mydb, Beginning_page):

    mycursor = mydb.cursor(dictionary = True)
    sql_command = '''
        SELECT  *
        FROM SCA_DATA3_TEST
        WHERE SUBSTRING_INDEX(page_number, '=', -1) > {}'''.format(Beginning_page)
    
    df = pd.read_sql_query(sql_command, mydb)
    
    return df


def driver_function_post_run_scraper_report(mydb, Beginning_page, End_page, report_output):
    '''
    Input:      mydb:  db connection 
                Return_value:  Either number of pages scraped or df_companies_sued
    Output:     Return df & write to Excel or standard output. 
    
    Functions:
                1.) Define first and last pages scraped
                2.) Define cases scraped - return dataframe
                    Derived values:  try to create a key of the attributes
                3.) If Starr is on the account (tbd)
                4.) Prediction (tbd)
                5.) Similar cases (tbd)
    '''
    

    # Print Results to Standard Output
    if report_output == 'print_results':
        df_companies_sued = get_df_data_companies_sued(mydb, Beginning_page)
        # For now lets just print the results
        print('\n Progress Report:')
        print('Number of pages scraped {}\n'.format(get_num_pages_scraped(mydb, Beginning_page)))
        print('The following companies were added to the database: {}'.format(
            ', '.join([x.split("\n")[0] for x in df_companies_sued['defendant_name']])))

    # Generate Dataframe & Write to Excel
    elif report_output == 'dataframe_w_results':
        df_companies_sued = get_df_data_companies_sued(mydb, Beginning_page)
        write_to_excel(df_companies_sued, 'SCA_Scraper_Results', 
                       '/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Scraper_output', 
                       add_datetime = False)
        return df_companies_sued
    
    # Return Dataframe Filename + Path
    elif report_output == 'dataframe_filename_plus_path':
        return '/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Scraper_output/SCA_Scraper_Results.xlsx'

    # Generate Text File for Body of Email
    
    elif report_output == 'email_text_body':
        # Source Url
        source_url = 'http://securities.stanford.edu/'
        # Generate Dataframe
        df_companies_sued = get_df_data_companies_sued(mydb, Beginning_page)
        num_companies_sued = len(df_companies_sued['defendant_name'])
        # Create Text File
        filename = 'Email_body.txt'
        target_dir = '/home/ccirelli2/Desktop/Programming/SCA_Web_scaper/Scraper_output/'
        Email_body = open('Email_body.txt', 'w')
        # Create Subject Line & Title
        Email_body.write('Intellisurance Securities Class Action Scraper Report \r')
        Email_body.write('Report Date                   => {} \r'.format(datetime.today()))
        Email_body.write('Number of Companies In Report => {} \r'.format(num_companies_sued))
        Email_body.write('Source                        => {} \n\n'.format(source_url))      
        
        # Add Content For Each Company Sued
        for row in df_companies_sued.itertuples():
            # Identify Values
            defendant_name  = str(row[2])
            link            = str(row[1])
            date_filed      = str(row[5])
            case_summary    = str(row[6])
            # Write to File
            Email_body.write('Defendant Name => {}'.format(defendant_name))
            Email_body.write('Date Filed     => {}\r'.format(date_filed))
            Email_body.write('Link to case   => {}\r'.format(link))
            Email_body.write('Case Summary:  => {}\r'.format(case_summary))
            Email_body.write('_________________________________________________________\n\n')
        
        # Add Copyright Disclosure At the End
        Copyright_disclosure ='''\r
        \n\n\n------------------------------------------------------------------------------
        Please be advised that the content of this report is sources from the Stanford Law
        Securities Class Action Web Page and is for academic purposes only.  In now way does
        the author warrant the accuracy of the information presented, its validity nor is the 
        author responsible for its use by recipients of this report. 
        ------------------------------------------------------------------------------------
        '''
        Email_body.write(Copyright_disclosure)

        # Close Email Body
        Email_body.close()

        # Return Path + Filename
        return  target_dir + filename   
    
    # END DRIVER FUNCTION__________________________________________________________________



def email_no_attachment(from_address, to_address, timeout_sec, password, message):
    '''Should probably add each of these objects as inputs'''

    # Objects:
    gmail_server = 'smtp.gmail.com'
    port         = 465
    message = 'Subject: Test subject line'
    # Create Secure Connection to Gmail Server
    server = smtplib.SMTP_SSL(gmail_server, port ,timeout = timeout_sec)
    print('Connection Created to Gmail Server \n')
    server.login(from_address, password)
    print('Log-on successful to gmail address {}'.format(from_address))
    server.sendmail(
        from_address,
        to_address,                  
        message)
    print('Email successfully sent') 
    server.quit()
 


def email_with_attachments(password, toaddr, subject, body, attachment_filename):

    # Define To & From Addresses
    fromaddr = 'intellisurance@gmail.com'

    # Create Instance Message Object
    msg = MIMEMultipart()

    # Define Attributes
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain')) # what does this do?

    # File Specification & Encoding 
    attachment = open(attachment_filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename = {}'.format(attachment_filename))
    msg.attach(part)

    # Login to Server & Send Message
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout = 5)
    server.login('intellisurance@gmail.com', password)
    text = msg.as_string()              # I guess we are converting the entire message to str
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    return print('\nEmail Successfully Sent to:  {}'.format(toaddr))








