"""
Created on 3 May 2017
@author: jackw
@author: Brian F
Naming convention
- Variables = no spaces, capitals for every word except the first : thisIsAVariable
- Local functions = prefixed with _, _ for spaces, no capitals : _a_local_function

"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
import BatchManager
import ProbeManager
import NanoZND
import ODMPlus
import Sessions
import Connection
import Datastore
from Connection import Ports

BM = BatchManager.BatchManager()
PM = ProbeManager.ProbeManager()
NanoZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
CO = Connection
DS = Datastore.DataStore()
SE = Sessions
P = Ports


def ignore():
    return 'break'


class ConnectionWindow(tk.Frame):
    def __init__(self, parent, controller):
        self.is_admin = ""
        # create the window and frame
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        self.label_9 = ttk.Label(self, text=" Please press connect to continue... ")
        self.label_9.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.connectBtn = ttk.Button(
            self, text="Connect", command=lambda: self._connect_btn_clicked(controller))
        self.connectBtn.grid(row=2, column=1)
        self.connectBtn.place(relx=0.4, rely=0.82, anchor=CENTER)
        self.bind('<Return>', self._connect_btn_clicked)
        self.cancelBtn = ttk.Button(
            self, text="Cancel", command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.cancelBtn.place(relx=0.6, rely=0.82, anchor=CENTER)
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(x=40, y=70)

    def refresh_window(self):
        try:
            admin_data = DS.get_username()
            self.is_admin = admin_data[1]
        except:
            self.text_area.delete('3.0', 'end')
            self.text_area.insert('3.0', "\nError in getting Admin data...")

        self.text_area.config(state=NORMAL)
        self.text_area.insert('2.0', DS.user_admin_status())
        self.text_area.insert('2.0', '\n\nPlease connect the external devices\nand progress to the testing screen.')
        self.text_area.config(state=DISABLED)

    def _connect_btn_clicked(self, controller):
        self.is_admin = DS.user_admin_status()
        if self.is_admin:
            controller.show_frame()
        else:
            controller.show_frame(CO.Connection)
        self.text_area.config(state=NORMAL)
        self.text_area.insert('1.0', 'Continue to check device connections...')
        self.text_area.config(state=DISABLED)


class ConnectionAdmin(tk.Frame):
    def __init__(self, parent, controller):
        self.is_admin = None
        self.monitor = StringVar()
        self.com_port = StringVar()
        self.analyser_usb = StringVar()
        self.move_probe = StringVar()
        self.analyser_usb.set('COM4')
        self.com_port.set('COM3')
        self.monitor.set('COM5')
        self.move_probe.set('Not Set')
        tk.Frame.__init__(self, parent, bg='#E0FFFF')
        self.label_1 = ttk.Label(self, text="ODM monitor port")
        self.label_2 = ttk.Label(self, text="Probe Interface Port")
        self.label_3 = ttk.Label(self, text="Analyser port")
        self.label_5 = ttk.Label(self, text="Probe Movement Interface")
        self.entry_1 = ttk.Entry(self, textvariable=self.monitor, )
        self.entry_2 = ttk.Entry(self, textvariable=self.com_port, )
        self.entry_3 = ttk.Entry(self, textvariable=self.analyser_usb, )
        self.entry_5 = ttk.Entry(self, textvariable=self.move_probe)
        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 28, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 18)).place(relx=0.85, rely=0.15)
        self.label_1.place(relx=0.275, rely=0.3, anchor=CENTER)
        self.label_2.place(relx=0.275, rely=0.5, anchor=CENTER)
        self.label_3.place(relx=0.275, rely=0.4, anchor=CENTER)
        self.label_5.place(relx=0.275, rely=0.6, anchor=CENTER)
        self.entry_1.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.entry_2.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.entry_3.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.entry_5.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.connectBtn = ttk.Button(
            self, text="Connect", command=lambda: self._connect_btn_clicked(controller))
        self.connectBtn.grid(row=2, column=1)
        self.connectBtn.place(relx=0.4, rely=0.82, anchor=CENTER)
        self.cancelBtn = ttk.Button(
            self, text="Cancel", command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.cancelBtn.place(relx=0.6, rely=0.82, anchor=CENTER)
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.25, rely=0.15, anchor=CENTER)

    def refresh_window(self):
        user_data = [DS.get_username()]
        self.is_admin = user_data[1]
        self.text_area.config(state=NORMAL)
        self.text_area.insert('2.0', DS.user_admin_status())
        self.text_area.insert('2.0', '\n\nPlease check any external devices\nand press continue...')
        self.text_area.config(state=DISABLED)

    def _connect_btn_clicked(self, controller):
        connection = P.Ports(odm=self.monitor.get(), probe=self.com_port.get(), analyer=self.analyser_usb.get())
        DS.write_device_to_file(connection)
        controller.show_frame(CO.Connection)
