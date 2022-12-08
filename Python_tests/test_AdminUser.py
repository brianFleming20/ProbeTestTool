import AdminUser
import Sessions
import tkinter as tk
import Datastore
import UserLogin
import Ports

DS = Datastore.Data_Store()
P = Ports

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

    def test_change_qty(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.AdminWindow(patient, controller)
        qty = Sessions.get_qty()
        assert qty is 100

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

    def test_password_entry(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.ChangePasswordWindow(patient, controller)
        AU.refresh_window()
        AU.password_entry()
        result = AU.newPassword
        assert result == "a"

    def test_conform_pwd(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.ChangePasswordWindow(patient, controller)
        AU.refresh_window()
        AU.conform_pwd()
        result = AU.confirmPassword
        assert result == "b"

    def test_set_admin_state_change_password(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.ChangePasswordWindow(patient, controller)
        AU.refresh_window()
        expected = False
        selected_user = P.Users("brian", True, pw_user="Jon")
        DS.write_user_data(selected_user)
        AU.set_admin_state()
        result = AU.is_admin.get()
        assert expected == result

    def test_check_user_admin(self):
        name = "Jon"
        expected = True
        expected1 = False
        result = AdminUser.check_user_admin(name)
        assert expected == result
        AdminUser.ADMIN_COUNT = 1
        result1 = AdminUser.check_user_admin(name)
        assert expected1 == result1

    def test_change_password(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.ChangePasswordWindow(patient, controller)
        AU.refresh_window()
        expected = False
        user = P.Users("Brian", True, pw_user="Jon")
        DS.write_user_data(user)
        result = AU.change_password(False, "1234", False)
        assert expected == result
        expected2 = True
        result2 = AU.change_password(True, "1234", False)
        assert expected2 == result2

    def test_check_entries(self):
        patient = tk.Tk()
        controller = tk.Tk()
        AU = AdminUser.ChangePasswordWindow(patient, controller)
        expected = False
        AU.refresh_window()
        AU.newPassword = "1234"
        AU.confirmPassword = "4567"
        AU.is_admin.set(False)
        result = AU.check_entries()
        assert expected == result

    def test__get_selected_user(self):
        assert False

    def test__del_usr_btn_clicked(self):
        assert False

    def test_check_delete(self):
        assert False

    def test__confm_btn_clicked(self):
        assert False

    def test_add_user(self):
        assert False

    def test_check_details(self):
        assert False

    def test_name_entry(self):
        assert False

    def test_password_entry_add(self):
        assert False

    def test_conform_pwd_add(self):
        assert False
