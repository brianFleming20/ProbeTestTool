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
import Connection
import datastore
import os

BM = BatchManager.BatchManager()
PM = ProbeManager.ProbeManager()
NanoZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
CO = Connection
DS = datastore.DataStore()

def ignore():
    return 'break'


class ConnectionWindow(tk.Frame):
    def __init__(self, parent, controller):
  
        self.is_admin = ""
        
        # create the window and frame
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
      
        self.label_9 = ttk.Label(self, text=" Please press connect to continue... ")
        
        self.label_9.place(relx=0.5, rely=0.5, anchor=CENTER)     
        self.connectBtn = ttk.Button(
                self, text="Connect", command=lambda: self._connect_btn_clicked(controller))
        self.connectBtn.grid(row=2, column=1)
        self.connectBtn.place(relx=0.4, rely=0.82, anchor=CENTER)
        self.bind('<Return>', self._connect_btn_clicked)

        self.cancelBtn = ttk.Button(
                self, text="Cancel",  command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.cancelBtn.place(relx=0.6, rely=0.82, anchor=CENTER)
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)

          
    def refresh_window(self):
        try:
     
            admin_data = DS.get_user()
            self.is_admin = admin_data[1]
        except:
            self.text_area.delete('3.0','end')
            self.text_area.insert('3.0', "\nError in getting Admin data...")
        
        self.text_area.config(state=NORMAL)   
        self.text_area.insert('2.0',admin_data[0])
        self.text_area.insert('2.0','\n\nPlease connect the external devices\nand progress to the testing screen.')
        self.text_area.config(state=DISABLED)
        
            

    def _connect_btn_clicked(self, controller):
      
        self.is_admin = DS.get_user_admin_status()
     
        if self.is_admin == True:
             controller.show_frame()
        else:
            controller.show_frame(CO.Connection)
   
            
        self.text_area.config(state=NORMAL)  
 
        self.text_area.insert('1.0','Continue to check device connections...')
 
        self.text_area.config(state=DISABLED)   
        
        
            
            
class ConnectionAdmin(tk.Frame):
    def __init__(self, parent, controller):
        self.monitor = StringVar()
        self.com_port = StringVar()
        self.analyser_usb = StringVar()
        self.move_probe = StringVar()
        self.analyser_usb.set('COM4')
        self.com_port.set('COM3')
        self.monitor.set('COM5')
        self.move_probe.set('Not Set') 
        
        tk.Frame.__init__(self, parent, bg='#E0FFFF')   
        self.label_1 = ttk.Label(self, text="ODM monitor port")
        self.label_2 = ttk.Label(self, text="Probe Interface Port")
        self.label_3 = ttk.Label(self, text="Analyser port")
        
        self.label_5 = ttk.Label(self, text="Probe Movement Interface")
        self.entry_1 = ttk.Entry(self, textvariable=self.monitor,)
        self.entry_2 = ttk.Entry(self, textvariable=self.com_port, )
        self.entry_3 = ttk.Entry(self, textvariable=self.analyser_usb, )
        
        self.entry_5 = ttk.Entry(self, textvariable=self.move_probe)
        self.deltex = (PhotoImage(file="images/deltex.gif"))
        self.label_8 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_8.place(relx=0.9, rely=0.2, anchor=CENTER)
        
        self.label_1.place(relx=0.275, rely=0.3, anchor=CENTER)
        self.label_2.place(relx=0.275, rely=0.5, anchor=CENTER)
        self.label_3.place(relx=0.275, rely=0.4,anchor=CENTER)
        
        self.label_5.place(relx=0.275, rely=0.6, anchor=CENTER)
        self.entry_1.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.entry_2.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.entry_3.place(relx=0.5, rely=0.4, anchor=CENTER)
        
        self.entry_5.place(relx=0.5, rely=0.6, anchor=CENTER)
        
        
        self.connectBtn = ttk.Button(
            self, text="Connect", command=lambda: self._connect_btn_clicked(controller))
        self.connectBtn.grid(row=2, column=1)
        self.connectBtn.place(relx=0.4, rely=0.82, anchor=CENTER)
        self.bind('<Return>', self._connect_btn_clicked)

        self.cancelBtn = ttk.Button(
            self, text="Cancel",  command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.cancelBtn.place(relx=0.6, rely=0.82, anchor=CENTER)
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
       
        
        def refresh_window(self):
            user_data = []
            user_data.append(DS.get_user())
            self.is_admin = user_data[1]
 
        
            self.text_area.config(state=NORMAL)   
            self.text_area.insert('2.0',user_data[0])
            self.text_area.insert('2.0','\n\nPlease check any external devices\nand press continue...')
            self.text_area.config(state=DISABLED)
            

    def _connect_btn_clicked(self, controller):
        cp = self.com_port.get()
        odm = self.monitor.get()
        usb = self.analyser_usb.get()
        session_data = []
        connection_data = []
        
        
           
        connection_data.append(cp)
        connection_data.append(odm)
        connection_data.append(usb)
        session_data.append(connection_data)
     
        DS.add_to_batch_file(session_data)
        
        controller.show_frame(CO.Connection)
            