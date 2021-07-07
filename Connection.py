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
import ProbeManager
import pickle
import Sessions
import NanoZND
import ODMPlus
from time import gmtime, strftime
import ProbeTest as PT
import Sessions as SE
import DeviceConnect as DC
import os

BM = BatchManager.BatchManager()
PM = ProbeManager.ProbeManager()
NanoZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()

def ignore():
    return 'break'

class Connection(tk.Frame):
    def __init__(self, parent, controller):
        self.usb = ""
        self.odm = ""
        self.cp = ""
        self.is_admin = ""
        self.test = False
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
        
        self.label_9 = ttk.Label(self, text=" Please press connect in progress, and wait... ")
        
        self.label_9.place(relx=0.5, rely=0.5, anchor=CENTER) 
        
        self.confm_btn = tk.Button(self, text='Continue', padx=2, pady=3,
                                   width=25, command=lambda: self.test_connections(controller))
        self.confm_btn.place(relx=0.3, rely=0.8, anchor=CENTER)

        self.bind('<Return>', self.test_connections)
        self.text_area.insert('1.0', "\nPlease continue to the next screen..")      
            
        
            
    def refresh_window(self):
        
        try:
            with open('file.ptt', 'rb') as file:
                fileData = pickle.load(file)
                self.is_admin = fileData[1]
            file.close() 
            self.usb = fileData[4][2]
            self.odm = fileData[4][1]
            self.cp = fileData[4][0]
            self.test = True
            print("test in {}".format(self.test))
            
            
        except:
            self.text_area.delete('3.0','end')
            self.text_area.insert('3.0', "\nError in getting Connection data...")
      
        
    
    def test_connections(self, controller):
         # Test the connection to the analyser
        
        print("Trying connection")
        try:
            if NanoZND.GetAnalyserPortNumber(self.usb):
                self.connected_to_analyser = True
        except:
            tm.showerror(
                'Connection Error', 'Unable to connect to analyser\nPlease check the NanoVNA is on and connected.')
            controller.show_frame(DC.ConnectionWindow)
        # Test connection to the ODM monitor
        try:
            if ODM.checkODMPort(self.odm) == True:
                self.odm_connection = True  
            else:
                tm.showerror('ODM data errror','Chech ODM is running...')
                controller.show_frame(DC.ConnectionWindow)
        except:
            tm.showerror(
                'Connection Error', 'Unable to connect to ODM monitor\nPlease check the ODM is on and connected.')
        # test the connection to the probe interface  
        try:
            if PM.ConnectToProbeInterface(self.cp):
                self.connected_to_com = True
        except:
            tm.showerror(
                'Connection Error', 'Unable to connect to Probe Interface\nPlease check the Probe interface port is correct.')
            controller.show_frame(DC.ConnectionWindow)

        # Check if all connections are true
        if self.connected_to_analyser == True and self.odm_connection == True and self.connected_to_com == True:
            
            controller.show_frame(PT.TestProgramWindow)

    

