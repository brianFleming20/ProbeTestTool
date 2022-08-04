
import unittest
import AdminUser
import Datastore
from SecurityManager import *
import tkinter as tk


AU = AdminUser
DS = Datastore.Data_Store()
SM = SecurityManager()
U = Users

class AdminTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.A = AU.AdminWindow(self.parent, self.controller)
    
    # Make the admin button unresponsive to non admin users
    def test_admin_button_in_sessions(self):
        print("Test login non user status")
        
        # Login non-admin user
        user = "User1"
        password = "u1"
        non_admin = User(user, password)
     
        signed_in = SM.logIn(non_admin)
        
        self.assertEqual(signed_in, False)
        SM.logOut()
        
        print("Test admin user status")
        # Login Admin user
        admin_user_name = "brian"
        admin_password = "password"
        admin_user = User(admin_user_name, admin_password)
        SM.logIn(admin_user)
        
        admin_status = DS.user_admin_status()
        
        self.assertEqual(admin_status, True)
        SM.logOut()
    
    
    # Create a list of all users in the system
    def test_list_users(self):
        print("Check user in user list")
        # Chech that the length os the list is greater than zero
        
        user_list = len(SM.GetUserList())
        self.assertGreater(user_list,0)

    
    
    # Complete and in progress file location
    def test_comp_and_prog_file_location(self):
        print("Test OS file access and file location")
        self.A.get_browse_file()
        location = "C:/Users/BrianFleming/Desktop/PTT_Results"
        result = DS.get_file_location()['File']
        
        self.assertGreater(len(location), 0)
        self.assertEqual(location, result)
        
        
        

    
    
    # allow serial number over-write
    def test_serial_number_overwrite(self):
        print("Serial number over write")
        
        username = "brian"
        admin = True
        user1 = U(username,admin,over_right=True)
        DS.write_user_data(user1)
        
        result = DS.get_user_data()['Over_rite']
        
        self.assertEqual(result, True)
        
        user2 = U(username,admin,over_right=False)
        DS.write_user_data(user2)
        
        result1 = DS.get_user_data()['Over_rite']
        
        self.assertEqual(result1, False)
        
        
   
    
if __name__ == '__main__':
    unittest.main()