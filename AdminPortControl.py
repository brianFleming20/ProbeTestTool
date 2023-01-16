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
import Datastore
import AdminUser
import OnScreenKeys
import Ports

KY = OnScreenKeys.Keyboard()
DS = Datastore.Data_Store()
AU = AdminUser


def ignore():
    return 'break'


class AdminPorts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#FFDAB9')
        self.analyser_usb = "COM4"
        self.com_port = "COM3"
        self.monitor = "COM5"
        self.move_probe = "Not Set"
        self.control = controller
        connection_data = Ports.Ports(odm=self.monitor,probe=self.com_port,analyer=self.analyser_usb,move=self.move_probe)
        DS.write_device_to_file(connection_data)
        ttk.Label(self, text="Deltex", background="#FFDAB9", foreground="#003865",
                  font=('Helvetica', 28, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#FFDAB9", foreground="#A2B5BB",
                  font=('Helvetica', 18)).place(relx=0.85, rely=0.15)
        self.connectBtn = Button(
            self, text="Continue", command=self.forward, font=('Courier', 16))
        self.connectBtn.place(height=35, width=150, relx=0.85, rely=0.82, anchor=CENTER)
        self.cancelBtn = Button(
            self, text="Cancel", command=self.cancel, font=('Courier', 14))
        self.cancelBtn.place(relx=0.7, rely=0.82, anchor=CENTER)
        self.text_area = tk.Text(self, font=("Courier",14),height=5, width=38)
        self.text_area.place(x=40, y=70)

    def cancel(self):
        self.destroy_canvas()
        self.control.show_frame(AU.AdminWindow)

    def forward(self):
        self.destroy_canvas()
        self._connect_btn_clicked(self.control)

    def refresh_window(self):
        self.canvas_1 = Canvas(bg="#eae9e9", width=500, height=45)
        self.canvas_1.place(relx=0.35, rely=0.3)
        self.canvas_2 = Canvas(bg="#eae9e9", width=500, height=45)
        self.canvas_2.place(relx=0.35, rely=0.4)
        self.canvas_3 = Canvas(bg="#eae9e9", width=500, height=45)
        self.canvas_3.place(relx=0.35, rely=0.5)
        self.canvas_4 = Canvas(bg="#eae9e9", width=500, height=45)
        self.canvas_4.place(relx=0.35, rely=0.6)
        self.btn_1 = Button(self.canvas_1, text="ODM monitor port", command=self.monitor_entry, font=('Courier', 12))
        Label(self.canvas_1, text="-->").place(x=240, y=12)
        self.btn_2 = Button(self.canvas_2, text="Probe Interface Port", command=self.probe_entry, font=('Courier', 12))
        Label(self.canvas_2, text="-->").place(x=240, y=12)
        self.btn_3 = Button(self.canvas_3, text="Analyser port", command=self.znd_entry, font=('Courier', 12))
        Label(self.canvas_3, text="-->").place(x=240, y=12)
        self.btn_4 = Button(self.canvas_4, text="Probe Movement Port", command=self.move_entry, font=('Courier', 12))
        Label(self.canvas_4, text="-->").place(x=240, y=12)
        self.btn_1.place(x=15, y=15)
        self.btn_2.place(x=15, y=15)
        self.btn_3.place(x=15, y=15)
        self.btn_4.place(x=15, y=15)
        self.znd_text = self.canvas_1.create_text(330, 20, text=" ", fill="black",
                                                  font=(OnScreenKeys.FONT_NAME, 14, "bold"))
        self.probe_text = self.canvas_2.create_text(330, 20, text=" ", fill="black",
                                                    font=(OnScreenKeys.FONT_NAME, 14, "bold"))
        self.monitor_text = self.canvas_3.create_text(330, 20, text=" ", fill="black",
                                                      font=(OnScreenKeys.FONT_NAME, 14, "bold"))
        self.move_text = self.canvas_4.create_text(330, 20, text=" ", fill="black",
                                                   font=(OnScreenKeys.FONT_NAME, 14, "bold"))

        self.text_area.config(state=NORMAL)
        self.text_area.insert('2.0', DS.get_username())
        self.text_area.insert('2.0', '\n\nPlease check any external devices\nand press continue...')
        self.text_area.config(state=DISABLED)

    def _connect_btn_clicked(self, controller):
        connection_data = Ports.Ports(odm=self.monitor,probe=self.com_port,analyer=self.analyser_usb,move=self.move_probe)
        DS.write_device_to_file(connection_data)
        controller.show_frame(AU.AdminWindow)

    def destroy_canvas(self):
        self.canvas_1.destroy()
        self.canvas_2.destroy()
        self.canvas_3.destroy()
        self.canvas_4.destroy()

    def get_keys(self):
        KY.display()
        self.btn_1.config(state=DISABLED)
        self.btn_2.config(state=DISABLED)
        self.btn_3.config(state=DISABLED)
        self.btn_4.config(state=DISABLED)

    def set_buttons_norm(self):
        self.btn_1.config(state=NORMAL)
        self.btn_2.config(state=NORMAL)
        self.btn_3.config(state=NORMAL)
        self.btn_4.config(state=NORMAL)

    def znd_entry(self):
        self.get_keys()
        self.current_user = ""
        data = self.wait_for_response(self.canvas_1, self.znd_text)
        self.analyser_usb = data
        self.set_buttons_norm()

    def probe_entry(self):
        self.get_keys()
        self.current_user = ""
        data = self.wait_for_response(self.canvas_2, self.probe_text)
        self.com_port = data
        self.set_buttons_norm()

    def monitor_entry(self):
        self.get_keys()
        self.current_user = ""
        data = self.wait_for_response(self.canvas_3, self.monitor_text)
        self.monitor = data
        self.set_buttons_norm()

    def move_entry(self):
        self.get_keys()
        self.current_user = ""
        data = self.wait_for_response(self.canvas_4, self.move_text)
        self.move_probe = data
        self.set_buttons_norm()

    def wait_for_response(self, master, label):
        DS.write_to_from_keys("_")
        data = DS.get_keyboard_data()
        while 1:
            data = DS.get_keyboard_data()
            if len(data) > 0 and data[-1] == "+":
                data = data[:-1]
                break
            master.itemconfig(label, text=data)
            Tk.update(master)
        return data