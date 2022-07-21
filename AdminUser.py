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
import AdminPortControl as AP
import Datastore
import OnScreenKeys
import ProbeManager
import PI
import ProbeInterface
from Connection import Location as LO
from SecurityManager import Users as U

SM = SecurityManager.SecurityManager()
BM = BatchManager.BatchManager()
DS = Datastore.Data_Store()
KY = OnScreenKeys.Keyboard()
PM = ProbeManager
P = PI.ProbeData()
PR = ProbeInterface.PRI()


def ignore():
    return 'break'


class AdminWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.file = StringVar()
        # self.file.set(DS.get_location_file())
        self.admin_state = BooleanVar()
        self.control = controller
        self.location = StringVar()
        #########################
        # Display admin window  #
        #########################

    def canvas_gone(self):
        self.checkbutton.destroy()
        self.canvas.destroy()
        self.canvas_back.destroy()

    def refresh_window(self):
        ##############################
        # Set up admin user options  #
        ##############################
        self.canvas_back = Canvas(bg='#FFDAB9', width=970, height=610)
        self.canvas_back.place(x=10, y=10)
        Label(self.canvas_back, text="Choose an option",font=("Courier", 12),background='#FFDAB9').place(x=100,y=150)
        Label(self.canvas_back, text="Users", font=("Courier", 12), background='#FFDAB9').place(x=450, y=150)
        Label(self.canvas_back, text="Probe Serial Number Replace", font=("Courier", 12), background='#FFDAB9').place(x=620, y=150)
        ###################
        # Show user list  #
        ###################
        self.userListBox = Listbox(self.canvas_back, height=12, width=25)
        self.userListBox.place(x=40, y=70)

        ttk.Label(self.canvas_back, text="Deltex", background="#FFDAB9", foreground="#003865",
                  font=('Helvetica', 24, 'bold'), width=12).place(x=850, y=25)
        ttk.Label(self.canvas_back, text="medical", background="#FFDAB9", foreground="#A2B5BB",
                  font=('Helvetica', 14)).place(x=850, y=57)

        self.text_area = tk.Text(self.canvas_back, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
        time_now = strftime("%H:%M:%p", gmtime())

        if "AM" in time_now:
            self.text_area.insert('1.0', 'Good Morning ')
        else:
            self.text_area.insert('1.0', 'Good Afternoon ')
        userList = []
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        self.text_area.insert('1.0', DS.get_username())
        self.text_area.insert('2.0', '\n\nPlease choose an option.')
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

        # Read admin state of the check box
        if self.admin_state.get() == True:
            self.text_area.insert('4.0', '\nProbe re-programming is enabled.')
        else:
            self.text_area.insert('4.0', '\nProbe re-programming is disabled.')
        self.userListBox.config(state=DISABLED)
        self.text_area.config(state=DISABLED)
        self.checkbutton = Checkbutton(text=" Serial number Replace ",
                                       variable=self.admin_state, command=lambda: self.set_admin_state(),
                                       font=("Courier", 10))

        self.admin_state.get()
        self.checkbutton.place(x=650, y=220)
        # User options
        self.show_user_options()
        self.probe = PM.Probe()
        Tk.update(self)

    def set_admin(self, state):
        self.admin_state.set(state)

    def show_user_options(self):
        ####################
        # Show user input  #
        ####################
        self.canvas = Canvas(bg="#eae9e9", width=250, height=200)
        self.canvas.place(x=100, y=190)
        self.AW_addUsrBtn = ttk.Button(
            self.canvas, text='Add a new user',
            command=lambda: [self.canvas_gone(), self.control.show_frame(AddUserWindow)])
        self.AW_addUsrBtn.place(relx=0.1, rely=0.14, anchor=W)
        self.AW_editUsrBtn = ttk.Button(
            self.canvas, text='Edit a current user',
            command=lambda: [self.canvas_gone(), self.control.show_frame(EditUserWindow)])
        self.AW_editUsrBtn.place(relx=0.1, rely=0.48, anchor=W)
        self.AW_editUsrBtn = ttk.Button(
            self.canvas, text='Edit a device port number',
            command=lambda: [self.canvas_gone(), self.control.show_frame(AP.AdminPorts)])
        self.AW_editUsrBtn.place(relx=0.1, rely=0.8, anchor=W)
        self.AW_adminLogoutBtn = ttk.Button(
            self.canvas_back, text='Done', width=30, command=lambda:
            [self.canvas_gone(), self.control.show_frame(SE.SessionSelectWindow)])
        self.AW_adminLogoutBtn.place(height=35, width=180, x=850, y=530, anchor=E)
        self.browseBtn = ttk.Button(
            self.canvas_back, text="Browse", command=lambda: self.get_browse_file())
        self.browseBtn.place(x=430, y=470)
        self.clearBtn = ttk.Button(
            self.canvas_back, text="...", command=lambda: self.clear_probe())
        self.clearBtn.place(x=880, y=570, width=30)
        self.location.set(DS.get_file_location()['File'])
        title = ttk.Label(self.canvas_back, text="File storage location",font=("Courier", 12),background='#FFDAB9')
        title.place(relx=0.1, rely=0.7)
        ttk.Label(self.canvas_back, textvariable=self.location).place(relx=0.1, rely=0.77, width=300)

    def get_browse_file(self):
        filename = filedialog.askdirectory(initialdir="/", title="Select file")
        file = LO(file=filename)
        DS.write_file_location(file)
        self.location.set(filename)
        LO(file=filename)
        Tk.update(self)


    #############################################
    # Set user admin status from the check box  #
    #############################################
    def set_admin_state(self):
        self.probe.set_over_write(self.admin_state.get())
        user = U(DS.get_username(),DS.user_admin_status(),over_right=self.admin_state.get())
        DS.write_user_data(user)

    def clear_probe(self):
        check = tm.askokcancel(title='Wipe probe', message='Insert probe to be wiped.')
        if check:
            snum = P.GenerateDataString('blank')
            PR.probe_write(snum)


class ChangePasswordWindow(tk.Frame):
    def __init__(self, parent, controller):
        self.newPassword = ""
        self.confirmPassword = ""
        self.name = ""
        self.canvas_1 = None
        self.canvas_2 = None
        self.newPassword = ""
        self.confirmPassword = ""
        self.control = controller

        tk.Frame.__init__(self, parent, bg='#FFDAB9')

        ttk.Label(self, text="Deltex", background="#FFDAB9", foreground="#003865",
                  font=('Helvetica', 24, 'bold'), width=12).place(x=850, y=25)
        ttk.Label(self, text="medical", background="#FFDAB9", foreground="#A2B5BB",
                  font=('Helvetica', 14)).place(x=850, y=57)

        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(x=40, y=70)

        self.confm_btn = ttk.Button(
            self, text='Confirm', command=lambda:
            [self.canvas_1.destroy(), self.canvas_2.destroy(), self.password_change()])
        self.confm_btn.place(height=35, width=180, x=880, y=530, anchor=E)

        self.confm_btn = ttk.Button(
            self, text='Back', command=lambda:
            [self.canvas_1.destroy(), self.canvas_2.destroy(), controller.show_frame(EditUserWindow)])
        self.confm_btn.place(height=30, width=80, x=625, y=530, anchor=E)

    def refresh_window(self):
        ##############################
        # Set up user entry options  #
        ##############################
        self.canvas_1 = Canvas(bg="#eae9e9", width=400, height=45)
        self.canvas_1.place(x=350, y=225)
        self.canvas_2 = Canvas(bg="#eae9e9", width=400, height=45)
        self.canvas_2.place(x=350, y=300)
        self.pass1_text = self.canvas_1.create_text(240, 20, text=" ", fill="black",
                                                    font=(OnScreenKeys.FONT_NAME, 16, "bold"))
        self.pass2_text = self.canvas_2.create_text(240, 20, text=" ", fill="black",
                                                    font=(OnScreenKeys.FONT_NAME, 14, "bold"))

        self.CPWb1 = ttk.Button(self.canvas_1, text='Enter a new password', command=lambda:
        [self.get_keys(), self.password_entry()])
        # Set keyboard icon to show button is used to show the keyboard
        Label(self.canvas_1, text="-->").place(x=170, y=12)
        self.CPWb1.place(relx=0.2, rely=0.3, anchor=N)

        self.CPWb2 = ttk.Button(self.canvas_2, text='Confirm new password', command=lambda:
        [self.get_keys(), self.conform_pwd()])
        Label(self.canvas_2, text="-->").place(x=170, y=12)
        self.CPWb2.place(relx=0.2, rely=0.3, anchor=N)
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        self.text_area.insert('1.0', DS.get_username())
        self.text_area.insert('2.0', '\nChange ' + DS.get_user_data()['Change_password'] + "'s password.")
        self.text_area.config(state=DISABLED)

    def password_entry(self):
        pw_data = self.wait_for_response(self.canvas_1, self.pass1_text)
        self.CPWb1.config(state=NORMAL)
        self.CPWb2.config(state=NORMAL)
        self.newPassword = pw_data

    def conform_pwd(self):
        DS.write_to_from_keys(" ")
        pw_data = self.wait_for_response(self.canvas_2, self.pass2_text)
        self.CPWb1.config(state=NORMAL)
        self.CPWb2.config(state=NORMAL)
        self.confirmPassword = pw_data

    def set_password(self, pwd):
        self.newPassword = pwd

    def set_confirm(self, conf):
        self.confirmPassword = conf

    def get_keys(self):
        KY.display()
        self.CPWb1.config(state=DISABLED)
        self.CPWb2.config(state=DISABLED)

    def wait_for_response(self, master, label):
        DS.write_to_from_keys("_")
        password_blank = "*********************"
        pw_data = DS.get_keyboard_data()
        while 1:
            pw_data = DS.get_keyboard_data()
            pw_len = len(pw_data)
            if pw_len > 0 and pw_data[-1] == "+":
                pw_data = pw_data[:-1]
                break
            master.itemconfig(label, text=password_blank[:pw_len])
            Tk.update(master)
        return pw_data

    def password_change(self):
        result = self.check_entries()
        if result == True:
            self.return_to_edit_user()
        else:
            self.refresh_window()

    def check_entries(self):
        pw_len = len(self.newPassword)
        cfm_pw = len(self.confirmPassword)
        if pw_len > 0 and cfm_pw > 0:
            if self.newPassword == self.confirmPassword:
                done = self.change_password(self.newPassword)
                return done
            else:
                tm.showerror(title="Error", message="Please check your password spelling \nThey don't match.")
                return False
        else:
            tm.showerror(title="Error", message="Your have left one of the entries empty.")
            return False

    def change_password(self, password):

        if SM.updatePassword(password):
            tm.showinfo('Changed password', 'Password change successful')
            return True
        else:
            return False

    def return_to_edit_user(self):
        self.control.show_frame(EditUserWindow)


class EditUserWindow(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg='#FFDAB9')
        #################################
        # set up display to sdit users  #
        #################################
        ttk.Label(self, text="Deltex", background="#FFDAB9", foreground="#003865",
                  font=('Helvetica', 24, 'bold'), width=12).place(x=850, y=25)
        ttk.Label(self, text="medical", background="#FFDAB9", foreground="#A2B5BB",
                  font=('Helvetica', 14)).place(x=850, y=57)

        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(x=40, y=70)

        self.Label1 = ttk.Label(self, text='Choose a user to edit')
        self.Label1.place(relx=0.5, rely=0.07, anchor=CENTER)
        # Box to hold user list
        self.userListBox = Listbox(self, height=10, width=20)
        self.userListBox.place(relx=0.3, rely=0.5, anchor=CENTER)

        self.CngPWrd_btn = ttk.Button(
            self, text='Change password', command=lambda: self._getSelectedUser(controller))
        self.CngPWrd_btn.place(height=30, width=150, x=550, y=300, anchor=E)

        self.delUsr_btn = ttk.Button(
            self, text='Delete', command=lambda: self._delUsr_btn_clicked(controller))
        self.delUsr_btn.place(height=30, width=120, x=550, y=400, anchor=E)

        self.finished_btn = ttk.Button(
            self, text='Done', command=lambda: controller.show_frame(AdminWindow))
        self.finished_btn.place(height=35, width=180, x=880, y=530, anchor=E)

    def _getSelectedUser(self, controller):
        # set up user list box to first selected item
        selectedId = self.userListBox.curselection()
        selectedUser = self.userListBox.get(selectedId[0])
        ##############################################
        # Send admin user and selected user to file  #
        # to be retrieved later                      #
        # in change password window                  #
        ##############################################
        # Update user object to hold user that wishes to chenge password #

        # DS.add_to_user_file(selectedUser)
        change_pw_name = U(DS.get_username(),DS.user_admin_status(),pw_user=selectedUser)
        DS.write_user_data(change_pw_name)
        # send to change selected user password
        controller.show_frame(ChangePasswordWindow)

    def _delUsr_btn_clicked(self, controller):
        self.delUsr_btn.config(command=ignore)
        self.finished_btn.config(command=ignore)
        self.CngPWrd_btn.config(command=ignore)
        lstid = self.userListBox.curselection()
        lstUsr = self.userListBox.get(lstid[0])

        if "--> Admin" in lstUsr:
            delete_user = lstUsr[:-9]
        else:
            delete_user = lstUsr

        result = self.check_delete(delete_user)

        if result == True:
            self.refresh_window()

        self.delUsr_btn.config(
            command=lambda: self._delUsr_btn_clicked(controller))
        self.finished_btn.config(
            command=lambda: controller.show_frame(AdminWindow))
        self.CngPWrd_btn.config(
            command=lambda: self._getSelectedUser(controller))

    def check_delete(self, delete_user):
        sure = tm.askyesno(
            'Delete confirm', 'Are you sure you want to Delete this user?')
        if sure == True:
            if delete_user != DS.get_username():
                SM.delete_user(SM.GetUserObject(delete_user))
                return True
            else:
                tm.showerror('Error', 'Cannot delete yourself')
                return False

    def refresh_window(self):
        # create a list of the current users using the dictionary of users
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        self.text_area.insert('1.0', DS.get_username())
        self.text_area.insert('2.0', '\n\nPlease choose an option.')
        self.text_area.config(state=DISABLED)
        userList = []
        ###############################################
        # Show user list and who is an administartor  #
        ###############################################
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

        self.is_admin = StringVar()
        self._setDefaults()
        self.control = controller

        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(x=40, y=70)
        self.text_area.config(state=DISABLED)

        ttk.Label(self, text="Deltex", background="#FFDAB9", foreground="#003865",
                  font=('Helvetica', 24, 'bold'), width=12).place(x=850, y=25)
        ttk.Label(self, text="medical", background="#FFDAB9", foreground="#A2B5BB",
                  font=('Helvetica', 14)).place(x=850, y=57)

        self.confm_btn = ttk.Button(
            self, text="Confirm", command=lambda:
            [self.remove_canvas(), self._confm_btn_clicked(controller)])
        self.confm_btn.place(height=35, width=180, x=880, y=530, anchor=E)

        self.cancl_btn = ttk.Button(
            self, text="Cancel", command=lambda:
            [self.remove_canvas(), controller.show_frame(AdminWindow)])
        self.cancl_btn.place(height=30, width=80, x=625, y=530, anchor=E)

    def _confm_btn_clicked(self, controller):
        self.confm_btn.config(command=ignore)
        self.cancl_btn.config(command=ignore)

        if self.check_details():
            self.enable_buttons_and_return(self.control)
        else:
            # Check the user admin and return the admin status
            admin = self.check_user_admin()
            # Check adding a new user to the system
            if self.add_user(admin):
                # User added
                tm.showinfo('New User', 'New user added')
            else:
                # User already in the system
                tm.showerror('Error', 'User already exsists')
            self._setDefaults()
            # Clear buttons and return to the start
            self.enable_buttons_and_return(self.control)
            controller.show_frame(AdminWindow)

    def add_user(self, admin):
        # Create a new user object
        user_added = False
        newUser = User(self.newusername, self.newpassword, admin)
        if SM.addUser(newUser):
            user_added = True
        return user_added

    def check_details(self):
        confirm = True
        if len(self.newusername) == 0:
            tm.showerror("User Error", "Please enter a name.")
            confirm = False
        elif len(self.newpassword) == 0:
            tm.showerror("Password Error", "Please enter a password.")
            confirm = False
        elif len(self.confpassword) == 0:
            tm.showerror("Password Error", "Please enter a confirm password.")
            confirm = False
        elif self.newpassword != self.confpassword:
            tm.showerror("Password Error", "Please check password spelling\nthey are not the same")
            confirm = False

        return confirm

    def check_user_admin(self):
        admin = False
        admin_count = 0
        for item in SM.GetUserList():
            if item.admin:
                admin_count += 1

        if admin_count > 1:
            tm.showerror(title="Admin User Error",
                         message=f"{self.newusername} cannot be an administrator,\nDefault standard user.")
            admin = False
        else:
            admin = True
        return admin

    def enable_buttons_and_return(self, control):
        self.confm_btn.config(
            command=lambda: [self.remove_canvas(), self._confm_btn_clicked(control)])
        self.cancl_btn.config(
            command=lambda: self.control.show_frame(AdminWindow))

    def remove_canvas(self):
        self.canvas_1.destroy(), self.canvas_2.destroy(), self.canvas_3.destroy()

    def refresh_window(self):
        self.rb1 = ttk.Radiobutton(
            self, text='Admin', variable=self.is_admin, value=True)
        self.rb1.place(relx=0.7, rely=0.35, anchor=CENTER)
        self.rb2 = ttk.Radiobutton(
            self, text='Non-Admin', variable=self.is_admin, value=False)
        self.rb2.place(relx=0.7, rely=0.45, anchor=CENTER)
        self.get_admin_status()
        self.is_admin.set("false")
        # create a list of the current users using the dictionary of users
        self.canvas_1 = Canvas(bg="#eae9e9", width=400, height=45)
        self.canvas_1.place(x=200, y=200)
        self.canvas_2 = Canvas(bg="#eae9e9", width=400, height=45)
        self.canvas_2.place(x=200, y=275)
        self.canvas_3 = Canvas(bg="#eae9e9", width=400, height=45)
        self.canvas_3.place(x=200, y=350)
        self.name_text = self.canvas_1.create_text(240, 20, text=" ", fill="black",
                                                   font=(OnScreenKeys.FONT_NAME, 16, "bold"))
        self.pass1_text = self.canvas_2.create_text(240, 20, text=" ", fill="black",
                                                    font=(OnScreenKeys.FONT_NAME, 14, "bold"))
        self.pass2_text = self.canvas_3.create_text(240, 20, text=" ", fill="black",
                                                    font=(OnScreenKeys.FONT_NAME, 14, "bold"))
        self.AUWl1 = ttk.Button(self.canvas_1, text='New user name: ', command=lambda:
        [self.get_keys(), self.name_entry()])
        Label(self.canvas_1, text="-->").place(x=170, y=12)
        self.AUWl2 = ttk.Button(self.canvas_2, text='Enter Password: ', command=lambda:
        [self.get_keys(), self.password_entry()])
        Label(self.canvas_2, text="-->").place(x=170, y=12)
        self.AUWl3 = ttk.Button(self.canvas_3, text='Confirm Password: ', command=lambda:
        [self.get_keys(), self.conform_pwd()])
        Label(self.canvas_3, text="-->").place(x=170, y=12)
        self.AUWl1.place(relx=0.15, rely=0.3, anchor=N)
        self.AUWl2.place(relx=0.15, rely=0.3, anchor=N)
        self.AUWl3.place(relx=0.15, rely=0.3, anchor=N)

        self.text_area.delete('1.0', 'end')
        self.text_area.insert('1.0', DS.get_username())
        self.text_area.insert('2.0', '\nPlease complete the form.')
        self.allow_add_admin = True
        admins = 0
        admin_names = []
        for item in SM.GetUserList():
            if item.admin == True:
                admin_names.append(item)
        admins = len(admin_names)

        if admins >= 2:
            self.allow_add_admin = False

    def get_admin_status(self):
        self.admin = self.is_admin.get()

    def _setDefaults(self):
        self.admin = False
        self.newusername = ""
        self.newpassword = ""
        self.confpassword = ""

    def name_entry(self):
        self.current_user = ""
        block = False
        data = self.wait_for_response(self.canvas_1, block, self.name_text)
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

    def set_unsername(self, name):
        self.newusername = name

    def get_username(self):
        return self.newusername

    def set_new_password(self, password):
        self.newpassword = password

    def get_new_password(self):
        return self.newpassword

    def set_confirm_pass(self, confirm):
        self.confpassword = confirm

    def get_confirm_pass(self):
        return self.confpassword

    def wait_for_response(self, master, block, label):
        DS.write_to_from_keys("_")
        password_blank = "*********************"
        pw_data = DS.get_keyboard_data()
        while 1:
            pw_data = DS.get_keyboard_data()
            pw_len = len(pw_data)
            if pw_len > 0 and pw_data[-1] == "+":
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