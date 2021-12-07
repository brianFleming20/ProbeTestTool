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
import ProbeTest as PT
import Sessions as SE
import DeviceConnect as DC
import datastore


BM = BatchManager.BatchManager()
PM = ProbeManager.ProbeManager()
ZND = NanoZND.NanoZND()
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
                                   width=20, command=lambda: self.test_connections(controller))
        self.confm_btn.place(relx=0.4, rely=0.8, anchor=CENTER)

        self.confm_btn = tk.Button(self, text='Cancel', padx=2, pady=3,
                                   width=20, command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.confm_btn.place(relx=0.6, rely=0.8, anchor=CENTER)

        self.bind('<Return>', self.test_connections)
        self.text_area.insert('1.0', "\nPlease continue to the next screen..")  

        ports = ["COM3","COM4","COM5"]
        read1 = ZND.get_vna_check() 
        read2 = ODM.get_monitor_port()
        DS.set_ODM_port(read2)

        for p in ports:
                if p == read1:
                    ports.remove(read1)
        DS.set_analyser_port(read1)

        for p in ports:
            if p == read2:   
                ports.remove(read2)
        DS.set_porbe_port(p)

        DS.set_porbe_port(ports[0])

        
       
   
    
    def test_connections(self, controller):
        # Check if all connections are true

        if self.test_probe_connection() == True and self.test_znd_connection() == True and self.test_odm_connection() == True:
 
            controller.show_frame(PT.TestProgramWindow)




    def test_probe_connection(self):
   
        if PM.ConnectToProbeInterface(DS.get_probe_port()) == True:
            return True       
        else:
            tm.showerror(
                'Connection Error', 'Unable to connect to Probe Interface\nPlease check the Probe interface port is correct.')
            
            return False



    def test_znd_connection(self):
      
        if ZND.get_analyser_port_number(DS.get_analyser_port()) == True:
            return True      
        else:
            tm.showerror(
                'Connection Error', 'Unable to connect to analyser\nPlease check the NanoVNA is on and connected.')
          
            return False



    def test_odm_connection(self):
        
        if ODM.checkODMPort(DS.get_ODM_port()) == True:
            return True       
        else:
                tm.showerror('ODM data errror','Chech ODM is running...')
               
                return False