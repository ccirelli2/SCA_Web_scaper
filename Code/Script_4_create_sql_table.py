### PURPOSE
'''
The purpose of this script is to show examples of how the SQL connector
works, how to create tables, input information, etc. 

web_page = www.w3school.com/python/python_mysql_create_table.asp

Syntax:
    mycursor = mydb.cursor()                creates a connection to the db
    mycursor.execute('SQL COMMAND')         executes commands to the db

'''


### IMPORT CONNECTOR 
import mysql.connector

# Instantiate Connector
'''
Once the database is defiend you would use the following syntax
cnx = mysql.connector.connect(user='joe', database='test_database')
'''

mydb = mysql.connector.connect(
        host="localhost", 
        user="ccirelli2", 
        passwd="", 
        database='SCA_SCRAPER'
        )

#print(mydb)

### CREATE DATABASE
'''
mycursor = mydb.cursor()
mycursor.execute('CREATE DATABASE test_database_09242018')
'''

### LIST AVAILABLE DATABASES
'''
mycursor = mydb.cursor()
mycursor.execute('SHOW DATABASES')
print(type(mycursor), '/n')
print([x for x in mycursor])
'''

### CREATE TABLE

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


### DROP TABLE
'''
mycursor = mydb.cursor()
mycursor.execute('DROP TABLE customers')
'''


### INSERT INTO TABLE
'''
mycursor = mydb.cursor()
sql_command = 'INSERT INTO customers (name, address) VALUES(%s,%s)'
val = [
       ('Chris', '1175 Lea Drive'), 
       ('Nubia', '1175 Lea Drive')]

mycursor.executemany(sql_command, val)
mydb.commit()
'''

### SELECT FROM A TABLE
'''
mycursor = mydb.cursor()
mycursor.execute('SELECT * FROM customers')
myresult= mycursor.fetchall()
print(myresult)
'''

### INSERTION WITHIN A FOR LOOP
'''
mycursor = mydb.cursor()
List_values = [x for x in range(0,10)]
for x in List_values:
    if x > 2:
        sql_command = 'INSERT INTO customers (name) VALUES(%s)'
        val = ['Chris_' + str(x)]
        mycursor.execute(sql_command, val)
        mydb.commit()
'''




























