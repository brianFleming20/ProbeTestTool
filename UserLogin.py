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
        self.login_btn = (PhotoImage(file="login_btn.gif"))
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        self.title = (PhotoImage(file="title.gif"))
        self.label_4 = ttk.Label(self, image=self.title)
        self.label_4.place(relx=0.5, rely=0.1, anchor=CENTER)

       
        self.label_5 = ttk.Label(self, text="Good morning.", font=("bold", 20))
        self.label_6 = ttk.Label(self, text="Good afternoon.", font=("bold", 20))
        time_now = strftime("%H:%M:%p", gmtime())
        DS.write_to_from_keys("  ")
  
      

        self.logbtn = ttk.Button(
            self, text="Login",image=self.login_btn, width=20,command=lambda: 
                [self.canvas_name.destroy(),self.canvas_pass.destroy(),self._login_btn_clicked(controller)])
        self.logbtn.place(relx=0.88, rely=0.5 ,anchor=CENTER)
       
        
        ttk.Button(self, text="Exit", width=20,command=lambda: self.quit(controller)).place(relx=0.88, rely=0.65 ,anchor=CENTER)
        self.bind('<Return>', lambda event: self._login_btn_clicked)
       
        if "AM" in time_now :
            self.label_5.place(relx=0.5, rely=0.25, anchor=CENTER)
            
        else:
            self.label_6.place(relx=0.5, rely=0.25, anchor=CENTER)
          
        
        
    def refresh_window(self):
        self.current_user = "brian"
        self.password = "password"
        
        # self.current_user.set("|")
       
        self.canvas_name = Canvas(bg="#eae9e9",width=400, height=40)
        self.canvas_name.place(x=350, y=225)
        self.canvas_pass = Canvas(bg="#eae9e9",width=400, height=40)
        self.canvas_pass.place(x=350, y=300)
        self.btn_1 = ttk.Button(self.canvas_name, text='Username', command=lambda: 
            [self.get_keys(),self.name_entry()], width=20)
        self.btn_2 = ttk.Button(self.canvas_pass, text='Password', command=lambda: 
            [self.get_keys(),self.password_entry()], width=20)
        self.name_text = self.canvas_name.create_text(220,20,text=" ",fill="black",font=(OnScreenKeys.FONT_NAME, 16, "bold"))
        self.pass_text = self.canvas_pass.create_text(220,20,text=" ",fill="black",font=(OnScreenKeys.FONT_NAME, 14, "bold"))
      
        
       
        self.btn_1.place(relx=0.2, rely=0.2, anchor=N)
        self.btn_2.place(relx=0.2, rely=0.2, anchor=N)
        
        
        
        
    def name_entry(self):
        self.current_user = ""
        pass_block = False
        data = self.wait_for_response(self.canvas_name,  pass_block)
        self.current_user = data
        self.btn_1.config(state=NORMAL)
        self.btn_2.config(state=NORMAL)
        # DS.write_to_from_keys(data)
    
        
        
    def password_entry(self):
        self.password = ""
        pass_block = True
        data = self.wait_for_response(self.canvas_pass, pass_block)  
        self.password = data
        self.btn_1.config(state=NORMAL)
        self.btn_2.config(state=NORMAL)
        
        
        # print(f"password is {self.password}")
        



    def _login_btn_clicked(self, controller):
        self.logbtn.config(command=ignore)
    
        DS.write_to_user_file([""])
        DS.write_to_batch_file([""])
        DS.write_to_admin_file('0')

        # create a user object from the users input
        username = self.current_user
        password = self.password
        user = User(username, password)
          
     
        if SM.logIn(user):
                controller.show_frame(SE.SessionSelectWindow)
        else:
            tm.showerror("Login error", "Incorrect username or password")
           
            self.refresh_window()
        self.logbtn.config(command=lambda: self.refresh_window())
            
            
    def quit(self, controller):
        shut = tm.askyesno("Shutting Down","Do you wish to proceed?")
        if shut:
            self.canvas_name.destroy()
            self.canvas_pass.destroy()
            controller.destroy()
            
            
    def wait_for_response(self, master, pass_block):
        block = pass_block
        DS.write_to_from_keys(" ")
        password_blank = "*********************"
        # pw_data = DS.get_keyboard_data()
        while 1:
            pw_data = DS.get_keyboard_data()
            pw_len = len(pw_data)
            if pw_data[-1] == "+":
                pw_data = pw_data[:-1]
                break 
            if block:
                
                # self.label2=ttk.Label(master, text=password_blank[:pw_len], font=("bold", 15)).place(relx=0.7, rely=0.3, width=150,anchor=N)
                self.canvas_pass.itemconfig(self.pass_text, text=password_blank[:pw_len])
            else:
                self.canvas_name.itemconfig(self.name_text, text=pw_data)
                
                # self.label1=ttk.Label(master, text=pw_data, font=("bold", 15)).place(relx=0.7, rely=0.3, width=150,anchor=N)
            Tk.update(master)
        return pw_data
        
    def get_keys(self):
      
        KY.display()
        
        self.btn_1.config(state=DISABLED)
        self.btn_2.config(state=DISABLED)

        