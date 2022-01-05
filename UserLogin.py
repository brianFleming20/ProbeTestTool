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
import BatchManager
import Sessions as SE
import datastore
import OnScreenKeys


from time import gmtime, strftime

SM = SecurityManager.SecurityManager()
BM = BatchManager.BatchManager()
DS = datastore.DataStore()
KY = OnScreenKeys.Keyboard()


def ignore():
    return 'break'

class LogInWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        self.current_user = StringVar()
        self.canvas_name = None
        self.canvas_pass = None
        self.login_btn = (PhotoImage(file="login_btn.gif"))
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        self.title = (PhotoImage(file="title.gif"))
        self.label_4 = ttk.Label(self, image=self.title)
        self.label_4.place(relx=0.5, rely=0.1, anchor=CENTER)

        # self.label_1 = ttk.Label(self, text="Username",width=40)
        # self.label_2 = ttk.Label(self, text="Password",width=40)
        self.label_5 = ttk.Label(self, text="Good morning.", font=("bold", 20))
        self.label_6 = ttk.Label(self, text="Good afternoon.", font=("bold", 20))
        time_now = strftime("%H:%M:%p", gmtime())
        DS.write_to_from_keys("  ")
        # self.current_user.set("Brian")
        # password = "********"
        
        # self.entry_1 = ttk.Label(text=self.current_user.get(), font=( "bold", 15))
        # self.entry_2 = ttk.Label(text=password, font=("bold", 15))

        # self.entry_1 = ttk.Entry(self, textvariable=self.current_user ,font="bold")
        # self.entry_2 = ttk.Entry(self, show="*", font="bold")
        # self.entry_1.insert(END, 'Jack')
        # self.entry_2.insert(END, 'password')

        # self.label_1.config(font=("Courier", 14))
        # self.label_2.config(font=("Courier", 14))
        # self.entry_1.config(font=("Courier", 14))
        # self.entry_2.config(font=("Courier", 14))
        # self.label_1.place(relx=0.55, rely=0.4, anchor=CENTER)
        # self.label_2.place(relx=0.55, rely=0.5, anchor=CENTER)
        # self.entry_1.place(relx=0.6, rely=0.4, anchor=CENTER)
        # self.entry_2.place(relx=0.6, rely=0.5, anchor=CENTER)
        
        # self.btn = ttk.Button(self, text="keyboard", command=lambda: 
        #     self.get_keys())
        # self.btn.place(relx=0.88, rely=0.75 ,anchor=CENTER)

        self.logbtn = ttk.Button(
            self, text="Login",image=self.login_btn, width=20,command=lambda: self._login_btn_clicked(controller))
        self.logbtn.place(relx=0.88, rely=0.5 ,anchor=CENTER)
       
        
        ttk.Button(self, text="Exit", width=20,command=lambda: self.quit(controller)).place(relx=0.88, rely=0.65 ,anchor=CENTER)
        self.bind('<Return>', lambda event: self._login_btn_clicked)
       
        if "AM" in time_now :
            self.label_5.place(relx=0.5, rely=0.25, anchor=CENTER)
            
        else:
            self.label_6.place(relx=0.5, rely=0.25, anchor=CENTER)
          
        
        
    def refresh_window(self):
        
        
        # self.current_user.set("|")
        
        self.canvas_name = Canvas(width=400, height=40)
        self.canvas_name.place(x=350, y=225)
        self.canvas_pass = Canvas(width=400, height=40)
        self.canvas_pass.place(x=350, y=300)
        self.label_1 = ttk.Button(self.canvas_name, text='Username', command=lambda: 
            [self.get_keys(),self.name_entry()], width=20)
        # self.label_1 = ttk.Label(canvas_name, text="Username",width=40)
        self.label_2 = ttk.Button(self.canvas_pass, text='Password', command=lambda: 
            [self.get_keys(),self.password_entry()], width=20)
        # self.label_2 = ttk.Label(canvas_pass, text="Password",width=40)
        self.label_1.place(relx=0.2, rely=0.2, anchor=N)
        self.label_2.place(relx=0.2, rely=0.2, anchor=N)
        
        
        
        
    def name_entry(self):
        
        data = DS.get_keyboard_data()
        while 1:
            data = DS.get_keyboard_data()
            
            if data[-1] == "+":
                self.label_1.config(state=NORMAL)
                self.label_2.config(state=NORMAL)
                data = data[:-1]
                break 
            self.entry_1 = ttk.Label(self.canvas_name,text=data, font=( "bold", 15))
            self.entry_1.place(relx=0.55, rely=0.2, anchor=N)
            Tk.update(self)
        self.current_user = data
   
        DS.write_to_from_keys(data)
    
        
        
    def password_entry(self):
        DS.write_to_from_keys(" ")
        self.password = ""
        password_blank = "*************************************"
        print(f"keys data {DS.get_keyboard_data()}")
        data = DS.get_keyboard_data()
        while True:
            data = DS.get_keyboard_data()
            pw_len = len(data)
            
            if data[-1] == "+":
                self.label_1.config(state=NORMAL)
                self.label_2.config(state=NORMAL)
                data = data[:-1]
                break
            
            self.entry_2 = ttk.Label(self.canvas_pass, text=password_blank[0:pw_len], font=("bold", 15))
            self.entry_2.place(relx=0.55, rely=0.58,anchor=N)
            Tk.update(self)
            
        self.password = data
        print(f"password is {self.password}")
        



    def _login_btn_clicked(self, controller):
        self.logbtn.config(command=ignore)
        blank_data = [""]
    
        DS.write_to_user_file(blank_data)
        DS.write_to_batch_file(blank_data)
        DS.write_to_admin_file('0')
        
        # create a user object from the users input
        username = self.current_user
        password = self.password
        user = User(username, password)
        self.canvas_name.destroy()
        self.canvas_pass.destroy()  
        Tk.update(self)
            
        if SM.logIn(user):
                controller.show_frame(SE.SessionSelectWindow)
        else:
            tm.showerror("Login error", "Incorrect username or password")
        self.logbtn.config(command=lambda: self.refresh_window())
            
            
    def quit(self, controller):
        shut = tm.askyesno("Shutting Down","Do you wish to proceed?")
        if shut:
            self.canvas_name.destroy()
            self.canvas_pass.destroy()
            controller.destroy()
        
    def get_keys(self):
      
        KY.display()
        
        self.label_1.config(state=DISABLED)
        self.label_2.config(state=DISABLED)

        