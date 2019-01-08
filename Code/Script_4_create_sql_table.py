### PURPOSE
'''
The purpose of this script is to show examples of how the SQL connector
works, how to create tables, input information, etc.

web_page = www.w3school.com/python/python_mysql_create_table.asp

Syntax:
    mycursor = mydb.cursor()                creates a connection to the db
    mycursor.execute('SQL COMMAND')         executes commands to the db

Once the database is defiend you would use the following syntax
cnx = mysql.connector.connect(user='joe', database='test_database')
'''
import json
import os
import mysql.connector


with open('./config.json', 'r') as f:
    config = json.load(f)
mydb = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    passwd=os.environ['MYSQL_PASSWORD'],
    database=config['database']['database'])

mycursor = mydb.cursor()
mycursor.execute('''CREATE TABLE SCA_data(
                    page_number                 SMALLINT        NOT NULL    UNIQUE,
                    defendant_address           VARCHAR(225),
                    defendant_name              VARCHAR(255), 
                    case_status                 VARCHAR(25), 
                    filling_date                DATE, 
                    close_date                  DATE, 
                    case_summary                VARCHAR(2000), 
                    1934_Exchange_Act           BINARY, 
                    1933_Act                    BINARY, 
                    10b5                        BINARY, 
                    Derivative                  BINARY, 
                    IPO                         BINARY, 
                    Secondary_Offering          BINARY, 
                    Bankruptcy                  BINARY, 
                    False_misleading            BINARY, 
                    Failed_disclose             BINARY, 
                    Commissions                 BINARY, 
                    Fees                        BINARY, 
                    Accounting                  BINARY, 
                    Conflicts_Interest          BINARY, 
                    Corporate_Governance        BINARY, 
                    10Q_Filling                 BINARY, 
                    10K_Filling                 BINARY, 
                    Press_Release               BINARY, 
                    Second_Quarter              BINARY, 
                    Third_Quarter               BINARY, 
                    Fourth_Quarter              BINARY, 
                    Customers                   BINARY, 
                    Net_Income                  BINARY, 
                    Revenue_Rec                 BINARY, 
                    Cash_Flow                   BINARY, 
                    Stock_Drop                  BINARY, 
                    Heavy_trading               BINARY,
                    Sector                      VARCHAR(25), 
                    Industry                    VARCHAR(25), 
                    Symbol                      VARCHAR(25), 
                    Status_2                    VARCHAR(25), 
                    Headquarters                VARCHAR(225), 
                    Company_market              VARCHAR(25), 
                    Court                       VARCHAR(25), 
                    Docket                      VARCHAR(25), 
                    Judge                       VARCHAR(25), 
                    Date_Filed                  DATE, 
                    Class_Period_Start          DATE, 
                    Class_Period_End            DATE, 
                    Plaintiff_firm              VARCHAR(2225),
                    PRIMARY KEY (page_number)

                                            )''')
mycursor.execute('SHOW TABLES')
print([x for x in mycursor])
