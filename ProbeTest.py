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
        self.odm_details = StringVar()
        self.probe_type = StringVar()
        self.SD_data = IntVar()
        self.FTc_data = IntVar()
        self.PV_data = IntVar()
        self.user_admin = False
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
        ttk.Label(self, textvariable=self.odm_details, relief=SUNKEN,
                  width=30).place(relx=0.7, rely=0.30, anchor='w')
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
        self.ff_btn = ttk.Button(self, text=' Start fault finding ', 
                command=lambda: self.find_fault_with_probe(controller), width=BTN_WIDTH)
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
            self.reset()
            self.refresh_window()
    
      
      

    def suspnd_btn_clicked(self, controller):
        self.session_complete = False
        self.session_on_going = False
        BM.SuspendBatch(self.current_batch.get())
        controller.show_frame(SE.SessionSelectWindow)
    
    
    
    def reset(self):
        self.session_on_going = True
        self.analyser_serial = None
        self.reprogram = False
        current_user = DS.get_username()
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0','end')
        file_data = DS.get_batch()
        ZND.flush_analyser_port()
        ZND.set_vna_controls()
        self.text_area.insert('1.0',current_user)
        self.text_area.insert('2.0','\nPlease continue testing batch ')
        self.text_area.insert('2.30', DS.get_current_batch())
        self.left_to_test.set(file_data[2])
        self.probe_type.set(DS.get_current_probe_type())
        self.current_batch.set(DS.get_current_batch())
        self.current_user.set(current_user)
        self.RLLimit = -1  # pass criteria for return loss measurement
        self.user_admin = DS.get_user_status()
        self.programmed = False
        self.status_image.configure(image=self.greylight)
        ttk.Label(self, textvariable=self.action, background='yellow',
                        width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')
        ##############################
        # Collect analyser port data #
        ##############################
        self.set_display()

  

    def refresh_window(self):
        self.reset()
        if self.user_admin == True:
                self.display_message("Probe re-programming enabled.")
        else:
                self.display_message("Probe re-programming disabled")
        if self.left_to_test.get() == 0:
            self.session_on_going == False
            self.session_complete == True
        Tk.update(self) 
                    
        while self.session_on_going == True:
            self.action.set('Connect New Probe')
            self.ff_btn.config(state=DISABLED)
            DS.set_plot_status(False)
            
            if PM.ProbePresent() == True:
                self.action.set('Probe connected') 
                self.update_odm_data()   
                ttk.Label(self, textvariable=self.action, background='#7FFF00',
                        width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w') 
                Tk.update(self) 
                
                if PM.ProbeIsProgrammed() == False:
                    snum = self.program_probe()
                    results = self.test_probe()
                    marker_data = self.get_marker_data()
                    if snum != False:
                        self.update_results(results, snum, marker_data)
                    break
                        
                elif PM.ProbeIsProgrammed() == True and self.user_admin == True:
                    go = tm.askyesno('Programmed Probe Detected', 
                            'This probe is already programmed.\nDo you wish to re-program and test?')
                    if go == True:
                        self.display_message("Probe re-programming enabled.")
                        snum = self.program_probe()
                        results = self.test_probe()
                        marker_data = self.get_marker_data()
                        if snum != False:
                            self.update_results(results, snum, marker_data)
                            
                        Tk.update(self)    
                    else:
                        self.display_message("Probe re-programming disabled")
                        # if PM.ZND.get_marker_values()[0] < self.RLLimit and PM.ZND.get_marker_values()[1] < self.RLLimit:
                        DS.write_to_admin_file(str([0]))
                        Tk.update(self) 
                        break
                     
            while 1:
                    if PM.ProbePresent() == False:
                        # PM.ClearAnalyzer()
                        self.status_image.configure(image=self.greylight)
                        ttk.Label(self, textvariable=self.action, background='yellow',
                        width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w') 
                        self.action.set('Connect New Probe')
                        self.set_display()
                        Tk.update(self)
                    else:
                        break
                    
        if self.session_complete == True:
                BM.CompleteBatch(BM.current_batch)
                
            
            
    def set_display(self):
        odm = "Not connected to ODM"
        device = "Not connected to analyser"
        if ZND.get_analyser_port_number(DS.get_analyser_port()):
            device = " NanoNVA "
        self.device_details.set(device)
        if ODM.get_monitor_port():
            odm = " ODM Monitor "
        self.odm_details.set(odm)    
            
            
            
    def display_message(self, message):
        self.text_area.config(state=NORMAL)
        self.text_area.delete('3.0','end')
        self.text_area.insert('3.0', "\n\n" + message) 
        self.text_area.config(state=DISABLED)
        


    def program_probe(self):
        self.action.set('Programming probe...')
        self.status_image.configure(image=self.amberlight)
        ttk.Label(self, textvariable=self.action, background='#00BFFF',
                        width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w') 
        Tk.update(self)
        serialNumber = PM.ProgramProbe(self.probe_type.get())
        if serialNumber == False:
            tm.showerror('Programming Error',
                                'Unable to program\nPlease check probe chip.')
            self.action.set('Probe failed')
            
            self.status_image.configure(image=self.redlight)
            ttk.Label(self, textvariable=self.action, background='orange',
                        width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w') 
            Tk.update(self) 
        else:
            snum = str(codecs.decode(serialNumber, "hex"),'utf-8')[:16]  
            self.programmed = True
            return snum
        return False
        


    def test_probe(self):
        self.action.set('Testing probe...')
        ttk.Label(self, textvariable=self.action, background='#00BFFF',
                        width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w') 
        self.ff_btn.config(state=NORMAL)
        Tk.update(self)
        if PM.ProbePresent() == True:
         
            results = PM.TestProbe()
            self.update_odm_data()
            if results == True:
                if self.RLLimit == -1: #check for crystal pass value, now pass every time
                    self.action.set('Testing complete. Disconnect probe')
                    self.status_image.configure(image=self.greenlight)
                else:
                    self.status_image.configure(image=self.redlight)
                    tm.showerror('Return Loss Error',
                                    'Check crystal connections')
            if results == False:
                self.display_message("Probe failed")
                tm.showerror('Probe Info',
                                    'Probe Failed....')
        else:
            tm.showerror('Probe failed',
                                    'Probe removed....')
            self.RLLimit = "removed"
        self.reset()
        return self.RLLimit
    
    

    def get_marker_data(self):
        NFFT = 16384
        analyser_data = ZND.fetch_frequencies()
        window = np.blackman(len(analyser_data))
        td = np.abs(np.fft.ifft(window * analyser_data , NFFT))
        min_freq = np.min(td)
        pk = np.max(td)
        marker = 1/(pk - min_freq)
        
        return marker / 2
        
        

    def update_odm_data(self):
        
        # Collect serial data 
        try:       
            serial_results = ODM.ReadSerialODM()
            if serial_results == []:
                serial_results = [0,0,0,0,0,0,0,0,0,0]
                serial_results = ODM.ReadSerialODM()
            self.SD_data.set(serial_results[5])
            self.FTc_data.set(serial_results[6])
            self.PV_data.set(serial_results[9])
        except:
            False
     


    def update_results(self, results, snum, marker_data):
        print(f"updating results {results} {snum} {marker_data}")
        data_list_to_file = []
        odm_results = self.update_odm_data()
        BM.UpdateResults(
            results, self.current_batch.get())
        self.left_to_test.set(self.left_to_test.get() - 1)
        self.probes_passed.set(self.probes_passed.get() + 1)
        self.status_image.configure(image=self.greenlight)
        data_list_to_file.append(snum)
        data_list_to_file.append(marker_data)
        data_list_to_file.append(self.current_user.get())
        data_list_to_file.append(self.current_batch.get())
        data_list_to_file.append(odm_results[9])
        BM.saveProbeInfoToCSVFile(data_list_to_file)   