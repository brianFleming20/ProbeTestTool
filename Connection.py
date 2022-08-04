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
import time

BM = BatchManager.BatchManager()
PM = ProbeManager.ProbeManager()
ZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
DS = Datastore.Data_Store()
PT = ProbeTest
PF = ProbeInterface.PRI()
SE = Sessions


def ignore():
    return 'break'


class Connection(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#B1D0E0')

        # self.is_admin = ""
        self.znd_working = False
        self.probe_working = False
        self.monitor_working = False
        self.control = controller
        self.znd = StringVar()
        self.odm = StringVar()
        self.probe = StringVar()

        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(x=40, y=70)
        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 24, 'bold'), width=12).place(x=850, y=25)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 14)).place(x=850, y=57)

        self.label_9 = ttk.Label(self, text=" Press 'Continue' and wait to connect sensors... ", background="#B1D0E0")
        self.label_9.config(font=("Courier", 14))
        self.label_9.place(relx=0.5, rely=0.4, anchor=CENTER)

        ttk.Label(self, text="NanoZND", background="#B1D0E0").place(relx=0.3, rely=0.6)
        ttk.Label(self, textvariable=self.znd, relief=SUNKEN, width=10).place(relx=0.38, rely=0.6)

        ttk.Label(self, text=" Probe ", background="#B1D0E0").place(relx=0.45, rely=0.6)
        ttk.Label(self, textvariable=self.probe, relief=SUNKEN, width=10).place(relx=0.52, rely=0.6)

        ttk.Label(self, text=" Monitor ", background="#B1D0E0").place(relx=0.6, rely=0.6)
        ttk.Label(self, textvariable=self.odm, relief=SUNKEN, width=10).place(relx=0.68, rely=0.6)

        self.confm_btn = tk.Button(self, text='Continue',
                                   width=30, command=lambda: self.test_connections(self.control))
        self.confm_btn.place(relx=0.7, rely=0.8, anchor=CENTER)
        self.confm_btn.config(state=NORMAL)

        tk.Button(self, text='Cancel', padx=2, pady=3, width=20,
                  command=lambda: self.control.show_frame(SE.SessionSelectWindow)).place(relx=0.3,
                                                                                         rely=0.8, anchor=CENTER)

        self.bind('<Return>', self.test_connections)
        self.text_area.insert('1.0', "\nPlease continue to the next screen..")

    def refresh_window(self):
        self.probe.set("")
        self.odm.set("")
        self.znd.set("")

    def test_comms(self):
        # Tests all of the external device connections
        true_ports = []

        analyser_port = self.sort_znd_interface()

        probe_port = self.sort_probe_interface()

        odm_port = self.sort_odm_interface()

        true_ports.append(probe_port)
        true_ports.append(analyser_port)
        true_ports.append(odm_port)
        ports = Ports.Ports(odm=odm_port, probe=probe_port, analyer=analyser_port)
        DS.write_device_to_file(ports)

        Tk.update(self)
        if not probe_port or not analyser_port or not odm_port:
            return False
        else:
            return True

    def sort_probe_interface(self):
        # Tests the probe interface connection

        probe = PF.check_probe_connection()

        self.probe.set(probe)
        self.probe_working = True

        return probe

    def sort_znd_interface(self):
        # Tests the analyser interface connection

        read1 = ZND.get_vna_check()

        self.znd.set(read1)
        self.znd_working = True

        return read1

    def sort_odm_interface(self):
        # Tests the ODM monitor interface connection
        port = "Not in use"
        if DS.get_devices()['odm_active']:
            port = ODM.check_odm_port()

            self.odm.set(port)
            self.monitor_working = True

        return port

    def test_connections(self, controller):

        if self.test_comms():
            if self.probe_working and self.znd_working:
                time.sleep(1)
                controller.show_frame(PT.TestProgramWindow)
            else:
                tm.showinfo("Port info", "Please reset all ports.")
                controller.show_frame(SE.SessionSelectWindow)
        try:
            while PM.ProbePresent():
                self.confm_btn.config(state=DISABLED)
                tm.showerror('Connection Error', 'Remove the inserted probe from the tester.')

                # Check if all connections are true
                self.confm_btn.config(state=NORMAL)
        except:
            pass
