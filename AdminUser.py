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
import BatchManager
from time import gmtime, strftime, sleep
import Sessions
import AdminPortControl
import Datastore
import OnScreenKeys
import ProbeManager
import PI
import ProbeInterface
import Ports
import UserLogin

SM = SecurityManager.SecurityManager()
BM = BatchManager.BatchManager()
DS = Datastore.Data_Store()
KY = OnScreenKeys.Keyboard()
K = OnScreenKeys
PM = ProbeManager
PI = PI.ProbeData()
PR = ProbeInterface.PRI()
SE = Sessions
AP = AdminPortControl
P = Ports
UL = UserLogin


def ignore():
    return 'break'


ADMIN_COUNT = 3

test = False


class AdminWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = None
        self.probe = None
        self.checkbutton = None
        self.text_area = None
        self.userListBox = None
        self.canvas_back = None
        self.odm_active = BooleanVar()
        self.admin_state = BooleanVar()
        self.non_human = BooleanVar()
        self.control = controller
        self.location = StringVar()
        #########################
        # Display admin window  #
        #########################

    def canvas_gone(self):
        self.checkbutton.destroy()
        self.odm_button.destroy()
        self.nhp_button.destroy()
        self.canvas.destroy()
        self.canvas_back.destroy()
        self.control.show_frame(SE.SessionSelectWindow)

    def refresh_window(self):
        ##############################
        # Set up admin user options  #
        ##############################
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        self.canvas_back = Canvas(bg='#FFDAB9', width=ws - 10, height=hs - 10)
        self.canvas_back.place(x=5, y=5)
        Label(self.canvas_back, text="Choose an option", font=("Courier", 16), background='#FFDAB9').place(relx=0.12,
                                                                                                           rely=0.25)
        Label(self.canvas_back, text="Users", font=("Courier", 16), background='#FFDAB9').place(relx=0.4, rely=0.25)
        Label(self.canvas_back, text="System controls", font=("Courier", 16), background='#FFDAB9').place(
            relx=0.6, rely=0.25)
        ###################
        # Show user list  #
        ###################
        self.non_human.set(DS.get_user_data()['Non_Human'])
        self.admin_state.set(DS.get_user_data()['Over_rite'])
        self.userListBox = Listbox(self.canvas_back, height=11, width=18)
        self.userListBox.place(relx=0.38, rely=0.35)
        self.userListBox.config(font=("Courier", 16))

        ttk.Label(self.canvas_back, text="Deltex", background="#FFDAB9", foreground="#003865",
                  font=('Helvetica', 30, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self.canvas_back, text="medical", background="#FFDAB9", foreground="#A2B5BB",
                  font=('Helvetica', 16)).place(relx=0.88, rely=0.15)

        self.text_area = tk.Text(self.canvas_back, font=("Courier", 14), height=5, width=38)
        self.text_area.place(relx=0.18, rely=0.1, anchor=CENTER)
        # time_now = strftime("%H:%M:%p", gmtime())

        # if "AM" in time_now:
        #     self.text_area.insert('1.0', 'Good Morning ')
        # else:
        #     self.text_area.insert('1.0', 'Good Afternoon ')
        userList = []
        # self.text_area.config(state=NORMAL)
        # self.text_area.delete('1.0', 'end')
        # self.text_area.insert('1.0', DS.get_username().title())
        # self.text_area.insert('2.0', '\n\nPlease choose an option.')
        for item in SM.GetUserList():
            if not DS.get_current_use_user(item.name):
                # print(f"user list = {item.name}")
                if item.admin:
                    # username = item.name
                    item.name = item.name + "--> Admin"
                userList.append(item.name)

        self.userListBox.delete(0, END)
        # fill the listbox with the list of users

        for item in userList:
            self.userListBox.insert(END, ' ' + item)
        self.userListBox.config(state=DISABLED)
        self.set_overwrite_state()
        # Read admin state of the check box
        # if self.admin_state.get():
        #     self.text_area.insert('4.0', '\nProbe serial number re-issue enabled.')
        # else:
        #     self.text_area.insert('4.0', '\nProbe serial number re-issue disabled.')
        # self.userListBox.config(state=DISABLED)
        # self.text_area.config(state=DISABLED)

        self.checkbutton = Checkbutton(text=" Serial number Replace ",
                                       variable=self.admin_state, command=lambda: self.set_admin_state(),
                                       font=("Courier", 12))

        self.admin_state.get()
        self.checkbutton.place(relx=0.6, rely=0.4)
        self.canvas = Canvas(bg="#eae9e9", width=320, height=300)
        self.canvas.place(relx=0.11, rely=0.32)
        self.show_user_options()

        self.odm_button = Checkbutton(text=" Set Monitor In-active Running",
                                      variable=self.odm_active, command=self.set_odm_state, font=("Courier", 12))
        self.odm_button.place(relx=0.6, rely=0.5)
        self.odm_active.get()

        self.nhp_button = Checkbutton(text=" Test Non-Human Probe",
                                      variable=self.non_human, command=self.set_non_human_probe, font=("Courier", 12))
        self.nhp_button.place(relx=0.6, rely=0.6)
        self.non_human.get()
        Tk.update(self)

    def show_user_options(self):
        ####################
        # Show user input  #
        ####################
        # self.canvas = Canvas(bg="#eae9e9", width=320, height=300)
        # self.canvas.place(relx=0.11, rely=0.32)
        self.btn1 = Button(self.canvas, text='Add a new user', command=self.to_new_user, font=("Courier", 12))
        self.btn1.place(relx=0.1, rely=0.14, height=50, anchor=W)

        Button(self.canvas, text='Edit a current user', command=self.to_edit_user,
               font=("Courier", 12)).place(relx=0.1, rely=0.38, height=50, anchor=W)
        # Button(self.canvas, text='Edit a device port number',
        #        command=self.to_devices, font=("Courier", 12)).place(relx=0.1, rely=0.62, height=50, anchor=W)
        Button(self.canvas, text="Change Batch Qty", command=self.change_qty,
               font=("Courier", 12)).place(relx=0.1, rely=0.65, height=50, anchor=W)
        Label(self.canvas, text=f"Current Qty\n{SE.get_qty()}", font=('Arial', 12)).place(relx=0.62, rely=0.78)

        Button(self.canvas_back, text='Exit', width=40, command=self.canvas_gone).place(height=40,
                                                                                        width=180, relx=0.88, rely=0.82,
                                                                                        anchor=E)

        ttk.Button(self.canvas_back, text="Browse", command=lambda: self.get_browse_file()).place(relx=0.52, rely=0.74,
                                                                                                  height=50, width=110)

        self.location.set(DS.get_file_location()['File'])
        title = ttk.Label(self.canvas_back, text="File storage location", font=("Courier", 14), background='#FFDAB9')
        title.place(relx=0.1, rely=0.7)
        ttk.Label(self.canvas_back, textvariable=self.location, font=("Courier", 14)).place(relx=0.1, rely=0.75,
                                                                                            width=520)
        Tk.update(self)

    def get_browse_file(self):
        default_loc = "/PTT_Results"
        filename = filedialog.askdirectory(initialdir="/", title="Select file")
        if default_loc not in filename:
            filename = f"{filename}{default_loc}"
        file = P.Location(file=filename)
        DS.write_file_location(file)
        self.location.set(filename)
        BM.CSVM.check_directories()
        Tk.update(self)

    def change_qty(self):
        qty_canvas = Canvas(bg="#FFDAB9", width=500, height=120)
        qty_canvas.place(relx=0.3, rely=0.45)
        # qty_text = None
        qty_text = qty_canvas.create_text(200, 45, text=" ", fill="black",
                                          font=(K.FONT_NAME, 8, "bold"))
        Label(qty_canvas, text="Enter a new batch quantity.", font=('Arial', 12)).place(x=75, y=42)
        KY.get_keyboard()

        data = K.wait_for_response(qty_canvas, qty_text)
        if not data:
            data = 100
        batchQty = int(data)

        SE.set_qty(batchQty)
        qty_canvas.destroy()
        self.show_user_options()

    def set_overwrite_state(self):
        time_now = strftime("%H:%M:%p", gmtime())
        self.text_area.config(state=NORMAL)
        if "AM" in time_now:
            self.text_area.insert('1.0', 'Good Morning ')
        else:
            self.text_area.insert('1.0', 'Good Afternoon ')
        self.text_area.delete('1.0', 'end')
        self.text_area.insert('1.0', DS.get_username().title())
        self.text_area.insert('2.0', '\n\nPlease choose an option.')
        if self.admin_state.get():
            self.text_area.insert('4.0', '\nProbe serial number re-issue enabled.')
        else:
            self.text_area.insert('4.0', '\nProbe serial number re-issue disabled.')
        # self.userListBox.config(state=DISABLED)
        self.text_area.config(state=DISABLED)

    #############################################
    # Set user admin status from the check box  #
    #############################################
    def set_admin_state(self):
        user_data = DS.get_user_data()
        user = P.Users(user_data['Username'], user_data['Admin'],
                       over_right=self.admin_state.get(), non_human=user_data['Non_Human'])
        DS.write_user_data(user)
        self.set_overwrite_state()

    def set_odm_state(self):
        odm_state = P.Ports(active=self.odm_active.get())
        DS.write_device_to_file(odm_state)

    def set_non_human_probe(self):
        user_data = DS.get_user_data()
        animal_probe = P.Users(user_data['Username'], user_data['Admin'],
                               non_human=self.non_human.get(), over_right=user_data['Over_rite'])
        DS.write_user_data(animal_probe)

    def to_new_user(self):
        self.canvas_gone()
        self.control.show_frame(AddUserWindow)

    def to_edit_user(self):
        self.canvas_gone()
        self.control.show_frame(EditUserWindow)

    # def to_devices(self):
    #     self.canvas_gone()
    #     self.control.show_frame(AP.AdminPorts)


class ChangePasswordWindow(tk.Frame):
    def __init__(self, parent, controller):
        self.not_to_login = True
        self.reset_pass = False
        self.CPWb1 = None
        self.CPWb2 = None
        self.pass2_text = None
        self.pass1_text = None
        self.newPassword = ""
        self.confirmPassword = ""
        self.is_admin = False
        self.name = ""
        self.canvas_1 = None
        self.canvas_2 = None
        self.newPassword = ""
        self.confirmPassword = ""
        self.control = controller
        tk.Frame.__init__(self, parent, bg='#FFDAB9')
        ttk.Label(self, text="Deltex", background="#FFDAB9", foreground="#003865",
                  font=('Helvetica', 30, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#FFDAB9", foreground="#A2B5BB",
                  font=('Helvetica', 16)).place(relx=0.88, rely=0.15)
        self.text_area = tk.Text(self, font=("Courier", 14), height=5, width=38)
        self.text_area.place(x=40, y=70)

    def confirm(self):
        self.canvas_1.destroy()
        self.canvas_2.destroy()
        # self.password_change()

    def confirm_change(self):
        self.canvas_1.destroy()
        self.canvas_2.destroy()
        result = self.check_entries()
        if not result:
            self.refresh_window()

    def back(self):
        self.canvas_1.destroy()
        self.canvas_2.destroy()
        self.return_to_edit_user()

    def refresh_window(self):
        ##############################
        # Set up user entry options  #
        ##############################
        self.canvas_1 = Canvas(bg="#eae9e9", width=550, height=48)
        self.canvas_1.place(relx=0.3, rely=0.4)
        self.canvas_2 = Canvas(bg="#eae9e9", width=550, height=48)
        self.canvas_2.place(relx=0.3, rely=0.54)
        Label(self, text="Change password", background="#FFDAB9", font=("Courier", 18)).place(relx=0.55, rely=0.07,
                                                                                              anchor=CENTER)
        self.pass1_text = self.canvas_1.create_text(350, 20, text=" ", fill="black",
                                                    font=(OnScreenKeys.FONT_NAME, 16, "bold"))
        self.pass2_text = self.canvas_2.create_text(350, 20, text=" ", fill="black",
                                                    font=(OnScreenKeys.FONT_NAME, 16, "bold"))
        self.reset_pass = DS.get_reset_password()
        self.CPWb1 = Button(self.canvas_1, text='Enter new password', font=('Courier', 12), command=self.password_entry)
        # Set keyboard icon to show button is used to show the keyboard
        Label(self.canvas_1, text="-->").place(x=230, y=12)
        self.CPWb1.place(x=15, y=15)

        self.CPWb2 = Button(self.canvas_2, text='Confirm new password', font=('Courier', 12), command=self.conform_pwd)
        Label(self.canvas_2, text="-->").place(x=230, y=12)
        self.CPWb2.place(x=15, y=15)
        self.is_admin = DS.user_admin_status()
        if not self.reset_pass:
            self.btn = Checkbutton(text=" Admin status ",
                                   variable=self.is_admin, command=self.set_admin_state,
                                   font=("Courier", 14))
            self.btn.place(relx=0.35, rely=0.68)

        self.confm_btn = Button(
            self, text='Confirm', command=self.confirm, font=('Courier', 16))
        self.confm_btn.place(height=40, width=180, relx=0.88, rely=0.83, anchor=E)

        self.back_btn = Button(
            self, text='Back', command=self.back, font=('Courier', 14))
        self.back_btn.place(height=35, width=80, relx=0.625, rely=0.83, anchor=E)

        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        self.text_area.insert('1.0', DS.get_username().title())
        self.text_area.insert('2.0', '\nChange password.')
        self.text_area.config(state=DISABLED)

    def password_entry(self):
        self.get_keys()
        pw_data = K.wait_for_response(self.canvas_1, self.pass1_text)
        self.CPWb1.config(state=NORMAL)
        self.CPWb2.config(state=NORMAL)
        self.newPassword = pw_data

    def conform_pwd(self):
        self.get_keys()
        DS.write_to_from_keys(" ")
        pw_data = K.wait_for_response(self.canvas_2, self.pass2_text)
        self.CPWb1.config(state=NORMAL)
        self.CPWb2.config(state=NORMAL)
        self.confirmPassword = pw_data

    def get_admin_status(self):
        return self.is_admin

    def set_admin_state(self):
        ################################################
        # Admin selects user to change their password  #
        # the selected user has an admin status so get #
        # this status to check is the selected user    #
        # can be an admin too                          #
        ################################################
        self.is_admin = DS.getUser(DS.get_reset_password_name()).admin

    def get_keys(self):
        KY.display()
        self.CPWb1.config(state=DISABLED)
        self.CPWb2.config(state=DISABLED)

    # def wait_for_response(self, master, label):
    #     DS.write_to_from_keys("_")
    #     password_blank = "*********************"
    #     while 1:
    #         pw_data = DS.get_keyboard_data()
    #         pw_len = len(pw_data)
    #         if pw_len > 0 and pw_data[-1] == "+":
    #             pw_data = pw_data[:-1]
    #             break
    #         master.itemconfig(label, text=password_blank[:pw_len])
    #         Tk.update(master)
    #     return pw_data

    # def password_change(self):
    #     if self.check_entries():
    #         self.return_to_edit_user()
    #     else:
    #         self.refresh_window()

    def check_entries(self):
        change = False
        name = DS.get_reset_password_name()
        user_admin = DS.getUser(name).admin
        if not user_admin and not check_user_admin(name):
            # if not check_user_admin(name):
            get_admin = False
        if len(self.newPassword) > 0 and len(self.confirmPassword) > 0:
            if self.newPassword == self.confirmPassword:
                change = True
            else:
                tm.showerror(title="Error", message="Please check your password spelling \nThey don't match.")
        else:
            if self.get_admin_status() is not user_admin:
                change = True

        return self.change_password(change, self.newPassword, self.get_admin_status())

    def change_password(self, change, password, admin):
        update = False
        if change and not DS.get_current_use_user(DS.get_reset_password_name()):
            if SM.updatePassword(password, admin):
                tm.showinfo('Change Password', 'Password change successful')
                update = True
        else:
            tm.showinfo("Change Password", "Unable to change user's password.")
        return update

    def return_to_edit_user(self):
        if self.reset_pass:
            self.control.show_frame(UL.LogInWindow)
        else:
            self.btn.destroy()
            self.control.show_frame(EditUserWindow)


class EditUserWindow(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg='#FFDAB9')
        self.selected_user = None
        self.userList = None
        self.index = 1
        global test
        #################################
        # set up display to sdit users  #
        #################################
        ttk.Label(self, text="Deltex", background="#FFDAB9", foreground="#003865",
                  font=('Helvetica', 30, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#FFDAB9", foreground="#A2B5BB",
                  font=('Helvetica', 16)).place(relx=0.88, rely=0.15)
        self.control = controller
        self.text_area = tk.Text(self, font=("Courier", 14), height=5, width=38)
        self.text_area.place(x=40, y=70)

        self.Label1 = ttk.Label(self, text='Edit user', background="#FFDAB9", font=("Courier", 18))
        self.Label1.place(relx=0.55, rely=0.07, anchor=CENTER)
        # Box to hold user list
        self.userListBox = Listbox(self, height=10, width=20, font=("Courier", 14))
        self.userListBox.place(relx=0.25, rely=0.5, anchor=CENTER)

        self.CngPWrd_btn = ttk.Button(
            self, text='Update User', command=lambda: self._getSelectedUser())
        self.CngPWrd_btn.place(height=40, width=150, relx=0.450, rely=0.42)

        self.delUsr_btn = ttk.Button(
            self, text='Delete User', command=lambda: self._delUsr_btn_clicked())
        self.delUsr_btn.place(height=40, width=120, relx=0.450, rely=0.58)

        self.finished_btn = ttk.Button(
            self, text='Exit', command=lambda: controller.show_frame(AdminWindow))
        self.finished_btn.place(height=40, width=180, relx=0.75, rely=0.78)

    def _getSelectedUser(self):
        # set up user list box to first selected item
        # selectedId = self.userListBox.curselection()
        # selectedUser = self.userListBox.get(selectedId[0])
        if test:
            # self.userListBox.selection_set(1)
            self.selectedUser = self.userListBox.get(self.index)
        else:
            selectedId = self.userListBox.curselection()
            self.selectedUser = self.userListBox.get(selectedId[0])
        ##############################################
        # Send admin user and selected user to file  #
        # to be retrieved later                      #
        # in change password window                  #
        ##############################################
        # Update user object to hold user that wishes to chenge password #
        change_pw_name = P.Users(DS.get_username(), DS.user_admin_status(), pw_user=self.selectedUser)
        DS.write_user_data(change_pw_name)
        # send to change selected user password
        if not test:
            self.control.show_frame(ChangePasswordWindow)

    def _delUsr_btn_clicked(self):
        self.delUsr_btn.config(command=ignore)
        self.finished_btn.config(command=ignore)
        self.CngPWrd_btn.config(command=ignore)
        lstid = self.userListBox.curselection()
        lstUsr = self.userListBox.get(lstid[0])
        if test:
            lstUsr = self.userListBox.get(self.index)

        if "--> Admin" in lstUsr:
            username = lstUsr[:-9]
        else:
            username = lstUsr

        self.result = self.delete_user(DS.getUser(username))

        if self.result:
            self.refresh_window()

        self.delUsr_btn.config(
            command=lambda: self._delUsr_btn_clicked())
        self.finished_btn.config(
            command=lambda: self.control.show_frame(AdminWindow))
        self.CngPWrd_btn.config(
            command=lambda: self._getSelectedUser())

    def delete_user(self, puser):
        # puser is the selected user from the list menu
        delete = False
        sure = tm.askyesno(
            'Delete confirm', 'Are you sure you want to Delete this user?')
        if sure:
            if puser.name != DS.get_username():
                delete = SM.delete_user(puser)
            else:
                tm.showerror("Error", "This user can't be deleted")
        return delete

    def refresh_window(self):
        # create a list of the current users using the dictionary of users
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        self.text_area.insert('1.0', DS.get_username().title())
        self.text_area.insert('2.0', '\n\nPlease choose an option.')
        self.text_area.config(state=DISABLED)
        self.userList = []
        ###############################################
        # Show user list and who is an administrator  #
        ###############################################
        for item in SM.GetUserList():
            if not DS.get_current_use_user(item.name):
                if item.admin is True:
                    item.name = item.name + "--> Admin"
                self.userList.append(item.name)

            # clear the listbox
        self.userListBox.delete(0, END)

        # fill the listbox with the list of users
        for item in self.userList:
            self.userListBox.insert(END, item)
        # Getting the selected user
        self.userListBox.select_set(0)

    def set_test(self):
        global test
        test = True


def check_user_admin(name):
    global ADMIN_COUNT
    admin = False
    admin_count = 0
    for item in SM.GetUserList():
        if item.admin:
            admin_count += 1
    if admin_count >= ADMIN_COUNT:
        tm.showerror(title="Admin User Error",
                     message=f"( {name} ) cannot be an administrator,\nDefault standard user.")
    else:
        admin = True
    return admin


class AddUserWindow(tk.Frame):
    def __init__(self, parent, controller):
        # add User screen
        tk.Frame.__init__(self, parent, bg='#FFDAB9')

        self.confpassword = None
        self.newpassword = None
        self.newusername = None
        self.AUWl3 = None
        self.AUWl2 = None
        self.AUWl1 = None
        self.canvas_3 = None
        self.canvas_2 = None
        self.canvas_1 = None
        # self.allow_add_admin = True
        self.is_admin = BooleanVar()
        self._setDefaults()
        self.control = controller

        self.text_area = tk.Text(self, font=("Courier", 14), height=5, width=38)
        self.text_area.place(x=40, y=70)

        ttk.Label(self, text="Deltex", background="#FFDAB9", foreground="#003865",
                  font=('Helvetica', 30, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#FFDAB9", foreground="#A2B5BB",
                  font=('Helvetica', 16)).place(relx=0.88, rely=0.15)

        self.confm_btn = ttk.Button(
            self, text="Confirm", command=lambda:
            [self.remove_canvas(), self._confm_btn_clicked])
        self.confm_btn.place(height=40, width=180, relx=0.880, rely=0.78, anchor=E)

        self.cancl_btn = ttk.Button(
            self, text="Cancel", command=lambda:
            [self.remove_canvas(), controller.show_frame(AdminWindow)])
        self.cancl_btn.place(height=35, width=100, relx=0.625, rely=0.78, anchor=E)

    def _confm_btn_clicked(self):
        self.confm_btn.config(command=ignore)
        self.cancl_btn.config(command=ignore)
        test_added = False
        if not self.check_details():
            self.enable_buttons_and_return()
        else:
            # Check adding a new user to the system
            if self.add_user(self.is_admin.get()):
                # User added
                tm.showinfo('New User', 'New user added.')
                test_added = True
            else:
                tm.showinfo('Add user', 'Unable to add the user.')
            if not test:
                self.enable_buttons_and_return()
                self.control.show_frame(AdminWindow)
        return test_added

    def add_user(self, admin):
        # Create a new user object
        user_added = False
        if not check_user_admin(self.newusername):
            admin = False
        newUser = P.User(self.newusername, self.newpassword, admin)
        if SM.addUser(newUser):
            user_added = True
            if self.newusername in DS.get_deleted_users().keys():
                DS.remove_from_delete_file(self.newusername)
        return user_added

    def check_details(self):
        confirm = True
        if len(self.newusername) == 0:
            tm.showerror("User Error", "Please enter a name.")
            confirm = False
        if len(self.newpassword) == 0:
            tm.showerror("Password Error", "Please enter a password.")
            confirm = False
        elif len(self.confpassword) == 0:
            tm.showerror("Password Error", "Please enter a confirm password.")
            confirm = False
        elif self.newpassword != self.confpassword:
            tm.showerror("Password Error", "Please check password spelling\nthey are not the same")
            confirm = False
        return confirm

    def enable_buttons_and_return(self):
        self.confm_btn.config(
            command=lambda: [self.remove_canvas(), self._confm_btn_clicked()])
        self.cancl_btn.config(
            command=lambda: self.control.show_frame(AdminWindow))

    def remove_canvas(self):
        self.canvas_1.destroy(), self.canvas_2.destroy(), self.canvas_3.destroy()

    def refresh_window(self):
        # create a list of the current users using the dictionary of users
        self.canvas_1 = Canvas(bg="#eae9e9", width=520, height=45)
        self.canvas_1.place(relx=0.15, rely=0.4)
        self.canvas_2 = Canvas(bg="#eae9e9", width=520, height=45)
        self.canvas_2.place(relx=0.15, rely=0.5)
        self.canvas_3 = Canvas(bg="#eae9e9", width=520, height=45)
        self.canvas_3.place(relx=0.15, rely=0.6)
        Label(self, text="Add new user", background="#FFDAB9", font=("Courier", 18)).place(relx=0.55, rely=0.07,
                                                                                           anchor=CENTER)
        self.name_text = self.canvas_1.create_text(240, 20, text=" ", fill="black",
                                                   font=(OnScreenKeys.FONT_NAME, 16, "bold"))
        self.pass1_text = self.canvas_2.create_text(240, 20, text=" ", fill="black",
                                                    font=(OnScreenKeys.FONT_NAME, 14, "bold"))
        self.pass2_text = self.canvas_3.create_text(240, 20, text=" ", fill="black",
                                                    font=(OnScreenKeys.FONT_NAME, 14, "bold"))
        self.AUWl1 = Button(self.canvas_1, text='New user name:   ', font=('Courier', 12), command=self.name_entry)
        Label(self.canvas_1, text="-->", font=('Courier', 12)).place(x=200, y=12)
        self.AUWl2 = Button(self.canvas_2, text='Enter Password:  ', font=('Courier', 12), command=self.password_entry)
        Label(self.canvas_2, text="-->", font=('Courier', 12)).place(x=200, y=12)
        self.AUWl3 = Button(self.canvas_3, text='Confirm Password:', font=('Courier', 12), command=self.conform_pwd)
        Label(self.canvas_3, text="-->", font=('Courier', 12)).place(x=200, y=12)
        self.AUWl1.place(x=10, y=12)
        self.AUWl2.place(x=10, y=12)
        self.AUWl3.place(x=10, y=12)

        Checkbutton(
            self, text=' Administrator', variable=self.is_admin, font=('Courier', 14)).place(relx=0.25, rely=0.75,
                                                                                             anchor=CENTER)

        self.get_admin_status()
        self.is_admin.set(False)
        self._setDefaults()
        self.text_area.delete('1.0', 'end')
        self.text_area.insert('1.0', DS.get_username().title())
        self.text_area.insert('2.0', '\nPlease complete the form.')
        self.text_area.config(state=DISABLED)
        Tk.update(self)
        # self.check_admin_state()

    def get_admin_status(self):
        self.admin = self.is_admin.get()

    # def check_admin_state(self):
    #     for num in range(1, 10):
    #         print(self.is_admin.get())
    #         sleep(2)
    #         self.refresh_window()

    def _setDefaults(self):
        self.admin = False
        self.newusername = ""
        self.newpassword = ""
        self.confpassword = ""

    def name_entry(self):
        self.disable_buttons()
        data = K.wait_for_response(self.canvas_1, self.name_text)
        self.newusername = data
        self.set_buttons_norm()

    def password_entry(self):
        self.disable_buttons()
        block = True
        pw_data = K.wait_for_response(self.canvas_2, block, self.pass1_text)
        self.newpassword = pw_data
        self.set_buttons_norm()

    def conform_pwd(self):
        self.disable_buttons()
        block = True
        pw_data = K.wait_for_response(self.canvas_3, block, self.pass2_text)
        self.confpassword = pw_data
        self.set_buttons_norm()

    # def wait_for_response(self, master, block, label):
    #     DS.write_to_from_keys("_")
    #     password_blank = "*********************"
    #     while 1:
    #         pw_data = DS.get_keyboard_data()
    #         pw_len = len(pw_data)
    #         if pw_len > 0 and pw_data[-1] == "+":
    #             pw_data = pw_data[:-1]
    #             break
    #         if block:
    #             master.itemconfig(label, text=password_blank[:pw_len])
    #             ttk.Label(master, text=password_blank[:pw_len], font=("bold", 15)).place(relx=0.62, rely=0.3, width=250,
    #                                                                                      anchor=N)
    #         else:
    #             master.itemconfig(label, text=pw_data)
    #             ttk.Label(master, text=pw_data, font=("bold", 15)).place(relx=0.62, rely=0.3, width=250, anchor=N)
    #         Tk.update(master)
    #     return pw_data

    def set_buttons_norm(self):
        self.AUWl1.config(state=NORMAL)
        self.AUWl2.config(state=NORMAL)
        self.AUWl3.config(state=NORMAL)

    def disable_buttons(self):
        KY.display()
        self.AUWl1.config(state=DISABLED)
        self.AUWl2.config(state=DISABLED)
        self.AUWl3.config(state=DISABLED)

    def set_test(self):
        global test
        test = True
