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
import datastore
import NanoZND
import random
import io
import pickle

SM = SecurityManager.SecurityManager()
BM = BatchManager.BatchManager()
NanoZND = NanoZND.NanoZND()
DS = datastore.DataStore()

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
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
        time_now = strftime("%H:%M:%p", gmtime())

        self.label_4.place(relx=0.59, rely=0.4, anchor=CENTER)
        self.entry_4.place(relx=0.45, rely=0.45, width=300, anchor="w")
        
        self.AW_addUsrBtn = ttk.Button(
            self, text='Add a new user', command=lambda: controller.show_frame(AddUserWindow))
        self.AW_addUsrBtn.place(relx=0.42, rely=0.65, anchor=CENTER)

        self.AW_editUsrBtn = ttk.Button(
            self, text='Edit a current user', command=lambda: controller.show_frame(EditUserWindow))
        self.AW_editUsrBtn.place(relx=0.62, rely=0.65, anchor=CENTER)
        
        self.AW_adminLogoutBtn = ttk.Button(
            self, text='Done', command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.AW_adminLogoutBtn.place(relx=0.8, rely=0.65, anchor=CENTER)
        
        self.browseBtn = ttk.Button(
            self, text="Browse", command=lambda: self._browse_btn_clicked(controller))
        self.browseBtn.grid(row=2, column=1)
        self.browseBtn.place(relx=0.8, rely=0.45, anchor=CENTER)
        self.bind('<Return>', self.update)
        
        self.label = ttk.Label(self, text="Probe re-program Off / On")
        self.label.place(relx=0.08, rely=0.42, anchor=CENTER)
        self.w2 = Scale(self, label="Off",from_=0, to=1, command=self.update ,orient=HORIZONTAL)
        self.w2.set(0)
        self.w2.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.w2.pack(side='left')
        
        if "AM" in time_now :
            self.text_area.insert('1.0','Good Morning ')
            
        else:
            self.text_area.insert('1.0','Good Afternoon ')
        
    def refresh_window(self):
           
        session_info = DS.get_user()
        
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0','end')
        self.text_area.insert('1.0',session_info[0])
        self.text_area.insert('2.0','\n\nPlease choose an option.')
        
        if self.w2.get() == 1:
            self.text_area.insert('4.0','\nProbe re-programming is enabled.')
        else:
            self.text_area.insert('4.0','\nProbe re-programming is disabled.')
        self.text_area.config(state=DISABLED)
        Tk.update(self) 
         
    def update(self, controller):
        admin_data = str([self.w2.get()])
        
       
        DS.write_to_admin_file(admin_data)
        
        # admin_data.append(self.w2.get())
        
        # with open('file.admin', 'wb') as file:
      
        #     # Call load method to deserialze
        #     pickle.dump(admin_data,file)
        # file.close()
        # DS.write_to_admin_file(admin_data)
        
        self.text_area.config(state=NORMAL)
        self.text_area.delete('4.0','end')
        if self.w2.get() == 1:
            self.text_area.insert('4.0','\nProbe re-programming is enabled.')
          
        else:
            self.text_area.insert('4.0','\nProbe re-programming is disabled.')
        self.text_area.config(state=DISABLED)
     
        
    def _browse_btn_clicked(self, controller):
        filename = filedialog.askopenfilenames(initialdir = "/",title = "Select file",
                                               filetypes = ((".csv files","*.csv"),
                                                            ("all files","*.*")))     
        NanoZND.SetFileLocation(filename)
        self.file = NanoZND.GetFileLocation()   
        

class ChangePasswordWindow(tk.Frame):
    def __init__(self, parent, controller):
        self.newPassword = StringVar()
        self.confirmPassword = StringVar()
        self.name = ""

        tk.Frame.__init__(self, parent, bg='#FFDAB9')
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)

        self.CPWl1 = ttk.Label(self, text='Enter a new password')
        self.CPWl1.place(relx=0.35, rely=0.3, anchor=CENTER)
        
        self.CPWl1 = ttk.Label(self, text='Confirm new password')
        self.CPWl1.place(relx=0.35, rely=0.35, anchor=CENTER)

        self.CPWe1 = ttk.Entry(self, textvariable=self.newPassword, show="*", font="bold")
        self.CPWe1.place(relx=0.65, rely=0.3, anchor=CENTER)
        
        self.CPWe1 = ttk.Entry(self, textvariable=self.confirmPassword, show="*", font="bold")
        self.CPWe1.place(relx=0.65, rely=0.35, anchor=CENTER)

        self.confm_btn = ttk.Button(
            self, text='Confirm', command=lambda: self.confm_btn_clicked(controller))
        self.confm_btn.place(relx=0.5, rely=0.6, anchor=CENTER)
        
        self.confm_btn = ttk.Button(
            self, text='Back', command=lambda: controller.show_frame(EditUserWindow))
        self.confm_btn.place(relx=0.65, rely=0.6, anchor=CENTER)
        
    def refresh_window(self):
        # create a list of the current users using the dictionary of users
        # with open('file.ptt', 'rb') as file:
        # # Call load method to deserialze
        #     session_info = pickle.load(file)
        # file.close()
        session_info = DS.get_user()
        
        # with open('file.admin', 'rb') as fileAd:
        #     myAdmin = pickle.load(fileAd)
        #     self.name = myAdmin[1]
        # fileAd.close()
        my_admin = DS.get_admin()
        self.name = my_admin[1]
        
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0','end')
        self.text_area.insert('1.0',session_info[0])
        self.text_area.insert('2.0','\nChange ' + self.name + "'s password.")
        self.text_area.config(state=DISABLED)

    def confm_btn_clicked(self, controller):
        if self.newPassword.get() == self.confirmPassword.get():
            # SM.editingUser.password = self.newPassword.get()
            user = SM.GetUserObject(self.name)
            SM.updatePassword(user)
            tm.showinfo('Changed password', 'Password change successful')
            controller.show_frame(EditUserWindow)
        else:
            self.text_area.config(state=NORMAL)
            self.text_area.insert('3.3','\nPlease check password spelling,\nthey are not the same.')
            self.text_area.config(state=DISABLED)
        
        
class EditUserWindow(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent, bg='#FFDAB9')
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)

        self.Label1 = ttk.Label(self, text='Choose a user to edit')
        self.Label1.place(relx=0.5, rely=0.07, anchor=CENTER)

        self.userListBox = Listbox(self, height=15, width=20)
        self.userListBox.place(relx=0.3, rely=0.5, anchor=CENTER)

        self.CngPWrd_btn = ttk.Button(
            self, text='Change password', command=lambda: self._getSelectedUser(controller))
        self.CngPWrd_btn.place(relx=0.6, rely=0.35, anchor=CENTER)

        self.delUsr_btn = ttk.Button(
            self, text='Delete', command=lambda: self._delUsr_btn_clicked(controller))
        self.delUsr_btn.place(relx=0.6, rely=0.45, anchor=CENTER)

        self.finished_btn = ttk.Button(
            self, text='Done', command=lambda: controller.show_frame(AdminWindow))
        self.finished_btn.place(relx=0.6, rely=0.55, anchor=CENTER)
        
    def _getSelectedUser(self, controller):
        update_file = []
        selectedId = self.userListBox.curselection()
        selectedUser = self.userListBox.get(selectedId[0])
        
        # Get admin file
        # with open('file.admin', 'rb') as fileAd:
        #     myAdmin = pickle.load(fileAd)
        # fileAd.close()
        my_admin = DS.get_admin()
        # Update admin file
        update_file.extend(my_admin)
        update_file.append(selectedUser)
        # Save new admin file with selected user to edit
        # with open('file.admin', 'wb') as file:
        #     pickle.dump(updateFile,file)
        # file.close()
        DS.add_to_admin_file(update_file)

        controller.show_frame(ChangePasswordWindow)

    def _delUsr_btn_clicked(self, controller):
        self.delUsr_btn.config(command=ignore)
        self.finished_btn.config(command=ignore)
        self.CngPWrd_btn.config(command=ignore)
        
        # with open('file.ptt', 'rb') as file:
        # # Call load method to deserialze
        #     session_info = pickle.load(file)
        # file.close()
        session_info = DS.get_user()
        
        lstid = self.userListBox.curselection()
        lstUsr = self.userListBox.get(lstid[0])
        if "--> Admin" in lstUsr:
            delete_user = lstUsr[:-9]
        else:
            delete_user = lstUsr
        sure = tm.askyesno(
                'Delete confirm', 'Are you sure you want to Delete this user?')
        
        try:
            if sure == True:
                if lstUsr != session_info[0]:
                    
                    SM.delete_user(SM.GetUserObject(delete_user))
                    self.refresh_window()
                else:
                    tm.showerror('Error', 'Cannot delete yourself')
        except:
            tm.showerror('Error', 'User not found')
        

        self.delUsr_btn.config(
            command=lambda: self._delUsr_btn_clicked(controller))
        self.finished_btn.config(
            command=lambda: controller.show_frame(AdminWindow))
        self.CngPWrd_btn.config(
            command=lambda: self._cngPwrd_btn_clicked(controller))

    def refresh_window(self):
        # create a list of the current users using the dictionary of users
        # with open('file.ptt', 'rb') as file:
        # # Call load method to deserialze
        #     session_info = pickle.load(file)
        # file.close()
        
        session_info = DS.get_user()
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0','end')
        self.text_area.insert('1.0',session_info[0])
        self.text_area.insert('2.0','\n\nPlease choose an option.')
        self.text_area.config(state=DISABLED)
        userList = []
        
        for item in SM.GetUserList():
            
            if item.admin == True:
                item.name = item.name + "--> Admin"
    
            userList.append(item.name)   
         

        # clear the listbox
        self.userListBox.delete(0, END)

        # fill the listbox with the list of users
        for item in userList:
            self.userListBox.insert(END, item)
        # Getting the selected user
        self.userListBox.select_set(0)
        
            
            
class AddUserWindow(tk.Frame):
    def __init__(self, parent, controller):
        # add User screen
        tk.Frame.__init__(self, parent, bg='#FFDAB9')

        self.newusername = StringVar()
        self.newpassword = StringVar()
        self.confpassword = StringVar()
        self.is_admin = StringVar()
        self.allow_add_admin = False
        self.allow_add = True
        self._setDefaults()
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
        self.text_area.config(state=NORMAL)
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)

        self.AUWl1 = ttk.Label(self, text='New user name: ')
        self.AUWl2 = ttk.Label(self, text='Enter Password: ')
        self.AUWl3 = ttk.Label(self, text='Confirm Password: ')
        #self.AUWl3 = ttk.Label(self.AUW, text='Admin: ')
        self.AUWe1 = ttk.Entry(self, textvariable=self.newusername)
        self.AUWe2 = ttk.Entry(self, textvariable=self.newpassword, show="*", font="bold")
        self.AUWe3 = ttk.Entry(self, textvariable=self.confpassword, show="*", font="bold")

        self.rb1 = ttk.Radiobutton(
            self, text='Admin', variable=self.is_admin, value='true')
        self.rb1.place(relx=0.5, rely=0.55, anchor=CENTER)
        self.rb2 = ttk.Radiobutton(
            self, text='Non-Admin', variable=self.is_admin, value='false')
        self.rb2.place(relx=0.5, rely=0.65, anchor=CENTER)

        self.AUWl1.place(relx=0.4, rely=0.25, anchor=CENTER)
        self.AUWl2.place(relx=0.4, rely=0.35, anchor=CENTER)
        self.AUWe1.place(relx=0.6, rely=0.25, anchor=CENTER)
        self.AUWe2.place(relx=0.6, rely=0.35, anchor=CENTER)
        self.AUWl3.place(relx=0.4, rely=0.4, anchor=CENTER)
        self.AUWe3.place(relx=0.6, rely=0.4, anchor=CENTER)

        self.confm_btn = ttk.Button(
            self, text="Confirm", command=lambda: self._confm_btn_clicked(controller))
        self.confm_btn.place(relx=0.4, rely=0.8, anchor=CENTER)

        self.cancl_btn = ttk.Button(
            self, text="Cancel", command=lambda: controller.show_frame(AdminWindow))
        self.cancl_btn.place(relx=0.6, rely=0.8, anchor=CENTER)

    def _confm_btn_clicked(self, controller):
        self.confm_btn.config(command=ignore)
        self.cancl_btn.config(command=ignore)
        self.text_area.config(state=NORMAL)
        if self.newpassword.get() == self.confpassword.get():
                
            # create user object
            if self.isAdmin.get() == 'false':
                admin = False
            else:
                admin = True
                
            newUser = User(self.newusername.get(), self.newpassword.get(), admin)
            
            if self.isAdmin.get() == 'true' and self.allow_add_admin == False:
                admin = False
                self.textArea.insert('4.30','\nThere are 2 administrators already,\nNo nore allowed')

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
        else:
            self.text_area.insert('3.3','\nPlease check password spelling,\nthey are not the same.')
        self.text_area.config(state=DISABLED)
        
    def refresh_window(self):
         # create a list of the current users using the dictionary of users
        
        # with open('file.ptt', 'rb') as file:
        # # Call load method to deserialze
        #     session_info = pickle.load(file)
        # file.close()
        session_info = DS.get_user()
    
        self.text_area.delete('1.0','end')
        self.text_area.insert('1.0',session_info[0])
        self.text_area.insert('2.0','\n\nPlease complete the form.')
        self.allow_add_admin = True
        admins = 0
        admin_names = []
        for item in SM.GetUserList():
            if item.admin == True:
                admin_names.append(item)
        admins = len(admin_names)
        
        if admins >= 2:
            self.allow_add_admin = False
        

    def _setDefaults(self):
        self.is_admin.set('false')
        self.newusername.set("")
        self.newpassword.set("")