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
from ProbeManager import ProbeManager
import datastore
import codecs
import NanoZND
import ODMPlus



from time import gmtime, strftime
PM = ProbeManager()
BM = BatchManager.BatchManager()
ZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
DS = datastore.DataStore()


def ignore():
    return 'break'

BTN_WIDTH = 25

REF_LEVEL = (1<<9)

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
        # self.analyserarker3 = IntVar()
        self.analyser_freq3 = IntVar()
        # self.analyserData2 = IntVar()
        self.cable_len = StringVar()
        self.fault_message = StringVar()
        self.plot_text = StringVar()
        self.action = StringVar()
        self.analyser_results = []
        self.SD_data = IntVar()
        self.FTc_data = IntVar()
        self.PV_data = IntVar()
        self.device = "Not connected to analyser"
       
        # List of fault messages
        self.no_fault = "No Faults"
        self.tx_fault = "Black or Red wire broken"
        self.rx_fault = "Blue or Green wire broken"
        self.screen_fault = "Check screen wires"
        self.crystal_error = "Check crystal"
        
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
        # ttk.Label(self, textvariable=self.analyser_freq3, relief=SUNKEN,
        #           width=10).place(relx=0.35, rely=0.48, anchor='w')
        ttk.Label(self, textvariable=self.cable_len, relief=SUNKEN,
                  width=10).place(relx=0.35, rely=0.53, anchor='w')
     
        # ttk.Label(self,text="marker 3. ").place(relx=0.2, rely=0.48, anchor='w')
        ttk.Label(self,text="cable length. ").place(relx=0.2, rely=0.53, anchor='w')
     
        
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
        
        ttk.Label(self, text='Action: ').place(relx=0.1, rely=0.65, anchor='w')
        ttk.Label(self, textvariable=self.action, background='#99c2ff',
                  width=40, relief=GROOVE).place(relx=0.2, rely=0.65, anchor='w')
        
        self.cancel_btn = ttk.Button(
            self, text='Cancel', command=lambda: controller.show_frame(PT.TestProgramWindow))
        self.cancel_btn.place(relx=0.6, rely=0.75, anchor=CENTER)
        self.show_btn = ttk.Button(
            self, text='Show plot', command=lambda: self.show_plot())
        self.show_btn.place(relx=0.72, rely=0.58, anchor=CENTER)
        ttk.Label(self, textvariable=self.plot_text, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.8, rely=0.58, anchor='w')
        ttk.Label(self, text='Faults found: ').place(
            relx=0.1, rely=0.75, anchor='w')
        self.message_display = ttk.Label(self, textvariable=self.fault_message, relief=SUNKEN, font="bold", 
                                         width=30).place(relx=0.2, rely=0.75, anchor='w')

    def show_plot(self):
        if DS.get_plot_status() == False:
            DS.set_plot_status(True)
         
            self.plot_text.set("ON")
        else:
            DS.set_plot_status(False)
      
            self.plot_text.set("OFF")
            
    

        
    def refresh_window(self):
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0','end')
        self.RLLimit = -1  # pass criteria for return loss measurement
        self.plot_text.set("OFF")
        file_data = DS.get_batch()
        user_data = DS.get_user()
        self.user_admin = DS.get_user_admin_status()
        self.analyser_port = DS.get_analyser_port()
        ZND.flush_analyser_port()
        ZND.set_vna_controls()
        self.text_area.insert('1.0',DS.get_username())
        self.text_area.insert('2.0','\nFault finding batch ')
        self.text_area.insert('2.30', file_data[0])
        self.probe_type.set(file_data[1])
        self.current_batch.set(file_data[0])
        self.current_user.set(user_data[0])
        self.device_details.set(self.device)
        self.serialNumber.set(" ")
        self.readSerialNumber.set(" ")
        self.text_area.config(state=NORMAL)
        self.ProbeIsProgrammed = PM.ProbeIsProgrammed()
        self.cable_length = 0
        self.fault_message.set("")
        Tk.update(self)
        
        
        if ZND.get_analyser_port_number(self.analyser_port):
                         # Set the device connected name
                self.device = " NanoNVA "
                self.device_details.set(self.device) 
                self.check_for_probe()
                        # Get the analyser to generate data points and return them
            
    def check_for_probe(self):
        while PM.ProbePresent() == False:
            self.cancel_btn.config(state=NORMAL)
            self.action.set('No probe connected...')
            ttk.Label(self, textvariable=self.action, background='yellow',
                        width=40, relief=GROOVE).place(relx=0.2, rely=0.65, anchor='w')
            ZND.set_vna_controls() 
            Tk.update(self)
                
        if PM.ProbePresent() == True:       
            self.get_serial_numbers()
            self.fault_message.set("")    
            self.fault_find_probe()
        
        if PM.ProbePresent() == False:
            self.fault_message.set("")
            self.refresh_window()
               
        
    def get_serial_numbers(self):
        serial_number = BM.CSVM.ReadLastLine(DS.get_current_batch())
        self.serialNumber.set(serial_number[0][0])
     
        pcb_serial_number = PM.read_serial_number()
        binary_str = codecs.decode(pcb_serial_number, "hex")
        self.readSerialNumber.set(str(binary_str,'utf-8')[:15]) 
        
        
    
    def show_odm_data(self):
        try:
            self.text_area.delete('3.0','end')
            serial_results = ODM.ReadSerialODM()
            self.SD_data.set(serial_results[5])
            self.FTc_data.set(serial_results[6])
            self.PV_data.set(serial_results[9])
        except:
            pass
        
        
        
        
    def fault_find_probe(self):
        # marker3 = ""
        
        while PM.ProbePresent() == True:
            self.cancel_btn.config(state=DISABLED)
            if self.ProbeIsProgrammed == False: 
                
                self.action.set('Probe not programmed...')
            else:
                self.action.set('Programmed Probe connected')
                ttk.Label(self, textvariable=self.action, background='#1fff1f',
                        width=40, relief=GROOVE).place(relx=0.2, rely=0.65, anchor='w')
            
            self.cable_length = ZND.tdr()
            if self.cable_length > 0.83 and self.cable_length < 0.9:
                self.fault_message.set(self.no_fault)
            
            # marker3 = ZND.get_marker_3_command()
            # marker3_id,marker3_val,marker3_freq = marker3.split(' ')
                    
            # marker1 = ZND.get_marker_1_command()
            # marker1_id,marker1_val,marker1_freq = marker1.split(' ')
            
                 
            self.cable_len.set(round(self.cable_length, 3))
            # print(f"Cable length = {cable_length}")
            # freq3 = marker3_freq[:6]
         
            # self.analyser_freq3.set(freq3)
         
            self.show_odm_data()
            Tk.update(self)
                       
        if PM.ProbePresent() == False:
            self.fault_message.set("")
            self.analyser_freq3.set(0)
         
            self.cable_length = 0
            self.cable_len.set(self.cable_length)
            self.action.set('No probe connected...')
            ttk.Label(self, textvariable=self.action, background='yellow',
                        width=40, relief=GROOVE).place(relx=0.2, rely=0.65, anchor='w')
            Tk.update(self)
        