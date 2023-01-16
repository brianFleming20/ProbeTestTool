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
import ProbeManager
import NanoZND
import ODMPlus
import ProbeTest
import Sessions
import Datastore
import ProbeInterface
import Ports
from time import sleep

BM = BatchManager.BatchManager()
PM = ProbeManager.ProbeManager()
ZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
DS = Datastore.Data_Store()
PT = ProbeTest
PF = ProbeInterface.PRI()
SE = Sessions
P = Ports

def ignore():
    return 'break'


def sort_probe_interface(self):
    # Tests the probe interface connection
    probe = PF.check_probe_connection()
    if probe:
        self.probe_working = True
    else:
        probe = "Not connected"
        self.probe_working = False
        self.probe.set(probe)
    return probe


def check_analyser():
    return ZND.get_vna_check()


class Connection(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#B1D0E0')
        self.znd_working = False
        self.probe_working = False
        self.monitor_working = False
        self.control = controller
        self.znd = StringVar()
        self.odm = StringVar()
        self.probe = StringVar()
        self.test = False
        self.text_area = tk.Text(self, font=("Courier",14),height=5, width=38)
        self.text_area.place(x=40, y=70)
        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 30, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 16)).place(relx=0.88, rely=0.15)

        self.label_9 = ttk.Label(self, text=" Press 'Continue' and wait to connect sensors... ", background="#B1D0E0")
        self.label_9.config(font=("Courier", 16))
        self.label_9.place(relx=0.5, rely=0.4, anchor=CENTER)
        ttk.Label(self, text="NanoZND", background="#B1D0E0", font=("Courier",14)).place(relx=0.25, rely=0.6)
        ttk.Label(self, textvariable=self.znd, relief=SUNKEN, font=("Courier",14)).place(relx=0.33, rely=0.6)
        ttk.Label(self, text=" Probe ", background="#B1D0E0", font=("Courier",14)).place(relx=0.38, rely=0.6)
        ttk.Label(self, textvariable=self.probe, relief=SUNKEN, font=("Courier",14)).place(relx=0.45, rely=0.6)
        ttk.Label(self, text=" Monitor ", background="#B1D0E0", font=("Courier",14)).place(relx=0.57, rely=0.6)
        ttk.Label(self, textvariable=self.odm, relief=SUNKEN, font=("Courier",14)).place(relx=0.65, rely=0.6)
        self.confm_btn = tk.Button(self, text='Continue', font=("Courier", 18),
                                   width=25, command= self.test_connections)
        self.confm_btn.place(relx=0.7, rely=0.8, anchor=CENTER)
        self.confm_btn.config(state=NORMAL)
        tk.Button(self, text='Cancel', font=("Courier", 12), width=20,command=self.to_sessions).place(relx=0.3,
                                                                                         rely=0.8, anchor=CENTER)
        self.bind('<Return>', self.test_connections)
        self.text_area.insert('1.0', "\nPlease continue to the next screen..")

    def refresh_window(self):
        self.probe.set("---")
        self.odm.set("---")
        self.znd.set("---")
        analyser_port = self.sort_znd_interface()
        probe_port = sort_probe_interface(self)
        odm_port = self.sort_odm_interface()
        if not odm_port:
            odm_active = False
        else:
            odm_active = True
        ports = Ports.Ports(odm=odm_port, probe=probe_port, analyer=analyser_port, active=odm_active)
        DS.write_device_to_file(ports)
        Tk.update(self)
        self.test_connections()

    def sort_znd_interface(self):
        # Tests the analyser interface connection
        read1 = check_analyser()
        if not read1:
            read1 = check_analyser()
        self.znd.set(read1)
        self.znd_working = True
        return read1

    def sort_odm_interface(self):
        # Tests the ODM monitor interface connection
        port = None
        if DS.get_monitor_setting():
            port = ODM.check_odm_port()
            if port:
                self.monitor_working = True
                self.odm.set(port)
            else:
                self.monitor_working = False
                # port = "Monitor not in use"
                port = False
        else:
            self.odm.set("Monitor not is use")
        return port

    def test_connections(self):
        if self.probe_working and self.znd_working:
            if not self.test:
                self.control.show_frame(PT.TestProgramWindow)
        else:
            self.to_sessions()

    def to_sessions(self):
        self.control.show_frame(SE.SessionSelectWindow)

    def yes_answer(self):
        self.info_canvas = True

    def no_answer(self):
        self.info_canvas = False

    def set_test(self):
        self.test = True
