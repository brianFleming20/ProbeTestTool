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

import NanoZND
import ODMPlus
from time import gmtime, strftime
import ProbeTest
import Sessions as SE
import DeviceConnect as DC
import datastore
import ProbeInterface


BM = BatchManager.BatchManager()
PM = ProbeManager.ProbeManager()
ZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
DS = datastore.DataStore()
PT = ProbeTest
PF = ProbeInterface.PRI()

def ignore():
    return 'break'

class Connection(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        
        # self.is_admin = ""
        self.znd_working = False
        self.probe_working = False
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
        
        self.label_9 = ttk.Label(self, text=" Press 'Continue' and wait to connect sensors... ")
        self.label_9.config(font=("Courier", 14))
        self.label_9.place(relx=0.5, rely=0.5, anchor=CENTER) 
        
        self.confm_btn = tk.Button(self, text='Continue', padx=2, pady=3,
                                   width=20, command=lambda: self.test_connections(controller))
        self.confm_btn.place(relx=0.4, rely=0.8, anchor=CENTER)
        self.confm_btn.config(state=NORMAL)

        tk.Button(self, text='Cancel', padx=2, pady=3,
                    width=20, command=lambda: 
                        controller.show_frame(SE.SessionSelectWindow)).place(relx=0.6, 
                            rely=0.8, anchor=CENTER)

        self.bind('<Return>', self.test_connections)
        self.text_area.insert('1.0', "\nPlease continue to the next screen..")  
        
        
    def test_comms(self):

        ports = ["COM3","COM4","COM5"]
        read1 = ZND.get_vna_check(ports) 
        read3 = PF.check_probe_connection(ports)
        
        for p in ports:
            if read1 == p:
                ports.remove(read1)
                self.znd_working = True
                DS.set_analyser_port(read1)

        for p in ports:
            if p == read3:   
                ports.remove(read3)
                self.probe_working = True
                DS.set_porbe_port(read3)

        DS.set_ODM_port(ports[0])
        
        

    def test_connections(self, controller):
        while PM.ProbePresent() == True:
            self.confm_btn.config(state=DISABLED)
            tm.showerror('Connection Error','Remove the inserted probe from the tester.')
            
        # Check if all connections are true
        self.confm_btn.config(state=NORMAL) 
        self.test_comms()
        if self.probe_working == True and self.znd_working == True and self.test_odm_connection() == True:
            controller.show_frame(PT.TestProgramWindow)
        else:
            controller.show_frame(SE.SessionSelectWindow)



    def test_odm_connection(self):
        connected = ODM.get_monitor_port()
        if connected == "not_connected":
            tm.showerror('ODM data errror','Check ODM is working...')
            return False
        else:
            return True       
          