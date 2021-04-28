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

'''

import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tm
import SecurityManager
from SecurityManager import User
from Main import SessionSelectWindow


class LogInWindow(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self)
        self.currentUser = StringVar()
        

        self.label_1 = ttk.Label(self, text="Username")
        self.label_2 = ttk.Label(self, text="Password")

        self.entry_1 = ttk.Entry(self, textvariable=self.currentUser ,font="bold")
        self.entry_2 = ttk.Entry(self, show="*", font="bold")
        self.entry_1.insert(END, 'Jack')
        self.entry_2.insert(END, 'password')

        self.label_1.place(relx=0.4, rely=0.3, anchor=CENTER)
        self.label_2.place(relx=0.4, rely=0.4, anchor=CENTER)
        self.entry_1.place(relx=0.6, rely=0.3, anchor=CENTER)
        self.entry_2.place(relx=0.6, rely=0.4, anchor=CENTER)

        self.logbtn = ttk.Button(
            self, text="Login", width="20",command=lambda: self._login_btn_clicked(controller))
        self.logbtn.place(relx=0.5, rely=0.6 ,anchor=CENTER)
        self.bind('<Return>', lambda: self._login_btn_clicked(controller))
        
        

        self.entry_1.focus_set()

    def _login_btn_clicked(self, controller):
        self.logbtn.config(command=ignore)

        # create a user object from the users input
        username = self.entry_1.get()
        password = self.entry_2.get()
        user = User(username, password)
        #self.entry_1.delete(0, 'end')
        self.entry_2.delete(0, 'end')
        # check to see if the details are valid
        if SM.logIn(user):
            controller.show_frame(SessionSelectWindow)
        else:
            tm.showerror("Login error", "Incorrect username or password")
        self.logbtn.config(command=lambda: self._login_btn_clicked(controller))