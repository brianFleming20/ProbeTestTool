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
import datastore
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
DS = datastore.DataStore()


def ignore():
    return 'break'

BTN_WIDTH = 25

class FaultFindWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        
        # Set up variavles
        self.current_batch = StringVar()
        self.current_user = StringVar()
        self.probe_type = StringVar()
        self.device_details = StringVar()
        self.serialNumber = StringVar()
        self.readSerialNumber = StringVar()
        self.analyserData = StringVar()
        self.action = StringVar()
        self.analyser_results = []
        self.SD_data = IntVar()
        self.FTc_data = IntVar()
        self.PV_data = IntVar()
        self.device = "Not connected to analyser"
        
        # Import images
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        
        self.text_area = tk.Text(self, height=5, width=40)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
        self.text_area.delete('1.0','end')
        
        ttk.Label(self, text='Batch number: ').place(
            relx=0.1, rely=0.3, anchor='w')
        ttk.Label(self, textvariable=self.current_batch, relief=SUNKEN, font="bold",
                 width=10).place(relx=0.2, rely=0.3, anchor='w')

        ttk.Label(self, text='Probe type: ').place(
            relx=0.1, rely=0.38, anchor='w')
        ttk.Label(self, textvariable=self.probe_type, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.2, rely=0.38, anchor='w')
        
        ttk.Label(self, text='Connected to: ').place(
            relx=0.1, rely=0.44, anchor='w')
        ttk.Label(self, textvariable=self.device_details, relief=SUNKEN,
                  width=30).place(relx=0.2, rely=0.44, anchor='w')
        ttk.Label(self, textvariable=self.analyserData, relief=SUNKEN,
                  width=40).place(relx=0.3, rely=0.48, anchor='w')
        
        ttk.Label(self, text='Serial Number: ').place(
            relx=0.78, rely=0.18, anchor='w')
        ttk.Label(self, text='From file: ').place(
            relx=0.6, rely=0.25, anchor='w')
        ttk.Label(self, text='From Probe: ').place(
            relx=0.6, rely=0.3, anchor='w')
        ttk.Label(self, textvariable=self.serialNumber, relief=SUNKEN,
                  width=20).place(relx=0.7, rely=0.25, anchor='w')
        ttk.Label(self, textvariable=self.readSerialNumber, relief=SUNKEN,
                  width=20).place(relx=0.7, rely=0.3, anchor='w')
        
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
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0','end')
        test = False
        
        # Open the file in binary mode
        self.RLLimit = -1  # pass criteria for return loss measurement
        try:
            # with open('file.ptt', 'rb') as file:
      
            #     # Call load method to deserialze
            #     fileData = pickle.load(file)
            #     analyser_port = fileData[4][2]
            #     self.user_admin = fileData[1]
            # file.close()
            file_data = DS.add_to_batch_file()
            user_data = DS.add_to_user_file()
            self.user_admin = DS.get_user_admin_status()
            analyser_port = file_data[3][0]
        except:
           self.text_area.insert('3.0','\nFault finding data ') 
            
        
        self.text_area.insert('1.0',user_data[0])
        self.text_area.insert('2.0','\nFault finding batch ')
        self.text_area.insert('2.30', file_data[0])
        
        self.probe_type.set(file_data[1])
        self.current_batch.set(file_data[0])
        self.current_user.set(user_data[0])
        self.device_details.set(self.device)
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
                serial_number = BM.CSVM.ReadLastLine(file_data[0])
                self.serialNumber.set(serial_number[0][0])
                # Collect serial number read from probe
                pcb_serial_number = PI.ReadSerialNumber()
                binary_str = codecs.decode(pcb_serial_number, "hex")
                self.readSerialNumber.set(str(binary_str,'utf-8')[:15])
                   
                    
                try:
                    # Check to see if the analyser port is connected
                    self.text_area.delete('3.0','end')
                    if NanoZND.GetAnalyserPortNumber(analyser_port):
                        # Get the analyser to generate data points and return them
                        analyser_data = NanoZND.ReadAnalyserData(analyser_port)
                        self.analyser_results.append(analyser_data[3])
                        # Print the analyser data points selected by 
                        self.analyserData.set(self.analyser_results[0])
                        print("Analyser data {}".format(analyser_data[3:10]))
                        # Set the device connected name
                        self.device = " NanoNVA "
                        self.device_details.set(self.device) 
                except:
                    self.text_area.insert('3.30', '\nAnalyser error..')
                    
                
                
                
                try:
                    self.text_area.delete('3.0','end')
                    serial_results = ODM.ReadSerialODM()
                   
                    self.SD_data.set(serial_results[0][5])
                    self.FTc_data.set(serial_results[0][6])
                    self.PV_data.set(serial_results[0][9])
                except:
                    self.text_area.insert('3.30', '\nODM monitor error..')
                 
                if PM.ProbePresent() == False:
                    self.refresh_window()
            
                Tk.update(self) 
      
            
   
             
        