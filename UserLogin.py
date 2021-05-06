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
import io
import pickle

SM = SecurityManager.SecurityManager()
BM = BatchManager.BatchManager()


def ignore():
    return 'break'



class LogInWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        self.currentUser = StringVar()
        cUser = ""

        self.label_1 = ttk.Label(self, text="Username")
        self.label_2 = ttk.Label(self, text="Password")

        self.entry_1 = ttk.Entry(self, textvariable=self.currentUser ,font="bold")
        self.entry_2 = ttk.Entry(self, show="*", font="bold")
        self.entry_1.insert(END, 'Jack')
        cUser = str(self.currentUser.get())
        self.entry_2.insert(END, 'password')

        self.label_1.place(relx=0.4, rely=0.3, anchor=CENTER)
        self.label_2.place(relx=0.4, rely=0.4, anchor=CENTER)
        self.entry_1.place(relx=0.6, rely=0.3, anchor=CENTER)
        self.entry_2.place(relx=0.6, rely=0.4, anchor=CENTER)

        self.logbtn = ttk.Button(
            self, text="Login", width=20,command=lambda: self._login_btn_clicked(controller))
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
            controller.show_frame(SE.SessionSelectWindow)
        else:
            tm.showerror("Login error", "Incorrect username or password")
        self.logbtn.config(command=lambda: self._login_btn_clicked(controller))
        
        


class AdminWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#FFDAB9')

        self.AW_addUsrBtn = ttk.Button(
            self, text='Add a new user', command=lambda: controller.show_frame(AddUserWindow))
        self.AW_addUsrBtn.place(relx=0.3, rely=0.5, anchor=CENTER)

        self.AW_editUsrBtn = ttk.Button(
            self, text='Edit a current user', command=lambda: controller.show_frame(EditUserWindow))
        self.AW_editUsrBtn.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.AW_adminLogoutBtn = ttk.Button(
            self, text='Done', command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.AW_adminLogoutBtn.place(relx=0.7, rely=0.5, anchor=CENTER)
            
   
    
      
        
class EditUserWindow(tk.Frame):
    def __init__(self, controller):
        
        tk.Frame.__init__(self, bg='#FFDAB9')

        self.Label1 = ttk.Label(self, text='Choose a user to edit')
        self.Label1.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.userListBox = Listbox(self, height=15, width=20)
        self.userListBox.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.CngPWrd_btn = ttk.Button(
            self, text='Change password', command=lambda: self._cngPwrd_btn_clicked(controller))
        self.CngPWrd_btn.place(relx=0.8, rely=0.35, anchor=CENTER)

        self.delUsr_btn = ttk.Button(
            self, text='Delete', command=lambda: self._delUsr_btn_clicked(controller))
        self.delUsr_btn.place(relx=0.8, rely=0.5, anchor=CENTER)

        self.finished_btn = ttk.Button(
            self, text='Done', command=lambda: controller.show_frame(AdminWindow))
        self.finished_btn.place(relx=0.5, rely=0.9, anchor=CENTER)

        self.refresh_window()

    def _cngPwrd_btn_clicked(self, controller):
        lstid = self.userListBox.curselection()
        lstUsr = self.userListBox.get(lstid[0])
        SM.editingUser = SM.GetUserObject(lstUsr)
        self.newPassword = StringVar()

        self.CPWl1 = ttk.Label(self, text='Enter a new password')
        self.CPWl1.place(relx=0.35, rely=0.3, anchor=CENTER)

        self.CPWe1 = ttk.Entry(self, textvariable=self.newPassword)
        self.CPWe1.place(relx=0.65, rely=0.3, anchor=CENTER)

        self.confm_btn = ttk.Button(
            self, text='Confirm', command=lambda: self.change_btn_clicked(controller))
        self.confm_btn.place(relx=0.5, rely=0.6, anchor=CENTER)
        
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
            
            
class ChangePasswordWindow(tk.Frame):
    def __init__(self, parent, controller):
        self.newPassword = StringVar()

        tk.Frame.__init__(self, parent)

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
        
        
class AddUserWindow(tk.Frame):
    def __init__(self, parent, controller):
        # add User screen
        tk.Frame.__init__(self, parent)

        self.newusername = StringVar()
        self.newpassword = StringVar()
        self.isAdmin = StringVar()

        self._setDefaults()

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
        
        

            
            
        