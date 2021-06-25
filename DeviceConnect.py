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

BM = BatchManager.BatchManager()
PM = ProbeManager.ProbeManager()
NanoZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()

def ignore():
    return 'break'







class ConnectionWindow(tk.Frame):
    def __init__(self, parent, controller):
        # define variables
        self.monitor = StringVar()
        self.com_port = StringVar()
        self.analyser_usb = StringVar()
        self.move_probe = StringVar()
        self.connected_to_com = False
        self.connected_to_analyser = False
        self.odm_connection = False
        self.analyser_usb.set('COM4')
        self.com_port.set('COM3')
        self.monitor.set('COM5')
        self.move_probe.set('Not Set')
        self.is_admin = []
        
        
        
        # create the window and frame
        tk.Frame.__init__(self, parent, bg='#E0FFFF')

        # create the widges
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
        time_now = strftime("%H:%M:%p", gmtime())
        
    def refresh_window(self):
        try:
            with open('file.ptt', 'rb') as file:
                fileData = pickle.load(file)
                self.is_admin.append(fileData[1])
            
            file.close()  
        except:
            self.text_area.delete('3.0','end')
            self.text_area.insert('3.0', "\nError in getting Admin data...")
        
        
        if True in self.is_admin:
            self.label_1 = ttk.Label(self, text="ODM monitor port")
            self.label_2 = ttk.Label(self, text="Probe Interface Port")
            self.label_3 = ttk.Label(self, text="Analyser port")
        
            self.label_5 = ttk.Label(self, text="Probe Movement Interface")
            self.entry_1 = ttk.Entry(self, textvariable=self.monitor,)
            self.entry_2 = ttk.Entry(self, textvariable=self.com_port, )
            self.entry_3 = ttk.Entry(self, textvariable=self.analyser_usb, )
        
            self.entry_5 = ttk.Entry(self, textvariable=self.move_probe)
            self.deltex = (PhotoImage(file="deltex.gif"))
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

            self.entry_1.focus_set()
        else:
            self.label_9 = ttk.Label(self, text=" Please press connect to continue. ")
            self.label_9.place(relx=0.5, rely=0.5, anchor=CENTER)
            
        self.text_area.insert('2.0',fileData[0])
        self.text_area.insert('2.0','\n\nPlease connect the external devices\nand progress to the testing screen.')
        self.text_area.config(state=DISABLED)
            

    def _connect_btn_clicked(self, controller):
        cp = self.com_port.get()
        odm = self.monitor.get()
        usb = self.analyser_usb.get()
        session_data = []
        connection_data = []
        
        try:
            with open('file.ptt', 'rb') as file:
                myvar = pickle.load(file)
                session_data.extend(myvar)
                self.is_admin.append(myvar)

            file.close()
        
        
            connection_data.append(cp)
            connection_data.append(odm)
            connection_data.append(usb)
            session_data.append(connection_data)
        except:
            self.text_area.delete('3.0','end')
            self.text_area.insert('3.0', "\nError in getting batch data in Connections...")
        
        try:    
            with open('file.ptt', 'wb') as file:
                pickle.dump(session_data, file)
                
            file.close()
        except:
            self.text_area.delete('3.0','end')
            self.text_area.insert('3.0', "\nError in writting batch data in connections...")
        
        try:
            if NanoZND.GetAnalyserPortNumber(usb):
                self.connected_to_analyser = True
        except:
            tm.showerror(
                'Connection Error', 'Unable to connect to analyser\nPlease check the NanoVNA is on and connected.')
           
        try:
            if ODM.checkODMPort(odm):
                
                self.odm_connection = True
        except:
            tm.showerror(
                'Connection Error', 'Unable to connect to ODM monitor\nPlease check the ODM is on and connected.')
           
        try:
            PM.ConnectToProbeInterface(cp)
            self.connected_to_com = True
        except:
            tm.showerror(
                'Connection Error', 'Unable to connect to Probe Interface\nPlease check the Probe interface port is correct.')

      
  
        

        if self.connected_to_com and self.odm_connection == True and self.connected_to_analyser == True :
            controller.show_frame(PT.TestProgramWindow)