import warnings
import pytest
import AdminUser
import Sessions
import tkinter as tk
import Datastore
import UserLogin
import Ports
import SecurityManager

DS = Datastore.DataStore()
P = Ports
SM = SecurityManager.SecurityManager()


class TestAdmin:

    def test_get_browse_file(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.AdminWindow(patient, controller)
        AU.location.set("")
        before = AU.location.get()
        assert before == ""

        AU.get_browse_file()
        after = len(AU.location.get())
        assert after > 0

    def test_change_qty(self, capsys):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.AdminWindow(patient, controller)
        qty = Sessions.get_qty()
        assert qty == 100
        with capsys.disabled():
            print('Enter a number lower than 100.')
        AU.change_qty()
        quantity = Sessions.get_qty()
        assert quantity < qty

    def test_set_admin_state(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.AdminWindow(patient, controller)
        UL = UserLogin.LogInWindow(patient, controller)
        UL.refresh_window()
        before = False
        AU.refresh_window()
        resultb = DS.get_overwrite_setting()
        assert resultb == before
        after = True
        AU.admin_state.set(True)
        AU.set_admin_state()
        resulta = DS.get_overwrite_setting()
        assert resulta == after

    def test_set_odm_state(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.AdminWindow(patient, controller)
        ports = P.Ports()
        DS.write_device_to_file(ports)
        expected1 = True
        result1 = DS.get_monitor_setting()
        assert expected1 == result1
        set_odm = False
        AU.odm_active.set(set_odm)
        AU.set_odm_state()
        result2 = DS.get_monitor_setting()
        assert set_odm == result2

    def test_non_human_probe(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.AdminWindow(patient, controller)
        expected = False
        animal = DS.get_animal_probe()
        assert expected == animal
        set_animal = True
        AU.non_human.set(set_animal)
        AU.set_non_human_probe()
        result = DS.get_animal_probe()
        assert result == set_animal

    def test_password_entry(self, capsys):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.ChangePasswordWindow(patient, controller)
        with capsys.disabled():
            print('Press the letter "h"')
        AU.refresh_window()
        AU.password_entry()
        result = AU.newPassword
        assert result == "h"

    def test_conform_pwd(self, capsys):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.ChangePasswordWindow(patient, controller)
        AU.refresh_window()
        with capsys.disabled():
            print('Press the letter "h"')
        AU.conform_pwd()
        result = AU.confirmPassword
        assert result == "h"

    def test_set_admin_state_change_password(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.ChangePasswordWindow(patient, controller)
        AU.refresh_window()
        expected = False
        selected_user = P.Users("brian", True, pw_user="Jon")
        DS.write_user_data(selected_user)
        AU.set_admin_state()
        result = AU.is_admin
        assert expected == result

    def test_check_user_admin(self):
        name = "Jon"
        expected = True
        expected1 = False
        result = AdminUser.check_user_admin(name)
        assert expected == result
        AdminUser.ADMIN_COUNT = 2
        result1 = AdminUser.check_user_admin(name)
        assert expected1 == result1

    def test_change_password(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser
        AU.refresh_window()
        expected = False
        user = P.Users("brian", True, pw_user="Jon")
        DS.write_user_data(user)
        result = AU.change_password(False, "1234", False)
        assert expected == result

        expected2 = True
        result2 = AU.change_password(True, "1234", False)
        assert expected2 == result2

        user_deleted = P.Users("brian", True, pw_user="User10")
        DS.write_user_data(user_deleted)
        result3 = AU.change_password(True, "1234", False)
        assert result3 is False

    def test_check_entries(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.ChangePasswordWindow(patient, controller)
        expected = False
        AU.refresh_window()
        AU.newPassword = "1234"
        AU.confirmPassword = "4567"
        AU.is_admin = False
        result = AU.check_entries()
        assert expected == result

    def test__get_selected_user(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser
        AU.refresh_window()
        AU.set_test()
        AU.userListBox.focus_set()
        AU.userListBox.selection_set(1)
        expected = AU.userListBox.get(1)
        AU._getSelectedUser()
        result = DS.get_reset_password_name()
        assert result == expected

    def test_check_delete(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser
        user8 = "User8"
        password = "password"
        # Create user object
        delete_user = P.User(user8, password)
        # Check to see if the user is registered to the system
        # if so, delete them and remove then from
        # to delete list
        check_list = DS.getUserList()
        for user in check_list:
            if user.name == user8:
                DS.delete_user(user8)
                DS.remove_from_delete_file(user8)
        # If the user is not in the list, add them
        check_user = DS.getUser(user8)
        if not check_user:
            SM.addUser(delete_user)

        AU.refresh_window()
        AU.set_test()
        # Check that the user has been added
        check_after = DS.getUser(user8)
        assert check_after.name == user8
        # Test that the newly added user can be deleted and
        # added to delete list
        result = AU.delete_user(delete_user)
        assert result is True

    def test__del_usr_btn_clicked(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser
        AU.refresh_window()
        AU.set_test()
        user10 = "User10"
        password = "password"
        # Create a test delete user
        delete_user = P.User(user10, password)
        SM.addUser(delete_user)
        # Detect that the user is now in the system
        # if so, remove them
        users = DS.getUserList()
        for user in users:
            if user.name == user10:
                DS.delete_user(user10)
        # Add the test user to the system
        check_user = DS.getUser(user10)
        if not check_user:
            SM.addUser(delete_user)
        # User selects the user from the user listbox
        user_list = AU.userList
        if user10 in user_list:
            # Set the index of the selected user, when
            # the user delete button is clicked in test
            # mode. The system selects the test user
            AU.index = user_list.index(user10)
            # Test that when the user presses the delete button
            # the correct actions are followed.
            AU._delUsr_btn_clicked()
            result = AU.result
            assert result is True

    ## Add user class  ##

    def test_name_entry(self, capsys):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.AddUserWindow(patient, controller)
        AU.refresh_window()
        check_username = AU.newusername
        AU._setDefaults()
        with capsys.disabled():
            print('Press the letter "h"')
        check_none = ""
        expected = "h"
        assert check_username == check_none
        AU.name_entry()
        result = AU.newusername
        assert result == expected

    def test_password_entry_add(self, capsys):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.AddUserWindow(patient, controller)
        AU.refresh_window()
        check_password = AU.newpassword
        AU._setDefaults()
        with capsys.disabled():
            print('Press the letter "h"')
        check_none = ""
        expected = "h"
        assert check_password == check_none
        AU.password_entry()
        result = AU.newpassword
        assert result == expected

    def test_conform_pwd_add(self, capsys):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.AddUserWindow(patient, controller)
        AU.refresh_window()
        check_password = AU.confpassword
        AU._setDefaults()
        with capsys.disabled():
            print('Press the letter "h"')
        check_none = ""
        expected = "h"
        assert check_password == check_none
        AU.conform_pwd()
        result = AU.confpassword
        assert result == expected

    def test_check_details(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.AddUserWindow(patient, controller)
        expected = True
        check = False
        new_user = "new_user"
        new_password = "new-password"
        diff_pass = "different"
        pass_null = ""

        AU.newusername = new_user
        AU.newpassword = pass_null
        AU.confpassword = new_password
        result1 = AU.check_details()
        assert result1 == check

        AU.newpassword = new_password
        AU.confpassword = pass_null
        result2 = AU.check_details()
        assert result2 == check

        AU.confpassword = diff_pass
        result3 = AU.check_details()
        assert result3 == check

        AU.newusername = pass_null
        AU.newpassword = new_password
        AU.confpassword = new_password
        result4 = AU.check_details()
        assert result4 == check

        AU.newusername = new_user
        result5 = AU.check_details()
        assert result5 == expected

    def test_add_user(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.AddUserWindow(patient, controller)
        expected = True
        adminF = False
        adminT = True
        new_user1 = "New user"
        new_password = "new-password"
        new_user2 = "New user2"
        check_user = DS.getUserList()
        # shows list of user objects

        AU.newusername = new_user1
        AU.newpassword = new_password
        for user in check_user:
            if user.name == new_user1:
                DS.delete_user(new_user1)
            if user.name == new_user2:
                DS.delete_user(new_user2)

        result = AU.add_user(adminF)
        assert result == expected

        AU.newusername = new_user2
        result = AU.add_user(adminT)
        assert result == expected

    def test__confm_btn_clicked(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.AddUserWindow(patient, controller)
        AU.refresh_window()
        AU.set_test()
        expected = True
        false_return = False
        adminF = False
        adminT = True
        new_user1 = "New user"
        new_password = "new-password"
        new_user2 = "New user2"
        check_user = DS.getUserList()
        AU.newusername = new_user1
        AU.newpassword = new_password
        for user in check_user:
            if user.name == new_user1:
                DS.delete_user(new_user1)
            if user.name == new_user2:
                DS.delete_user(new_user2)
        # Set the admin flag to false
        AU.is_admin.set(adminF)
        result = AU._confm_btn_clicked()
        assert result is false_return
        AU.newusername = new_user2
        AU.confpassword = new_password
        result = AU._confm_btn_clicked()
        assert result is expected
        # Check to see if the user admin is false
        user_false = DS.getUser(new_user2).admin
        assert user_false is false_return
        # remove the last user from the system
        DS.delete_user(new_user2)
        # set the admin flag to true
        AdminUser.ADMIN_COUNT = 2
        AU.is_admin.set(adminT)
        result = AU._confm_btn_clicked()
        assert result is expected
        # Check to see if the user admin is still false
        user_true = DS.getUser(new_user2).admin
        assert user_true is false_return



