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
import ProbeTest
import BatchManager
from ProbeManager import ProbeManager
import Datastore
import NanoZND
import ODMPlus
import Ports
import RetestProbe

PM = ProbeManager()
BM = BatchManager.BatchManager()
ZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
DS = Datastore.Data_Store()
PT = ProbeTest
P = Ports
RT = RetestProbe


BTN_WIDTH = 25

# REF_LEVEL = (1 << 9)


class FaultFindWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas_back = None
        self.control = controller
        self.current_batch = StringVar()
        self.current_user = StringVar()
        self.probe_type = StringVar()
        self.device_details = StringVar()
        self.serialNumber = StringVar()
        self.read_probe_number = StringVar()
        self.cable_code = IntVar()
        self.fault_message = StringVar()
        self.plot_text = StringVar()
        self.action = StringVar()
        self.analyser_results = []
        self.SD_data = IntVar()
        self.FTc_data = IntVar()
        self.PV_data = IntVar()
        self.wait_for_test = True
        self.test = False
        self.user_admin = DS.user_admin_status()
        self.analyser_port = DS.get_devices()['Analyser']
        self.cable_length_code = 0
        self.device = "Not connected to analyser"
        self.graph_text = StringVar()

    def display(self):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        self.cent_x = ws / 2
        self.cent_y = hs / 2
        self.canvas_back = Canvas(bg='#B1D0E0', width=ws - 10, height=hs - 10)
        self.canvas_back.place(x=5, y=5)
        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 28, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 18)).place(relx=0.85, rely=0.15)
        self.graph_text.set("Show Graph")
        self.text_area = tk.Text(self.canvas_back, font=("Courier", 14), height=5, width=40)
        self.text_area.place(relx=0.07, rely=0.07)
        self.text_area.delete('1.0', 'end')

        ttk.Label(self.canvas_back, text='Batch number: ', background='#B1D0E0', font=("Courier", 14)).place(
            relx=0.1, rely=0.3, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.current_batch, font=("Courier", 14), relief=SUNKEN,
                  width=15).place(relx=0.25, rely=0.3, anchor='w')

        ttk.Label(self.canvas_back, text='Probe type: ', background='#B1D0E0', font=("Courier", 14)).place(
            relx=0.1, rely=0.38, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.probe_type, relief=SUNKEN, font=("Courier", 14),
                  width=10).place(relx=0.25, rely=0.38, anchor='w')

        ttk.Label(self.canvas_back, text='Connected to: ', background='#B1D0E0', font=("Courier", 14)).place(
            relx=0.1, rely=0.44, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.device_details, font=("Courier", 14), relief=SUNKEN,
                  width=30).place(relx=0.25, rely=0.44, anchor='w')

        ttk.Label(self.canvas_back, text="cable code. ",
                  background='#B1D0E0', font=("Courier", 14)).place(relx=0.1, rely=0.53, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.cable_code, relief=SUNKEN,
                  width=14, font=("Courier", 14)).place(relx=0.25, rely=0.53, anchor='w')

        ttk.Label(self.canvas_back, text='Serial Number: ', background='#B1D0E0', font=("Courier", 16)).place(
            relx=0.68, rely=0.18, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.read_probe_number,
                  relief=SUNKEN, width=20, font=("Courier", 20)).place(relx=0.68, rely=0.25, anchor='w')
        ttk.Label(self.canvas_back, text='From Probe:', background='#B1D0E0', font=("Courier", 16)).place(
            relx=0.56, rely=0.25, anchor='w')

        ttk.Label(self.canvas_back, text="Probe parameter data", background='#B1D0E0', font=("Courier", 14)).place(
            relx=0.7, rely=0.42, anchor="w")
        ttk.Label(self.canvas_back, text="SD", background='#B1D0E0', font=("Courier", 14)).place(relx=0.70, rely=0.46,
                                                                                                 anchor="w")
        ttk.Label(self.canvas_back, text="FTc", background='#B1D0E0', font=("Courier", 14)).place(relx=0.77, rely=0.46,
                                                                                                  anchor="w")
        ttk.Label(self.canvas_back, text="PV", background='#B1D0E0', font=("Courier", 14)).place(relx=0.85, rely=0.46,
                                                                                                 anchor="w")
        ttk.Label(self.canvas_back, textvariable=self.SD_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.69, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.FTc_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.76, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.PV_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.84, rely=0.51, anchor='w')

        ttk.Label(self.canvas_back, text='Action: ', background='#B1D0E0', font=("Courier", 14)).place(relx=0.1,
                                                                                                       rely=0.65,
                                                                                                       anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.action, background='#99c2ff',
                  width=28, relief=GROOVE, font=("Courier", 16)).place(relx=0.25, rely=0.65, anchor='w')

        Button(self.canvas_back, textvariable=self.graph_text, font=('Arial', 14),
               command=self.show_plot).place(relx=0.78, rely=0.58, anchor=CENTER)
        ttk.Label(self.canvas_back, text='Faults found: ', background='#B1D0E0', font=("Courier", 14)).place(
            relx=0.1, rely=0.75, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.fault_message, relief=SUNKEN, font=("Courier", 16),
                  width=30).place(relx=0.25, rely=0.75, anchor='w')
        Label(self.canvas_back, text="Remove probe when finished", background="#B1D0E0",
              font=("Courier", 14)).place(relx=0.4, rely=0.85)
        self.setup()
        Tk.update(self)

    def show_plot(self):
        admin = DS.user_admin_status()
        name = DS.get_username()
        if not DS.get_plot_status():
            self.graph_text.set("Remove Graph")
            status = P.Users(name, admin, plot=True)
            DS.write_user_data(status)
            self.control.attributes('-topmost', False)
        else:
            self.graph_text.set("Show Graph")
            status = P.Users(name, admin, plot=False)
            DS.write_user_data(status)
            self.control.attributes('-topmost', True)
        self.cable_length_code = round(ZND.tdr(), 3)

    def break_out(self):
        if DS.get_plot_status():
            self.show_plot()
        ZND.close()
        self.canvas_back.destroy()
        self.control.show_frame(PT.TestProgramWindow)

    def setup(self):
        self.text_area.delete('1.0', 'end')
        self.RLLimit = -1  # pass criteria for return loss measurement
        ZND.flush_analyser_port()
        ZND.set_vna_controls()
        batch_data = DS.get_probe_data()
        self.text_area.insert('1.0', DS.get_username().title())
        self.text_area.insert('2.0', '\nCurrent batch ')
        self.text_area.insert('2.30', batch_data['Batch'])
        self.probe_type.set(batch_data['Probe_Type'])
        batch, serial_number = PT.detect_recorded_probe()
        if not batch:
            batch = "Not Found"
        self.current_batch.set(batch)
        self.read_probe_number.set(serial_number)
        self.current_user.set(DS.get_username())
        self.device_details.set(self.device)
        self.serialNumber.set(" ")
        self.read_probe_number.set(" ")
        self.text_area.config(state=DISABLED)
        self.fault_message.set("")
        vna = ZND.get_vna_check()
        if vna == DS.get_devices()['Analyser']:
            self.device = " NanoNVA "
            self.device_details.set(self.device)
        Tk.update(self)

    def refresh_window(self):
        self.display()
        self.plot_text.set("OFF")
        while PM.ProbePresent():
            self.read_probe_number.set(self.get_probe_serial_number())
            self.fault_find_probe()
        self.break_out()

    def get_probe_serial_number(self):
        return PM.read_serial_number()

    def update_odm_data(self):
        if DS.get_devices()['odm_active']:
            try:
                serial_results = ODM.ReadSerialODM()
            except IOError:
                pass
            else:
                if not serial_results:
                    serial_results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                self.SD_data.set(serial_results[5])
                self.FTc_data.set(serial_results[6])
                self.PV_data.set(serial_results[9])
                Tk.update(self)

    def fault_find_probe(self):
        if not PM.ProbeIsProgrammed():
            self.action.set('No serial number detected')
            ttk.Label(self.canvas_back, textvariable=self.action, background='#99c2ff',
                      width=28, relief=GROOVE, font=("Courier", 16)).place(relx=0.25, rely=0.65, anchor='w')
        else:
            self.action.set('Programmed Probe connected')
            ttk.Label(self.canvas_back, textvariable=self.action, background='#1fff1f',
                      width=28, relief=GROOVE, font=("Courier", 16)).place(relx=0.25, rely=0.65, anchor='w')
        Tk.update(self)
        fault = self.test_probe()
        self.fault_message.set(fault)
        self.update_odm_data()

    def test_probe(self):
        cable = self.get_cable_length()
        self.cable_code.set(cable)
        fault = "Unknown"
        # probe_passed = "No Fault"
        upper = self.get_lower_limit()
        lower = self.get_upper_limit()
        # self.fault_text = ["No Fault", "Unknown", "Break in Blue/Green wire",
        #                    "Break in Red/Black wires", "Poor pass Red/Black",
        #                    "Poor pass Blue/Green", "Poor pass Red/Black",
        #                    "Signal wires connected", "S/C Screen to Blue wire",
        #                    "Break in Red wire", "Crystal Fault",
        #                    "S/C Screen to Red wires"]
        ############################################################
        # Adjusting the limits for each of the failure types could #
        # be achieved by using the lower and upper limits with a   #
        # calculation on each fault required to find.              #
        # These parameters can be inserted into the Admin screen   #
        # to be adjusted from there. The limits would have to be   #
        # recorded in the system data sets.                        #
        ############################################################
        fault_fails = [
            {(lower, upper): "No Fault"},
            {(0.6, 0.8): "Break in Blue / Green wire"},
            {(2.8, 5.0): "Short circuit in crystal"},
            {(0.01, 0.1): "Open circuit Black / Blue wire"},
            {(0.1, 0.4): "Crystal fault"},
            {(0.4, 0.5): "S/C  to screen"}
        ]
        # No Fault
        # if lower < cable < upper:
        #     fault = probe_passed
        for items in fault_fails:
            data = list(items.keys())[0]
            lower_data = float(data[0])
            upper_data = float(data[1])
            val = list(items.values())[0]
            if lower_data < cable < upper_data:
                fault = val
            if self.test:
                print(f" {lower_data} - {upper_data} : {val} cable = {cable}")
        return fault

    def yes_answer(self):
        self.info_canvas = True

    def no_answer(self):
        self.info_canvas = False

    def get_cable_length(self):
        return ZND.tdr()

    def get_upper_limit(self):
        return PT.UPPER_LIMIT

    def get_lower_limit(self):
        return PT.LOWER_LIMIT

    def set_test(self):
        self.test = True
