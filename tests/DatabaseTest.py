from io import StringIO
import unittest
import sys
from unittest import result
sys.path.append("../")

import datastore
from io import StringIO
import pickle

DS = datastore.DataStore()

with open('../file.user', 'rb') as load_user_file:
            load_data = pickle.load(load_user_file)


class DatastoreTest(unittest.TestCase):
    
    
    
    def test_user_name(self):
        expected_name = "Jack"
        result = load_data[0]
        
        self.assertEqual(expected_name, result)
        
    def test_admin_status(self):
        expected_admin = True
        result = load_data[1]
        
        self.assertEqual(expected_admin, result)   
        
    def test_set_plot_status(self):
            expected = True
        
            DS.set_plot_status(True)
            result = load_data[2]
        
            self.assertEqual(expected, result)
        
        
    def test_plot_status(self):
        expected_plot = False
        result = load_data[2]
        
        self.assertEqual(expected_plot, result )
        
        
   
        
        
if __name__ == '__main__':
    unittest.main()