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
import NanoZND
import io
import pickle
from PIL import Image, ImageTk

SM = SecurityManager.SecurityManager()
BM = BatchManager.BatchManager()
NanoZND = NanoZND.NanoZND()

def ignore():
    return 'break'



class LogInWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        self.currentUser = StringVar()
        cUser = ""
        
        self.login_btn = (PhotoImage(file="login_btn.gif"))
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        self.title = (PhotoImage(file="title.gif"))
        self.label_4 = ttk.Label(self, image=self.title)
        self.label_4.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.label_1 = ttk.Label(self, text="Username")
        self.label_2 = ttk.Label(self, text="Password")
       

        self.entry_1 = ttk.Entry(self, textvariable=self.currentUser ,font="bold")
        self.entry_2 = ttk.Entry(self, show="*", font="bold")
        self.entry_1.insert(END, 'Jack')
        cUser = str(self.currentUser.get())
        self.entry_2.insert(END, 'password')

        self.label_1.place(relx=0.4, rely=0.4, anchor=CENTER)
        self.label_2.place(relx=0.4, rely=0.5, anchor=CENTER)
        self.entry_1.place(relx=0.6, rely=0.4, anchor=CENTER)
        self.entry_2.place(relx=0.6, rely=0.5, anchor=CENTER)

        self.logbtn = ttk.Button(
            self, text="Login",image=self.login_btn, width=20,command=lambda: self._login_btn_clicked(controller))
        self.logbtn.place(relx=0.5, rely=0.75 ,anchor=CENTER)
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
            controller.show_frame(SE.SessionSelectWindow)
        else:
            tm.showerror("Login error", "Incorrect username or password")
        self.logbtn.config(command=lambda: self._login_btn_clicked(controller))
        
        


class AdminWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#FFDAB9')
        self.file = StringVar()
        self.file.set(NanoZND.GetFileLocation())
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        self.label_4 = ttk.Label(self, text="NanoZND file storage location")
        self.entry_4 = ttk.Entry(self, textvariable=self.file)

        self.AW_addUsrBtn = ttk.Button(
            self, text='Add a new user', command=lambda: controller.show_frame(AddUserWindow))
        self.AW_addUsrBtn.place(relx=0.42, rely=0.5, anchor=CENTER)

        self.AW_editUsrBtn = ttk.Button(
            self, text='Edit a current user', command=lambda: controller.show_frame(EditUserWindow))
        self.AW_editUsrBtn.place(relx=0.62, rely=0.5, anchor=CENTER)
        self.label_4.place(relx=0.18, rely=0.7, anchor=CENTER)
        self.entry_4.place(relx=0.3, rely=0.7, width=300, anchor="w")
        
        self.browseBtn = ttk.Button(
            self, text="Browse", command=lambda: self._browse_btn_clicked(controller))
        self.browseBtn.grid(row=2, column=1)
        self.browseBtn.place(relx=0.8, rely=0.7, anchor=CENTER)
        self.bind('<Return>', self.update)
        
        self.label = ttk.Label(self, text="Probe re-program Off / On")
        self.label.place(relx=0.05, rely=0.42, anchor=CENTER)
        self.w2 = Scale(self, label="Off",from_=0, to=1, command= self.update ,orient=HORIZONTAL)
        self.w2.set(0)
        self.w2.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.w2.pack(side=LEFT)
        

        self.AW_adminLogoutBtn = ttk.Button(
            self, text='Done', command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.AW_adminLogoutBtn.place(relx=0.8, rely=0.5, anchor=CENTER)
        
        
         
    def update(self, controller):
        batch_data = [self.w2.get()]
        
        with open('file.admin', 'wb') as file:
      
            # Call load method to deserialze
            pickle.dump(batch_data,file)
        file.close()
        
        batch_data.append(self.w2.get())
        
        with open('file.admin', 'wb') as file:
      
            # Call load method to deserialze
            pickle.dump(batch_data,file)
        file.close()
        
    def _browse_btn_clicked(self, controller):
        filename = filedialog.askopenfilenames(initialdir = "/",title = "Select file",
                                               filetypes = ((".csv files","*.csv"),
                                                            ("all files","*.*")))     
        NanoZND.SetFileLocation(filename)
        self.file = NanoZND.GetFileLocation()   
        
        
        
       
   
    
      
        

            

        
        

        

        
        
        
            

            
            
        