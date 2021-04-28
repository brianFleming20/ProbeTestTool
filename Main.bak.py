'''
Created on 3 May 2017

@author: jackw

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
-make the windows all the same size and screen position

#         s = ttk.Separator(self.root, orient=VERTICAL)
#         s.grid(row=0, column=1, sticky=(N,S))

'''
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tm
import pyvisa as visa
import time 

# import PI
import SecurityManager
from SecurityManager import User
import BatchManager
from BatchManager import Batch
import InstrumentManager
from InstrumentManager import ZND
import ProbeManager
from ProbeManager import Probe
from ProbeManager import ProbeManager

#create instances
SM = SecurityManager.SecurityManager()
IM = InstrumentManager.InstrumentationManager()
BM = BatchManager.BatchManager()
PM = ProbeManager()
ZND = ZND()

#define global variables
TaTTVersion = 'Transducer Test Tool V0.1'
w = 600 #window width
h = 350 #window height


#Assign as a command when I want to disable a button (double click prevention)
def ignore():
    return 'break'

class TestProgramWindow(object):
    def __init__(self):
        self.root = Tk()
        self.root.title(TaTTVersion)
        self.root.resizable(width=False, height=False)
        self.rootFrame = ttk.Frame(self.root)
        
        #get window width and height
        ws = self.root.winfo_screenwidth() 
        hs = self.root.winfo_screenheight() 
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.sessionOnGoing = False
        self.sessionComplete = None
        
        #define variables
        self.currentBatch = StringVar()
        self.currentUser = StringVar()
        self.probesPassed = IntVar()
        self.deviceDetails = StringVar()
        self.probeType = StringVar()
        
        #import images
        self.greenlight = (PhotoImage(file="green128.gif"))
        self.amberlight = (PhotoImage(file="amber128.gif"))
        self.redlight = (PhotoImage(file="red128.gif"))
        self.greylight = (PhotoImage(file="grey128.gif"))

        progress_label1 = ttk.Label(self.root, text='Probes Passed: ')
        progress_label1.place(relx=0.17, rely=0.05, anchor=CENTER)
        
        progress_label2 = ttk.Label(self.root, textvariable=self.probesPassed)
        progress_label2.place(relx=0.325, rely=0.05, anchor=CENTER)
        
        label1 = ttk.Label(self.root, text='Batch number: ')
        label1.place(relx=0.47, rely=0.05, anchor=CENTER)
        
        label2 = ttk.Label(self.root, textvariable=self.currentBatch)
        label2.place(relx=0.57, rely=0.05, anchor=CENTER)

        label3 = ttk.Label(self.root, text='Probe type: ')
        label3.place(relx=0.75, rely=0.05, anchor=CENTER)
        
        label4 = ttk.Label(self.root, textvariable=self.probeType)
        label4.place(relx=0.84, rely=0.05, anchor=CENTER)
        
        label5 = ttk.Label(self.root, text='User: ')
        label5.place(relx=0.13, rely=0.15, anchor=CENTER)
        
        label6 = ttk.Label(self.root, textvariable=self.currentUser)
        label6.place(relx=0.2, rely=0.15, anchor=CENTER)

        label7 = ttk.Label(self.root, text='Connected to: ')
        label7.place(relx=0.45, rely=0.15, anchor=CENTER)
        
        label8 = ttk.Label(self.root, textvariable=self.deviceDetails)
        label8.place(relx=0.55, rely=0.15, anchor=CENTER)
    
        
        label9 = ttk.Label(self.root, text='Program/test status: ')
        label9.place(relx=0.25, rely=0.5, anchor=CENTER)
        
        self.status_label = ttk.Label(self.root, image = self.greylight)
        self.status_label.place(relx=0.5, rely=0.5, anchor=CENTER)
    
        self.root_complete_btn = ttk.Button(self.root, text='Complete Session', command=self.cmplt_btn_clicked)
        self.root_complete_btn.place(relx=0.4, rely=0.9, anchor=CENTER)
        
        self.root_suspend_btn = ttk.Button(self.root, text='Suspend Session', command=self.suspnd_btn_clicked)
        self.root_suspend_btn.place(relx=0.6, rely=0.9, anchor=CENTER)
        
        self.root.withdraw()
        
    def cmplt_btn_clicked(self):
        Tk.update(self.rootFrame)
        self.sessionComplete = True
        self.sessionOnGoing = False
    
    def suspnd_btn_clicked(self):
        self.sessionComplete = False
        self.sessionOnGoing = False
    
    def RefreshWindow(self):
        Tk.update(self.root)
        Tk.update_idletasks(self.root)
    
    def OpenWindow(self):
        self.sessionOnGoing = True

        self.root.deiconify()
        self.probeType.set(BM.currentBatch.probeType)
        self.currentBatch.set(BM.currentBatch.batchNumber)
        self.probesPassed.set(0)
        self.currentUser.set(SM.loggedInUser.name)
        self.deviceDetails.set(PM.ZND.deviceDetails)
        self.RLLimit = -1 #pass criteria for return loss measurement

        while(self.sessionOnGoing == True):
            Tk.update(self.root)
            if PM.ProbePresent() == True:
                self.status_label.configure(image=self.amberlight)
                ProbeIsProgrammed = PM.ProbeIsProgrammed()
                if ProbeIsProgrammed == False:
                    serialNumber = PM.ProgramProbe(BM.currentBatch.probeType)
                    if serialNumber == False:
                        tm.showerror('Programming Error', 'Unable to program\nPlease check U1')
                        self.status_label.configure(image=self.redlight)
                    else:
                        Tk.update(self.root)
                        results = PM.TestProbe(serialNumber, BM.currentBatch.batchNumber, self.currentUser.get())
                        if PM.ZND.get_marker_values()[0] < self.RLLimit and PM.ZND.get_marker_values()[1] < self.RLLimit:
                            BM.UpdateResults(results, BM.currentBatch.batchNumber)
                            self.probesPassed.set(self.probesPassed.get() + 1)
                            self.status_label.configure(image=self.greenlight)
                            Tk.update(self.root)
                        else:
                            self.status_label.configure(image=self.redlight)
                            tm.showerror('Return Loss Error', 'Check crystal connections')
                            Tk.update(self.root)

                else:
                    if tm.askyesno('Programmed Probe Detected', 'This probe is already programmed.\nDo you with to re-program and test?'):
                        serialNumber = PM.ProgramProbe(BM.currentBatch.probeType)
                        if serialNumber == False:
                            tm.showerror('Programming Error', 'Unable to program\nPlease check U1')
                            self.status_label.configure(image=self.redlight)
                            break
                        else:
                            results = PM.TestProbe(serialNumber, BM.currentBatch.batchNumber, self.currentUser.get())
                            if PM.ZND.get_marker_values()[0] < self.RLLimit and PM.ZND.get_marker_values()[1] < self.RLLimit:
                                BM.UpdateResults(results, BM.currentBatch.batchNumber)
                                self.probesPassed.set(self.probesPassed.get() + 1)
                                self.status_label.configure(image=self.greenlight)
                                Tk.update(self.root)
                            else:
                                self.status_label.configure(image=self.redlight)
                                tm.showerror('Return Loss Error', 'Check crystal connections')
                                Tk.update(self.root)
        
                while 1:
                    if PM.ProbePresent() == False:
                        PM.ClearAnalyzer()
                        self.status_label.configure(image=self.greylight)
                        break
                    
        #put something here to move csv?
        if self.sessionComplete == True:
            BM.CompleteBatch(BM.currentBatch)
            
        self.CloseWindow()

    def CloseWindow(self): 
        self.root.withdraw()
        SSW.OpenWindow()

class LogInWindow(object):
    def __init__(self):
        self.currentUser = StringVar()
        
        self.LW = Toplevel()
        self.LW.title('Login')
        self.LW.resizable(width=False, height=False)
        self.LWFrame = ttk.Frame(self.LW)
       
        #get window width and height
        ws = self.LW.winfo_screenwidth() 
        hs = self.LW.winfo_screenheight() 
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen and where it is placed
        self.LW.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.label_1 = ttk.Label(self.LW, text="Username")
        self.label_2 = ttk.Label(self.LW, text="Password")
        
        self.entry_1 = ttk.Entry(self.LW, textvariable=self.currentUser)
        self.entry_2 = ttk.Entry(self.LW, show="*")
        #self.entry_1.insert(END, 'Jack')
        #self.entry_2.insert(END, 'password')
        
        self.label_1.place(relx=0.4, rely=0.3, anchor=CENTER)
        self.label_2.place(relx=0.4, rely=0.4, anchor=CENTER)
        self.entry_1.place(relx=0.6, rely=0.3, anchor=CENTER)
        self.entry_2.place(relx=0.6, rely=0.4, anchor=CENTER)

        
        self.logbtn = ttk.Button(self.LW, text="Login", command =self._login_btn_clicked)
        self.logbtn.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.LW.bind('<Return>', self._login_btn_clicked)
        
        self.entry_1.focus_set()
    
    def _login_btn_clicked(self, *args):
        self.logbtn.config(command=ignore)
        
        #create a user object from the users input
        username = self.entry_1.get()
        password = self.entry_2.get()
        user = User(username,password)
        #self.entry_1.delete(0, 'end')
        self.entry_2.delete(0, 'end')
        #check to see if the details are valid 
        if SM.logIn(user):
            #SM.logIn(user)
            #tm.showinfo("Login info", "Welcome")
            self.LW.withdraw()
            SSW.OpenWindow()
        else:
            tm.showerror("Login error", "Incorrect username or password")
        self.logbtn.config(command=self._login_btn_clicked)
            
    def CloseWindow(self):
        self.LW.withdraw

    def OpenWindow(self):
        SM.loggedInUser = False
        self.LW.deiconify()
            
class SessionSelectWindow(object):
    def __init__(self):
        #create a choose session window
        self.SSW = Toplevel()
        self.SSW.title('Session type')
        self.SSW.resizable(width=False, height=False)
        SSWFrame = ttk.Frame(self.SSW)
        
        #get window width and height
        ws = self.SSW.winfo_screenwidth() 
        hs = self.SSW.winfo_screenheight() 
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen and where it is placed
        self.SSW.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        SSW_b1 = ttk.Button(self.SSW, text='Start a new session', command=self.b1_clicked, width = 30) 
        SSW_b1.place(relx=0.3, rely=0.3, anchor=CENTER)
        
        SSW_b2 = ttk.Button(self.SSW, text='Continue a previous session', command=self.b2_clicked , width = 30)
        SSW_b2.place(relx=0.7, rely=0.3, anchor=CENTER)
        
        SSW_b3 = ttk.Button(self.SSW, text='Log out', command=self.b3_clicked)
        SSW_b3.place(relx=0.3, rely=0.8, anchor=CENTER)
        
        self.SSW_b4 = ttk.Button(self.SSW, text='Edit Users', command=self.b4_clicked)
        self.SSW_b4.place(relx=0.7, rely=0.8, anchor=CENTER)
        
        self.SSW.withdraw()
        
    def b1_clicked(self):
        self.SSW.withdraw()
        NSW.OpenWindow()

    def b2_clicked(self):
        self.SSW.withdraw()
        CSW.OpenWindow()
        
    def b3_clicked(self):
        self.SSW.withdraw()
        LW.OpenWindow()
    
    def b4_clicked(self):
        self.SSW.withdraw()
        AW.OpenWindow()
    
    def CloseWindow(self):
        self.SSW.withdraw
    
    def OpenWindow(self):
        self.SSW.deiconify()
        if SM.loggedInUser.admin == False:
            self.SSW_b4.config(state=DISABLED)
        else:
            self.SSW_b4.config(state=NORMAL) 
           
class AdminWindow(object):
    def __init__(self):
        self.AW = Toplevel()
        self.AW.title('Admin')
        self.AW.resizable(width=False, height=False)
        AWFrame = ttk.Frame(self.AW)
        
        #get window width and height
        ws = self.AW.winfo_screenwidth() 
        hs = self.AW.winfo_screenheight() 
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen and where it is placed
        self.AW.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.AW_addUsrBtn = ttk.Button(self.AW, text='Add a new user', command=self.AW_addUsrBtn_clicked)
        self.AW_addUsrBtn.place(relx=0.3, rely=0.5, anchor=CENTER)
        
        self.AW_editUsrBtn = ttk.Button(self.AW, text='Edit a current user', command= self.AW_editUsrBtn_clicked)
        self.AW_editUsrBtn.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.AW_adminLogoutBtn = ttk.Button(self.AW, text='Finished', command= self.AW_adminFinishedBtn_clicked)
        self.AW_adminLogoutBtn.place(relx=0.7, rely=0.5, anchor=CENTER)
        
        self.AW.withdraw()
        
    def AW_addUsrBtn_clicked(self):
        self.AW.withdraw()
        AUW.OpenWindow()
    
    def AW_editUsrBtn_clicked(self):
        self.AW.withdraw()
        EUW.OpenWindow()
    
    def AW_adminFinishedBtn_clicked(self):
        self.AW.withdraw()
        SSW.OpenWindow()
        
    def OpenWindow(self):
        self.AW.deiconify()
    
    def CloseWindow(self):
        self.AW.withdraw() 
        
class EditUserWindow(object):
    def __init__(self): 
        global lstUsr
        self.EUW = Toplevel()
        self.EUW.title('Edit user')
        self.EUW.resizable(width=False, height=False)
        self.EUWFrame = ttk.Frame(self.EUW)
        
        #get window width and height
        ws = self.EUW.winfo_screenwidth() 
        hs = self.EUW.winfo_screenheight() 
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen and where it is placed
        self.EUW.geometry('%dx%d+%d+%d' % (w, h, x, y))
            
        self.Label1 = ttk.Label(self.EUW, text='Choose a user to edit')
        self.Label1.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.userListBox = Listbox(self.EUW, height=15, width=20)
        self.userListBox.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.CngPWrd_btn = ttk.Button(self.EUW, text='Change password', command=self.cngPwrd_btn_clicked)
        self.CngPWrd_btn.place(relx=0.8, rely=0.35, anchor=CENTER)
        
        self.delUsr_btn = ttk.Button(self.EUW, text='Delete', command=self.delUsr_btn_clicked)
        self.delUsr_btn.place(relx=0.8, rely=0.5, anchor=CENTER)
        
        self.finished_btn = ttk.Button(self.EUW, text = 'finished', command=self.finished_btn_clicked)
        self.finished_btn.place(relx=0.5, rely=0.9, anchor=CENTER)
        
        self.EUW.withdraw()
        
    def finished_btn_clicked(self):
        self.EUW.withdraw()
        AW.OpenWindow()
        
    def cngPwrd_btn_clicked(self): 
        lstid = self.userListBox.curselection()
        lstUsr = self.userListBox.get(lstid[0])
        SM.editingUser = SM.GetUserObject(lstUsr)
        self.EUW.withdraw()
        CPW.OpenWindow()

    def delUsr_btn_clicked(self):
        self.delUsr_btn.config(command=ignore)
        self.finished_btn.config(command=ignore)
        self.CngPWrd_btn.config(command=ignore)
        
        try:
            lstid = self.userListBox.curselection()
            lstUsr = self.userListBox.get(lstid[0])
            sure = tm.askyesno('Delete confirm', 'Are you sure you want to Delete this user?')
            if sure == True:
                if lstUsr != SM.loggedInUser.name:
                    SM.deleteUser(SM.GetUserObject(lstUsr))
                    self.RefreshUserList()
                else:
                    tm.showerror('Error', 'Cannot delete yourself')
        except:
            pass
        
        self.delUsr_btn.config(command=self.delUsr_btn_clicked)
        self.finished_btn.config(command=self.finished_btn_clicked)
        self.CngPWrd_btn.config(command=self.cngPwrd_btn_clicked)

        
    def RefreshUserList(self):
        #create a list of the current users using the dictionary of users
        userList = []
        for item in SM.GetUserList():
            userList.append(item.name)
        
        #clear the listbox
        self.userListBox.delete(0, END)
        
        #fill the listbox with the list of users
        for item in userList:
            self.userListBox.insert(END, item)
        
    def OpenWindow(self):
        self.RefreshUserList()
        self.EUW.deiconify()
    
    def CloseWindow(self):
        self.EUW.deiconify() 
    
class ChangePasswordWindow(object):
    def __init__(self):
        self.newPassword = StringVar()
        
        self.CPW = Toplevel()
        self.CPW.title('Change password')
        self.CPWFrame = ttk.Frame(self.CPW)
        self.CPW.resizable(width=False, height=False)
        
        #get window width and height
        ws = self.CPW.winfo_screenwidth() 
        hs = self.CPW.winfo_screenheight() 
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen and where it is placed
        self.CPW.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.CPWl1 = ttk.Label(self.CPW, text='Enter a new password')    
        self.CPWl1.place(relx=0.35, rely=0.3, anchor=CENTER)
        
        self.CPWe1 = ttk.Entry(self.CPW, textvariable=self.newPassword)
        self.CPWe1.place(relx=0.65, rely=0.3, anchor=CENTER)
        
        self.confm_btn = ttk.Button(self.CPW, text='Confirm', command=self.confm_btn_clicked)
        self.confm_btn.place(relx=0.5, rely=0.6, anchor=CENTER)
        
        self.CPW.withdraw()
        
    def confm_btn_clicked(self):
        SM.editingUser.password = self.newPassword.get()
        SM.updatePassword(SM.editingUser)
        tm.showinfo('Changed password', 'Password change successful')
        self.CPW.withdraw()
        EUW.OpenWindow()
        
    def OpenWindow(self):
        self.CPW.deiconify()
    
    def CloseWindow(self):
        self.CPW.deiconify() 
        
class AddUserWindow():
    def __init__(self):
        #add User screen 
        self.AUW = Toplevel()
        self.AUW.title('Add a new user')
        self.AUW.resizable(width=False, height=False)
        self.AUW.Frame = ttk.Frame(self.AUW)
        
        #get window width and height
        ws = self.AUW.winfo_screenwidth() 
        hs = self.AUW.winfo_screenheight() 
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen and where it is placed
        self.AUW.geometry('%dx%d+%d+%d' % (w, h, x, y))
         
        self.newusername = StringVar()
        self.newpassword = StringVar()
        self.isAdmin = StringVar()
         
        self.AUWl1 = ttk.Label(self.AUW, text='New user name: ')
        self.AUWl2 = ttk.Label(self.AUW, text='Password: ')
        #self.AUWl3 = ttk.Label(self.AUW, text='Admin: ')
        self.AUWe1 = ttk.Entry(self.AUW, textvariable=self.newusername)
        self.AUWe2 = ttk.Entry(self.AUW, textvariable=self.newpassword)
 
        self.rb_DP240 = ttk.Radiobutton(self.AUW, text='Admin', variable=self.isAdmin, value='admin')
        self.rb_DP240.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.AUWl1.place(relx=0.4, rely=0.25, anchor=CENTER)
        self.AUWl2.place(relx=0.4, rely=0.35, anchor=CENTER)
        self.AUWe1.place(relx=0.6, rely=0.25, anchor=CENTER)
        self.AUWe2.place(relx=0.6, rely=0.35, anchor=CENTER)
         
        self.confm_btn = ttk.Button(self.AUW, text="Confirm", command =self.confm_btn_clicked)
        self.confm_btn.place(relx=0.4, rely=0.8, anchor=CENTER)
          
        self.cancl_btn = ttk.Button(self.AUW, text="Cancel", command = self.cancl_btn_clicked)
        self.cancl_btn.place(relx=0.6, rely=0.8, anchor=CENTER)
        
        self.AUW.withdraw()
         
    def confm_btn_clicked(self):
        self.confm_btn.config(command=ignore)
        self.cancl_btn.config(command=ignore)
        
        #create user object
        admin = False
        if self.isAdmin.get() == 'admin':
            admin = True
        newUser = User(self.newusername.get(), self.newpassword.get(), admin )
        
        #try adding it to the list of users
        if SM.addUser(newUser):
            tm.showinfo('New User', 'New user added')
            self.AUW.withdraw()
            AW.OpenWindow()
        else:
            tm.showerror('Error', 'User already exsists')
        self.confm_btn.config(command=self.confm_btn_clicked)
        self.cancl_btn.config(command=self.cancl_btn_clicked)
    
    def cancl_btn_clicked(self):
        self.AUW.withdraw()
        AW.OpenWindow()
         
    def OpenWindow(self):
        self.AUW.deiconify()
     
    def CloseWindow(self):
        self.AUW.deiconify() 

class NewSessionWindow():
    def __init__(self):
        self.batchNumber = StringVar()
        self.probeType = StringVar()
        
        #Details Screen
        self.NSW = Toplevel()
        self.NSW.title('Test Details')
        self.NSW.resizable(width=False, height=False)
        self.NSW.grid_columnconfigure(0, weight=1)
        self.NSW.grid_rowconfigure(0,weight=1)
        
        #get window width and height
        ws = self.NSW.winfo_screenwidth() 
        hs = self.NSW.winfo_screenheight() 
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen and where it is placed
        self.NSW.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.NSWL1 = ttk.Label(self.NSW, text='Batch number: ')
        self.NSWL1.place(relx=0.3, rely=0.1, anchor=CENTER)
        
        self.NSWE1 = ttk.Entry(self.NSW, textvariable=self.batchNumber)
        self.NSWE1.place(relx=0.6, rely=0.1, anchor=CENTER)
        
        self.NSWL2 = ttk.Label(self.NSW, text='Probe type: ')
        self.NSWL2.place(relx=0.3, rely=0.5, anchor=CENTER)
        rely = 0.4
        self.rb_SDP30 = ttk.Radiobutton(self.NSW, text='SDP30', variable=self.probeType, value='SDP30')
        self.rb_SDP30.place(relx=0.6, rely=rely, anchor=CENTER)
        rely += 0.05
        self.rb_DP240 = ttk.Radiobutton(self.NSW, text='DP240', variable=self.probeType, value='DP240')
        self.rb_DP240.place(relx=0.6, rely=rely, anchor=CENTER)
        rely += 0.05
#         self.rb_DP12 = ttk.Radiobutton(self.NSW, text='DP12', variable=self.probeType, value='DP12')
#         self.rb_DP12.place(relx=0.595, rely=0.45, anchor=CENTER)
#         self.rb_DP6 = ttk.Radiobutton(self.NSW, text='DP6', variable=self.probeType, value='DP6')
#         self.rb_DP6.place(relx=0.59, rely=0.5, anchor=CENTER)
#         self.rb_I2C = ttk.Radiobutton(self.NSW, text='I2C', variable=self.probeType, value='I2C')
#         self.rb_I2C.place(relx=0.5905, rely=0.55, anchor=CENTER)
#         self.rb_I2P = ttk.Radiobutton(self.NSW, text='I2P', variable=self.probeType, value='I2P')
#         self.rb_I2P.place(relx=0.59, rely=0.60, anchor=CENTER)
#         self.rb_I2S = ttk.Radiobutton(self.NSW, text='I2S', variable=self.probeType, value='I2S')
#         self.rb_I2S.place(relx=0.584, rely=0.65, anchor=CENTER)
#         self.rb_KDP = ttk.Radiobutton(self.NSW, text='KDP', variable=self.probeType, value='KDP')
#         self.rb_KDP.place(relx=0.59, rely=0.70, anchor=CENTER)
        self.rb_Blank = ttk.Radiobutton(self.NSW, text='Blank', variable=self.probeType, value='Blank')
        self.rb_Blank.place(relx=0.6, rely=rely, anchor=CENTER)
        rely += 0.05
                
        self.confm_btn = ttk.Button(self.NSW, text='Confirm', command=self.confm_btn_clicked)
        self.confm_btn.place(relx=0.3, rely=0.9, anchor=CENTER)
        self.NSW.bind('<Return>', self.confm_btn_clicked) 
        
        self.cancl_btn = ttk.Button(self.NSW, text='Cancel', command=self.cancl_btn_clicked)
        self.cancl_btn.place(relx=0.6, rely=0.9, anchor=CENTER)
         
        self.NSW.withdraw()
        
    def cancl_btn_clicked (self):
        self.NSW.withdraw()
        SSW.OpenWindow()
        
    def confm_btn_clicked(self, *args):
        self.confm_btn.config(command=ignore)
        self.cancl_btn.config(command=ignore)
        self.NSWE1.config(state=DISABLED)
        self.rb_SDP30.config(state=DISABLED)
#         self.rb_DP240.config(state=DISABLED)
#         self.rb_DP12.config(state=DISABLED)
#         self.rb_DP6.config(state=DISABLED)
#         self.rb_I2C.config(state=DISABLED)
#         self.rb_I2P.config(state=DISABLED)
#         self.rb_I2S.config(state=DISABLED)
#         self.rb_KDP.config(state=DISABLED)

        
        #create batch object
        newBatch = Batch(self.batchNumber.get())
        newBatch.probeType = self.probeType.get()
            
        DAnswer = tm.askyesno('Confirm', 'Are batch details correct?')
        if DAnswer == True:
            #create the batch file
            if BM.CreateBatch(newBatch, SM.loggedInUser.name) == False:
                tm.showerror('Error', 'Batch number not unique')
            else:
                BM.currentBatch = newBatch
                self.NSW.withdraw()
                CW.OpenWindow()
        else:
            self.confm_btn.config(command=self.confm_btn_clicked)
            self.cancl_btn.config(command=self.cancl_btn_clicked)
            self.NSWE1.config(state=NORMAL)
            self.NSWE1.config(state=NORMAL)
            self.rb_DP240.config(state=NORMAL)
            self.rb_DP12.config(state=NORMAL)
            self.rb_DP6.config(state=NORMAL)
            self.rb_I2C.config(state=NORMAL)
            self.rb_I2P.config(state=NORMAL)
            self.rb_I2S.config(state=NORMAL)
            self.rb_KDP.config(state=NORMAL)
            
    def OpenWindow(self):
        self.NSW.deiconify()

    def CloseWindow(self):
        self.NSW.withdraw()
        
class ContinueSessionWindow(object):
    def __init__(self):
        self.CSW = Toplevel()
        self.CSW.title('Continue Session')
        self.CSW.resizable(width=False, height=False)
        self.CSWFrame = ttk.Frame(self.CSW)
        
        #get window width and height
        ws = self.CSW.winfo_screenwidth() 
        hs = self.CSW.winfo_screenheight() 
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen and where it is placed
        self.CSW.geometry('%dx%d+%d+%d' % (w, h, x, y))
            
        self.Label1 = ttk.Label(self.CSW, text='Choose a session to resume')
        self.Label1.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.sessionListBox = Listbox(self.CSW)
        self.sessionListBox.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.sessionListBox.config(height=14, width=20)
        
        self.continue_btn = ttk.Button(self.CSW, text='Continue Session', command=self.continue_btn_clicked)
        self.continue_btn.place(relx=0.4, rely=0.9, anchor=CENTER)
        
        self.cancel_btn = ttk.Button(self.CSW, text='Cancel', command=self.cancel_btn_clicked)
        self.cancel_btn.place(relx=0.6, rely=0.9, anchor=CENTER)

        self.CSW.withdraw()
    
    def RefreshSessionList(self):
        # #create a list of the current users using the dictionary of users
        sessionList = []
        for item in BM.GetAvailableBatches():
            sessionList.append(item)
        
        #clear the listbox
        self.sessionListBox.delete(0, END)
        
        #fill the listbox with the list of users
        for item in sessionList:
            self.sessionListBox.insert(END, item)
        
    def continue_btn_clicked(self):
        lstid = self.sessionListBox.curselection()
        
        try:
            lstBatch = self.sessionListBox.get(lstid[0])
            BM.currentBatch = BM.GetBatchObject(lstBatch)
            CW.OpenWindow()
            self.CSW.withdraw()
        except:
            tm.showerror('Error', 'Please select a batch from the batch list')

    def cancel_btn_clicked(self):
        self.CSW.withdraw()
        SSW.OpenWindow()
        
    def OpenWindow(self):
        self.RefreshSessionList()
        self.CSW.deiconify()
    
    def CloseWindow(self):
        self.CSW.withdraw()

class ConnectionWindow(object):
    def __init__(self):
        #define variables
        self.AnalyserIP = StringVar()
        self.comPort = StringVar()
        self.connectedToCom = False
        self.connectedToAnalyser = False
        
        #create the window and frame
        self.CW = Toplevel()
        self.CW.title('Connection Details')
        self.CW.resizable(width=False, height=False)
        self.CWFrame = ttk.Frame(self.CW)
        
        #get window width and height
        ws = self.CW.winfo_screenwidth() 
        hs = self.CW.winfo_screenheight() 
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen and where it is placed
        self.CW.geometry('%dx%d+%d+%d' % (w, h, x, y))

        #create the widgets
        self.label_1 = ttk.Label(self.CW, text="Analyser IP Address")
        self.label_2 = ttk.Label(self.CW, text="Probe Interface COM Port")
        
        self.entry_1 = ttk.Entry(self.CW, textvariable=self.AnalyserIP,)
        self.entry_2 = ttk.Entry(self.CW, textvariable=self.comPort, )
        self.entry_1.insert(END, '192.168.0.126')
        self.entry_2.insert(END, 'COM7')
        
        self.label_1.place(relx=0.4, rely=0.2, anchor=CENTER)
        self.label_2.place(relx=0.375, rely=0.4, anchor=CENTER)
        self.entry_1.place(relx=0.6, rely=0.2, anchor=CENTER)
        self.entry_2.place(relx=0.6, rely=0.4, anchor=CENTER)
        
        self.connectBtn = ttk.Button(self.CW, text="Connect", command =self._connect_btn_clicked)
        self.connectBtn.grid(row=2, column=1)
        self.connectBtn.place(relx=0.4, rely=0.8, anchor=CENTER)
        self.CW.bind('<Return>', self._connect_btn_clicked)
        
        self.cancelBtn = ttk.Button(self.CW, text="Cancel", command =self._cancel_btn_clicked)
        self.cancelBtn.place(relx=0.6, rely=0.8, anchor=CENTER)
        
        self.entry_1.focus_set()
        
        self.CW.withdraw()
    
    def _connect_btn_clicked(self, *args):
        cp =  self.comPort.get()
        ip = self.AnalyserIP.get()
        try:
            PM.ConnectToProbeInterface(cp)
            self.connectedToCom = True
        except:
            self.connectedToCom = False
            tm.showerror('Connection Error', 'Unable to connect to Probe Interface\nPlease check the COM Port is correct.')
              
        try:
            PM.SetVNAAddress(ip)
            PM.ZND.TestConnection()
            PM.ZND.Configure()
            self.connectedToAnalyser = True
        except:
            self.connectedToAnalyser = False
            tm.showerror('Connection Error', 'Unable to connect to Analyser\nPlease check the IP address is correct.')
  
        if self.connectedToAnalyser and self.connectedToCom == True:
            self.CW.withdraw()
            TPW.OpenWindow()


            
    def _cancel_btn_clicked(self, *args):
        self.CW.withdraw()
        SSW.OpenWindow()
            
    def CloseWindow(self):
        self.CW.withdraw

    def OpenWindow(self):
        self.CW.deiconify()
            
TPW = TestProgramWindow()
LW = LogInWindow()
SSW = SessionSelectWindow()
AW = AdminWindow()
EUW = EditUserWindow()
CPW = ChangePasswordWindow()
AUW = AddUserWindow()
NSW = NewSessionWindow()
CSW = ContinueSessionWindow()
CW = ConnectionWindow()
  
TPW.root.mainloop()
        
