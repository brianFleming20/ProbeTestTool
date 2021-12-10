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
import numpy as np
import codecs
from time import gmtime, strftime
import BatchManager
import InstrumentManager
import ProbeManager
from ProbeManager import Probe
from ProbeManager import ProbeManager
import NanoZND
import ODMPlus
import Sessions as SE
import FaultFinder as FF
import datastore


# create instances
IM = InstrumentManager.InstrumentationManager()
BM = BatchManager.BatchManager()
PM = ProbeManager()
ZND = NanoZND.NanoZND()
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
                  width=12).place(relx=0.3, rely=0.45, anchor='w')

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
        
        self.ff_btn = ttk.Button(self, text=' Start fault finding ', command=lambda: controller.show_frame(FF.FaultFindWindow), 
                   width=BTN_WIDTH)
        self.ff_btn.place(relx=0.53, rely=0.7, anchor=CENTER)
        
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
        
        if self.left_to_test.get() == 0:
            
            current_batch = DS.get_batch()[0]

            BM.CompleteBatch(current_batch)
            controller.show_frame(SE.SessionSelectWindow)
            
            
            
    def find_fault_with_probe(self, controller):
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
        self.reprogram = False
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0','end')
        file_data = DS.get_batch()
        user_data = DS.get_user()
        ZND.set_vna_controls(DS.get_analyser_port())
        ZND.flush_analyser_port(DS.get_analyser_port())
        self.text_area.insert('1.0',user_data[0])
        self.text_area.insert('2.0','\nPlease continue testing batch ')
        self.text_area.insert('2.30', file_data[0])
        self.left_to_test.set(file_data[2])
        self.probe_type.set(DS.get_current_probe_type())
        self.current_batch.set(DS.get_current_batch())
        self.current_user.set(DS.get_username())
        self.device_details.set(self.device)
        self.RLLimit = -1  # pass criteria for return loss measurement
        self.user_admin = DS.get_user_status()
        self.programmed = False
        DS.set_plot_status(False)
        
        ##############################
        # Collect analyser port data #
        ##############################
       
        if ZND.get_analyser_port_number(DS.get_analyser_port()):
            self.device = " NanoNVA "
            self.device_details.set(self.device)
    
        if self.user_admin == True:
                self.display_message("Probe re-programming enabled.")
        else:
                self.display_message("Probe re-programming disabled")
        Tk.update(self)
       
        while(self.session_on_going == True):
            
            self.status_image.configure(image=self.greylight)
            if self.left_to_test.get() == False and self.check == False:
                self.session_on_going == False
                self.session_complete == True
          
            if PM.ProbePresent() == False:
                self.ff_btn.config(state=DISABLED)
                self.action.set('Connect New Probe')
                ttk.Label(self, textvariable=self.action, background='yellow',
                    width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w') 
                Tk.update(self) 
                self.update_odm_data()
                self.refresh_window()
                
            if PM.ProbePresent() == True:
           
                self.ff_btn.config(state=NORMAL)
                self.action.set('Probe connected')    
                self.programmed = False
                if PM.ProbePresent() == True:
                    ttk.Label(self, textvariable=self.action, background='#1fff1f',
                        width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w') 
                    Tk.update(self) 
          
                    if PM.ProbeIsProgrammed() == False and self.programmed == False:
                        snum = self.program_probe()
                        results, marker_data = self.test_probe()
                        self.status_image.configure(image=self.amberlight)

                    elif PM.ProbeIsProgrammed() and self.user_admin:
                
                        go = tm.askyesno('Programmed Probe Detected', 
                        'This probe is already programmed.\nDo you wish to re-program and test?') and self.status_image.configure(image=self.amberlight)
                    
                        if go == None:
                            self.display_message("Probe re-programming enabled.")
                            snum = self.program_probe()
                            results, marker_data = self.test_probe()
                            self.update_results(results, snum, marker_data)
                         
                            self.status_image.configure(image=self.amberlight)
                            
                    else:
                        self.display_message("Probe re-programming disabled")
                        self.display_message("You can't re-program this probe.") 
                   
                    # if PM.ZND.get_marker_values()[0] < self.RLLimit and PM.ZND.get_marker_values()[1] < self.RLLimit:
                         
                    self.update_odm_data()
                    Tk.update(self)
                          
            if self.session_complete == True:
                BM.CompleteBatch(BM.current_batch)



    def display_message(self, message):
        self.text_area.config(state=NORMAL)
        self.text_area.delete('3.0','end')
        self.text_area.insert('3.0', "\n\n" + message) 
        self.text_area.config(state=DISABLED)
        


    def program_probe(self):
            probe_type = self.probe_type.get()
         
            serialNumber = PM.ProgramProbe(self.probe_type.get())
            if serialNumber == False:
                tm.showerror('Programming Error',
                                'Unable to program\nPlease check U1')
                self.action.set('Probe failed')
                self.status_image.configure(image=self.redlight)
            snum = str(codecs.decode(serialNumber, "hex"),'utf-8')[1:16]  
      
            self.programmed = True
            Tk.update(self)
            return snum



    def test_probe(self):
        self.action.set('Testing probe...')
        results = PM.TestProbe()
        marker_data = ""
        if results == True:
                analyser_data = ZND.get_marker_3_command(DS.get_analyser_port())
                x = []      
                for line in analyser_data.split('\n'):
                    if line:
                        x.extend([int(d, 16) for d in line.strip().split(' ')])
                        marker_data = np.array(x, dtype=np.int16)
                     
                else:
                    self.display_message("Probe failed")
        if self.RLLimit == -1: #check for crystal pass value, now pass every time
            self.action.set('Testing complete. Disconnect probe')
            self.probes_passed.set(self.probes_passed.get() + 1)
            self.status_image.configure(image=self.greenlight)
            
            
        else:
            self.status_image.configure(image=self.redlight)
            tm.showerror('Return Loss Error',
                                    'Check crystal connections')
        
        return results, marker_data



    def update_odm_data(self):
        # Collect serial data                   
        try:
            serial_results = ODM.ReadSerialODM()
            self.SD_data.set(serial_results[0][5])
            self.FTc_data.set(serial_results[0][6])
            self.PV_data.set(serial_results[0][9])
            if self.user_admin == True:
                self.display_message("Probe re-programming enabled.")
            else:
                self.display_message("Probe re-programming disabled")
            Tk.update(self) 
            return serial_results
        except:
            self.display_message(
                     'Unable to collect the data from the ODM.')
            return False
        


    def update_results(self, results, snum, marker_data):
        data_list_to_file = []
        odm_results = self.update_odm_data()
        BM.UpdateResults(
            results, self.current_batch.get())
        self.left_to_test.set(self.left_to_test.get() - 1)
        self.status_image.configure(image=self.greenlight)
        data_list_to_file.append(snum)
        data_list_to_file.append(marker_data)
        data_list_to_file.append(self.current_user.get())
        data_list_to_file.append(self.current_batch.get())
        data_list_to_file.append(odm_results[0][9])
        BM.saveProbeInfoToCSVFile(data_list_to_file)
        
            