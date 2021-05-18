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
import SecurityManager
from SecurityManager import User
import UserLogin as UL
import DeviceConnect as DC
import pickle

BM = BatchManager.BatchManager()
SM = SecurityManager.SecurityManager()


def ignore():
    return 'break'

BTN_WIDTH = 25

class SessionSelectWindow(tk.Frame):
    def __init__(self, parent, controller):
        # create a choose session window
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        self.isAdmin = False
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        
        self.SSW_b1 = ttk.Button(self, text='Start a new session', command=lambda: controller.show_frame(
            NewSessionWindow), width=BTN_WIDTH)
        self.SSW_b1.place(relx=0.3, rely=0.3, anchor=CENTER)

        self.SSW_b2 = ttk.Button(self, text='Continue a previous session',
                                 command=lambda: controller.show_frame(ContinueSessionWindow), width=BTN_WIDTH)
        self.SSW_b2.place(relx=0.7, rely=0.3, anchor=CENTER)

        self.SSW_b3 = ttk.Button(self, text='Log Out', command=lambda: controller.show_frame(
            UL.LogInWindow), width=BTN_WIDTH)
        self.SSW_b3.place(relx=0.3, rely=0.6, anchor=CENTER)

        self.SSW_b4 = ttk.Button(self, text='Edit Users', command=lambda: controller.show_frame(
            UL.AdminWindow), width=BTN_WIDTH)
        self.SSW_b4.place(relx=0.7, rely=0.6, anchor=CENTER)

        

        

    def refresh_window(self):
       
       # Open the file in binary mode
        with open('file.ptt', 'rb') as file:
      
        # Call load method to deserialze
            session_info = pickle.load(file)
            self.isAdmin = session_info[:]
        file.close()
        
        if False in self.isAdmin:
            self.SSW_b4.config(state=DISABLED)
        else:
            self.SSW_b4.config(state=NORMAL)

        if len(BM.GetAvailableBatches()) == 0:
            self.SSW_b2.config(state=DISABLED)
        else:
            self.SSW_b2.config(state=NORMAL)
            
            
            
class NewSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        self.batchNumber = StringVar()
        self.probeType = StringVar()
        self.batchQty = IntVar()

        # Details Screen
        tk.Frame.__init__(self, parent, bg='#E0FFFF')

        batch_frame = tk.Frame(self, pady=3)
        probe_type_frame = tk.Frame(self, pady=3, padx=50, bg= '#E0FFFF')
        button_frame = tk.Frame(self, pady=3)
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)

        #batch_frame.grid(row=0, sticky="ew")
        probe_type_frame.place(relx=0.2, rely=0.35,anchor=CENTER)
        
        self.NSWL1 = ttk.Label(self, text='Probe selection window. ', justify=RIGHT)
        self.NSWL1.place(relx=0.5, rely=0.05, anchor=CENTER)

        self.NSWL1 = ttk.Label(self, text='Batch number: ', justify=RIGHT)
        self.NSWL1.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.NSWE1 = ttk.Entry(self, textvariable=self.batchNumber)
        self.NSWE1.place(relx=0.7, rely=0.2, anchor=CENTER)
        
        self.NSWL1 = ttk.Label(self, text='Batch Qty: ', justify=RIGHT)
        self.NSWL1.place(relx=0.5, rely=0.3, anchor=CENTER)
        
        self.NSWE1 = ttk.Entry(self, textvariable=self.batchQty)
        self.NSWE1.place(relx=0.7, rely=0.3, anchor=CENTER)

        self.NSWL2 = ttk.Label(self, text='Select Probe Type: ')
        self.NSWL2.place(relx=0.2, rely=0.65, anchor=CENTER)
        
       
      

        # tk.Radiobutton(probe_type_frame, text='SDP30 [Suprasternal Probe]',
        #                variable=self.probeType, value='SDP30').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='DP240 [9070-]',
                       variable=self.probeType, value='DP240').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='DP12 [Doppler 12 Hour]',
                       variable=self.probeType, value='DP12').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='DP6 [Doppler 6 Hour]',
                       variable=self.probeType, value='DP6').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='I2C [Doppler 72 Hour]',
                       variable=self.probeType, value='I2C').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='I2P [Doppler 12 Hour]', 
                       variable=self.probeType, value='I2P').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='I2S [Doppler 6 Hour]', 
                       variable=self.probeType, value='I2S').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='KDP [Kinder 72 Hour]', 
                       variable=self.probeType, value='KDP').pack(fill=X, ipady=5)
        # tk.Radiobutton(probe_type_frame, text='Blank',
        #                variable=self.probeType, value='Blank').pack(fill=X, ipady=7)
        
        self.confm_btn = tk.Button(self, text='Confirm', padx=2, pady=3,
                                   width=BTN_WIDTH, command=lambda: self.confm_btn_clicked(controller))
        self.confm_btn.place(relx=0.3, rely=0.8, anchor=CENTER)

        self.cancl_btn = tk.Button(self, text='Cancel', padx=2, pady=3, width=BTN_WIDTH,
                                   command=lambda: controller.show_frame(SessionSelectWindow))
        self.cancl_btn.place(relx=0.7, rely=0.8, anchor=CENTER)

        self.bind('<Return>', self.confm_btn_clicked)

    def confm_btn_clicked(self, controller):
        # create batch object
        session_data = []
        batch_data = []
        newBatch = Batch(self.batchNumber.get())
        newBatch.probeType = self.probeType.get()
        newBatch.batchQty = self.batchQty.get()

        DAnswer = tm.askyesno('Confirm', 'Are batch details correct?' )
        if DAnswer == True and self.batchQty.get() > 0:
            # create the batch file
            # Open the file in binary mode
            with open('file.ptt', 'rb') as file:
      
            # Call load method to deserialze
                myvar = pickle.load(file)
            session_data.extend(myvar)
            file.close()
            name = session_data[0]
            if BM.CreateBatch(newBatch, name) == False:
                tm.showerror('Error', 'Batch number not unique')
            else:
                BM.currentBatch = newBatch
                session_data.append(self.batchNumber.get())
                session_data.append(self.probeType.get())
                session_data.append(self.batchQty.get())
            
                with open('file.ptt', 'wb') as file:
                    pickle.dump(session_data, file)
                file.close()
                with open("file_batch", "wb") as file:
                    batch_data.append(self.batchNumber.get())
                    batch_data.append(self.probeType.get())
                    batch_data.append(self.batchQty.get())
                    pickle.dump(batch_data, file)
                file.close()
                self.NSWE1.delete(0, 'end')
                controller.show_frame(DC.ConnectionWindow)


class ContinueSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        
        self.Label1 = ttk.Label(self, text='Choose a session to resume')
        self.Label1.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.sessionListBox = Listbox(self)
        self.sessionListBox.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.sessionListBox.config(height=5, width=20)
        
        self.probeTypeListBox = Listbox(self)
        self.probeTypeListBox.place(relx=0.7, rely=0.4, anchor=CENTER)
        self.probeTypeListBox.config(height=5, width=15)

        self.continue_btn = ttk.Button(
            self, text='Continue Session', command=lambda: self.continue_btn_clicked(controller))
        self.continue_btn.place(relx=0.4, rely=0.8, anchor=CENTER)

        self.cancel_btn = ttk.Button(
            self, text='Cancel', command=lambda: controller.show_frame(SessionSelectWindow))
        self.cancel_btn.place(relx=0.6, rely=0.8, anchor=CENTER)

        self.refresh_window()

    def refresh_window(self):
        # #create a list of the current users using the dictionary of users
        sessionList = []
        probeTypeList = []
        for item in BM.GetAvailableBatches():
            sessionList.append(item)
            batchObj = BM.GetBatchObject(item)
            probeTypeList.append(batchObj.probeType)
            batchObj = None
        
       

        # clear the listbox
        self.sessionListBox.delete(0, END)
        self.probeTypeListBox.delete(0, END)

        # fill the listbox with the list of users
        for item in sessionList:
            self.sessionListBox.insert(END, item)
            
        for item in probeTypeList:
            self.probeTypeListBox.insert(END, item)

    def continue_btn_clicked(self, controller):
     
        lstid = self.sessionListBox.curselection()
        session_data = []
        batch_data = []

        try:
            lstBatch = self.sessionListBox.get(lstid[0])
            batch = BM.GetBatchObject(lstBatch)
            # Open the file in binary mode
            with open('file.ptt', 'rb') as file:
      
            # Call load method to deserialze
                myvar = pickle.load(file)
                session_data.extend(myvar)
            file.close()
            
            session_data.append(lstBatch)
            session_data.append(batch.probeType)
            
            with open('file.ptt', 'wb') as file:
                pickle.dump(session_data, file)
            file.close()
            
            with open("file_batch", "wb") as file:
                batch_data.append(lstBatch)
                batch_data.append(batch.probeType)
                batch_data.append(batch.batchQty)
                pickle.dump(batch_data, file)
            file.close()
           
            controller.show_frame(DC.ConnectionWindow)
        except:
            tm.showerror('Error', 'Please select a batch from the batch list')
