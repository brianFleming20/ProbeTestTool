import unittest


import UserLogin
import SecurityManager
import tkinter as tk

UL = UserLogin
USER = SecurityManager.SecurityManager()
U = SecurityManager


class LoginTests(unittest.TestCase):

    def setUp(self):
        self.canvas_name = tk.Canvas(bg="#eae9e9", width=400, height=45)
        self.canvas_pass = tk.Canvas(bg="#eae9e9", width=400, height=45)
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.UL = UserLogin.LogInWindow(self.parent, self.controller)

    def test_username(self):
        print("Test user login")
        name = "brian"       
        password = "password"
        
        # Test return true when checking user
        result_user = U.User(name, password)
        # Test user object has the same username and password
        # from the one provided by the system
        
        USER.logIn(result_user)
        
        check_user = USER.GetUserObject(name)

        self.assertEqual(check_user.name, name)
        self.assertEqual(check_user.password, password)
        
        
    def test_no_username(self):
        print("Test no user login")
        name = ""       
        password = "password"
        expected = False
        
        # Test return true when checking user
        result_user = U.User(name, password)
        # Test user object has the same username and password
        # from the one provided by the system
        
        USER.logIn(result_user)
        
        
        self.assertTrue(result_user, expected)
        
        
    def test_no_password(self):
        print("Test no password login")
        name = "brian"       
        password = ""
        expected = False
        
        # Test return true when checking user
        result_user = U.User(name, password)
        # Test user object has the same username and password
        # from the one provided by the system
        
        USER.logIn(result_user)

        self.assertTrue(result_user, expected)
        
    def next_window(self):
        return True


    def test_login_class(self):
        print("Test user login")

        name = "brian"       
        password = "password"
        self.UL.entry()
        self.UL.set_username(name)
        self.UL.set_password(password)

        result = self.UL._login_btn_clicked()

        self.assertEqual(result, True)


    def test_incorrect_password(self):
        print("Incorrect password")

        name = "brian"
        password = "nothing"

        self.UL.entry()
        self.UL.set_username(name)
        self.UL.set_password(password)
        result = self.UL._login_btn_clicked()

        self.assertEqual(result,False)
        
        
if __name__ == '__main__':
    unittest.main()

