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
import time
import pickle
import serial
from serial import Serial
import codecs
import binascii
import time
from time import gmtime, strftime

from bitstring import BitArray

# Import modules

import SecurityManager
from SecurityManager import User
import BatchManager
from BatchManager import Batch
import InstrumentManager
import ProbeManager
from ProbeManager import Probe
from ProbeManager import ProbeManager
import NanoZND
import ODMPlus
import UserLogin as UL
import Sessions as SE
import FaultFinder as FF
import datastore

# create instances
SM = SecurityManager.SecurityManager()
IM = InstrumentManager.InstrumentationManager()
BM = BatchManager.BatchManager()
PM = ProbeManager()
NanoZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
DS = datastore.DataStore()



# define global variables
PTT_Version = 'Deltex Medical : XXXX-XXXX Probe Test Tool V0.1'
w = 800  # window width
h = 600  # window height
LARGE_FONT = ("Verdana", 14)
BTN_WIDTH = 30


# Assign as a command when I want to disable a button (double click prevention)
def ignore():
    return 'break'


class TestProgramWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # define variables
        self.session_on_going = False
        self.session_complete = None
        self.action = StringVar()
        self.left_to_test = IntVar()
        self.analyser_results = []
        self.current_batch = StringVar()
        self.current_user = StringVar()
        self.probes_passed = IntVar()
        self.device_details = StringVar()
        self.device = "Not connected to analyser"
        self.probe_type = StringVar()
        self.SD_data = IntVar()
        self.FTc_data = IntVar()
        self.PV_data = IntVar()
        self.user_admin = False
        self.check = 0
        self.go = False
        self.probes_passed.set(0)
        

        #import images
        self.greenlight = (PhotoImage(file="green128.gif"))
        self.amberlight = (PhotoImage(file="amber128.gif"))
        self.redlight = (PhotoImage(file="red128.gif"))
        self.greylight = (PhotoImage(file="grey128.gif"))
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.complete_btn = (PhotoImage(file="completetesting.gif"))
        self.suspend_btn = (PhotoImage(file="suspend.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        
        self.text_area = tk.Text(self, height=5, width=40)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
        time_now = strftime("%H:%M:%p", gmtime())
        self.text_area.delete('1.0','end')
        if "AM" in time_now :
            self.text_area.insert('1.0','Good Morning ')
            
        else:
            self.text_area.insert('1.0','Good Afternoon ')
        

        ttk.Label(self, text='Batch number: ').place(
            relx=0.1, rely=0.3, anchor='w')
        ttk.Label(self, textvariable=self.current_batch, relief=SUNKEN, font="bold",
                 width=10).place(relx=0.3, rely=0.3, anchor='w')

        ttk.Label(self, text='Probe type: ').place(
            relx=0.1, rely=0.45, anchor='w')
        ttk.Label(self, textvariable=self.probe_type, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.3, rely=0.45, anchor='w')

        ttk.Label(self, text='Connected to: ').place(
            relx=0.73, rely=0.2, anchor='w')
        ttk.Label(self, textvariable=self.device_details, relief=SUNKEN,
                  width=30).place(relx=0.7, rely=0.25, anchor='w')
        
        ttk.Label(self, text="Data from ODM").place(
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

        ttk.Label(self, text='Program/Test Status: ').place(relx=0.1,
                                            rely=0.58, anchor='w')
        self.status_image = ttk.Label(self, image=self.greylight)
        self.status_image.place(relx=0.53, rely=0.56, anchor=CENTER)

        ttk.Label(self, text='Probes Passed: ').place(
            relx=0.1, rely=0.75, anchor='w')
        ttk.Label(self, textvariable=self.probes_passed, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.28, rely=0.75, anchor='w')
        
        ttk.Button(self, text=' Start fault finding ', command=lambda: controller.show_frame(FF.FaultFindWindow), 
                   width=BTN_WIDTH).place(relx=0.53, rely=0.7, anchor=CENTER)
        
        ttk.Label(self, text='Probes to test: ').place(
            relx=0.7, rely=0.75, anchor='w')
        ttk.Label(self, textvariable=self.left_to_test, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.83, rely=0.75, anchor='w')
        
        ttk.Label(self, text='Action: ').place(relx=0.1, rely=0.9, anchor='w')
        
        ttk.Label(self, textvariable=self.action, background='yellow',
                  width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')

        ttk.Button(self, text='Complete Session', image=self.complete_btn, command=lambda: self.cmplt_btn_clicked(
            controller)).place(relx=0.68, rely=0.9, anchor=CENTER)
        
        ttk.Button(self, text='Suspend Session', image=self.suspend_btn, command=lambda: self.suspnd_btn_clicked(
            controller)).place(relx=0.85, rely=0.9, anchor=CENTER)
        
       

    def cmplt_btn_clicked(self, controller):
        Tk.update(self)
        self.session_complete = True
        self.session_on_going = False
        batch_data = []
        
        if self.left_to_test.get() == 0:
            
            current_batch = DS.get_batch()[0]

            BM.CompleteBatch(current_batch)
            controller.show_frame(SE.SessionSelectWindow)
            
            
    def find_fault_with_probe(self, controller):
        self.go = False
        if PM.ProbePresent() == True:
            controller.show_frame(FF.FaultFindWindow)
        else:
            self.go = True
      

    def suspnd_btn_clicked(self, controller):
        self.session_complete = False
        self.session_on_going = False
      
        BM.SuspendBatch(self.current_batch.get())
    
        controller.show_frame(SE.SessionSelectWindow)
   


    def refresh_window(self):
        self.session_on_going = True
        self.analyser_serial = None
        label = tk.ttk
        batchData = []
        serial_results = []
        analyser_data = []
       
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0','end')
     
        file_data = DS.get_batch()
        user_data = DS.get_user()
        
        self.analyser_serial = file_data[3][1]
        NanoZND.set_vna_controls(self.analyser_serial)
        NanoZND.flush_analyser_port(self.analyser_serial)
        
        self.user_admin = DS.get_user_admin_status()
    
        self.text_area.insert('1.0',user_data[0])
        self.text_area.insert('2.0','\nPlease continue testing batch ')
        self.text_area.insert('2.30', file_data[0])
       
      
        self.left_to_test.set(file_data[2])
     
        # self.root.deiconify()
        self.probe_type.set(file_data[1])
        self.current_batch.set(file_data[0])
        self.current_user.set(user_data[0])
        self.device_details.set(self.device)
        self.RLLimit = -1  # pass criteria for return loss measurement
        
        ##############################
        # Collect analyser port data #
        ##############################
      
            # Check to see if the analyser port is connected
            
        if NanoZND.GetAnalyserPortNumber(self.analyser_serial):
                # Get the analyser to generate data points and return them
            analyser_data = NanoZND.ReadAnalyserData(self.analyser_serial)
            self.device = " NanoNVA "
            self.device_details.set(self.device)
        
        #######################
        # Collect serial data #
        #######################
        try:
            serial_results = ODM.ReadSerialODM()
            self.SD_data.set(serial_results[0][5])
            self.FTc_data.set(serial_results[0][6])
            self.PV_data.set(serial_results[0][9])
            Tk.update(self)
        except:
            tm.showerror("ODM Error", "Chech ODM is running...")
      
        
        self.text_area.config(state=NORMAL)
        if DS.get_programme_status() == True:
                self.text_area.delete('3.0','end')
                self.text_area.insert('3.0', "\n\nProbe re-programming enabled.")
                
        else:
                self.text_area.delete('3.0','end')
                self.text_area.insert('3.0', "\n\nProbe re-programming disabled")
        self.text_area.config(state=DISABLED)
      
       
        # Detect if probe is present.        
        while(self.session_on_going == True):
            Tk.update(self) 
            if self.left_to_test.get() == False and self.check == False:
                tm.showinfo("Batch complete.","\nPlease press the Complete Session button.")
                self.check = 1
            self.go = False  
            
            if PM.ProbePresent() == False:
                
                self.action.set('Connect New Probe')
                ttk.Label(self, textvariable=self.action, background='yellow',
                    width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')   
            
            if PM.ProbePresent() == True:
                self.action.set('Probe connected')
                ProbeIsProgrammed = PM.ProbeIsProgrammed() 
                 
                if PM.ProbePresent() == True:
                    ttk.Label(self, textvariable=self.action, background='#1fff1f',
                        width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')
                
                if DS.get_programme_status() == False:
                    self.text_area.config(state=NORMAL)
                    self.text_area.delete('3.0','end')
                    self.text_area.insert('3.0', "\n\nYou can't re-program this probe.")   
                    self.text_area.config(state=DISABLED)
                    self.go = False
                
                if ProbeIsProgrammed == True and DS.get_programme_status() == True:
                    self.go = tm.askyesno('Programmed Probe Detected', 'This probe is already programmed.\nDo you wish to re-program and test?')
                    self.status_image.configure(image=self.amberlight) 
                else:
                    self.text_area.config(state=NORMAL)
                    if DS.get_programme_status() == True:
                        self.text_area.delete('3.0','end')
                        self.text_area.insert('3.0', "\n\nProbe re-programming enabled.")
                
                    else:
                        self.text_area.delete('3.0','end')
                        self.text_area.insert('3.0', "\n\nProbe re-programming disabled")
                    self.text_area.config(state=DISABLED)
                   
                if ProbeIsProgrammed == False:
                    self.go = True
                    self.status_image.configure(image=self.amberlight) 
                Tk.update(self) 
                
                if self.go == True:  
                    self.action.set('Programming probe')
                    serialNumber = PM.ProgramProbe(self.probe_type.get())
                    
                    try:
                        snum = str(codecs.decode(serialNumber, "hex"),'utf-8')[1:16]
                    except:
                        snum = "unable to get serial number"
                
                   
                  
                    
                    if serialNumber == False:
                        tm.showerror('Programming Error',
                                'Unable to program\nPlease check U1')
                        self.action.set('Probe failed')
                        self.status_image.configure(image=self.redlight)
                    else:
                        Tk.update(self)
                        self.action.set('Testing probe...')
                            
                        results = PM.TestProbe(
                            serialNumber, self.current_batch.get(), self.current_user.get())
                        self.action.set('Testing complete. Disconnect probe')
                        analyser_data = NanoZND.ReadAnalyserData(self.analyser_serial)
                    
                        # if PM.ZND.get_marker_values()[0] < self.RLLimit and PM.ZND.get_marker_values()[1] < self.RLLimit:
                        if self.RLLimit == -1: #check for crystal pass value, now pass every time
                            BM.UpdateResults(
                                results, self.current_batch.get())
                            self.probes_passed.set(self.probes_passed.get() + 1)
                            self.left_to_test.set(self.left_to_test.get() - 1)
                            self.status_image.configure(image=self.greenlight)
                            BM.saveProbeInfoToCSVFile(snum,analyser_data[1:2],self.current_user.get(), self.current_batch.get(),serial_results[0][9])
                            Tk.update(self)
                        else:
                            self.status_image.configure(image=self.redlight)
                            tm.showerror('Return Loss Error',
                                    'Check crystal connections')
                            Tk.update(self)
                        
                        # Collect serial data
                        while PM.ProbePresent() == True:
                                # serial_results = IM.GetPatientParamerts()
                            try:
                                serial_results = ODM.ReadSerialODM()
                                self.SD_data.set(serial_results[0][5])
                                self.FTc_data.set(serial_results[0][6])
                                self.PV_data.set(serial_results[0][9])
                                Tk.update(self)
                            except:
                                tm.showerror(
                                        'Connection Error', 'Unable to collect the data from the ODM.')
    
                            
                        
                while 1:
                    self.probePresent = PM.ProbePresent()
                    if self.probePresent == False:
                        
                        self.status_image.configure(image=self.greylight)
                        self.action.set('Connect New Probe')
                        break
                    
        if self.session_complete == True:
            BM.CompleteBatch(BM.current_batch)
            