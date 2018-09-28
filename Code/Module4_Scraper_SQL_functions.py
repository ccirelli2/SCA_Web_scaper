# SQL Functions to be used in our scraper. 




def insert_function_2(mydb, action, 
                      row_number, obj_name, data_obj):
    '''
    action:         can either be create row or update_value.
    page_number:    Will be required everytime for this function
    data_obj_name   Name of data object we are looking to update. Type string. 
    data_obj:       The column for which we are looking to update. 
    '''
    
    mycursor = mydb.cursor()

    if action == 'create_row':

        sql_command = "INSERT INTO SCA_data (page_number, defendant_name) VALUES (%s,%s)"
        val = (row_number, data_obj)
        mycursor.execute(sql_command, val)
        mydb.commit()

    else:
        sql_command = '''UPDATE SCA_data
                            SET {} = '{}'
                            WHERE page_number = '{}' '''.format(obj_name, data_obj, row_number)
        
        mycursor.execute(sql_command)
        mydb.commit()
    
    return None






























