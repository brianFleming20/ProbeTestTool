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
from tkinter import filedialog
import SecurityManager
from SecurityManager import User
import BatchManager
import Sessions as SE
import AdminUser as AU
import NanoZND
import sys
import io
import pickle
from time import gmtime, strftime

SM = SecurityManager.SecurityManager()
BM = BatchManager.BatchManager()
NanoZND = NanoZND.NanoZND()

def ignore():
    return 'break'



class LogInWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        self.current_user = StringVar()
        c_user = ""
        
        self.login_btn = (PhotoImage(file="login_btn.gif"))
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        self.title = (PhotoImage(file="title.gif"))
        self.label_4 = ttk.Label(self, image=self.title)
        self.label_4.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.label_1 = ttk.Label(self, text="Username")
        self.label_2 = ttk.Label(self, text="Password")
        self.label_5 = ttk.Label(self, text="Good morning.", font=("bold", 20))
        self.label_6 = ttk.Label(self, text="Good afternoon.", font=("bold", 20))
        time_now = strftime("%H:%M:%p", gmtime())
        
       

        self.entry_1 = ttk.Entry(self, textvariable=self.current_user ,font="bold")
        self.entry_2 = ttk.Entry(self, show="*", font="bold")
        self.entry_1.insert(END, 'Jon')
        c_user = str(self.current_user.get())
        self.entry_2.insert(END, 'Batman')

        self.label_1.place(relx=0.4, rely=0.4, anchor=CENTER)
        self.label_2.place(relx=0.4, rely=0.5, anchor=CENTER)
        self.entry_1.place(relx=0.6, rely=0.4, anchor=CENTER)
        self.entry_2.place(relx=0.6, rely=0.5, anchor=CENTER)

        self.logbtn = ttk.Button(
            self, text="Login",image=self.login_btn, width=20,command=lambda: self._login_btn_clicked(controller))
        self.logbtn.place(relx=0.5, rely=0.75 ,anchor=CENTER)
        ttk.Button(self, text="Exit", width=20,command=lambda: self.quit()).place(relx=0.7, rely=0.75 ,anchor=CENTER)
        
        self.bind('<Return>', lambda: self._login_btn_clicked(controller))
        with open('file.ptt','wb') as file:
            pickle.dump([],file)
        file.close()
        
        with open('file_batch','wb') as file:
            pickle.dump([],file)
        file.close()
        
        with open('file.admin', 'wb') as file:
            
            # Call load method to deserialze
            pickle.dump(['0'],file)
        file.close()
        
        
        if "AM" in time_now :
            self.label_5.place(relx=0.5, rely=0.25, anchor=CENTER)
            
        else:
            self.label_6.place(relx=0.5, rely=0.25, anchor=CENTER)
            
        
        self.entry_1.focus_set()
        
        
        

    def _login_btn_clicked(self, controller):
        self.logbtn.config(command=ignore)
        
        if '(' in self.entry_1.get() or ')' in self.entry_1.get() or '(' in self.entry_2.get() or ')' in self.entry_2.get():
            tm.showerror("Login error", "Incorrect characters used.")
        else:
             # create a user object from the users input
            username = self.entry_1.get()
            password = self.entry_2.get()
            user = User(username, password)
                
        
            #self.entry_1.delete(0, 'end')
            self.entry_2.delete(0, 'end')
            # check to see if the details are valid
            
            if SM.logIn(user):
                controller.show_frame(SE.SessionSelectWindow)
            else:
                tm.showerror("Login error", "Incorrect username or password")
            self.logbtn.config(command=lambda: self._login_btn_clicked(controller))
            
    def quit(self):
        quit()
        
        


 
        
        
        
       
   
    
      
        

            

        
        

        

        
        
        
            

            
            
        