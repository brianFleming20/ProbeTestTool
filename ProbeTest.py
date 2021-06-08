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

# create instances
SM = SecurityManager.SecurityManager()
IM = InstrumentManager.InstrumentationManager()
BM = BatchManager.BatchManager()
PM = ProbeManager()
NanoZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()



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

        self.sessionOnGoing = False
        self.sessionComplete = None
        self.action = StringVar()
        self.leftToTest = IntVar()
        

        # define variables
        self.currentBatch = StringVar()
        self.currentUser = StringVar()
        self.leftToTest = IntVar()
        self.probesPassed = IntVar()
        self.deviceDetails = StringVar()
        self.device = "Not connected to analyser"
        self.probeType = StringVar()
        self.SD_data = IntVar()
        self.FTc_data = IntVar()
        self.PV_data = IntVar()
        self.userAdmin = False
        self.check = 0
        

        #import images
        self.greenlight = (PhotoImage(file="green128.gif"))
        self.amberlight = (PhotoImage(file="amber128.gif"))
        self.redlight = (PhotoImage(file="red128.gif"))
        self.greylight = (PhotoImage(file="grey128.gif"))
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        
        self.textArea = tk.Text(self, height=5, width=38)
        self.textArea.place(relx=0.25, rely=0.15, anchor=CENTER)
        timeNow = strftime("%H:%M:%p", gmtime())
        if "AM" in timeNow :
            self.textArea.insert('1.0','Good Morning ', font=('bold',12))
            
        else:
            self.textArea.insert('1.0','Good Afternoon ')
        

        ttk.Label(self, text='Batch number: ').place(
            relx=0.1, rely=0.3, anchor='w')
        ttk.Label(self, textvariable=self.currentBatch, relief=SUNKEN, font="bold",
                 width=10).place(relx=0.3, rely=0.3, anchor='w')

        ttk.Label(self, text='Probe type: ').place(
            relx=0.1, rely=0.45, anchor='w')
        ttk.Label(self, textvariable=self.probeType, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.3, rely=0.45, anchor='w')

        # ttk.Label(self, text='User: ').place(relx=0.1, rely=0.15, anchor='w')
        # ttk.Label(self, textvariable=self.currentUser, relief=SUNKEN, font="bold",
        #           width=20).place(relx=0.3, rely=0.15, anchor='w')

        ttk.Label(self, text='Connected to: ').place(
            relx=0.73, rely=0.2, anchor='w')
        ttk.Label(self, textvariable=self.deviceDetails, relief=SUNKEN,
                  width=30).place(relx=0.7, rely=0.25, anchor='w')
        
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

        ttk.Label(self, text='Program/Test Status: ').place(relx=0.1,
                                            rely=0.58, anchor='w')
        self.status_image = ttk.Label(self, image=self.greylight)
        self.status_image.place(relx=0.53, rely=0.56, anchor=CENTER)

        ttk.Label(self, text='Probes Passed: ').place(
            relx=0.1, rely=0.75, anchor='w')
        ttk.Label(self, textvariable=self.probesPassed, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.28, rely=0.75, anchor='w')
        
        ttk.Label(self, text='Probes to test: ').place(
            relx=0.7, rely=0.75, anchor='w')
        ttk.Label(self, textvariable=self.leftToTest, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.83, rely=0.75, anchor='w')

        
        
        ttk.Label(self, text='Action: ').place(relx=0.1, rely=0.85, anchor='w')
        ttk.Label(self, textvariable=self.action, background='yellow',
                  width=40, relief=GROOVE).place(relx=0.3, rely=0.85, anchor='w')
        self.action.set('Connect New Probe')

        self.completeButton = ttk.Button(self, text='Complete Session', command=lambda: self.cmplt_btn_clicked(
            controller))
        self.completeButton.place(relx=0.68, rely=0.92, anchor=CENTER)
        
        ttk.Button(self, text='Suspend Session', command=lambda: self.suspnd_btn_clicked(
            controller)).place(relx=0.85, rely=0.92, anchor=CENTER)

    def cmplt_btn_clicked(self, controller):
        Tk.update(self)
        self.sessionComplete = True
        self.sessionOnGoing = False
        batch_data = []
        with open('file.ptt', 'rb') as file:
      
        # Call load method to deserialze
            myvar = pickle.load(file)
            currentBatch = myvar[2]
        file.close()
        with open("file_batch", "wb") as file:
                batch_data.append(self.currentBatch.get())
                batch_data.append(self.probeType.get())
                batch_data.append(self.leftToTest.get())
                pickle.dump(batch_data, file)
        file.close()
        
        if self.leftToTest.get() == False:
            BM.CompleteBatch(currentBatch)
            controller.show_frame(SE.SessionSelectWindow)
            
    

    def suspnd_btn_clicked(self, controller):
        self.sessionComplete = False
        self.sessionOnGoing = False
        batch_data = []
        
        with open("file_batch", "wb") as file:
                batch_data.append(self.currentBatch.get())
                batch_data.append(self.probeType.get())
                batch_data.append(self.leftToTest.get())
                pickle.dump(batch_data, file)
        file.close()
        BM.SuspendBatch(self.currentBatch.get())
        
        controller.show_frame(SE.SessionSelectWindow)


    def refresh_window(self):
        self.sessionOnGoing = True
        
        serial_results = []
        analyser_data = []
        BM.updateBatchInfo()
        
        # Open the file in binary mode
        try:
            with open('file.ptt', 'rb') as file:
      
        # Call load method to deserialze
                myvar = pickle.load(file)
                name = myvar[0]
                currentBatch = myvar[2]
                probeType = myvar[3]
                analyser_port = myvar[4][2]
                self.userAdmin = myvar[1]
            file.close()
            self.textArea.insert('2.0',name)
            self.textArea.insert('4.0','\n\nPlease continue testing batch ')
            self.textArea.insert('3.30', currentBatch)
        except:
             tm.showerror(
                'Data Collection Error', 'Unable to collect the data from system files.')  

        try:
            with open('file_batch', 'rb') as file:
                myvar = pickle.load(file)
                self.leftToTest.set(myvar[2])
            file.close()
            
        except:
            self.leftToTest.set(100)
            
        # self.root.deiconify()
        self.probeType.set(probeType)
        self.currentBatch.set(currentBatch)
        self.currentUser.set(name)
        self.deviceDetails.set(self.device)
        self.RLLimit = -1  # pass criteria for return loss measurement
        
        
        ##############################
        # Collect analyser port data #
        ##############################
        
        try:
            # Check to see if the analyser port is connected
            
            if NanoZND.GetAnalyserPortNumber(analyser_port):
                # Get the analyser to generate data points and return them
                analyser_data = NanoZND.ReadAnalyserData(analyser_port)
                
                # Print the analyser data points selected by 
                print("Analyser data {}".format(analyser_data[3:10]))
                # Set the device connected name
                self.device = " NanoNVA "
                self.deviceDetails.set(self.device)
                
        except:
               tm.showerror(
                'Data Collection Error', 'Unable to collect the data from the NanoVNA Analyser. \nOr turn it on.')  
        # write data to .csv file
        
        try:
            
            NanoZND.CVSOutPut(currentBatch)
        except:
            tm.showerror(
                'Data write Error', 'Unable to start write the data from the NanoVNA Analyser. \n to file.')  
   
        #######################
        # Collect serial data #
        #######################
        try:
            serial_results = ODM.ReadSerialODM()
            # serial_results = IM.GetPatientParamerts()
            # self.SD_data.set(serial_results[0])
            # self.FTc_data.set(serial_results[1])
            # self.PV_data.set(serial_results[2])
           
            self.SD_data.set(serial_results[0][5])
            self.FTc_data.set(serial_results[0][6])
            self.PV_data.set(serial_results[0][9])
            Tk.update(self)
        except:
            tm.showerror(
                'Connection Error', 'Unable to collect the data from the ODM.')
                # controller.show_frame(ConnectionWindow)
        control_data = []
        with open('file.ptt', 'rb') as file:
      
            # Call load method to deserialze
                myvar = pickle.load(file)
                control_data.extend(myvar)
        file.close()
        
        with open('file.admin', 'rb') as fileAd:
            myvar = pickle.load(fileAd)
            reprogramOK = myvar[0]
            
        fileAd.close()

        # Detect if probe is present.        
        while(self.sessionOnGoing == True):
            Tk.update(self)
            if self.leftToTest.get() == False and self.check == 0:
                tm.showinfo("Batch complete.","\nPlease press the Complete Session button.")
                self.check = 1
                
            if PM.ProbePresent() == True:
                self.action.set('Probe connected')
                go = False
                ProbeIsProgrammed = PM.ProbeIsProgrammed()  
                   
                if reprogramOK == False:
                    tm.Dialog("Unable to re-programme probe.")
                    go = False
                    
                if ProbeIsProgrammed == True and reprogramOK == True:    
                    go = tm.askyesno('Programmed Probe Detected', 'This probe is already programmed.\nDo you wish to re-program and test?')
                    self.status_image.configure(image=self.amberlight) 
                    
                if ProbeIsProgrammed == False:
                    go = True
                    self.status_image.configure(image=self.amberlight) 
                if go == True:  
                    self.action.set('Programming probe')
                    serialNumber = PM.ProgramProbe(BM.currentBatch.probeType)
                    if serialNumber == False:
                        tm.showerror('Programming Error',
                                'Unable to program\nPlease check U1')
                        self.action.set('Probe failed')
                        self.status_image.configure(image=self.redlight)
                    else:
                        Tk.update(self)
                        self.action.set('Testing probe...')
                            
                        results = PM.TestProbe(
                            serialNumber, BM.currentBatch.batchNumber, self.currentUser.get())
                        self.action.set('Testing complete. Disconnect probe')
                        # if PM.ZND.get_marker_values()[0] < self.RLLimit and PM.ZND.get_marker_values()[1] < self.RLLimit:
                        if self.RLLimit == -1: #check for crystal pass value, now pass every time
                            BM.UpdateResults(
                                results, BM.currentBatch.batchNumber)
                            self.probesPassed.set(self.probesPassed.get() + 1)
                            self.leftToTest.set(self.leftToTest.get() - 1)
                            self.status_image.configure(image=self.greenlight)
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
                                # print(serial_results)
                                # self.SD_data.set(serial_results[0])
                                # self.FTc_data.set(serial_results[1])
                                # self.PV_data.set(serial_results[2])
                                # Tk.update(self)
                            
                                self.SD_data.set(serial_results[0][5])
                                self.FTc_data.set(serial_results[0][6])
                                self.PV_data.set(serial_results[0][9])
                                Tk.update(self)
                            except:
                                tm.showerror(
                                        'Connection Error', 'Unable to collect the data from the ODM.')
    
                            
                        
                while 1:
                    if PM.ProbePresent() == False:
                        
                        self.status_image.configure(image=self.greylight)
                        self.action.set('Connect New Probe')
                        break
        
       
                        
        # put something here to move csv?
        if self.sessionComplete == True:
            BM.CompleteBatch(BM.currentBatch)
            





# PI = PI()
# PD = ProbeData()
# PI.Connect('COM3')
# sn = PI.ProbeReadAllBytes()
# 
# print(sn)
