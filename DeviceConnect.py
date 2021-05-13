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
import pickle
import Sessions
import NanoZND
import ODMPlus
import ProbeTest as PT
import Sessions as SE

BM = BatchManager.BatchManager()
PM = ProbeManager.ProbeManager()
NanoZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()

def ignore():
    return 'break'







class ConnectionWindow(tk.Frame):
    def __init__(self, parent, controller):
        # define variables
        self.Monitor = StringVar()
        self.comPort = StringVar()
        self.AnalyserUSB = StringVar()
        self.moveProbe = StringVar()
        self.file = StringVar()
        self.connectedToCom = False
        self.connectedToAnalyser = False
        self.odm_connection = False
        self.AnalyserUSB.set('COM4')
        self.comPort.set('COM3')
        self.Monitor.set('COM5')
        self.moveProbe.set('Not Set')
        self.file.set(NanoZND.GetFileLocation())
        # create the window and frame
        tk.Frame.__init__(self, parent, bg='#E0FFFF')

        # create the widgets
        self.label_1 = ttk.Label(self, text="ODM monitor port")
        self.label_2 = ttk.Label(self, text="Probe Interface Port")
        self.label_3 = ttk.Label(self, text="Analyser port")
        self.label_4 = ttk.Label(self, text="NanoZND file storage location")
        self.label_5 = ttk.Label(self, text="Probe Movement Interface")
        self.entry_1 = ttk.Entry(self, textvariable=self.Monitor,)
        self.entry_2 = ttk.Entry(self, textvariable=self.comPort, )
        self.entry_3 = ttk.Entry(self, textvariable=self.AnalyserUSB, )
        self.entry_4 = ttk.Entry(self, textvariable=self.file)
        self.entry_5 = ttk.Entry(self, textvariable=self.moveProbe)
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_8 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_8.place(relx=0.9, rely=0.1, anchor=CENTER)
        
      

        self.label_1.place(relx=0.275, rely=0.2, anchor=CENTER)
        self.label_2.place(relx=0.275, rely=0.4, anchor=CENTER)
        self.label_3.place(relx=0.275, rely=0.3,anchor=CENTER)
        self.label_4.place(relx=0.25, rely=0.7, anchor=CENTER)
        self.label_5.place(relx=0.275, rely=0.5, anchor=CENTER)
        self.entry_1.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.entry_2.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.entry_3.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.entry_4.place(relx=0.42, rely=0.7, width=250, anchor="w")
        self.entry_5.place(relx=0.5, rely=0.5, anchor=CENTER)
       
        self.browseBtn = ttk.Button(
            self, text="Browse", command=lambda: self._browse_btn_clicked(controller))
        self.browseBtn.grid(row=2, column=1)
        self.browseBtn.place(relx=0.8, rely=0.7, anchor=CENTER)
        self.bind('<Return>', self._connect_btn_clicked)
        
        self.connectBtn = ttk.Button(
            self, text="Connect", command=lambda: self._connect_btn_clicked(controller))
        self.connectBtn.grid(row=2, column=1)
        self.connectBtn.place(relx=0.4, rely=0.82, anchor=CENTER)
        self.bind('<Return>', self._connect_btn_clicked)

        self.cancelBtn = ttk.Button(
            self, text="Cancel",  command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.cancelBtn.place(relx=0.6, rely=0.82, anchor=CENTER)

        self.entry_1.focus_set()
        
      
    def _browse_btn_clicked(self, controller):
        filename = filedialog.askopenfilenames(initialdir = "/",title = "Select file",
                                               filetypes = ((".csv files","*.csv"),
                                                            ("all files","*.*")))     
        NanoZND.SetFileLocation(filename)
        self.file = NanoZND.GetFileLocation()
        
        
            

    def _connect_btn_clicked(self, controller):
        cp = self.comPort.get()
        odm = self.Monitor.get()
        usb = self.AnalyserUSB.get()
        session_data = []
        connection_data = []
        try:
            with open('file.ptt', 'rb') as file:
      
            # Call load method to deserialze
                myvar = pickle.load(file)
            session_data.extend(myvar)
        
            file.close()
        except:
            with open('file.ptt', 'wb') as file:
                pickle.dump(session_data, file)
            file.close()
            self._connect_btn_clicked(controller)
        
        connection_data.append(cp)
        connection_data.append(odm)
        connection_data.append(usb)
        session_data.append(connection_data)
        
        with open('file.ptt', 'wb') as file:
                pickle.dump(session_data, file)
        file.close()
        
        
            
        
        try:
            if ODM.checkODMPort(odm):
                
                self.odm_connection = True
        except:
            tm.showerror(
                'Connection Error', 'Unable to connect to ODM Monitor\nPlease check the ODM is on and connected.')
           
        try:
            PM.ConnectToProbeInterface(cp)
            self.connectedToCom = True
        except:
            self.connectedToCom = False
            tm.showerror(
                'Connection Error', 'Unable to connect to Probe Interface\nPlease check the Probe interface port is correct.')

      
  
        

        if self.connectedToCom and self.odm_connection == True :
            controller.show_frame(PT.TestProgramWindow)