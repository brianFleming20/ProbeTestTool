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

import pickle
from time import gmtime, strftime



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
        
        ttk.Label(self, text='Serial Number: ').place(
            relx=0.73, rely=0.2, anchor='w')
        ttk.Label(self, textvariable=self.serialNumber, relief=SUNKEN,
                  width=30).place(relx=0.7, rely=0.25, anchor='w')
        
        self.cancel_btn = ttk.Button(
            self, text='Cancel', command=lambda: controller.show_frame(PT.TestProgramWindow))
        self.cancel_btn.place(relx=0.6, rely=0.8, anchor=CENTER)
        
    def refresh_window(self):
        
        self.textArea.delete('1.0','end')
        # Open the file in binary mode
       
        with open('file.ptt', 'rb') as file:
      
        # Call load method to deserialze
            fileData = pickle.load(file)
            analyser_port = fileData[4][2]
            self.userAdmin = fileData[1]
        file.close()
        self.textArea.insert('1.0',fileData[0])
        self.textArea.insert('2.0','\nFault finding batch ')
        self.textArea.insert('2.30', fileData[2])
        
        self.probeType.set(fileData[3])
        self.currentBatch.set(fileData[2])
        self.currentUser.set(fileData[0])
        self.deviceDetails.set(self.device)
        
        
        with open("file_temp", "wb") as file:
                        
            batchData = pickle.load( file)
            
        file.close()
        self.serialNumber.set(batchData[0])