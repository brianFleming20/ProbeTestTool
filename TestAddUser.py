import unittest
import AdminUser
import Datastore
import tkinter as tk
import SecurityManager
import Ports

AU = AdminUser
DS = Datastore.Data_Store
SC = SecurityManager
P = Ports


class AdminTestsNewUser(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.A = AU.AddUserWindow(self.parent,self.controller)
    
    # Test no username  
    def test_no_user(self):
        print("Test No username")
        
        username = ""
        password = "123"
        confirm = "123"

        self.A._setDefaults()
        
        self.A.set_unsername(username)
        self.A.set_new_password(password)
        self.A.set_confirm_pass(confirm)
        
        result = self.A.check_details()
        
        self.assertEqual(result, False)

    # Test no password
    def test_no_password(self):
        print("Test no password")
        
        username = "User"
        password = ""
        confirm = "123"
        
        self.A._setDefaults()
        
        self.A.set_unsername(username)
        self.A.set_new_password(password)
        self.A.set_confirm_pass(confirm)
        
        result = self.A.check_details()
        
        self.assertEqual(result, False)

    # Test no confirm password
    def test_no_confirm_password(self):
        print("Test no confirm password")
        
        username = "User"
        password = "123"
        confirm = ""
        
        self.A._setDefaults()
        
        self.A.set_unsername(username)
        self.A.set_new_password(password)
        self.A.set_confirm_pass(confirm)
        
        result = self.A.check_details()
        
        self.assertEqual(result, False)

    # Test different passwords
    def test_different_passwords(self):
        print("Test different passwords")
        
        username = "User"
        password = "456A"
        confirm = "123"
        
        self.A._setDefaults()
        
        self.A.set_unsername(username)
        self.A.set_new_password(password)
        self.A.set_confirm_pass(confirm)
        
        result = self.A.check_details()
        
        self.assertEqual(result, False)

    # Test add user
    def test_add_user(self):
        print("Test add new user")
        # Change username to retest
        
        username = "User3"
        password = "1234"
        confirm = "1234"

        usr = P.User(username, password)

        users = DS.getUser(usr)
        if not users:
            pass
        else:
            DS.removeUser(username)
        
        self.A._setDefaults()
        
        self.A.set_unsername(username)
        self.A.set_new_password(password)
        self.A.set_confirm_pass(confirm)
        
        result = self.A.add_user(False)
        
        self.assertEqual(result, True)

    # Test not allow more than 2 admin
    def test_not_2_admin(self):
        print("Test not adding two admins")
        
        self.A._setDefaults()
        
        username = "User"
        self.A.set_unsername(username)
        
        self.A.check_admin()

        result = self.A.allow_add_admin
        
        self.assertEqual(result, False)

    def test_user_exsists(self):
        print("User already exists")

        username = "Brian"
        password = "1234"
        confirm = "1234"

        self.A._setDefaults()

        self.A.set_unsername(username)
        self.A.set_new_password(password)
        self.A.set_confirm_pass(confirm)

        result = self.A.add_user(False)

        self.assertEqual(result, False)



if __name__ == '__main__':
    unittest.main()