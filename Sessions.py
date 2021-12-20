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
from tkinter import font
import tkinter.messagebox as tm
import BatchManager
from BatchManager import Batch
import SecurityManager
from SecurityManager import User
import UserLogin as UL
import Connection as CO
import AdminUser as AU
import datastore
import pickle
from time import gmtime, strftime

BM = BatchManager.BatchManager()
SM = SecurityManager.SecurityManager()
DS = datastore.DataStore()

def ignore():
    return 'break'

BTN_WIDTH = 25
BTN_HEIGHT = 18

class SessionSelectWindow(tk.Frame):
    def __init__(self, parent, controller):
        # create a choose session window
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        
 
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
        time_now = strftime("%H:%M:%p", gmtime())
        
        ttk.Button(self, text='Start a new session' , command=lambda: 
            controller.show_frame(NewSessionWindow), 
            width=BTN_WIDTH).place(relx=0.28, rely=0.3,  anchor=CENTER)
        

        self.SSW_b2 = ttk.Button(self, text='Continue a previous session',
            command=lambda: controller.show_frame(ContinueSessionWindow), width=BTN_WIDTH)
     
        self.SSW_b2.place(relx=0.6, rely=0.3, anchor=CENTER)

        ttk.Button(self, text='Completed Batches', command=lambda: 
            self.completed_btn_clicked(controller), 
            width=BTN_WIDTH).place(relx=0.28, rely=0.55, anchor=CENTER)

        self.SSW_b4 = ttk.Button(self, text='Admin area', command=lambda: 
            controller.show_frame(AU.AdminWindow), width=BTN_WIDTH)
       
        self.SSW_b4.place(relx=0.6, rely=0.55, anchor=CENTER)
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0','end')
        if "AM" in time_now :
            self.text_area.insert('1.0','Good Morning ')
            
        else:
            self.text_area.insert('1.0','Good Afternoon ')
        self.text_area.config(state=DISABLED)
            
        self.SSW_b3 = ttk.Button(self, text='Log Out', command=lambda: 
            controller.show_frame(UL.LogInWindow), width=BTN_WIDTH)
        self.SSW_b3.place(relx=0.3, rely=0.8, anchor=CENTER)
            

    def refresh_window(self):
       
        # DS.write_to_batch_file("")
        user_info = DS.get_user_admin_status()
      
        
        if user_info == False:
            self.SSW_b4.config(state=DISABLED)
        else:
            self.SSW_b4.config(state=NORMAL)

        if len(BM.GetAvailableBatches()) == 0:
            self.SSW_b2.config(state=DISABLED)
        else:
            self.SSW_b2.config(state=NORMAL)
         
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0','end')
        self.text_area.insert('2.0',DS.get_username())
        self.text_area.insert('3.3','\n\nPlease choose an option.')
        self.text_area.config(state=DISABLED)
        
    def completed_btn_clicked(self, controller):
        print("Completed button clicked...")
      
            
            
class NewSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        self.batchNumber = StringVar()
        self.probe_type = StringVar()
        self.batchQty = IntVar()

        # Details Screen
        tk.Frame.__init__(self, parent, bg='#E0FFFF')

        # batch_frame = tk.Frame(self, pady=3)
        probe_type_frame = tk.Frame(self, pady=3, padx=50, bg= '#E0FFFF')
        # button_frame = tk.Frame(self, pady=3)
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_3 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_3.place(relx=0.9, rely=0.1, anchor=CENTER)
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
        # time_now = strftime("%H:%M:%p", gmtime())

        #batch_frame.grid(row=0, sticky="ew")
        probe_type_frame.place(relx=0.2, rely=0.45,anchor=CENTER)
        
        self.NSWL1 = ttk.Label(self, text='Probe selection window. ', justify=RIGHT)
        self.NSWL1.place(relx=0.5, rely=0.05, anchor=CENTER)

        self.NSWL1 = ttk.Label(self, text='Batch number: ', justify=RIGHT)
        self.NSWL1.place(relx=0.5, rely=0.35, anchor=CENTER)

        self.NSWE1 = ttk.Entry(self, textvariable=self.batchNumber)
        self.NSWE1.place(relx=0.62, rely=0.35, anchor=CENTER)
        
        self.NSWL1 = ttk.Label(self, text='Batch Qty: ', justify=RIGHT)
        self.NSWL1.place(relx=0.5, rely=0.45, anchor=CENTER)
        
        self.NSWE1 = ttk.Entry(self, textvariable=self.batchQty)
        self.NSWE1.place(relx=0.7, rely=0.45, anchor=E)

        self.NSWL2 = ttk.Label(self, text='Select Probe Type: ')
        self.NSWL2.place(relx=0.2, rely=0.7, anchor=CENTER)
        
        self.probe_type = StringVar(probe_type_frame, "DP240")
        # Dictionary to create multiple buttons
        values = {"DP240 [9070-7005]" : "DP240",
        "DP12 [9070-7003]  " : "DP12 ",
        "DP6 [9070-7001]    " : "DP6  ",
        "I2C [9090-7014]     " : "I2C  ",
        "I2P [9090-7013]     " : "I2P  ",
        "I2S [9090-7012]      " : "I2S  ",
        "KDP72 [9081-7001]" : "KDP  "}
        
        for (text, value) in values.items():
            Radiobutton(probe_type_frame, text = text, variable = self.probe_type,
            value = value).pack(side = TOP, ipady = 5)
      

        # # tk.Radiobutton(probe_type_frame, text='SDP30 [Suprasternal Probe]',
        # #                variable=self.probe_type, value='SDP30').pack(fill=X, ipady=5)
        # tk.Radiobutton(probe_type_frame, text='DP240 [9070-7005]',
        #                variable=self.probe_type, value='DP240').pack(side=TOP, ipady=5)
        # tk.Radiobutton(probe_type_frame, text='DP12 [9070-7003]',
        #                variable=self.probe_type, value='DP12').pack(fill=X, ipady=5)
        # tk.Radiobutton(probe_type_frame, text='DP6 [9070-7001]',
        #                variable=self.probe_type, value='DP6').pack(fill=X, ipady=5)
        # tk.Radiobutton(probe_type_frame, text='I2C [9090-7014]',
        #                variable=self.probe_type, value='I2C').pack(fill=X, ipady=5)
        # tk.Radiobutton(probe_type_frame, text='I2P [9090-7013]', 
        #                variable=self.probe_type, value='I2P').pack(fill=X, ipady=5)
        # tk.Radiobutton(probe_type_frame, text='I2S [9090-7012]', 
        #                variable=self.probe_type, value='I2S').pack(fill=X, ipady=5)
        # tk.Radiobutton(probe_type_frame, text='KDP72 [9081-7001]', 
        #                variable=self.probe_type, value='KDP').pack(fill=X, ipady=5)
        # # tk.Radiobutton(probe_type_frame, text='Blank',
        # #                variable=self.probe_type, value='Blank').pack(fill=X, ipady=7)
        
        self.confm_btn = tk.Button(self, text='Confirm', padx=2, pady=3,
                width=BTN_WIDTH, command=lambda: self.confm_btn_clicked(controller))
        self.confm_btn.place(relx=0.8, rely=0.8, anchor=CENTER)

        self.cancl_btn = tk.Button(self, text='Cancel', padx=2, pady=3, width=BTN_WIDTH,
                command=lambda: controller.show_frame(SessionSelectWindow))
        self.cancl_btn.place(relx=0.5, rely=0.8, anchor=CENTER)

        self.bind('<Return>', self.confm_btn_clicked)
        
  
        
    def refresh_window(self):
        self.text_area.config(state=NORMAL)
        self.text_area.insert('1.0',DS.get_username())
        self.text_area.insert('3.3','\n\nPlease enter the batch number\nselect the probe type\nand batch quantity.')
        self.text_area.config(state=DISABLED)
        

    def confm_btn_clicked(self, controller):
        # create batch object
        session_data = []
        batch_data = []
        DAnswer = False
        newBatch = Batch(self.batchNumber.get())
        newBatch.probe_type = self.probe_type.get()
        newBatch.batchQty = self.batchQty.get()

        if self.batchQty.get() > 100:
                self.text_area.config(state=NORMAL)
                self.text_area.delete('2.0','end')
                self.text_area.insert('2.0','\nCheck batch quantity. ')
                self.text_area.config(state=DISABLED)
        else:
            DAnswer = tm.askyesno('Confirm', 'Are batch details correct?' )
        if DAnswer == True and self.batchQty.get() > 0:
            # create the batch file
        
            temp_var = DS.get_user()
            
            name = temp_var[0]
            if BM.CreateBatch(newBatch, name) == False:
                tm.showerror('Error', 'Batch number not unique')
                self.refresh_window()
            else:
                BM.current_batch = newBatch
                session_data.append(newBatch.batchNumber)
                session_data.append(newBatch.probe_type)
                batch_data.append(self.batchNumber.get())
                batch_data.append(self.probe_type.get())
                batch_data.append(self.batchQty.get())
            
            
                DS.write_to_batch_file(batch_data)
            
                controller.show_frame(CO.Connection)
            
            self.NSWE1.delete(0, 'end')
            


class ContinueSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        ttk.Label(self, text=" ", image=self.deltex).place(relx=0.9, rely=0.1, 
                                                           anchor=CENTER)
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)
        
        
        ttk.Label(self, text='Choose a session to resume').place(relx=0.5, 
                rely=0.05, anchor=CENTER)
        
        ttk.Label(self, text="Batch number").place(relx=0.35, rely=0.3)
        ttk.Label(self, text="Batch type").place(relx=0.55, rely=0.3)

        self.sessionListBox = Listbox(self)
        self.sessionListBox.place(relx=0.4, rely=0.4, anchor=CENTER)
        self.sessionListBox.config(height=4, width=20)
        
        self.probe_typeListBox = Listbox(self)
        self.probe_typeListBox.place(relx=0.6, rely=0.4, anchor=CENTER)
        self.probe_typeListBox.config(height=4, width=15)
        

        self.continue_btn = ttk.Button(
            self, text='Continue Session', command=lambda: self.continue_btn_clicked(controller))
        self.continue_btn.place(relx=0.7, rely=0.8, anchor=CENTER)

        self.cancel_btn = ttk.Button(
            self, text='Cancel', command=lambda: controller.show_frame(SessionSelectWindow))
        self.cancel_btn.place(relx=0.3, rely=0.8, anchor=CENTER)
        


    def refresh_window(self):
        # #create a list of the current users using the dictionary of users
        sessionList = []
        probe_typeList = []
       
        self.text_area.config(state=NORMAL)
        self.text_area.insert('1.0',DS.get_username())
        self.text_area.insert('3.3','\n\nPlease select a batch number\nto continue testing.')
        self.text_area.config(state=DISABLED)

        for item in BM.GetAvailableBatches():
            sessionList.append(item)
            
            batch_obj = BM.GetBatchObject(item)
            probe_typeList.append(batch_obj.probe_type)
            
            batch_obj = None

        # clear the listbox
        self.sessionListBox.delete(0, END)
        self.probe_typeListBox.delete(0, END)

        # fill the listbox with the list of users
        for item in sessionList:
            self.sessionListBox.insert(END, item)
            
        for item in probe_typeList:
            self.probe_typeListBox.insert(END, item)
        self.probe_typeListBox.config(state=DISABLED)
        

    def continue_btn_clicked(self, controller):
        self.probe_typeListBox.config(state=NORMAL)
        batch_data = []
        try:
            
            lstid = self.sessionListBox.curselection()
        
            lstBatch = self.sessionListBox.get(lstid[0])
            batch = BM.GetBatchObject(lstBatch)
            batch_data.append(batch.batchNumber)
            batch_data.append(batch.probe_type)
            batch_data.append(batch.batchQty)
         
            DS.write_to_batch_file(batch_data)
      
            controller.show_frame(CO.Connection)
        except:
            tm.showerror('Select a batch',
                                'Unable to continue testing until you select a batch.')
      
       
        
