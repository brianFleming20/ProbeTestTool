import warnings
import pytest
import AdminUser
import Sessions
import tkinter as tk
import Datastore
import UserLogin
import Ports
import SecurityManager
import OnScreenKeys

DS = Datastore.DataStore()
P = Ports
SM = SecurityManager.SecurityManager()
K = OnScreenKeys.Keyboard()


@pytest.fixture
def one():
    parent = tk.Tk()
    controller = tk.Tk()
    AU = AdminUser.AdminWindow(parent, controller)
    parent.geometry("1200x850")
    return AU


@pytest.fixture
def two():
    parent = tk.Tk()
    controller = tk.Tk()
    UL = UserLogin.LogInWindow(parent, controller)
    return UL


@pytest.fixture
def change():
    parent = tk.Tk()
    controller = tk.Tk()
    AU = AdminUser.ChangePasswordWindow(parent, controller)
    parent.geometry("1200x850")
    return AU


@pytest.fixture
def edit():
    parent = tk.Tk()
    controller = tk.Tk()
    EU = AdminUser.EditUserWindow(parent, controller)
    return EU


@pytest.fixture
def add():
    parent = tk.Tk()
    controller = tk.Tk()
    AD = AdminUser.AddUserWindow(parent, controller)
    parent.geometry("1200x850")
    return AD


def test_get_browse_file(one):
    one.file_loc.set("")
    before = one.file_loc.get()
    assert before == ""

    one.get_browse_file()
    after = len(one.file_loc.get())
    one.destroy()
    assert after > 0


def test_change_qty(one):
    one.layout()
    qty = Sessions.get_qty()
    assert qty == 100
    tk.Label(K.canvas, text="Enter a number lower than 100", font=("Arial", 18)).place(relx=0.4, rely=0.1)
    one.change_qty()
    quantity = Sessions.get_qty()
    one.destroy()
    assert quantity < qty


def test_set_admin_state(one, two):
    two.refresh_window()
    before = False
    one.refresh_window()
    resultb = DS.get_overwrite_setting()
    assert resultb == before
    after = True
    one.admin_state.set(True)
    one.set_admin_state()
    resulta = DS.get_overwrite_setting()
    one.destroy()
    two.destroy()
    assert resulta == after


def test_set_odm_state(one):
    ports = P.Ports()
    DS.write_device_to_file(ports)
    expected1 = True
    result1 = DS.get_monitor_setting()
    assert expected1 == result1
    set_odm = False
    one.odm_active.set(set_odm)
    one.set_odm_state()
    result2 = DS.get_monitor_setting()
    one.destroy()

    assert set_odm == result2


def test_non_human_probe(one):
    expected = False
    animal = DS.get_animal_probe()
    assert expected == animal
    set_animal = True
    one.non_human.set(set_animal)
    one.set_non_human_probe()
    result = DS.get_animal_probe()
    one.destroy()
    assert result == set_animal


def test_password_entry(change):
    tk.Label(K.canvas, text="Enter a letter 'h'", font=("Arial", 18)).place(relx=0.4, rely=0.1)
    # print([user.name for user in SM.GetUserList()])
    user = P.Users("Jon", False, pw_user="User10")
    DS.write_user_data(user)
    change.refresh_window()
    change.password_entry()
    result = change.newPassword
    change.destroy()
    assert result == "h"


def test_conform_pwd(change):
    tk.Label(K.canvas, text="Enter a letter 'h'", font=("Arial", 18)).place(relx=0.4, rely=0.1)
    change.refresh_window()
    change.conform_pwd()
    result = change.confirmPassword
    change.destroy()
    assert result == "h"


def test_set_admin_state_change_password(change):
    # patient = tk.Tk()
    # controller = tk.Tk()
    # AU = AdminUser.ChangePasswordWindow(patient, controller)
    change.refresh_window()
    expected = False
    selected_user = P.Users("brian", True, pw_user="Jon")
    DS.write_user_data(selected_user)
    change.set_admin_state()
    result = change.is_admin
    change.destroy()
    assert expected == result


def test_check_user_admin():
    name = "Jon"
    expected = True
    expected1 = False
    result = AdminUser.check_user_admin(name)
    assert expected == result
    AdminUser.ADMIN_COUNT = 2
    result1 = AdminUser.check_user_admin(name)
    assert expected1 == result1


def test_check_entries(change):
    expected = False
    change.refresh_window()
    change.newPassword = "1234"
    change.confirmPassword = "4567"
    change.is_admin = False
    result = change.check_entries()
    change.destroy()
    assert expected == result


def test__get_selected_user(edit):
    AU = AdminUser
    edit.refresh_window()
    AU.set_test()
    edit.userListBox.focus_set()
    edit.userListBox.selection_set(1)
    expected = edit.userListBox.get(1)
    edit._getSelectedUser()
    result = DS.get_reset_password_name()
    assert result == expected


def test_check_delete(edit):
    AU = AdminUser
    user8 = "User8"
    password = "password"
    # Create user object
    print(f"\n{[user.name for user in SM.GetUserList()]}")
    delete_user = P.User(user8, password)
    # Check to see if the user is registered to the system
    # if so, delete them and remove then from
    # to delete list
    check_list = DS.getUserList()
    for user in check_list:
        if user.name == user8:
            DS.delete_user(user8)
            DS.remove_from_delete_file(user8)
    print([user.name for user in SM.GetUserList()])
    # If the user is not in the list, add them
    check_user = DS.getUser(user8)
    if not check_user:
        SM.addUser(delete_user)

    edit.refresh_window()
    AU.set_test()
    # Check that the user has been added
    check_after = DS.getUser(user8)
    assert check_after.name == user8
    # Test that the newly added user can be deleted and
    # added to delete list
    print([user.name for user in SM.GetUserList()])
    result = AU.delete_user(delete_user)
    assert result is True


def test__del_usr_btn_clicked(edit):
    # patient = tk.Tk()
    # controller = tk.Tk()
    AU = AdminUser
    edit.refresh_window()
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
    user_list = edit.userList
    if user10 in user_list:
        # Set the index of the selected user, when
        # the user delete button is clicked in test
        # mode. The system selects the test user
        one.index = user_list.index(user10)
        # Test that when the user presses the delete button
        # the correct actions are followed.
        edit._delUsr_btn_clicked()
        result = edit.result
        assert result is True


def test_name_entry(add):
    add.refresh_window()
    check_username = add.newusername
    add._setDefaults()
    tk.Label(K.canvas, text="Enter a letter 'h' in name.", font=("Arial", 18)).place(relx=0.2, rely=0.35)
    check_none = ""
    expected = "h"
    assert check_username == check_none
    add.name_entry()
    result = add.newusername
    add.destroy()
    assert result == expected


def test_password_entry_add(add):
    add.refresh_window()
    check_password = add.newpassword
    add._setDefaults()
    tk.Label(K.canvas, text="Enter a letter 'h' in the password", font=("Arial", 18)).place(relx=0.2, rely=0.455)
    check_none = ""
    expected = "h"
    assert check_password == check_none
    add.password_entry()
    result = add.newpassword
    add.destroy()
    assert result == expected


def test_conform_pwd_add(add):
    add.refresh_window()
    check_password = add.confpassword
    add._setDefaults()
    tk.Label(K.canvas, text="Enter a letter 'h' in the password", font=("Arial", 18)).place(relx=0.2, rely=0.57)
    check_none = ""
    expected = "h"
    assert check_password == check_none
    add.conform_pwd()
    result = add.confpassword
    add.destroy()
    assert result == expected


def test_check_details(add):
    expected = True
    check = False
    new_user = "new_user"
    new_password = "new-password"
    diff_pass = "different"
    pass_null = ""
    user = P.User(new_user, new_password)
    # add.newusername = new_user
    # add.newpassword = pass_null
    add.confpassword = new_password
    result1 = add.check_details(user)
    assert result1 == check

    # add.newpassword = new_password
    add.confpassword = pass_null
    result2 = add.check_details(user)
    assert result2 == check

    add.confpassword = diff_pass
    result3 = add.check_details(user)
    assert result3 == check

    # add.newusername = pass_null
    user.name = pass_null
    # add.newpassword = new_password
    add.confpassword = new_password
    result4 = add.check_details(user)
    assert result4 == check

    # add.newusername = new_user
    user.name = new_user
    user.password = new_password
    result5 = add.check_details(user)
    add.destroy()
    assert result5 == expected


def test_add_user(add):
    expected = True
    adminF = False
    adminT = True
    new_user1 = "New user"
    new_password = "new-password"
    new_user2 = "New user2"
    check_user = DS.getUserList()
    # shows list of user objects

    add.newusername = new_user1
    add.newpassword = new_password
    for user in check_user:
        if user.name == new_user1:
            DS.delete_user(new_user1)
        if user.name == new_user2:
            DS.delete_user(new_user2)

    result = add.add_user(adminF)
    assert result == expected

    add.newusername = new_user2
    result = add.add_user(adminT)
    add.destroy()
    assert result == expected


def test__confm_btn_clicked(add):
    ####################################
    # Test the add user process for    #
    # missing and wrong user inputs    #
    # then add a user to the system    #
    ####################################
    add.refresh_window()
    add.set_test()
    expected = True
    false_return = False
    new_user1 = "New user"
    new_user2 = "New user2"
    new_user3 = "New user3"
    new_password = "new-password"
    wrong_password = "old-password"
    empty_password = ""
    check_user = DS.getUserList()
    ######################################
    # Remove any left over test data     #
    ######################################
    for user in check_user:
        if user.name == new_user1:
            DS.delete_user(new_user1)
        if user.name == new_user2:
            DS.delete_user(new_user2)
        if user.name == new_user3:
            DS.delete_user(new_user3)

    ######################################
    # User with empty passwords and user #
    ######################################
    add.newusername = empty_password
    add.newpassword = empty_password
    add.confpassword = empty_password
    add.is_admin.set(False)
    test_user = P.User(empty_password, empty_password, False)

    result1 = add.check_details(test_user)
    assert result1 == false_return

    test_user.name = new_user1
    result2 = add.check_details(test_user)
    assert result2 == false_return

    test_user.password = new_password
    result3 = add.check_details(test_user)
    assert result3 == false_return

    test_user.password = wrong_password
    add.confpassword = new_password
    result4 = add.check_details(test_user)
    assert result4 == false_return

    test_user.password = new_password
    result5 = add.check_details(test_user)
    assert result5 == expected

    #######################################
    # Test button clicked to create user  #
    # object to transfer to check         #
    #######################################
    add.newusername = new_user1
    add.newpassword = new_password
    add.confpassword = wrong_password
    add.is_admin.set(False)
    result6 = add._confm_btn_clicked()
    assert result6 == false_return

    ########################################
    # Add new user to the system and check #
    # admin is false and true. Remove user #
    # after insertion.                     #
    ########################################
    add.newusername = new_user1
    add.newpassword = new_password
    add.confpassword = new_password
    add.is_admin.set(False)

    result7 = add._confm_btn_clicked()
    print([user.name for user in SM.GetUserList()])
    assert result7 == expected
    assert new_user1 in [item.name for item in DS.getUserList()]
    for user in DS.getUserList():
        if user.name == new_user1:
            assert user.admin == false_return

    ###############################################
    # Check if a new user is added to the system  #
    # if the user is wanted to be an admin but    #
    # add admins are taken, then added as non     #
    # admin.                                      #
    ###############################################

    add.newusername = new_user2
    add.newpassword = new_password
    add.confpassword = new_password
    add.is_admin.set(True)

    result8 = add._confm_btn_clicked()
    print([user.name for user in SM.GetUserList()])
    assert result8 == expected
    assert new_user2 in [item.name for item in DS.getUserList()]
    for user in DS.getUserList():
        if user.name == new_user1:
            assert user.admin == false_return

    ################################################
    # Add a new user as an admin that the user has #
    # space to add.                                #
    ################################################

    add.newusername = new_user3
    add.newpassword = new_password
    add.confpassword = new_password
    add.is_admin.set(True)

