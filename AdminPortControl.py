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
from time import gmtime, strftime
import datastore
import AdminUser as AU
import OnScreenKeys



KY = OnScreenKeys.Keyboard()
DS = datastore.DataStore()

def ignore():
    return 'break'


class AdminPorts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#FFDAB9')
        
        
        self.analyser_usb = "COM4"
        self.com_port = "COM3"
        self.monitor = "COM5"
        self.move_probe = "Not Set"
        ports_data = []
        connection_data = []
        connection_data.append(self.com_port)
        connection_data.append(self.analyser_usb)
        connection_data.append(self.monitor)
        connection_data.append(self.move_probe)
        ports_data.extend(connection_data)
     
        DS.write_to_port_file(ports_data)
        
        tk.Frame.__init__(self, parent, bg='#E0FFFF')   
        
        self.deltex = (PhotoImage(file="deltex.gif"))
        self.label_8 = ttk.Label(self, text=" ", image=self.deltex)
        self.label_8.place(relx=0.9, rely=0.15, anchor=CENTER)
        
        self.connectBtn = ttk.Button(
            self, text="Continue", command=lambda: 
                [self.destroy_canvas(),self._connect_btn_clicked(controller)])
        self.connectBtn.place(height=35,width=150, x=850, y=530 ,anchor=CENTER)
        self.bind('<Return>', self._connect_btn_clicked)

        self.cancelBtn = ttk.Button(
            self, text="Cancel",  command=lambda: 
                [self.destroy_canvas(),controller.show_frame(AU.AdminWindow)])
        self.cancelBtn.place(relx=0.7, rely=0.82, anchor=CENTER)
        
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(relx=0.20, rely=0.15, anchor=CENTER)

        
    def refresh_window(self):
            self.canvas_1 = Canvas(bg="#eae9e9",width=250, height=40)
            self.canvas_1.place(x=375, y=120)
            self.canvas_2 = Canvas(bg="#eae9e9",width=250, height=40)
            self.canvas_2.place(x=375, y=195)
            self.canvas_3 = Canvas(bg="#eae9e9",width=250, height=40)
            self.canvas_3.place(x=375, y=270)
            self.canvas_4 = Canvas(bg="#eae9e9",width=250, height=40)
            self.canvas_4.place(x=375, y=345)
            self.btn_1 = ttk.Button(self.canvas_1, text="ODM monitor port", command=lambda:
                [self.get_keys(), self.monitor_entry()])
            self.btn_2 = ttk.Button(self.canvas_2, text="Probe Interface Port", command=lambda:
                [self.get_keys(), self.probe_entry()])
            self.btn_3 = ttk.Button(self.canvas_3, text="Analyser port", command=lambda:
                [self.get_keys(), self.znd_entry()])
            self.btn_4 = ttk.Button(self.canvas_4, text="Probe Movement Interface", command=lambda:
                [self.get_keys(), self.move_entry()])
            self.btn_1.place(relx=0.25, rely=0.3, anchor=N)
            self.btn_2.place(relx=0.25, rely=0.3, anchor=N)
            self.btn_3.place(relx=0.20, rely=0.3, anchor=N)
            self.btn_4.place(relx=0.32, rely=0.3, anchor=N)
            self.znd_text = self.canvas_1.create_text(180,20,text=" ",fill="black",font=(OnScreenKeys.FONT_NAME, 16, "bold"))
            self.probe_text = self.canvas_2.create_text(180,20,text=" ",fill="black",font=(OnScreenKeys.FONT_NAME, 14, "bold"))
            self.monitor_text = self.canvas_3.create_text(180,20,text=" ",fill="black",font=(OnScreenKeys.FONT_NAME, 14, "bold"))
            self.move_text = self.canvas_4.create_text(180,20,text=" ",fill="black",font=(OnScreenKeys.FONT_NAME, 14, "bold"))
            user_data = []
            user_data.append(DS.get_user())
        
            self.text_area.config(state=NORMAL)   
            self.text_area.insert('2.0',user_data[0])
            self.text_area.insert('2.0','\n\nPlease check any external devices\nand press continue...')
            self.text_area.config(state=DISABLED)
            



    def _connect_btn_clicked(self, controller):
        ports_data = []
        connection_data = []
        connection_data.append(self.com_port)
        connection_data.append(self.analyser_usb)
        connection_data.append(self.monitor)
        connection_data.append(self.move_probe)
        ports_data.extend(connection_data)
        DS.write_to_port_file(ports_data)
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
        self.current_user = ""
        data = self.wait_for_response(self.canvas_1, self.znd_text)
        self.newusername = data
        self.set_buttons_norm()
        
        
        
    def probe_entry(self):
        self.current_user = ""
        data = self.wait_for_response(self.canvas_1, self.probe_text)
        self.newusername = data
        self.set_buttons_norm()
        
        
        
    def monitor_entry(self):
        self.current_user = ""
        data = self.wait_for_response(self.canvas_1, self.monitor_text)
        self.newusername = data
        self.set_buttons_norm()
        
        
        
    def move_entry(self):
        self.current_user = ""
        data = self.wait_for_response(self.canvas_1, self.move_text)
        self.newusername = data
        self.set_buttons_norm()
        
             
        
    def wait_for_response(self, master, label):
        DS.write_to_from_keys(" ")
        data = DS.get_keyboard_data()
        while 1:
            data = DS.get_keyboard_data()
            if data[-1] == "+":
                data = data[:-1]
                break 
       
            master.itemconfig(label, text=data)
                # ttk.Label(master, text=pw_data, font=("bold", 15)).place(relx=0.7, rely=0.3, width=150,anchor=N)
            Tk.update(master)
        return data
            