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
import tkinter.font as font
import tkinter.messagebox as tm
from tkinter import filedialog
import SecurityManager
from SecurityManager import User
import BatchManager
from time import gmtime, strftime
import Sessions as SE
import AdminPortControl as AP
import datastore
import NanoZND
import OnScreenKeys


SM = SecurityManager.SecurityManager()
BM = BatchManager.BatchManager()
ZND = NanoZND.NanoZND()
DS = datastore.DataStore()
KY = OnScreenKeys.Keyboard()

def ignore():
    return 'break'

class AdminWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#FFDAB9')
        self.file = StringVar()
        self.file.set(ZND.GetFileLocation())
        self.control = controller
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
     
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
        time_now = strftime("%H:%M:%p", gmtime())

        self.userListBox = Listbox(self, height=15, width=20)
        self.userListBox.place(relx=0.75, rely=0.5, anchor=CENTER)
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
        
      
        self.checked_state = IntVar()
    
    
        
        if "AM" in time_now :
            self.text_area.insert('1.0','Good Morning ')
            
        else:
            self.text_area.insert('1.0','Good Afternoon ')
        
    def canvas_gone(self):
        self.checkbutton.destroy()
        self.canvas.destroy() 
        
        
    def refresh_window(self):
           
        session_info = DS.get_user()
        # DS.write_to_admin_file(str([self.w2.get()]))
        DS.write_to_admin_file(str([self.checked_state.get()]))
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0','end')
        self.text_area.insert('1.0',session_info[0])
        self.text_area.insert('2.0','\n\nPlease choose an option.')
        
        # if self.w2.get() == 1:
        if self.checked_state.get() == 1:
            self.text_area.insert('4.0','\nProbe re-programming is enabled.')
        else:
            self.text_area.insert('4.0','\nProbe re-programming is disabled.')
        self.text_area.config(state=DISABLED)
        self.checkbutton = Checkbutton(text="Admin user- if checked. ", 
                                  variable=self.checked_state,command=self.update, font=("Courier",10))
                                  
        self.checked_state.get()
        self.checkbutton.place(relx=0.5, rely=0.42, anchor=CENTER)
        self.show_user_options()
        Tk.update(self) 
        
    def show_user_options(self):
        self.canvas = Canvas(bg="#eae9e9",width=250, height=150)
        self.canvas.place(x=100, y=250)
        self.AW_addUsrBtn = ttk.Button(
            self.canvas, text='Add a new user', command=lambda: [self.canvas_gone(),self.control.show_frame(AddUserWindow)])
        self.AW_addUsrBtn.place(relx=0.1, rely=0.1, anchor=W)

        self.AW_editUsrBtn = ttk.Button(
            self.canvas, text='Edit a current user', command=lambda: [self.canvas_gone(),self.control.show_frame(EditUserWindow)])
        self.AW_editUsrBtn.place(relx=0.1, rely=0.45, anchor=W)
        
        self.AW_editUsrBtn = ttk.Button(
            self.canvas, text='Edit a device port number', command=lambda: [self.canvas_gone(),self.control.show_frame(AP.AdminPorts)])
        self.AW_editUsrBtn.place(relx=0.1, rely=0.8, anchor=W)
        self.AW_adminLogoutBtn = ttk.Button(
            self, text='Done', width=30, command=lambda:
                [self.canvas_gone(),self.control.show_frame(SE.SessionSelectWindow)])
        self.AW_adminLogoutBtn.place(relx=0.8, rely=0.78, anchor=E)
        
        self.label_4 = ttk.Label(self, text="NanoZND file storage location")
        self.entry_4 = ttk.Entry(self, textvariable=self.file)
        self.label_4.place(relx=0.1, rely=0.7)
        self.entry_4.place(relx=0.1, rely=0.78, width=300)
        
        self.browseBtn = ttk.Button(
            self, text="Browse", command=lambda: self._browse_btn_clicked())
        self.browseBtn.place(relx=0.42, rely=0.78)
        

         
    def update(self):
        # admin_data = str([self.w2.get()])
        admin_data = str(self.checked_state.get())
       
        DS.write_to_admin_file(admin_data)
     
        self.text_area.config(state=NORMAL)
        self.text_area.delete('4.0','end')
        # if self.w2.get() == 1:
        if self.checked_state.get() == 1:
            self.text_area.insert('4.0','\nProbe re-programming is enabled.')
            # DS.write_to_admin_file(str([self.w2.get()]))
            DS.write_to_admin_file(str([self.checked_state.get()]))
           
        else:
            self.text_area.insert('4.0','\nProbe re-programming is disabled.')
            DS.write_to_admin_file(str([self.checked_state.get()]))
            
        self.text_area.config(state=DISABLED)
     
        
    def _browse_btn_clicked(self):
        filename = filedialog.askopenfilenames(initialdir = "/",title = "Select file",
                                               filetypes = ((".csv files","*.csv"),
                                                            ("all files","*.*")))     
        ZND.SetFileLocation(filename)
        self.file = ZND.GetFileLocation()   
        

class ChangePasswordWindow(tk.Frame):
    def __init__(self, parent, controller):
        self.newPassword = ""
        self.confirmPassword = ""
        self.name = ""
        self.canvas_1 = None
        self.canvas_2 = None

        tk.Frame.__init__(self, parent, bg='#FFDAB9')
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)


        self.confm_btn = ttk.Button(
            self, text='Confirm', command=lambda: self.confm_btn_clicked(controller))
        self.confm_btn.place(relx=0.8, rely=0.8, anchor=CENTER)
        
        self.confm_btn = ttk.Button(
            self, text='Back', command=lambda: 
                [self.canvas_1.destroy(),self.canvas_2.destroy(),controller.show_frame(EditUserWindow)])
        self.confm_btn.place(relx=0.25, rely=0.8, anchor=CENTER)
        
    def refresh_window(self):
        self.canvas_1 = Canvas(bg="#eae9e9",width=400, height=40)
        self.canvas_1.place(x=350, y=225)
        self.canvas_2 = Canvas(bg="#eae9e9",width=400, height=40)
        self.canvas_2.place(x=350, y=300)
        self.pass1_text = self.canvas_1.create_text(220,20,text=" ",fill="black",font=(OnScreenKeys.FONT_NAME, 16, "bold"))
        self.pass2_text = self.canvas_2.create_text(220,20,text=" ",fill="black",font=(OnScreenKeys.FONT_NAME, 14, "bold"))
      
        session_info = DS.get_user()
        self.CPWb1 = ttk.Button(self.canvas_1, text='Enter a new password', command=lambda:
            [self.get_keys(),self.password_entry()])
        self.CPWb1.place(relx=0.2, rely=0.3, anchor=N)
        
        self.CPWb2 = ttk.Button(self.canvas_2, text='Confirm new password', command=lambda: 
            [self.get_keys(),self.conform_pwd()])
        self.CPWb2.place(relx=0.2, rely=0.3, anchor=N)
      
        
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0','end')
        self.text_area.insert('1.0',session_info[0])
        self.text_area.insert('2.0','\nChange ' + DS.get_username() + "'s password.")
        self.text_area.config(state=DISABLED)
        
        
        
    def password_entry(self):
    
        pw_data = self.wait_for_response(self.canvas_1,self.pass1_text)
        self.CPWb1.config(state=NORMAL)
        self.CPWb2.config(state=NORMAL)
        self.newPassword = pw_data
        
        
        
    def conform_pwd(self):
        DS.write_to_from_keys(" ")
        
        pw_data = self.wait_for_response(self.canvas_2,self.pass2_text)
        self.CPWb1.config(state=NORMAL)
        self.CPWb2.config(state=NORMAL)
        self.confirmPassword = pw_data
        
        
        
    def get_keys(self):
        KY.display()
        self.CPWb1.config(state=DISABLED)
        self.CPWb2.config(state=DISABLED)
        
        
        
    def wait_for_response(self, master, label):
        DS.write_to_from_keys(" ")
        password_blank = "*********************"
        pw_data = DS.get_keyboard_data()
        while 1:
            pw_data = DS.get_keyboard_data()
            pw_len = len(pw_data)
            if pw_data[-1] == "+":
                pw_data = pw_data[:-1]
                break 
            master.itemconfig(label, text=password_blank[:pw_len])
            
            Tk.update(master)
            
        return pw_data
    
    

    def confm_btn_clicked(self, controller):
        self.canvas_1.destroy()
        self.canvas_2.destroy()
        if self.newPassword == self.confirmPassword:
            SM.editingUser.password = self.newPassword
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

        self.userListBox = Listbox(self, height=10, width=20)
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
   
        my_admin = DS.get_admin()
        # Update admin file
        update_file.extend(my_admin)
        update_file.append(selectedUser)
      
        DS.add_to_admin_file(update_file)

        controller.show_frame(ChangePasswordWindow)

    def _delUsr_btn_clicked(self, controller):
        self.delUsr_btn.config(command=ignore)
        self.finished_btn.config(command=ignore)
        self.CngPWrd_btn.config(command=ignore)
        

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

        self.newusername = ""
        self.newpassword = ""
        self.confpassword = ""
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

        self.rb1 = ttk.Radiobutton(
            self, text='Admin', variable=self.is_admin, value='true')
        self.rb1.place(relx=0.7, rely=0.35, anchor=CENTER)
        self.rb2 = ttk.Radiobutton(
            self, text='Non-Admin', variable=self.is_admin, value='false')
        self.rb2.place(relx=0.7, rely=0.45, anchor=CENTER)

        self.confm_btn = ttk.Button(
            self, text="Confirm", command=lambda: 
            [self.canvas_1.destroy(),self.canvas_2.destroy(),self.canvas_3.destroy(),self._confm_btn_clicked(controller)])
        self.confm_btn.place(relx=0.85, rely=0.8, anchor=CENTER)

        self.cancl_btn = ttk.Button(
            self, text="Cancel", command=lambda: 
            [self.canvas_1.destroy(),self.canvas_2.destroy(),self.canvas_3.destroy(),controller.show_frame(AdminWindow)])
        self.cancl_btn.place(relx=0.7, rely=0.8, anchor=CENTER)

    def _confm_btn_clicked(self, controller):
        self.confm_btn.config(command=ignore)
        self.cancl_btn.config(command=ignore)
        self.text_area.config(state=NORMAL)
        if self.newpassword == self.confpassword:
                
            # create user object
            if self.is_admin.get() == 'false':
                admin = False
            else:
                admin = True
                
            newUser = User(self.newusername, self.newpassword, admin)
            
            if self.is_admin.get() == 'true' and self.allow_add_admin == False:
                admin = False
                self.text_area.insert('4.30','\nThere are 2 administrators already,\nNo nore allowed')

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
        self.canvas_1 = Canvas(bg="#eae9e9",width=400, height=40)
        self.canvas_1.place(x=200, y=200)
        self.canvas_2 = Canvas(bg="#eae9e9",width=400, height=40)
        self.canvas_2.place(x=200, y=275)
        self.canvas_3 = Canvas(bg="#eae9e9",width=400, height=40)
        self.canvas_3.place(x=200, y=350)
        self.name_text = self.canvas_1.create_text(220,20,text=" ",fill="black",font=(OnScreenKeys.FONT_NAME, 16, "bold"))
        self.pass1_text = self.canvas_2.create_text(220,20,text=" ",fill="black",font=(OnScreenKeys.FONT_NAME, 14, "bold"))
        self.pass2_text = self.canvas_3.create_text(220,20,text=" ",fill="black",font=(OnScreenKeys.FONT_NAME, 14, "bold"))
        self.AUWl1 = ttk.Button(self.canvas_1, text='New user name: ',command=lambda:
            [self.get_keys(),self.name_entry()])
        self.AUWl2 = ttk.Button(self.canvas_2, text='Enter Password: ', command=lambda:
            [self.get_keys(),self.password_entry()])
        self.AUWl3 = ttk.Button(self.canvas_3, text='Confirm Password: ', command=lambda:
            [self.get_keys,self.conform_pwd])
        self.AUWl1.place(relx=0.15, rely=0.3, anchor=N)
        self.AUWl2.place(relx=0.15, rely=0.3, anchor=N)
        self.AUWl3.place(relx=0.15, rely=0.3, anchor=N)
      
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
        self.newusername = ""
        self.newpassword = ""
        
        
    def name_entry(self):
        self.current_user = ""
        block = False
        data = self.wait_for_response(self.canvas_1,  block, self.name_text)
        self.newusername = data
        self.set_buttons_norm()
      
        
        
    def password_entry(self):
        block = True
        pw_data = self.wait_for_response(self.canvas_2, block, self.pass1_text)
        self.newpassword = pw_data
        self.set_buttons_norm()
        
        
        
        
    def conform_pwd(self):
        block = True
        pw_data = self.wait_for_response(self.canvas_3, block, self.pass2_text)
        self.confpassword = pw_data
        self.set_buttons_norm()
        
        
        
    def wait_for_response(self, master, block, label):
        DS.write_to_from_keys(" ")
        password_blank = "*********************"
        pw_data = DS.get_keyboard_data()
        while 1:
            pw_data = DS.get_keyboard_data()
            pw_len = len(pw_data)
            if pw_data[-1] == "+":
                pw_data = pw_data[:-1]
                break 
            if block:
                master.itemconfig(label, text=password_blank[:pw_len])
                # ttk.Label(master, text=password_blank[:pw_len], font=("bold", 15)).place(relx=0.7, rely=0.3, width=150,anchor=N)
            else:
                master.itemconfig(label, text=pw_data)
                # ttk.Label(master, text=pw_data, font=("bold", 15)).place(relx=0.7, rely=0.3, width=150,anchor=N)
            Tk.update(master)
        return pw_data
    
    
    
    def set_buttons_norm(self):
        self.AUWl1.config(state=NORMAL)
        self.AUWl2.config(state=NORMAL)
        self.AUWl3.config(state=NORMAL)
        
        
    def get_keys(self):
          
        KY.display()
        self.AUWl1.config(state=DISABLED)
        self.AUWl2.config(state=DISABLED)
        self.AUWl3.config(state=DISABLED)