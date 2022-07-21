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
import ProbeTest as PT
import BatchManager
from ProbeManager import ProbeManager
from SecurityManager import Users as U
import Datastore
import codecs
import NanoZND
import ODMPlus

PM = ProbeManager()
BM = BatchManager.BatchManager()
ZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
DS = Datastore.Data_Store()


def ignore():
    return 'break'


BTN_WIDTH = 25

REF_LEVEL = (1 << 9)


class FaultFindWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Set up variavles
        self.canvas_back = None
        self.control = controller
        self.current_batch = StringVar()
        self.current_user = StringVar()
        self.probe_type = StringVar()
        self.device_details = StringVar()
        self.serialNumber = StringVar()
        self.read_probe_number = StringVar()
        self.analyser_freq3 = IntVar()
        self.cable_len = IntVar()
        self.fault_message = StringVar()
        self.plot_text = StringVar()
        self.action = StringVar()
        self.analyser_results = []
        self.SD_data = IntVar()
        self.FTc_data = IntVar()
        self.PV_data = IntVar()
        self.wait_for_test = True
        self.user_admin = DS.user_admin_status()
        self.analyser_port = DS.get_devices()['Analyser']
        self.cable_length = 0
        self.device = "Not connected to analyser"

    def display(self):
        # Import images
        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 24, 'bold'), width=12).place(x=850, y=25)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 14)).place(x=850, y=57)

        self.text_area = tk.Text(self.canvas_back, height=5, width=40)
        self.text_area.place(x=40, y=70)
        self.text_area.delete('1.0', 'end')

        ttk.Label(self.canvas_back, text='Batch number: ', background='#B1D0E0').place(
            relx=0.1, rely=0.3, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.current_batch, relief=SUNKEN, font="bold",
                  width=15).place(relx=0.2, rely=0.3, anchor='w')

        ttk.Label(self.canvas_back, text='Probe type: ', background='#B1D0E0').place(
            relx=0.1, rely=0.38, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.probe_type, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.2, rely=0.38, anchor='w')

        ttk.Label(self.canvas_back, text='Connected to: ', background='#B1D0E0').place(
            relx=0.1, rely=0.44, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.device_details, relief=SUNKEN,
                  width=30).place(relx=0.2, rely=0.44, anchor='w')

        ttk.Label(self.canvas_back, text="cable length. ", background='#B1D0E0').place(relx=0.2, rely=0.53, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.cable_len, relief=SUNKEN,
                  width=10).place(relx=0.35, rely=0.53, anchor='w')

        ttk.Label(self.canvas_back, text='Serial Number: ', background='#B1D0E0').place(
            relx=0.68, rely=0.18, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.serialNumber, relief=SUNKEN, width=28).place(relx=0.68, rely=0.25, anchor='w')
        ttk.Label(self.canvas_back, text='From Batch: ', background='#B1D0E0').place(
            relx=0.58, rely=0.25, anchor='w')
        ttk.Label(self.canvas_back, text='From Probe: ', background='#B1D0E0').place(
            relx=0.58, rely=0.3, anchor='w')

        ttk.Label(self.canvas_back, textvariable=self.read_probe_number, relief=SUNKEN, width=28).place(relx=0.68, rely=0.3,
                                                                                            anchor='w')

        ttk.Label(self.canvas_back, text="Probe parameter data", background='#B1D0E0').place(
            relx=0.7, rely=0.42, anchor="w")
        ttk.Label(self.canvas_back, text="SD", background='#B1D0E0').place(relx=0.70, rely=0.46, anchor="w")
        ttk.Label(self.canvas_back, text="FTc", background='#B1D0E0').place(relx=0.77, rely=0.46, anchor="w")
        ttk.Label(self.canvas_back, text="PV", background='#B1D0E0').place(relx=0.85, rely=0.46, anchor="w")
        ttk.Label(self.canvas_back, textvariable=self.SD_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.69, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.FTc_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.76, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.PV_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.84, rely=0.51, anchor='w')

        ttk.Label(self.canvas_back, text='Action: ', background='#B1D0E0').place(relx=0.1, rely=0.65, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.action, background='#99c2ff',
                  width=40, relief=GROOVE).place(relx=0.2, rely=0.65, anchor='w')

        self.cancel_btn = ttk.Button(self.canvas_back, text='Cancel',command= self.break_out)
        self.cancel_btn.place(relx=0.6, rely=0.75, anchor=CENTER)
        ttk.Button(self.canvas_back, text='Show Graph',
                   command=lambda: self.show_plot()).place(relx=0.72, rely=0.58, anchor=CENTER)
        ttk.Label(self.canvas_back, textvariable=self.plot_text, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.8, rely=0.58, anchor='w')
        ttk.Label(self.canvas_back, text='Faults found: ', background='#B1D0E0').place(
            relx=0.1, rely=0.75, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.fault_message, relief=SUNKEN, font="bold",
                                         width=30).place(relx=0.2, rely=0.75, anchor='w')
        Label(self.canvas_back, text="Remove probe when finished",background="#B1D0E0").place(x=400,y=520)

    def show_plot(self):
        admin = DS.user_admin_status()
        name = DS.get_username()
        if not DS.get_plot_status():
            status = U(name,admin,plot=True)
            DS.write_user_data(status)
            self.plot_text.set("ON")
            self.control.attributes('-topmost', False)
        else:
            status = U(name,admin,plot=False)
            DS.write_user_data(status)
            self.plot_text.set("OFF")
            self.control.attributes('-topmost', True)
        self.cable_length = round(ZND.tdr(), 3)

    def break_out(self):
        self.canvas_back.destroy()
        self.control.show_frame(PT.TestProgramWindow)

    def setup(self):
        self.text_area.delete('1.0', 'end')
        self.RLLimit = -1  # pass criteria for return loss measurement
        self.plot_text.set("OFF")
        ZND.flush_analyser_port()
        ZND.set_vna_controls()
        self.text_area.insert('1.0', DS.get_username())
        self.text_area.insert('2.0', '\nFault finding batch ')
        self.text_area.insert('2.30', DS.get_current_batch())
        self.probe_type.set(DS.get_current_probe_type())
        self.current_batch.set(DS.get_current_batch())
        self.current_user.set(DS.get_username())
        self.device_details.set(self.device)
        self.serialNumber.set(" ")
        self.read_probe_number.set(" ")
        self.text_area.config(state=DISABLED)
        self.fault_message.set("")
        if ZND.get_analyser_port_number(self.analyser_port):
            self.device = " NanoNVA "
            self.device_details.set(self.device)

    def refresh_window(self):
        self.canvas_back = Canvas(bg='#B1D0E0',width=980,height=600)
        self.canvas_back.place(x=10, y=10)
        self.display()
        self.setup()
        self.wait_for_test = True
        while PM.ProbePresent():
            read = self.get_serial_numbers()
            try:
                self.read_probe_number.set(str(read, 'utf-8')[:16])
            except:
                self.read_probe_number.set("Unable to read")
            self.fault_find_probe()
            self.update_odm_data()
            # if PM.ProbePresent() and self.wait_for_test:
            #     read = self.get_serial_numbers()
            #     try:
            #         self.read_probe_number.set(str(read, 'utf-8')[:16])
            #     except:
            #         self.read_probe_number.set("Unable to read")
            #     self.fault_find_probe()
            #     self.update_odm_data()
            if not PM.ProbePresent():
                break
        # if not PM.ProbePresent():
        self.cancel_btn.config(state=NORMAL)
        self.action.set('No probe connected...')
        ttk.Label(self.canvas_back, textvariable=self.action, background='yellow',
                          width=40, relief=GROOVE).place(relx=0.2, rely=0.65, anchor='w')
                # Tk.update(self)
        self.fault_message.set("")
        self.analyser_freq3.set(0)
        self.cable_len.set(0)
        self.wait_for_test = False
        Tk.update(self)

            # if not self.wait_for_test:
            #     self.cancel_btn.config(state=NORMAL)
            #     break

    def get_serial_numbers(self):
        serial_number = BM.CSVM.ReadLastLine(DS.get_current_batch())
        if len(serial_number[0][1]) < 7:
            self.serialNumber.set(serial_number[0][2])
        else:
            self.serialNumber.set(serial_number[0][1])
        pcb_serial_number = PM.read_serial_number()
        binary_str = codecs.decode(pcb_serial_number, "hex")
        return binary_str

    def update_odm_data(self):
        serial_results = ODM.ReadSerialODM()
        if serial_results == []:
            serial_results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.SD_data.set(serial_results[5])
        self.FTc_data.set(serial_results[6])
        self.PV_data.set(serial_results[9])

    def fault_find_probe(self):
        self.cable_length = 0
        while PM.ProbePresent():
            self.cancel_btn.config(state=DISABLED)
            if not PM.ProbeIsProgrammed():
                ttk.Label(self.canvas_back, textvariable=self.action, background='#99c2ff',
                          width=40, relief=GROOVE).place(relx=0.2, rely=0.65, anchor='w')
            else:
                self.action.set('Programmed Probe connected')
                ttk.Label(self.canvas_back, textvariable=self.action, background='#1fff1f',
                          width=40, relief=GROOVE).place(relx=0.2, rely=0.65, anchor='w')
            fault = self.test_probe()
            self.fault_message.set(fault)
            self.cable_len.set(self.cable_length)
            # self.set_cable_length()
            Tk.update(self)

    def test_probe(self):
        fault = "Unknown"
        self.fault_text = ["No Fault", "Unkown", "Break in Blue wire",
                           "S/C in Red/Black wires", "S/C in Blue/Green wires",
                           "Break in Black wire", "Break in Green wire",
                           "Signal wires connected", "S/C Screen to Blue wire",
                           "Break in Red wire", "Crystal Fault",
                           "S/C Screen to Red wires"]
        # No Fault
        if self.cable_length > 1.14 and self.cable_length < 1.25:
            fault = self.fault_text[0]
        # S/C Red / Black wires
        if self.cable_length > 1.45 and self.cable_length < 1.40:
            fault = self.fault_text[3]
        # S/C in Blue / Green wires
        if self.cable_length > -0.1 and self.cable_length < -0.00:
            fault = self.fault_text[4]
        # S/C Screen / Blue wire
        if self.cable_length > 1.175 and self.cable_length < 1.19:
            fault = self.fault_text[8]
        # S/C Screen / Red wires
        if self.cable_length > 0.005 and self.cable_length < 0.01:
            fault = self.fault_text[-1]
        # Green wire disconnected
        if self.cable_length > 0.001 and self.cable_length < -0.001:
            fault = self.fault_text[6]
        # Black wire disconnected
        if self.cable_length > 0.001 and self.cable_length < 0.003:
            fault = self.fault_text[7]
        # Break in Blue wire
        if self.cable_length > -0.01 and self.cable_length < -0.01:
            fault = self.fault_text[5]
        # Break in Red wire
        if self.cable_length > 1.3 and self.cable_length < 0.01:
            fault = self.fault_text[8]
        # Crystal fault
        if self.cable_length > 000 and self.cable_length < 0.01:
            fault = self.fault_text[10]
        return fault
