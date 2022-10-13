'''
Created on 3 May 2017
@author: jackw
@amended by Brian F
Naming convention
- Variables = no spaces, capitals for every word except the first : thisIsAVariable
- Local functions = prefixed with _, _ for spaces, no capitals : _a_local_function
Dependencies
-NI VISA Backend
-Non standard python modules
    pyvisa
    pyserial
to do:
-complete button on TPW doesn't work
-TPW freezes if a probe is inserted
-add SQ probe to list
#         s = ttk.Separator(self.root, orient=VERTICAL)
#         s.grid(row=0, column=1, sticky=(N,S))
-------------------------------------------------
# For testing purposes comment out the following
import BatchManager
import Sessions as SE
BM = BatchManager.BatchManager()
-- in Login button clicked --
self.canvas_name.destroy()
self.canvas_pass.destroy()
self.direct_session_window()
self.refresh_window()
self.activate_login_button()
self.refresh_window()
---------------------------------------------------
'''

import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tm
import SecurityManager
import BatchManager
import Sessions
import Datastore
import OnScreenKeys
import Ports
import ProbeTest
import AdminUser

from time import gmtime, strftime, sleep

SM = SecurityManager.SecurityManager()
BM = BatchManager.BatchManager()
DS = Datastore.Data_Store()
KY = OnScreenKeys.Keyboard()
P = Ports
SE = Sessions
PT = ProbeTest
AU = AdminUser


class LogInWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#B1D0E0')
        self.canvas_pass = None
        self.canvas_name = None
        self.control = controller
        DS.write_to_from_keys("  ")
        self.current_user = None
        self.password = None
        self.user = ""
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.cent_x = self.ws / 2
        self.cent_y = self.hs / 2

    def setup(self):
        self.current_user = ""
        self.password = ""

    def entry(self):
        self.canvas_name = Canvas(bg="#eae9e9", width=520, height=55)
        self.canvas_name.place(relx=0.35, rely=0.32)
        self.canvas_pass = Canvas(bg="#eae9e9", width=520, height=55)
        self.canvas_pass.place(relx=0.35, rely=0.40)

    def refresh_window(self):
        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 28, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 18)).place(relx=0.85, rely=0.15)
        time_now = strftime("%H:%M:%p", gmtime())
        self.setup()
        self.label_4 = ttk.Label(self, text="           Probe Test Tool", background="#3AB4F2", width=25,
                                 font=('Helvetica', 24))
        self.label_4.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.label_5 = ttk.Label(self, text="Good morning.", font=("bold", 20), background="#B1D0E0")
        self.label_6 = ttk.Label(self, text="Good afternoon.", font=("bold", 20), background="#B1D0E0")
        self.setup()
        self.logbtn = Button(self, text="Log In", font=("Courier", 18), width=18, background="#3AB4F2",
                             highlightthickness=0, command=self._login_btn_clicked)
        self.logbtn.place(relx=0.65, rely=0.64)
        Button(self, text="Forgot Password.", font=("Courier", 12), command=self.forgot_login).place(relx=0.35, rely=0.5)
        ttk.Button(self, text="Exit", width=20, command=self.quit).place(relx=0.88, rely=0.8, anchor=CENTER)
        self.bind('<Return>', lambda event: self._login_btn_clicked)
        if "AM" in time_now:
            self.label_5.place(relx=0.5, rely=0.25, anchor=CENTER)
        else:
            self.label_6.place(relx=0.5, rely=0.25, anchor=CENTER)
        self.logbtn.config(command=lambda: self._login_btn_clicked())
        ###################################
        # Testing data only               #
        # comment out when PTT is in use  #
        ###################################
        self.set_username("brian")
        self.set_password("password")
        reset_user = P.Users("", "")
        DS.write_user_data(reset_user)
        probe_data = P.Probes("", "", 0, 0, failed=0, scrap=0)
        DS.write_probe_data(probe_data)
        self.entry()

        self.btn_1 = Button(self.canvas_name, text='Username ',font=("Courier", 14), command=self.name_entry, width=20)
        Label(self.canvas_name, text="-->",font=("Courier", 14)).place(x=248, y=14)
        self.btn_2 = Button(self.canvas_pass, text='Password',font=("Courier", 14), command=self.password_entry, width=20)
        Label(self.canvas_pass, text="-->",font=("Courier", 14)).place(x=248, y=14)
        self.name_text = self.canvas_name.create_text(350, 20, text=" ", fill="black",
                                                      font=(OnScreenKeys.FONT_NAME, 16, "bold"))
        self.pass_text = self.canvas_pass.create_text(350, 20, text=" ", fill="black",
                                                      font=(OnScreenKeys.FONT_NAME, 14, "bold"))
        self.btn_1.place(x=18, y=14)
        self.btn_2.place(x=18, y=14)
        self.control.attributes('-topmost', True)

    def name_entry(self):
        self.logbtn.config(state=DISABLED)
        self.set_username("")
        self.get_keys()
        pass_block = False
        data = self.wait_for_response(self.canvas_name, pass_block, self.name_text)
        self.current_user = data
        self.set_username(data)
        self.btn_1.config(state=NORMAL)
        self.btn_2.config(state=NORMAL)
        self.logbtn.config(state=NORMAL)

    def password_entry(self):
        self.logbtn.config(state=DISABLED)
        self.set_password("")
        self.get_keys()
        pass_block = True
        data = self.wait_for_response(self.canvas_pass, pass_block, self.pass_text)
        self.password = data
        self.set_password(data)
        self.btn_1.config(state=NORMAL)
        self.btn_2.config(state=NORMAL)
        self.logbtn.config(state=NORMAL)

    def _login_btn_clicked(self):
        self.canvas_name.destroy()
        self.canvas_pass.destroy()
        ########################################
        # Get user inputs from the keyboard    #
        ########################################
        username = self.get_username()
        password = self.get_password()
        if len(username) > 0 and len(password) > 0:
            #######################################
            # Create user object with admin false #
            #######################################
            user = P.User(username, password)
            event = SM.logIn(user)
            if event:
                self.canvas_go()
                self.sessions()
            else:
                tm.showerror("Login error", "Incorrect username or password")
                self.refresh_window()
            self.activate_login_button()
            return event
        else:
            tm.showerror("Login error", "Please enter a Username and Password")
            self.refresh_window()

    def quit(self):
        shut = tm.askyesno("   Shutting Down   ", "   Do you wish to proceed?     ")
        #################################
        # Clear screen and distroy app  #
        #################################
        if shut:
            self.timer()
            self.canvas_name.destroy()
            self.canvas_pass.destroy()
            self.control.destroy()

    def direct_session_window(self):
        self.control.show_frame(SE.SessionSelectWindow)

    def timer(self):
        timer_canvas = Canvas(bg="#eae9e9", width=180, height=50)
        timer_canvas.place(x=600, y=500)
        timer_canvas.create_text(90,20, text="Wait for close")
        timer_label = timer_canvas.create_text(80, 35, text=" ", font=("bold", 20), anchor=W)
        bip = "."
        show_bip = ""
        for a in range(0,6):
            timer_canvas.itemconfig(timer_label, text=show_bip)
            sleep(0.75)
            show_bip += bip
            Tk.update(self)
        timer_canvas.destroy()


    def activate_login_button(self):
        try:
            self.logbtn.config(command=lambda: self.control.show_frame(SE.SessionSelectWindow))
        except:
            pass

    def wait_for_response(self, master, pass_block, location):
        block = pass_block
        DS.write_to_from_keys("_")
        password_blank = "*********************"
        while 1:
            pw_data = DS.get_keyboard_data()
            pw_len = len(pw_data)
            if pw_len > 0 and pw_data[-1] == "+":
                pw_data = pw_data[:-1]
                break

            if block:
                master.itemconfig(location, text=password_blank[:pw_len])
            else:
                master.itemconfig(location, text=pw_data)
            Tk.update(master)
        return pw_data

    def get_keys(self):
        KY.display()
        self.btn_1.config(state=DISABLED)
        self.btn_2.config(state=DISABLED)

    def set_username(self, name):
        self.current_user = name

    def get_username(self):
        return self.current_user

    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password

    def canvas_go(self):
        self.canvas_name.destroy()
        self.canvas_pass.destroy()

    def sessions(self):
        try:
            self.control.show_frame(SE.SessionSelectWindow)
        except:
            pass

    def forgot_login(self):
        user_list = SM.GetUserList()
        found = False
        if not self.current_user:
            PT.probe_canvas(self, "Enter your name to \nreset your password", False)
            sleep(3)
            PT.text_destroy(self)
            self.name_entry()
        for name in user_list:
            if name.name == self.current_user:
                login_user = P.Users(name=name.name, admin=False, reset_password=True)
                DS.write_user_data(login_user)
                found = True

        if found:
            self.canvas_go()
            self.control.show_frame(AU.ChangePasswordWindow)
        else:
            PT.probe_canvas(self, "Your name is not registered.", False)
            sleep(3)
            PT.text_destroy(self)


    def yes_answer(self):
        pass

    def no_answer(self):
        pass

