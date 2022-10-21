
import unittest
import AdminUser
import Ports
from SecurityManager import *
import tkinter as tk
import BatchManager
import os

AU = AdminUser
DS = Datastore.Data_Store()
SM = SecurityManager()
P = Ports
CSV = BatchManager.CSVManager()
BM = BatchManager.BatchManager()


class AdminTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.A = AU.AdminWindow(self.parent, self.controller)

    # Make the admin button unresponsive to non admin users
    def test_admin_user_status(self):
        print("Test login non user status")

        # Login non-admin user
        user = "User1"
        password = "u1"
        non_admin = P.User(user, password)

        signed_in = SM.logIn(non_admin)

        self.assertEqual(signed_in, False)
        SM.logOut()

        print("Test admin user status")
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
        print("Check user in user list")
        # Chech that the length os the list is greater than zero

        user_list = len(SM.GetUserList())
        self.assertGreater(user_list,0)

    # allow serial number over-write
    def test_serial_number_overwrite(self):
        print("Serial number over write")

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