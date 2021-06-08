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
from time import gmtime, strftime
import Sessions as SE
import NanoZND
import io
import pickle

SM = SecurityManager.SecurityManager()
BM = BatchManager.BatchManager()
NanoZND = NanoZND.NanoZND()

def ignore():
    return 'break'

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
        
        self.textArea = tk.Text(self, height=5, width=38)
        self.textArea.place(relx=0.25, rely=0.15, anchor=CENTER)
        timeNow = strftime("%H:%M:%p", gmtime())

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
        if "AM" in timeNow :
            self.textArea.insert('1.0','Good Morning ', font=('bold',12))
            
        else:
            self.textArea.insert('1.0','Good Afternoon ')
        
    def refresh_window(self):
           
       # Open the file in binary mode
        with open('file.ptt', 'rb') as file:
        # Call load method to deserialze
            session_info = pickle.load(file)
        file.close()
        self.textArea.insert('2.0',session_info[0])
        self.textArea.insert('3.3','\n\nPlease choose an option.')
        self.textArea.config(state=DISABLED)
         
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
        

class ChangePasswordWindow(tk.Frame):
    def __init__(self, parent, controller):
        self.newPassword = StringVar()

        tk.Frame.__init__(self, parent)
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        

        self.CPWl1 = ttk.Label(self, text='Enter a new password')
        self.CPWl1.place(relx=0.35, rely=0.3, anchor=CENTER)

        self.CPWe1 = ttk.Entry(self, textvariable=self.newPassword)
        self.CPWe1.place(relx=0.65, rely=0.3, anchor=CENTER)

        self.confm_btn = ttk.Button(
            self, text='Confirm', command=lambda: self.confm_btn_clicked(controller))
        self.confm_btn.place(relx=0.5, rely=0.6, anchor=CENTER)

    def confm_btn_clicked(self, controller):
        SM.editingUser.password = self.newPassword.get()
        SM.updatePassword(SM.editingUser)
        tm.showinfo('Changed password', 'Password change successful')
        controller.show_frame(EditUserWindow)
        
class EditUserWindow(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent, bg='#FFDAB9')
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)

        self.Label1 = ttk.Label(self, text='Choose a user to edit')
        self.Label1.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.userListBox = Listbox(self, height=15, width=20)
        self.userListBox.place(relx=0.3, rely=0.4, anchor=CENTER)

        self.CngPWrd_btn = ttk.Button(
            self, text='Change password', command=lambda: self._cngPwrd_btn_clicked(controller))
        self.CngPWrd_btn.place(relx=0.6, rely=0.25, anchor=CENTER)

        self.delUsr_btn = ttk.Button(
            self, text='Delete', command=lambda: self._delUsr_btn_clicked(controller))
        self.delUsr_btn.place(relx=0.6, rely=0.35, anchor=CENTER)

        self.finished_btn = ttk.Button(
            self, text='Done', command=lambda: controller.show_frame(AdminWindow))
        self.finished_btn.place(relx=0.6, rely=0.45, anchor=CENTER)

        self.refresh_window()

    def _cngPwrd_btn_clicked(self, controller):
        
        lstid = self.userListBox.curselection()
        lstUsr = self.userListBox.get(lstid[0])
        SM.editingUser = SM.GetUserObject(lstUsr)
        self.newPassword = StringVar()
        
        

        self.CPWl1 = ttk.Label(self, text='Enter a new password')
        self.CPWl1.place(relx=0.3, rely=0.7, anchor=CENTER)

        self.CPWe1 = ttk.Entry(self, textvariable=self.newPassword)
        self.CPWe1.place(relx=0.55, rely=0.7, anchor=CENTER)

        self.confm_btn = ttk.Button(
            self, text='Confirm', command=lambda: self.change_btn_clicked(controller))
        self.confm_btn.place(relx=0.4, rely=0.8, anchor=CENTER)
        
    def change_btn_clicked(self, controller):
        SM.editingUser.password = self.newPassword.get()
        SM.updatePassword(SM.editingUser)
        tm.showinfo('Changed password', 'Password change successful')
        controller.show_frame(EditUserWindow)

    def confm_btn_clicked(self, controller):
        SM.editingUser.password = self.newPassword.get()
        SM.updatePassword(SM.editingUser)
        tm.showinfo('Changed password', 'Password change successful')
        controller.show_frame(EditUserWindow)

    def _delUsr_btn_clicked(self, controller):
        self.delUsr_btn.config(command=ignore)
        self.finished_btn.config(command=ignore)
        self.CngPWrd_btn.config(command=ignore)

        try:
            lstid = self.userListBox.curselection()
            lstUsr = self.userListBox.get(lstid[0])
            sure = tm.askyesno(
                'Delete confirm', 'Are you sure you want to Delete this user?')
            if sure == True:
                if lstUsr != SM.loggedInUser.name:
                    SM.deleteUser(SM.GetUserObject(lstUsr))
                    self.refresh_window()
                else:
                    tm.showerror('Error', 'Cannot delete yourself')
        except:
            pass

        self.delUsr_btn.config(
            command=lambda: self._delUsr_btn_clicked(controller))
        self.finished_btn.config(
            command=lambda: controller.show_frame(AdminWindow))
        self.CngPWrd_btn.config(
            command=lambda: self._cngPwrd_btn_clicked(controller))

    def refresh_window(self):
        # create a list of the current users using the dictionary of users
        userList = []
        for item in SM.GetUserList():
            userList.append(item.name)

        # clear the listbox
        self.userListBox.delete(0, END)

        # fill the listbox with the list of users
        for item in userList:
            self.userListBox.insert(END, item)
            
            
class AddUserWindow(tk.Frame):
    def __init__(self, parent, controller):
        # add User screen
        tk.Frame.__init__(self, parent, bg='#FFDAB9')

        self.newusername = StringVar()
        self.newpassword = StringVar()
        self.isAdmin = StringVar()

        self._setDefaults()
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)

        self.AUWl1 = ttk.Label(self, text='New user name: ')
        self.AUWl2 = ttk.Label(self, text='Password: ')
        #self.AUWl3 = ttk.Label(self.AUW, text='Admin: ')
        self.AUWe1 = ttk.Entry(self, textvariable=self.newusername)
        self.AUWe2 = ttk.Entry(self, textvariable=self.newpassword)

        self.rb1 = ttk.Radiobutton(
            self, text='Admin', variable=self.isAdmin, value='true')
        self.rb1.place(relx=0.5, rely=0.45, anchor=CENTER)
        self.rb2 = ttk.Radiobutton(
            self, text='Non-Admin', variable=self.isAdmin, value='false')
        self.rb2.place(relx=0.5, rely=0.55, anchor=CENTER)

        self.AUWl1.place(relx=0.4, rely=0.25, anchor=CENTER)
        self.AUWl2.place(relx=0.4, rely=0.35, anchor=CENTER)
        self.AUWe1.place(relx=0.6, rely=0.25, anchor=CENTER)
        self.AUWe2.place(relx=0.6, rely=0.35, anchor=CENTER)

        self.confm_btn = ttk.Button(
            self, text="Confirm", command=lambda: self._confm_btn_clicked(controller))
        self.confm_btn.place(relx=0.4, rely=0.8, anchor=CENTER)

        self.cancl_btn = ttk.Button(
            self, text="Cancel", command=lambda: controller.show_frame(AdminWindow))
        self.cancl_btn.place(relx=0.6, rely=0.8, anchor=CENTER)

    def _confm_btn_clicked(self, controller):
        self.confm_btn.config(command=ignore)
        self.cancl_btn.config(command=ignore)

        # create user object
        admin = False
        if self.isAdmin.get() == 'true':
            admin = True
        newUser = User(self.newusername.get(), self.newpassword.get(), admin)

        # try adding it to the list of users
        if SM.addUser(newUser):
            tm.showinfo('New User', 'New user added')
            self._setDefaults()
            controller.show_frame(AdminWindow)
        else:
            tm.showerror('Error', 'User already exsists')
        self.confm_btn.config(
            command=lambda: self._confm_btn_clicked(controller))
        self.cancl_btn.config(
            command=lambda: controller.show_frame(AdminWindow))

    def _setDefaults(self):
        self.isAdmin.set('false')
        self.newusername.set("")
        self.newpassword.set("")