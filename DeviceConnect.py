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
        self.Monitor = StringVar()
        self.comPort = StringVar()
        self.AnalyserUSB = StringVar()
        self.moveProbe = StringVar()
        self.connectedToCom = False
        self.connectedToAnalyser = False
        self.odm_connection = False
        self.AnalyserUSB.set('COM4')
        self.comPort.set('COM3')
        self.Monitor.set('COM5')
        self.moveProbe.set('Not Set')
        self.isAdmin = []
        self.name = []
        
        
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
        
        self.textArea = tk.Text(self, height=5, width=38)
        self.textArea.place(relx=0.25, rely=0.15, anchor=CENTER)
        timeNow = strftime("%H:%M:%p", gmtime())
        
        if "AM" in timeNow :
            self.textArea.insert('1.0','Good Morning ', font=('bold',12))
            
        else:
            self.textArea.insert('1.0','Good Afternoon ')
        
        
      
    
    def refresh_window(self):
        with open('file.ptt', 'rb') as file:
            myvar = pickle.load(file)
            self.isAdmin.append(myvar[1])
            self.name.append(myvar[0])
        file.close()  
         
        if True in self.isAdmin:
            self.label_1 = ttk.Label(self, text="ODM monitor port")
            self.label_2 = ttk.Label(self, text="Probe Interface Port")
            self.label_3 = ttk.Label(self, text="Analyser port")
        
            self.label_5 = ttk.Label(self, text="Probe Movement Interface")
            self.entry_1 = ttk.Entry(self, textvariable=self.Monitor,)
            self.entry_2 = ttk.Entry(self, textvariable=self.comPort, )
            self.entry_3 = ttk.Entry(self, textvariable=self.AnalyserUSB, )
        
            self.entry_5 = ttk.Entry(self, textvariable=self.moveProbe)
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
        self.textArea.insert('2.0',self.name)
        self.textArea.insert('2.0','\n\nPlease connect the external devices\nand progress to the testing screen.')
        self.textArea.config(state=DISABLED)
            

    def _connect_btn_clicked(self, controller):
        cp = self.comPort.get()
        odm = self.Monitor.get()
        usb = self.AnalyserUSB.get()
        session_data = []
        connection_data = []
        
        
        with open('file.ptt', 'rb') as file:
            myvar = pickle.load(file)
            session_data.extend(myvar)
            self.isAdmin.append(myvar)

        file.close()
        
        
        connection_data.append(cp)
        connection_data.append(odm)
        connection_data.append(usb)
        session_data.append(connection_data)
        
        with open('file.ptt', 'wb') as file:
                pickle.dump(session_data, file)
                
        file.close()
       
        
        try:
            if NanoZND.GetAnalyserPortNumber(usb):
                self.connectedToAnalyser = True
        except:
            tm.showerror(
                'Connection Error', 'Unable to connect to analyser\nPlease check the NanoVNA is on and connected.')
           
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
            tm.showerror(
                'Connection Error', 'Unable to connect to Probe Interface\nPlease check the Probe interface port is correct.')

      
  
        

        if self.connectedToCom and self.odm_connection == True and self.connectedToAnalyser == True :
            controller.show_frame(PT.TestProgramWindow)