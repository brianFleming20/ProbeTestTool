
import unittest
import AdminUser
import Ports as P
from SecurityManager import *
import tkinter as tk
import BatchManager
import os

AU = AdminUser
DS = Datastore.Data_Store()
SM = SecurityManager()
CSV = BatchManager.CSVManager()
BM = BatchManager.BatchManager()


class AdminTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.A = AU.AdminWindow(self.parent, self.controller)
        self.AD = AU.AddUserWindow(self.parent, self.controller)
        self.AE = AU.EditUserWindow(self.parent, self.controller)
        self.AC = AU.ChangePasswordWindow(self.parent, self.controller)
        self.user3 = "User3"
        self.Jon = "Jon"
        self.user4 = "User4"
        self.brian = "brian"

    # admin flag to restrict access to the admin area
    def test_admin_flag(self):
        print("*** Test allow admin ***")
        false_user = P.Users("Brian", False)
        DS.write_user_data(false_user)
        result1 = DS.user_admin_status()
        self.assertFalse(result1)

        true_user = P.Users("Brian", True)
        DS.write_user_data(true_user)
        result2 = DS.user_admin_status()
        self.assertTrue(result2)

    def test_add_new_user(self):
        print("*** Test add new user ***")
        user = "User1"
        password = "u1"
        admin = True

        add_user = P.User(user, password, admin)
        added_user = SM.addUser(add_user)

        self.assertTrue(added_user)

    def test_add_user_exists(self):
        print("*** Test add existing user ***")
        user = "User1"
        password = "u1"
        admin = True

        user_exists = DS.getUser(user).name
        self.assertEqual(user_exists, user)

        old_user = P.User(user, password, admin)
        add_user = SM.addUser(old_user)

        self.assertFalse(add_user)

    # identify a logged in admin user
    def test_admin_user(self):
        print("*** Test if the user is admin ***")

        u3_password = "1234"
        u1_password = "batman"
        # check for missing user
        users = DS.getUserList()
        if self.user3 not in users:
            newUser = P.User(self.user3, u3_password, True)
            SM.addUser(newUser)
        # log in admin user
        user1 = P.User("brian", "password")
        result1 = SM.logIn(user1)
        self.assertTrue(result1)
        admin = DS.user_admin_status()
        self.assertTrue(admin)
        # log in non admin user
        user2 = P.User(self.Jon, u1_password)
        result2 = SM.logIn(user2)
        self.assertTrue(result2)
        admin2 = DS.user_admin_status()
        self.assertFalse(admin2)

    # change password not empty string
    def test_no_password(self):
        print("*** Test no password ***")
        username = "User"
        password = ""
        confirm = "123"

        self.AD._setDefaults()

        self.AD.set_unsername(username)
        self.AD.set_new_password(password)
        self.AD.set_confirm_pass(confirm)

        result = self.AD.check_details()

        self.assertEqual(result, False)

    # change password are same
    def test_different_passwords(self):
        print("*** Test different passwords ***")

        username = "User"
        password = "456A"
        confirm = "123"

        self.AD._setDefaults()

        self.AD.set_unsername(username)
        self.AD.set_new_password(password)
        self.AD.set_confirm_pass(confirm)

        result = self.AD.check_details()

        self.assertEqual(result, False)

    # confirm the change of password
    def test_change_user_password(self):
        print("*** Change user password ***")

        password = "1234"
        user = P.User(self.user3, password)
        result2 = SM.logIn(user)
        self.assertTrue(result2)
        user_change = P.Users("brian", True, pw_user=self.user3)
        DS.write_user_data(user_change)
        # check passwords are the same
        self.AC.newPassword = "2345"
        self.AC.confirmPassword = "9876"
        change_f = self.AC.check_entries()
        self.assertFalse(change_f)
        # change password
        self.AC.newPassword = "1234"
        self.AC.confirmPassword = "1234"
        # change = P.Users("brian", True, pw_user=user3)
        # DS.write_user_data(change)
        change_t = self.AC.check_entries()
        self.assertTrue(change_t)

    # delete a user from the user list
    def test_remove_user_from_list(self):
        print("*** Delete user from list ***")
        found = False
        user3 = "User3"
        user1 = P.User(self.brian, "password")
        result1 = SM.logIn(user1)
        self.assertTrue(result1)
        result = self.AE.check_delete(user3)
        self.AE.check_delete("User1")
        self.assertTrue(result)
        users = DS.getUserList()
        for usr in users:
            if usr.name == user3:
                found = True
        self.assertFalse(found)

    # update user's status to admin where available
    def test_change_user_status(self):
        print("*** Update user status ***")
        # change user status on admin to non-admin
        password = "9876543"
        user_login = P.User(self.brian, "password")
        SM.logIn(user_login)
        user = P.User(self.user4, password, admin=True)
        result = SM.addUser(user)
        user = P.Users(self.brian, True, pw_user=self.user4)
        DS.write_user_data(user)
        user_change = DS.get_reset_password_name()
        self.assertEqual(user_change, self.user4)
        user_admin = DS.getUser(user_change).admin
        self.assertTrue(user_admin)
        # change user status on non-admin to admin

        # change user status on non-admin to admin where 2 admin users already exist

        # remove test user
        self.AE.check_delete(self.user4)

    # not delete a logged in user
    def test_delete_logged_in_user(self):
        print("*** Try delete logged in user ***")
        user1 = P.User("brian", "password")
        result1 = SM.logIn(user1)
        self.assertTrue(result1)
        delete = self.AE.check_delete("brian")
        self.assertFalse(delete)

    # Make the admin button unresponsive to non admin users
    def test_admin_user_status(self):
        print("*** Test login non admin user status ***")

        # Login non-admin user
        user = "User1"
        password = "u1"
        non_admin = P.User(user, password)

        signed_in = SM.logIn(non_admin)

        self.assertEqual(signed_in, True)
        SM.logOut()

        print("*** Test login admin user status ***")
        # Login Admin user
        admin_user_name = "brian"
        admin_password = "password"
        admin_user = P.User(admin_user_name, admin_password)
        SM.logIn(admin_user)

        admin_status = DS.user_admin_status()

        self.assertEqual(admin_status, True)
        SM.logOut()

    # Create a list of all users in the system
    def test_list_users(self):
        print("*** Check user in user list ***")
        # Chech that the length os the list is greater than zero

        user_list = len(SM.GetUserList())
        self.assertGreater(user_list,0)

    # allow serial number over-write
    def test_serial_number_overwrite(self):
        print("*** Serial number over write ***")

        username = "brian"
        admin = True
        user1 = P.Users(username, admin, over_right=True)
        DS.write_user_data(user1)

        result = DS.get_user_data()['Over_rite']

        self.assertEqual(result, True)

        user2 = P.Users(username, admin, over_right=False)
        DS.write_user_data(user2)

        result1 = DS.get_user_data()['Over_rite']

        self.assertEqual(result1, False)

    def test_monitor_status(self):
        print("Test monitor use status")

        odm_active = self.A.odm_active.get()

        self.A.set_odm_state()
        odm_data = DS.get_devices()['odm_active']
        self.assertEqual(odm_data, odm_active)

    def test_animal_probe(self):
        print("Test animal probe settings")
        user_data = DS.get_user_data()
        non_human = user_data['Non_Human']
        over_write = user_data['Over_rite']
        ##############################################
        # Set up non-human probe settings for False  #
        # and set over-write to False, Default       #
        ##############################################
        user = P.Users("Brian", True)
        DS.write_user_data(user)
        ##############################################
        # Set for non-human probe and not over-write #
        ##############################################
        self.assertFalse(non_human)
        self.A.non_human.set(True)
        self.A.non_human_probe()
        non_human_set = DS.get_user_data()['Non_Human']
        self.assertTrue(non_human_set)
        self.assertFalse(over_write)
        ##############################################
        # Set for over-write and not non-human probe #
        ##############################################
        self.A.admin_state.set(True)
        self.A.set_admin_state()
        self.assertTrue(DS.get_user_data()['Over_rite'])
        self.A.non_human.set(False)
        self.A.non_human_probe()
        self.assertFalse(DS.get_user_data()['Non_Human'])
        ##############################################
        # Set both over-write and non-human probe on #
        ##############################################
        self.A.admin_state.set(True)
        self.A.non_human.set(True)
        self.A.set_admin_state()
        self.A.non_human_probe()
        self.assertTrue(DS.get_user_data()['Over_rite'])
        self.assertTrue(DS.get_user_data()['Non_Human'])

    def test_create_remote_path(self):
        print("Create a remote PTT_Results folder")

        path = DS.get_file_location()['File']
        CSV.check_directories()
        batch_number = "14762N"

        is_here = os.path.isdir(path)

        self.assertTrue(is_here)

        batch = P.Batch(batch_number)
        batch.probe_type = "DP6"
        batch.batchQty = 100
        user = "Brian"
        BM.CreateBatch(batch, user)

        line = CSV.ReadLastLine(batch_number, False)
        result = line[0]

        self.assertEqual(result, batch_number)


if __name__ == '__main__':
    unittest.main()
