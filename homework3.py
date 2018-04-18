'''
Ian Kirkman
DATA 515a - HW 3
Python Module for Youtube data
'''

# Import required packages
import pandas as pd
import sqlite3 as sql

def _create_dataframe_helper(lang_arg):
    '''
    Helper function to create query string for Youtube data tables.
    NOTE: Internal use only.
    
    INPUT:
        lang_arg: The (case-insensitive) 2-char string that identifies 
        source table and language.
            
    RETURNS:
        A select statement (as a string) to run on that table
    '''
    return "select video_id, category_id, '%s' as language from %svideos "%(
        lang_arg.lower(),lang_arg.upper())

def  create_dataframe(db_path):
    '''
    Creates a pandas dataframe with query results of video_id, 
    category_id, and language from each of the tables (US, GB, 
    FR, DE, CA) on the Youtube sql database class.db. (Note that
    database structure is assumed).

    INPUT:
        db_path: the path of the Youtube SQL database (relative to current dir)

    RETURNS:
        the query results as a pandas dataframe
    '''
    # Create sqlite connection to specified database
    # Reference: https://www.dataquest.io/blog/python-pandas-databases/
    conn = sql.connect(db_path)
    
    # Create query string from HW1
    query_str = ''
    langs = ['us','ca','gb','de','fr']
    for lang in langs[:-1]:
        query_str += _create_dataframe_helper(lang) + "union "
    query_str += _create_dataframe_helper(langs[-1]) + ";"
    
    # Use the sqlite connection to pull query results into a pandas DataFrame
    try:
        return pd.read_sql_query(query_str,conn)
    except:
        raise ValueError("Please enter valid database path.")
    
def test_create_dataframe(df_arg):
    '''
    Tests that the pandas DataFrame meets the following conditions:
        1. The DataFrame contains only the columns video_id, category_id, 
           and language.
        2. The columns video_id and language could be a key.
        3. There are at least 10 rows in the DataFrame.

    INPUT:
        df_arg: the pandas DataFrame to test

    RETURNS:
        True if all three tests pass, otherwise False.
    ''' 
    test1 = (len(df_arg.columns) == 3 and 
             'video_id' in df_arg.columns and 
             'category_id' in df_arg.columns and 
             'language' in df_arg.columns)

    test2 = True # TODO: Update
    
    test3 = df_arg.shape[0]>10
    
    return (test1 and test2 and test3)
