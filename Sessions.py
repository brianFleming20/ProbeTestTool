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
import BatchManager
from BatchManager import Batch
import SecurityManager
from SecurityManager import User
import UserLogin
import DeviceConnect as DC


BM = BatchManager.BatchManager()
SM = SecurityManager.SecurityManager()


def ignore():
    return 'break'

BTN_WIDTH = 30


class SessionSelectWindow(tk.Frame):
    def __init__(self, parent, controller):
        # create a choose session window
        tk.Frame.__init__(self, parent)
        from UserLogin import LogInWindow, AdminWindow
        
        self.SSW_b1 = ttk.Button(self, text='Start a new session', command=lambda: controller.show_frame(
            NewSessionWindow), width=BTN_WIDTH)
        self.SSW_b1.place(relx=0.3, rely=0.3, anchor=CENTER)

        self.SSW_b2 = ttk.Button(self, text='Continue a previous session',
                                 command=lambda: controller.show_frame(ContinueSessionWindow), width=BTN_WIDTH)
        self.SSW_b2.place(relx=0.7, rely=0.3, anchor=CENTER)

        self.SSW_b3 = ttk.Button(self, text='Log Out', command=lambda: controller.show_frame(
            LogInWindow), width=BTN_WIDTH)
        self.SSW_b3.place(relx=0.3, rely=0.6, anchor=CENTER)

        self.SSW_b4 = ttk.Button(self, text='Edit Users', command=lambda: controller.show_frame(
            AdminWindow), width=BTN_WIDTH)
        self.SSW_b4.place(relx=0.7, rely=0.6, anchor=CENTER)

        exitBtn = ttk.Button(
            self, text='Exit', command=lambda: controller.show_frame(LogInWindow), width=BTN_WIDTH)
        exitBtn.place(relx=0.5, rely=0.8, anchor=CENTER)

    def refresh_window(self):
        admin_user = SM.get_user_admin_status()
        print("user admin {}".format(admin_user))
        if SM.loggedInUser.admin == False:
            self.SSW_b4.config(state=DISABLED)
        else:
            self.SSW_b4.config(state=NORMAL)

        if len(BM.GetAvailableBatches()) == 0:
            self.SSW_b2.config(state=DISABLED)
        else:
            self.SSW_b2.config(state=NORMAL)
            
            
class NewSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        self.batchNumber = StringVar()
        self.probeType = StringVar()

        # Details Screen
        tk.Frame.__init__(self, parent)

        batch_frame = tk.Frame(self, pady=3)
        probe_type_frame = tk.Frame(self, pady=3)
        button_frame = tk.Frame(self, pady=3)

        #batch_frame.grid(row=0, sticky="ew")
        probe_type_frame.grid(row=1, column=1, sticky="news")

        self.NSWL1 = ttk.Label(self, text='Batch number: ', justify=RIGHT)
        self.NSWL1.grid(row=0, column=0)

        self.NSWE1 = ttk.Entry(self, textvariable=self.batchNumber)
        self.NSWE1.grid(row=0, column=1)

        self.NSWL2 = ttk.Label(self, text='Select Probe Type: ')
        self.NSWL2.grid(row=1, column=0)

        tk.Radiobutton(probe_type_frame, text='SDP30 [Suprasternal Probe]',
                       variable=self.probeType, value='SDP30').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='DP240 [Doppler 10 Day]',
                       variable=self.probeType, value='DP240').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='DP12 [Doppler 12 Hour]',
                       variable=self.probeType, value='DP12').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='DP6 [Doppler 6 Hour]',
                       variable=self.probeType, value='DP6').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='I2C',
                       variable=self.probeType, value='I2C').pack(fill=X, ipady=5)
#        tk.Radiobutton(probe_type_frame, text='I2P', variable=self.probeType, value='I2P').pack(fill = X, ipady = 5)
#        tk.Radiobutton(probe_type_frame, text='I2S', variable=self.probeType, value='I2S').pack(fill = X, ipady = 5)
#        tk.Radiobutton(probe_type_frame, text='KDP', variable=self.probeType, value='KDP').pack(fill = X, ipady = 5)
        tk.Radiobutton(probe_type_frame, text='Blank',
                       variable=self.probeType, value='Blank').pack(fill=X, ipady=5)

        self.confm_btn = tk.Button(self, text='Confirm', padx=3, pady=3,
                                   width=BTN_WIDTH, command=lambda: self.confm_btn_clicked(controller))
        self.confm_btn.grid(row=2, column=0)

        self.cancl_btn = tk.Button(self, text='Cancel', padx=3, pady=3, width=BTN_WIDTH,
                                   command=lambda: controller.show_frame(SessionSelectWindow))
        self.cancl_btn.grid(row=2, column=1)

        self.bind('<Return>', self.confm_btn_clicked)

    def confm_btn_clicked(self, controller):
        # create batch object
        from Main import ConnectionWindow
        newBatch = Batch(self.batchNumber.get())
        newBatch.probeType = self.probeType.get()

        DAnswer = tm.askyesno('Confirm', 'Are batch details correct?')
        if DAnswer == True:
            # create the batch file
            if BM.CreateBatch(newBatch, SM.loggedInUser.name) == False:
                tm.showerror('Error', 'Batch number not unique')
            else:
                BM.currentBatch = newBatch
                self.NSWE1.delete(0, 'end')
                controller.show_frame(ConnectionWindow)


class ContinueSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        

        self.Label1 = ttk.Label(self, text='Choose a session to resume')
        self.Label1.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.sessionListBox = Listbox(self)
        self.sessionListBox.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.sessionListBox.config(height=14, width=20)

        self.continue_btn = ttk.Button(
            self, text='Continue Session', command=lambda: self.continue_btn_clicked(controller))
        self.continue_btn.place(relx=0.4, rely=0.9, anchor=CENTER)

        self.cancel_btn = ttk.Button(
            self, text='Cancel', command=lambda: controller.show_frame(SessionSelectWindow))
        self.cancel_btn.place(relx=0.6, rely=0.9, anchor=CENTER)

        self.refresh_window()

    def refresh_window(self):
        # #create a list of the current users using the dictionary of users
        sessionList = []
        for item in BM.GetAvailableBatches():
            sessionList.append(item)

        # clear the listbox
        self.sessionListBox.delete(0, END)

        # fill the listbox with the list of users
        for item in sessionList:
            self.sessionListBox.insert(END, item)

    def continue_btn_clicked(self, controller):
     
        lstid = self.sessionListBox.curselection()

        try:
            lstBatch = self.sessionListBox.get(lstid[0])
            BM.currentBatch = BM.GetBatchObject(lstBatch)
            controller.show_frame(DC.ConnectionWindow)
        except:
            tm.showerror('Error', 'Please select a batch from the batch list')
