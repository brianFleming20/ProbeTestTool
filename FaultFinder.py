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
import ProbeTest as PT
import ProbeManager
import BatchManager
from ProbeManager import Probe
from ProbeManager import ProbeManager
import codecs
import PI
import NanoZND
import ODMPlus
import pickle

from time import gmtime, strftime
PM = ProbeManager()
BM = BatchManager.BatchManager()
NanoZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
PI = PI.PI()


def ignore():
    return 'break'

BTN_WIDTH = 25

class FaultFindWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        
        # Set up variavles
        self.currentBatch = StringVar()
        self.currentUser = StringVar()
        self.probeType = StringVar()
        self.deviceDetails = StringVar()
        self.serialNumber = StringVar()
        self.readSerialNumber = StringVar()
        self.analyserData = StringVar()
        self.action = StringVar()
        self.analyserResults = []
        self.SD_data = IntVar()
        self.FTc_data = IntVar()
        self.PV_data = IntVar()
        self.device = "Not connected to analyser"
        
        # Import images
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        
        self.textArea = tk.Text(self, height=5, width=40)
        self.textArea.place(relx=0.25, rely=0.15, anchor=CENTER)
        self.textArea.delete('1.0','end')
        
        ttk.Label(self, text='Batch number: ').place(
            relx=0.1, rely=0.3, anchor='w')
        ttk.Label(self, textvariable=self.currentBatch, relief=SUNKEN, font="bold",
                 width=10).place(relx=0.2, rely=0.3, anchor='w')

        ttk.Label(self, text='Probe type: ').place(
            relx=0.1, rely=0.38, anchor='w')
        ttk.Label(self, textvariable=self.probeType, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.2, rely=0.38, anchor='w')
        
        ttk.Label(self, text='Connected to: ').place(
            relx=0.1, rely=0.44, anchor='w')
        ttk.Label(self, textvariable=self.deviceDetails, relief=SUNKEN,
                  width=30).place(relx=0.2, rely=0.44, anchor='w')
        ttk.Label(self, textvariable=self.analyserData, relief=SUNKEN,
                  width=40).place(relx=0.3, rely=0.48, anchor='w')
        
        ttk.Label(self, text='Serial Number: ').place(
            relx=0.78, rely=0.18, anchor='w')
        ttk.Label(self, text='From file: ').place(
            relx=0.73, rely=0.25, anchor='w')
        ttk.Label(self, text='From Probe: ').place(
            relx=0.73, rely=0.25, anchor='w')
        ttk.Label(self, textvariable=self.serialNumber, relief=SUNKEN,
                  width=30).place(relx=0.7, rely=0.25, anchor='w')
        ttk.Label(self, textvariable=self.readSerialNumber, relief=SUNKEN,
                  width=30).place(relx=0.7, rely=0.3, anchor='w')
        
        ttk.Label(self, text="Probe parameter data").place(
            relx=0.7, rely=0.42, anchor="w")
        ttk.Label(self, text="SD").place(relx=0.70, rely=0.46, anchor="w")
        ttk.Label(self, text="FTc").place(relx=0.77, rely=0.46, anchor="w")
        ttk.Label(self, text="PV").place(relx=0.85, rely=0.46, anchor="w")
        ttk.Label(self, textvariable=self.SD_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.69, rely=0.51, anchor='w')
        ttk.Label(self, textvariable=self.FTc_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.76, rely=0.51, anchor='w')
        ttk.Label(self, textvariable=self.PV_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.84, rely=0.51, anchor='w')
        
        ttk.Label(self, text='Action: ').place(relx=0.1, rely=0.55, anchor='w')
        ttk.Label(self, textvariable=self.action, background='#99c2ff',
                  width=40, relief=GROOVE).place(relx=0.2, rely=0.55, anchor='w')
        
        self.cancel_btn = ttk.Button(
            self, text='Cancel', command=lambda: controller.show_frame(PT.TestProgramWindow))
        self.cancel_btn.place(relx=0.6, rely=0.75, anchor=CENTER)
        
        
    def refresh_window(self):
        self.textArea.config(state=NORMAL)
        self.textArea.delete('1.0','end')
        test = False
        
        # Open the file in binary mode
        self.RLLimit = -1  # pass criteria for return loss measurement
        try:
            with open('file.ptt', 'rb') as file:
      
                # Call load method to deserialze
                fileData = pickle.load(file)
                analyser_port = fileData[4][2]
                self.userAdmin = fileData[1]
            file.close()
        except:
           self.textArea.insert('3.0','\nFault finding data ') 
            
        
        self.textArea.insert('1.0',fileData[0])
        self.textArea.insert('2.0','\nFault finding batch ')
        self.textArea.insert('2.30', fileData[2])
        
        self.probeType.set(fileData[3])
        self.currentBatch.set(fileData[2])
        self.currentUser.set(fileData[0])
        self.deviceDetails.set(self.device)
        self.serialNumber.set(" ")
        self.readSerialNumber.set(" ")
        
        while True:
            if PM.ProbePresent() == False:
                test = False
                self.action.set('No probe connected...')
            else:
                self.action.set('Probe connected')
                test = True
                break
            Tk.update(self)
                
            
       
        while test == True:  
                ProbeIsProgrammed = PM.ProbeIsProgrammed()
                if ProbeIsProgrammed == False: 
                    self.action.set('Probe not programmed...')
                else:
                    self.action.set('Programmed Probe connected')
                    
                # Collect serial number written to file   
                serial_number = BM.CSVM.ReadLastLine(fileData[2])
                self.serialNumber.set(serial_number[0][0])
                # Collect serial number read from probe
                pcb_serial_number = PI.ReadSerialNumber()
                binary_str = codecs.decode(pcb_serial_number, "hex")
                self.readSerialNumber.set(str(binary_str,'utf-8')[:16])
                   
                    
                try:
                    # Check to see if the analyser port is connected
                    self.textArea.delete('3.0','end')
                    if NanoZND.GetAnalyserPortNumber(analyser_port):
                        # Get the analyser to generate data points and return them
                        analyser_data = NanoZND.ReadAnalyserData(analyser_port)
                        self.analyserResults.append(analyser_data[3])
                        # Print the analyser data points selected by 
                        self.analyserData.set(self.analyserResults[0])
                        # print("Analyser data {}".format(analyser_data[3:10]))
                        # Set the device connected name
                        self.device = " NanoNVA "
                        self.deviceDetails.set(self.device) 
                except:
                    self.textArea.insert('3.30', '\nAnalyser error..')
                    
                
                
                self.textArea.delete('3.0','end')
                try:
                    serial_results = ODM.ReadSerialODM()
                   
                    self.SD_data.set(serial_results[0][5])
                    self.FTc_data.set(serial_results[0][6])
                    self.PV_data.set(serial_results[0][9])
                except:
                    self.textArea.insert('3.30', '\nODM Monitor error..')
                 
                if PM.ProbePresent() == False:
                    self.refresh_window()
            
                Tk.update(self) 
      
            
   
             
        