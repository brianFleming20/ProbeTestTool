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
from SecurityManager import User
import BatchManager
import Sessions
import Datastore
import OnScreenKeys
import Ports

from time import gmtime, strftime

SM = SecurityManager.SecurityManager()
BM = BatchManager.BatchManager()
DS = Datastore.Data_Store()
KY = OnScreenKeys.Keyboard()
P = Ports
SE = Sessions


def ignore():
    return 'break'


class LogInWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#B1D0E0')
        self.canvas_pass = None
        self.canvas_name = None
        self.control = controller
        DS.write_to_from_keys("  ")
        self.current_user = None
        self.password = None

    def setup(self):
        self.current_user = ""
        self.password = ""

    def entry(self):
        self.canvas_name = Canvas(bg="#eae9e9", width=500, height=55)
        self.canvas_name.place(relx=0.35, rely=0.32)
        self.canvas_pass = Canvas(bg="#eae9e9", width=500, height=55)
        self.canvas_pass.place(relx=0.35, rely=0.40)

    def refresh_window(self):
        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 28, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 18)).place(relx=0.85, rely=0.15)
        time_now = strftime("%H:%M:%p", gmtime())
        self.label_4 = ttk.Label(self, text="           Probe Test Tool", background="#3AB4F2", width=25,
                                 font=('Helvetica', 24))
        self.label_4.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.label_5 = ttk.Label(self, text="Good morning.", font=("bold", 20), background="#B1D0E0")
        self.label_6 = ttk.Label(self, text="Good afternoon.", font=("bold", 20), background="#B1D0E0")
        self.setup()
        self.logbtn = Button(self, text="Log In", font=("Courier", 18), width=18, background="#3AB4F2",
                             highlightthickness=0, command=self._login_btn_clicked)
        self.logbtn.place(relx=0.65, rely=0.64)
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
        reset_user = P.Users("","")
        DS.write_user_data(reset_user)
        probe_data = P.Probes("","",0,0)
        DS.write_probe_data(probe_data)
        self.entry()

        self.btn_1 = Button(self.canvas_name, text='Username ',font=("Courier", 12), command=self.name_entry, width=20)
        Label(self.canvas_name, text="-->").place(x=245, y=14)
        self.btn_2 = Button(self.canvas_pass, text='Password',font=("Courier", 12), command=self.password_entry, width=20)
        Label(self.canvas_pass, text="-->").place(x=245, y=14)
        self.name_text = self.canvas_name.create_text(350, 20, text=" ", fill="black",
                                                      font=(OnScreenKeys.FONT_NAME, 16, "bold"))
        self.pass_text = self.canvas_pass.create_text(350, 20, text=" ", fill="black",
                                                      font=(OnScreenKeys.FONT_NAME, 14, "bold"))
        self.btn_1.place(x=18, y=14)
        self.btn_2.place(x=18, y=14)
        self.control.attributes('-topmost', True)

    def name_entry(self):
        self.set_username("")
        self.get_keys()
        pass_block = False
        data = self.wait_for_response(self.canvas_name, pass_block)
        self.current_user = data
        self.set_username(data)
        self.btn_1.config(state=NORMAL)
        self.btn_2.config(state=NORMAL)
        DS.write_to_from_keys(data)

    def password_entry(self):
        self.set_password("")
        self.get_keys()
        pass_block = True
        data = self.wait_for_response(self.canvas_pass, pass_block)
        self.password = data
        self.set_password(data)
        self.btn_1.config(state=NORMAL)
        self.btn_2.config(state=NORMAL)

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
            user = User(username, password)
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
            self.canvas_name.destroy()
            self.canvas_pass.destroy()
            self.control.destroy()

    def direct_session_window(self):
        self.control.show_frame(SE.SessionSelectWindow)

    def activate_login_button(self):
        try:
            self.logbtn.config(command=lambda: self.control.show_frame(SE.SessionSelectWindow))
        except:
            pass

    def wait_for_response(self, master, pass_block):
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
                self.canvas_pass.itemconfig(self.pass_text, text=password_blank[:pw_len])
            else:
                self.canvas_name.itemconfig(self.name_text, text=pw_data)
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
