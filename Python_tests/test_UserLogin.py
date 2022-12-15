import UserLogin
import tkinter as tk
import pytest


class TestLogin:

    def test_quit_(self):
        parent = tk.Tk()
        controller = tk.Tk()
        UL = UserLogin.LogInWindow(parent, controller)
        UL.set_test()
        UL.refresh_window()
        UL.quit_()

    def test_timer(self):
        parent = tk.Tk()
        controller = tk.Tk()
        UL = UserLogin.LogInWindow(parent, controller)
        UL.set_test()
        UL.refresh_window()

        UL.timer()
        result = UL.show_bip
        assert result == "......"

    def test_name_entry(self, capsys):
        parent = tk.Tk()
        controller = tk.Tk()
        UL = UserLogin.LogInWindow(parent, controller)
        UL.set_test()
        UL.refresh_window()
        master = tk.Canvas(width=200, height=100)
        master.pack()
        name_text = master.create_text(50, 20, text=" ", fill="black",
                                       font=('Arial', 16, "bold"))
        UL.canvas_name = master
        with capsys.disabled():
            print('Press the letter "h"')
        UL.name_text = name_text
        expected = "h"
        UL.name_entry()
        result = UL.get_username()
        assert result == expected

    def test_password_entry(self, capsys):
        parent = tk.Tk()
        controller = tk.Tk()
        UL = UserLogin.LogInWindow(parent, controller)
        UL.set_test()
        UL.refresh_window()
        master = tk.Canvas(width=200, height=100)
        master.pack()
        name_text = master.create_text(50, 20, text=" ", fill="black",
                                       font=('Arial', 16, "bold"))
        UL.canvas_name = master
        with capsys.disabled():
            print('Press the letter "h"')
        UL.pass_text = name_text
        expected = "h"
        UL.password_entry()
        result = UL.get_password()
        assert result == expected

    def test_unknown_user(self):
        parent = tk.Tk()
        controller = tk.Tk()
        UL = UserLogin.LogInWindow(parent, controller)
        UL.set_test()
        UL.refresh_window()
        UL.set_username("none")
        UL.set_password("password")
        result = UL._login_btn_clicked()
        assert result is False

    def test__login_btn_clicked(self):
        parent = tk.Tk()
        controller = tk.Tk()
        UL = UserLogin.LogInWindow(parent, controller)
        UL.set_test()
        UL.refresh_window()
        UL.set_username("brian")
        UL.set_password("password")
        result = UL._login_btn_clicked()
        assert result is True

        UL.set_username("User3")
        UL.set_password("123456")
        result_error = UL._login_btn_clicked()
        assert result_error is False

        UL.set_username("")
        UL.set_password("")
        result_empty = UL._login_btn_clicked()
        assert result_empty is None
