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
import BatchManager
from BatchManager import Batch
import ProbeManager
import Sessions
import NanoZND
import ODMPlus
import ProbeTest as PT

BM = BatchManager.BatchManager()
PM = ProbeManager.ProbeManager()
NanoZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()

def ignore():
    return 'break'


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
            self, text='Cancel', command=lambda: controller.show_frame(SE.SessionSelectWindow))
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
            controller.show_frame(ConnectionWindow)
        except:
            tm.showerror('Error', 'Please select a batch from the batch list')


class ConnectionWindow(tk.Frame):
    def __init__(self, parent, controller):
        # define variables
        self.Monitor = StringVar()
        self.comPort = StringVar()
        self.AnalyserUSB = StringVar()
        self.file = StringVar()
        self.connectedToCom = False
        self.connectedToAnalyser = False
        self.odm_connection = False
        self.AnalyserUSB.set('COM4')
        self.comPort.set('COM3')
        self.Monitor.set('COM5')
        self.file.set(NanoZND.GetFileLocation())
        # create the window and frame
        tk.Frame.__init__(self, parent)

        # create the widgets
        self.label_1 = ttk.Label(self, text="ODM monitor port")
        self.label_2 = ttk.Label(self, text="Probe Interface Port")
        self.label_3 = ttk.Label(self, text="Analyser port")
        self.label_4 = ttk.Label(self, text="NanoZND file storage location")
        self.entry_1 = ttk.Entry(self, textvariable=self.Monitor,)
        self.entry_2 = ttk.Entry(self, textvariable=self.comPort, )
        self.entry_3 = ttk.Entry(self, textvariable=self.AnalyserUSB, )
        self.entry_4 = ttk.Entry(self, textvariable=self.file)
        
      

        self.label_1.place(relx=0.275, rely=0.2, anchor=CENTER)
        self.label_2.place(relx=0.275, rely=0.4, anchor=CENTER)
        self.label_3.place(relx=0.275, rely=0.3,anchor=CENTER)
        self.label_4.place(relx=0.25, rely=0.55, anchor=CENTER)
        self.entry_1.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.entry_2.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.entry_3.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.entry_4.place(relx=0.42, rely=0.55, width=250, anchor="w")
       
        self.browseBtn = ttk.Button(
            self, text="Browse", command=lambda: self._browse_btn_clicked(controller))
        self.browseBtn.grid(row=2, column=1)
        self.browseBtn.place(relx=0.8, rely=0.55, anchor=CENTER)
        self.bind('<Return>', self._connect_btn_clicked)
        
        self.connectBtn = ttk.Button(
            self, text="Connect", command=lambda: self._connect_btn_clicked(controller))
        self.connectBtn.grid(row=2, column=1)
        self.connectBtn.place(relx=0.4, rely=0.8, anchor=CENTER)
        self.bind('<Return>', self._connect_btn_clicked)

        self.cancelBtn = ttk.Button(
            self, text="Cancel",  command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.cancelBtn.place(relx=0.6, rely=0.8, anchor=CENTER)

        self.entry_1.focus_set()
        
      
    def _browse_btn_clicked(self, controller):
        filename = filedialog.askopenfilenames(initialdir = "/",title = "Select file",
                                               filetypes = ((".csv files","*.csv"),
                                                            ("all files","*.*")))     
        NanoZND.SetFileLocation(filename)
        self.file = NanoZND.GetFileLocation()
        print(self.file)
        
            

    def _connect_btn_clicked(self, controller):
        cp = self.comPort.get()
        odm = self.Monitor.get()
        usb = self.AnalyserUSB.get()
        
        
        try:
            NanoZND.SetAnalyserPort(usb)
            NanoZND.ReadAnalyserData()
            self.connectedToAnalyser = True
        except:
            self.connectedToAnalyser = False
            tm.showerror(
                'Connection Error', 'Unable to connect to Analyser Interface\nPlease check the nanoZND Port is correct or turned on.')
            
        try:
            PM.ConnectToProbeInterface(cp)
            self.connectedToCom = True
        except:
            self.connectedToCom = False
            tm.showerror(
                'Connection Error', 'Unable to connect to Probe Interface\nPlease check the Probe interface port is correct.')

        try:
           ODM.set_ODM_port_number(odm) 
           self.odm_connection = True
        except:
           self.odm_connection = False
           tm.showerror(
                'Connection Error', 'Unable to connect to Probe Interface\nPlease check the ODM port is correct and turned on.')
  

        if self.connectedToCom and self.connectedToAnalyser and self.odm_connection == True :
            controller.show_frame(PT.TestProgramWindow)