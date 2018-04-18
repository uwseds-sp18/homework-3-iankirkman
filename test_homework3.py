'''
Ian Kirkman
DATA 515a - HW 3
Python Module to test Homework 3 (Youtube data)
'''

# Import required packages
import pandas as pd
import unittest
from homework3 import create_dataframe

# Define a class to test homework3
class DB_Test(unittest.TestCase):

    def test_badpath(self):
        '''
        Checks that a ValueError is raised when a bad path is provided.
        
        Use as smoke test-- returns true if ValueError is raised. 
        Other exceptions are not caught.
        '''
        try:
            create_dataframe('badpath')
        except ValueError:
            return True
    
    def test_colnames(self):
        '''
        Asserts the column names of the dataframe match specs.
        '''
        df = create_dataframe("homework-3-iankirkman/class.db")
        self.assertTrue(len(df.columns)==3 &
                        'video_id' in df.columns &
                        'category_id' in df.columns &
                        'language' in df.columns)
    
    def test_numrows(self):
        '''
        Asserts that the dataframe has at least 2K rows.
        '''
        df = create_dataframe("homework-3-iankirkman/class.db")
        self.assertTrue(df.shape[0] > 2000)
    
    def test_key(self):
        '''
        Confirms that all three columns are required for a unique key.
        '''
        df = create_dataframe("homework-3-iankirkman/class.db")
        
        # All three columns with dups removed
        df_nodups = df.drop_duplicates()
        
        # All pairs of 2 cols with dups removed
        df_vid_cat = df.drop(columns=['language']).drop_duplicates()
        df_vid_lang = df.drop(columns=['category_id']).drop_duplicates()
        df_cat_lang = df.drop(columns=['video_id']).drop_duplicates()
        
        # Confirm all three columns can be a key, and any combo of 2 cannot:
        self.assertTrue(df.shape[0] == df_nodups.shape[0] &
                        df.shape[0] > df_vid_cat.shape[0] &
                        df.shape[0] > df_vid_lang.shape[0] &
                        df.shape[0] > df_cat_lang.shape[0])
    
if __name__ == '__main__':
    unittest.main()
