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
import datastore
import os

BM = BatchManager.BatchManager()
PM = ProbeManager.ProbeManager()
NanoZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
DS = datastore.DataStore()

def ignore():
    return 'break'

class Connection(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        
      
        
        # self.is_admin = ""
        self.connected_to_analyser = False
        self.odm_connection = False
        self.connected_to_com = False
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
        
        self.label_9 = ttk.Label(self, text=" Please press connect in progress, and wait... ")
        
        self.label_9.place(relx=0.5, rely=0.5, anchor=CENTER) 
        
        self.confm_btn = tk.Button(self, text='Continue', padx=2, pady=3,
                                   width=25, command=lambda: self.test_connections(controller))
        self.confm_btn.place(relx=0.5, rely=0.8, anchor=CENTER)

        self.bind('<Return>', self.test_connections)
        self.text_area.insert('1.0', "\nPlease continue to the next screen..")      
            
        
            
    def refresh_window(self):
        connect_data = []
        
        connect_data.extend(DS.get_ports())
       
        self.cp = connect_data[0]
        self.analyser = connect_data[1]
        self.odm = connect_data[2]
        
        
       
       
    
    def test_connections(self, controller):
         # Test the connection to the analyser#
       
      
        if NanoZND.GetAnalyserPortNumber(self.analyser) == True:
                self.connected_to_analyser = True
        else:
            tm.showerror(
                'Connection Error', 'Unable to connect to analyser\nPlease check the NanoVNA is on and connected.')
           
        # Test connection to the ODM monitor
    
        if ODM.checkODMPort(self.odm) == True:
                self.odm_connection = True  
        else:
                tm.showerror('ODM data errror','Chech ODM is running...')
     
        
        if PM.ConnectToProbeInterface(self.cp) == True:
                self.connected_to_com = True
        else:
            tm.showerror(
                'Connection Error', 'Unable to connect to Probe Interface\nPlease check the Probe interface port is correct.')
            
        
        # Check if all connections are true
        if self.connected_to_analyser == True and self.odm_connection == True and self.connected_to_com == True:
            
            controller.show_frame(PT.TestProgramWindow)

    

