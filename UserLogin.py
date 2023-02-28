"""
Created on 3 May 2017
@author: jackw
@author: Brian F
Naming convention
- Variables = no spaces, capitals for every word except the first : thisIsAVariable
- Local functions = prefixed with _, _ for spaces, no capitals : _a_local_function
Dependencies

User input via an onscreen keyboard
System cache data stored locally
Logged user / admin and status recorded

-------------------------------------------------

"""

import tkinter as tk
from tkinter import *
# from tkinter import ttk
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
DS = Datastore.DataStore()
KY = OnScreenKeys.Keyboard()
K = OnScreenKeys
P = Ports
SE = Sessions
PT = ProbeTest
AU = AdminUser


class LogInWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#B1D0E0')
        self.btn_2 = None
        self.logbtn = None
        self.label_6 = None
        self.label_5 = None
        self.btn_1 = None
        self.show_bip = None
        self.pass_text = None
        self.name_text = None
        self.canvas_pass = None
        self.canvas_name = None
        self.check_name = None
        self.control = controller
        DS.write_to_from_keys("  ")
        self.current_user = None
        self.password = None
        self.user = ""
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.cent_x = self.ws / 2
        self.cent_y = self.hs / 2
        self.test = False

    def setup(self):
        self.current_user = ""
        self.password = ""

    def entry(self):
        self.canvas_name = Canvas(bg="#eae9e9", width=520, height=55)
        self.canvas_name.place(relx=0.35, rely=0.32)
        self.canvas_pass = Canvas(bg="#eae9e9", width=520, height=55)
        self.canvas_pass.place(relx=0.35, rely=0.40)

    def refresh_window(self):
        Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
              font=('Helvetica', 30, 'bold'), width=12).place(relx=0.79, rely=0.1)
        Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
              font=('Helvetica', 16)).place(relx=0.88, rely=0.15)
        time_now = strftime("%H:%M:%p", gmtime())
        self.setup()
        Label(self, text="Probe Test Tool", background="#3AB4F2", width=25,
              font=('Helvetica', 24)).place(relx=0.5, rely=0.1, anchor=CENTER)
        self.label_5 = Label(self, text="Good morning.", font=("bold", 20), background="#B1D0E0")
        self.label_6 = Label(self, text="Good afternoon.", font=("bold", 20), background="#B1D0E0")
        self.setup()
        self.logbtn = Button(self, text="Log In", font=("Courier", 18), width=18, background="#3AB4F2",
                             highlightthickness=0, command=self._login_btn_clicked)
        self.logbtn.place(relx=0.65, rely=0.64)
        Button(self, text="Exit", width=20, command=self.quit_).place(relx=0.88, rely=0.8, anchor=CENTER)
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
        self.set_username("Jon")
        self.set_password("Batman")
        reset_user = P.Users("", "", over_right=False, non_human=False)
        DS.write_user_data(reset_user)
        probe_data = P.Probes("", "", 0, 0, failed=0, scrap=0)
        DS.write_probe_data(probe_data)
        self.entry()
        self.btn_1 = Button(self.canvas_name, text='Username ', font=("Courier", 14), command=self.name_entry, width=20)
        Label(self.canvas_name, text="-->", font=("Courier", 14)).place(x=248, y=14)
        self.btn_2 = Button(self.canvas_pass, text='Password', font=("Courier", 14), command=self.password_entry,
                            width=20)
        Label(self.canvas_pass, text="-->", font=("Courier", 14)).place(x=248, y=14)
        self.btn_1.place(x=18, y=14)
        self.btn_2.place(x=18, y=14)
        self.control.attributes('-topmost', True)

    def name_entry(self):
        self.btn_1.config(state=DISABLED)
        self.btn_2.config(state=DISABLED)
        self.set_username("")
        self.get_keys()
        data = K.wait_for_response(self.canvas_name, self.name_text)
        self.set_username(data)
        self.check_name = DS.get_current_use_user(data)
        self.btn_1.config(state=NORMAL)
        self.btn_2.config(state=NORMAL)

    def password_entry(self):
        self.btn_1.config(state=DISABLED)
        self.btn_2.config(state=DISABLED)
        self.set_password("")
        self.get_keys()
        data = K.wait_for_response(self.canvas_pass, self.pass_text, block=True)
        self.set_password(data)
        self.btn_1.config(state=NORMAL)
        self.btn_2.config(state=NORMAL)

    def _login_btn_clicked(self):
        ########################################
        # Get user inputs from the keyboard    #
        ########################################
        username = self.get_username()
        password = self.get_password()
        if len(username) > 0 and len(password) > 0 and not self.check_name:
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

    def quit_(self):
        shut = tm.askyesno("   Shutting Down   ", "   Do you wish to proceed?     ")
        #################################
        # Clear screen and destroy app  #
        #################################
        if shut:
            self.timer()
            self.canvas_name.destroy()
            self.canvas_pass.destroy()
            self.control.destroy()

    def direct_session_window(self):
        self.control.show_frame(SE.SessionSelectWindow)

    def timer(self):
        timer_canvas = Canvas(bg="#B1D0E0", bd=0, width=180, height=50)
        timer_canvas.place(x=600, y=500)
        timer_canvas.create_text(90, 20, text="Wait for close", font=("Courier", 14))
        timer_label = timer_canvas.create_text(80, 35, text=" ", font=("bold", 20), anchor=W)
        bip = "."
        self.show_bip = ""
        for a in range(0, 6):
            timer_canvas.itemconfig(timer_label, text=self.show_bip)
            sleep(0.75)
            self.show_bip += bip
            Tk.update(self)
        timer_canvas.destroy()

    def activate_login_button(self):
        if not self.test:
            self.logbtn.config(command=lambda: self.control.show_frame(SE.SessionSelectWindow))

    def get_keys(self):
        KY.display()

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
        self.canvas_name.destroy()
        self.canvas_pass.destroy()
        if not self.test:
            self.control.show_frame(SE.SessionSelectWindow)

    def yes_answer(self):
        pass

    def no_answer(self):
        pass

    def set_test(self):
        self.test = True
