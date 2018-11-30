### PURPOSE:
'''
The Purpose of this script is to house the documentation for all of the scripts and modules associated with this project. 





### AREAS OF IMPROVEMENT_________________________________________________________________


MYSQL SCA_data TABLE----------------------------------------------------------------------

1.) Null Values:        The insert statements need to be corrected to remove arbitary entries
                        for when a datapoint cannot be scraped and insert a Null value. 
                        This way we will have a uniform way of identifying those values. 

2.) Pre-Machine Learning Data Cleaning:

    Filing_date, Close_Date, Year_filed:
                        During the original construction of the scraper we ran into issues
                        where the web page developer had variations in the structure of 
                        their web page and we generated errors when trying to scrape these 
                        fields.  Therefore, when we couldn't scrape the field, we used 
                        an except statement and input an arbitrary date of 1/1/1900.
                        That being said, and because we are not using these dates in the ML
                        model as features, we do not need to remove them from the final 
                        table. 
    
    Class_Period_End, Class_Period_Start
                        except statement inserts 01/01/1900'
                        Class_Period_Start:  Count = 12
                        Class_Period_End: Count = 11

    Judge:              
                        We had some issues scraping this object. 
                        Count = 29 rows include 'None' as the value for Judge
                        Count = 107 include a char() object with length of less than 
                        2 and no value for judge.  These will be removed from the 
                        table in the pre-ML training clearning process. 

    Plaintiff_firm:     Except statement set to error. 
                        Appears in 55 rows. 




MODULES & SCRIPTS-------------------------------------------------------------------------

1.) Naming Convention:  We need to better name our scripts to accurately reflect their purpose
                        and functions. 


2.) Script_8_ML_Driver / Module_8_Machine_Learning_Functions:

    i.) Class Duration:     This derived value should be built into the SQL scheme as a 
                            trigger to be executed upon every insert or update statement. 

    ii.) SQL Table:         The SQL table schema should be updated to reflect all of 
                            these changes that we are making.  For instance, any additional 
                            derived values or values we are chosing to drop that no longer 
                            are needed. 


'''










