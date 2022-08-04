import unittest
import AdminUser
from SecurityManager import *
import Datastore
import tkinter as tk

AU = AdminUser
DS = Datastore.Data_Store()
SM = SecurityManager()
U = Users

class AdminTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.A = AU.ChangePasswordWindow(self.parent, self.controller)
        self.C = AU.EditUserWindow(self.parent, self.controller)
    
        # The new password entry shall not be empty.
    def test_empty_password(self):
        print("Check change user password missing entry")

        password = "pass987"
        
        self.A.set_password("")
        self.A.set_confirm(password)
        
        result1 = self.A.check_entries()
        
        self.assertEqual(result1, False)
        
        self.A.set_password(password)
        self.A.set_confirm("")
        
        result2 = self.A.check_entries()
        self.assertEqual(result2, False)
        
        
        
    def test_different_passwords(self):
        print("Check change user password with different entries")
        
        password1 = "pass987"
        password2 = "pass123"
        
        self.A.set_password(password1)
        self.A.set_confirm(password2)
        
        result1 = self.A.check_entries()
        
        self.assertEqual(result1, False)
        
    
    
    # The PTT shall confirm the change of password.
    def test_change_password(self):
        print("Test change password")
        
        password1 = "pass987"
        password2 = "pass987"
        user = "User1"
        username = "Brian"
        
        self.A.set_password(password1)
        self.A.set_confirm(password2)
        # create user obj and add change password transfer name
        user_data = U(username,False,pw_user=user)
        DS.write_user_data(user_data)
        
        result1 = self.A.change_password(password1)
        # DS.clean_admin_file()

        self.assertEqual(result1, True)
    
    
    # The PTT shall delete a selected user from a list.
    def test_delete_user(self):
        print("Delete user")
        
        admin_user_name = "brian"
        admin_password = "password"
        admin_user = User(admin_user_name, admin_password)
        SM.logIn(admin_user)
        
        del_user = "User3"
      
        
        result = self.C.check_delete(del_user)
        
        self.assertEqual(result, True)
        
    
    
    # The PTT shall not delete the logged in user.
    def test_not_delete_current_user(self):
        print("Test delete current user")
        
        del_user = "brian"
     
        
        admin_user_name = "brian"
        admin_password = "password"
        admin_user = User(admin_user_name, admin_password)
        SM.logIn(admin_user)
        
        result = self.C.check_delete(del_user)
        
        self.assertEqual(result, False)
        
        
if __name__ == '__main__':
    unittest.main()        
