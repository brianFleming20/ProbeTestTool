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
from tkinter.ttk import *
import tkinter.messagebox as tm
import BatchManager
from BatchManager import Batch
import SecurityManager
import UserLogin
import Connection
import AdminUser
import Datastore
import OnScreenKeys
import codecs
import ProbeManager
from time import gmtime, strftime, sleep
import Ports
import ProbeTest
import ProbeInterface
import os

BM = BatchManager.BatchManager()
SM = SecurityManager.SecurityManager()
DS = Datastore.Data_Store()
KY = OnScreenKeys.Keyboard()
P = Ports
UL = UserLogin
CO = Connection
AU = AdminUser
PT = ProbeTest
PI = ProbeInterface.PRI()
PM = ProbeManager.ProbeManager()


def ignore():
    return 'break'


BTN_WIDTH = 22
BTN_HEIGHT = 20


class SessionSelectWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__()
        ##################################
        # create a choose session window #
        ##################################
        tk.Frame.__init__(self, parent, bg="#B1D0E0")
        self.probe_date = False
        self.probe_type = False
        self.complete_canvas = None
        self.control = controller
        self.info_canvas = None
        self.batch_from_file = None
        self.canvas_text = None
        self.test = False


    def refresh_window(self):
        ####################################################
        # Refresh window on navigation from another window #
        ####################################################
        # Check user status for admin of logged in user #
        ################################
        # Window title                 #
        ################################
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        self.cent_x = ws / 2
        self.cent_y = hs / 2
        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 28, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 18)).place(relx=0.85, rely=0.15)
        self.text_area = tk.Text(self, font=("Courier", 14), height=5, width=38)
        self.text_area.place(x=40, y=70)
        time_now = strftime("%H:%M:%p", gmtime())
        self.NSWL1 = ttk.Label(self, text='Session Selection Window. ', justify=RIGHT,
                               font=("Courier", 24, "bold"), background="#B1D0E0")
        self.NSWL1.place(relx=0.5, rely=0.05, anchor=CENTER)
        ports = P.Ports()
        DS.write_device_to_file(ports)
        ################################
        # Start a new batch session    #
        ################################
        btn1 = tk.Button(self, text='Start a new session', background="#5FD068", command=lambda: self.control.show_frame(NewSessionWindow))
        btn1.place(height=50, width=250, relx=0.2, rely=0.35)
        ################################
        # Continue a suspended batch   #
        ################################
        self.SSW_b2 = tk.Button(self, text='Continue a previous session', background="#FFCB42",
                             command=lambda: self.control.show_frame(ContinueSessionWindow), width=BTN_WIDTH)

        self.SSW_b2.place(height=50, width=250, relx=0.5, rely=0.35)
        ################################
        # Retest failed probe          #
        ################################
        self.failed = tk.Button(self, text='Re-test Failed Probe.', background="#FFCB42", command=self.failed_probe)
        self.failed.place(height=30, width=200, relx=0.52, rely=0.45)

        ################################
        # Display completed batches    #
        ################################
        btn2 = tk.Button(self, text='Completed Batches', background="#40DFEF", command=self.completed_btn_clicked)
        btn2.place(height=50, width=250, relx=0.2, rely=0.65)
        ################################
        # Access admin window          #
        ################################
        self.SSW_b4 = tk.Button(self, text='Admin area', background="#FFDAB9",
                             command=lambda: self.control.show_frame(AU.AdminWindow), width=BTN_WIDTH)
        self.SSW_b4.place(height=50, width=250, relx=0.5, rely=0.65)
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        if "AM" in time_now:
            self.text_area.insert('1.0', 'Good Morning ')
        else:
            self.text_area.insert('1.0', 'Good Afternoon ')
        self.text_area.config(state=DISABLED)
        self.SSW_b3 = tk.Button(self, text='Log Out', background="#F37878", command=self.logout, width=BTN_WIDTH)
        self.SSW_b3.place(height=40, width=180, relx=0.85, rely=0.8, anchor=E)
        user_info = DS.user_admin_status()

        if not user_info:
            self.SSW_b4.config(state=DISABLED)
        else:
            self.SSW_b4.config(state=NORMAL)
        if not BM.GetAvailableBatches():
            self.SSW_b2.config(state=DISABLED)
        else:
            self.SSW_b2.config(state=NORMAL)
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        self.text_area.insert('2.0', DS.get_username())
        self.text_area.insert('3.3', '\n\nPlease choose an option.')
        self.text_area.config(state=DISABLED)

    def completed_btn_clicked(self):
        self.complete_canvas = Canvas(bg="#eae9e9", width=200, height=300)
        self.complete_canvas.place(relx=0.73, rely=0.25)
        self.complete_canvas.create_text(100, 20, text="Probes Completed", fill="black",
                                         font=(OnScreenKeys.FONT_NAME, 12, "bold"))
        ttk.Button(self.complete_canvas, text="Close",
                   command=self.complete_canvas.destroy).place(x=120, y=270)
        item = 0
        for probes in BM.get_completed_batches():
            position = (item * 20) + 50
            item += 1
            self.complete_canvas.create_text(80, position, text=f"{probes}", fill="black",
                                             font=(OnScreenKeys.FONT_NAME, 10))

    def logout(self):
        SM.logOut()
        self.control.show_frame(UL.LogInWindow)

    def failed_probe(self):
        probe_port = CO.sort_probe_interface(self)
        port = P.Ports(probe=probe_port)
        DS.write_device_to_file(port)
        PT.probe_canvas(self, " Insert a failed probe. \n or press Cancel", True)
        self.info_canvas = None

    def remove_probe(self):
        self.info_canvas = False
        PT.probe_canvas(self, "Please remove probe", False)
        while PI.probe_present():
            pass
        PT.text_destroy(self)

    def yes_answer(self):
        while not PI.probe_present():
            pass
        PT.text_destroy(self)

        binary_str = codecs.decode(PI.read_serial_number(), "hex")
        serial_number = str(binary_str)[2:18]
        probe_type = serial_number[:4]
        self.probe_date = serial_number[8:]
        filepath = DS.get_file_location()
        path = filepath['File']
        inProgressPath = os.path.join(path, "in_progress", "")
        completePath = os.path.join(path, "complete", "")
        print("start")
        if self.probe_date:
            PT.probe_canvas(self, "Checking in-progress folder", False)
            self.check_folder(inProgressPath,self.probe_date, probe_type)
            PT.text_destroy(self)
        elif self.probe_date:
            PT.probe_canvas(self, "Checking Complete folder", False)
            self.check_folder(completePath,self.probe_date, probe_type)
            PT.text_destroy(self)
        else:
            self.passed_probe()

    def check_folder(self, folder, probe_date, probe_data):
        for file_loc in os.listdir(folder):
            lines = BM.CSVM.ReadAllLines(file_loc[:-4])
            for batch in lines:
                self.batch_from_file = file_loc[:-4]
                SN = batch[0][1:-1]
                if len(SN) > 5:
                    if 'Fail' in SN:
                        print("found")
                        self.probe_type = self.get_probe_type(probe_data[:-1])
                        print(f"{probe_date} - {SN[8:]}")
                        if SN[8:] == probe_date:
                            self.test = True
                    # else:
                    #     PT.text_destroy(self)
        if self.test:
            print("Testing found probe")
            retest = tm.askyesno(title="Inserted probe",
                                 message=f"({self.batch_from_file})\n Is this Batch number correct")

            if retest:
                PT.probe_canvas(self, f" ({self.batch_from_file}) \nRe-testing - {self.probe_type} - probe", False)
                results, marker_data, odm_data = PT.TestProgramWindow.test_probe(self)

                PT.text_destroy(self)
                sleep(2)
                PT.probe_canvas(self, f" ({self.batch_from_file}) \n{self.probe_type} - probe passed", False)
                if results:
                    SN_seperated = []
                    limit = 16
                    start = 0
                    dec_start = '53A00900'
                    end = '50'
                    pcb_serial_number = PM.read_serial_number()
                    binary_str = codecs.decode(pcb_serial_number, "hex")
                    print(f"serial number = {str(binary_str)[2:18]}")
                    SN_bytes = PI.read_all_bytes()
                    while limit <= len(SN_bytes):
                        makeup = dec_start + SN_bytes[start:limit] + end
                        SN_seperated.append(makeup)
                        limit += 16
                        start += 16
                    probe_type = SN_seperated[0][8:16]
                    probe_sn = SN_seperated[1][8:-2]
                    new_probe_sn = probe_type + '3232' + probe_sn + '3031'
                    new_probe_bin = codecs.decode(new_probe_sn, 'hex')
                    new_probe = new_probe_bin.decode('utf-8')
                    PM.construct_new_serial_number(new_probe, True)
                sleep(3)
                PT.text_destroy(self)
                self.remove_probe()
        else:
            return False

    def no_answer(self):
        self.info_canvas = False
        PT.text_destroy(self)

    def passed_probe(self):
        self.info_canvas = False
        PT.probe_canvas(self, "Please remove the probe.\n\nInsert a failed probe.", False)
        while PI.probe_present():
            pass
        PT.text_destroy(self)

    def get_probe_type(self,probe_data):
        probe_type = "---"
        if probe_data == "2F0":
            probe_type = "DP240"
        elif probe_data == "20C":
            probe_type = "DP12"
        elif probe_data == "206":
            probe_type = "DP6"
        elif probe_data == "648":
            probe_type = "I2C"
        elif probe_data == "618":
            probe_type = "I2P"
        elif probe_data == "606":
            probe_type = "I2S"
        elif probe_data == "548":
            probe_type = "KDP72"

        return probe_type


class NewSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.btn_2 = None
        self.btn_1 = None
        self.text_area = None
        self.canvas_qty = None
        self.canvas_type = None
        self.canvas_back = None
        self.batchNumber = None
        self.probe_type = StringVar()
        self.batchQty = 100
        self.control = controller

    def refresh_window(self):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        self.canvas_back = Canvas(bg='#B1D0E0', width=ws - 10, height=hs - 10)
        self.canvas_back.place(x=5, y=5)
        self.canvas_type = Canvas(width=400, height=50)
        self.canvas_type.place(relx=0.5, rely=0.4)
        self.canvas_qty = Canvas(width=400, height=50)
        self.canvas_qty.place(relx=0.5, rely=0.55)
        probe_type_frame = tk.Frame(self.canvas_back, pady=3, padx=50, bg='#E0FFFF')

        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 28, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 18)).place(relx=0.85, rely=0.15)
        self.batchQty = 100
        self.batchNumber = None
        self.probe_type.set("")
        self.text_area = tk.Text(self.canvas_back, font=("Courier", 14), height=5, width=38)
        self.text_area.place(x=40, y=70)

        probe_type_frame.place(relx=0.20, rely=0.5, anchor=CENTER)

        ttk.Label(self.canvas_back, text='Probe selection window. ',
                  justify=RIGHT, font=("Courier", 20, "bold"), background="#B1D0E0").place(relx=0.5, rely=0.05,
                                                                                           anchor=CENTER)

        ttk.Label(self.canvas_back, text='Select Probe Type: ',
                  justify=RIGHT, font=("Courier", 18, "bold"), background="#B1D0E0").place(relx=0.12, rely=0.3)

        self.probe_type = StringVar(probe_type_frame, "DP240")
        # Dictionary to create multiple buttons
        values = {"DP240 [9070-7005]": 'DP240',
                  "DP12 [9070-7003]  ": 'DP12 ',
                  "DP6 [9070-7001]    ": 'DP6  ',
                  "I2C [9090-7014]     ": 'I2C  ',
                  "I2P [9090-7013]     ": 'I2P  ',
                  "I2S [9090-7012]      ": 'I2S  ',
                  "KDP72 [9081-7001]": 'KDP  '}

        for (text, value) in values.items():
            style = Style(probe_type_frame)
            style.configure("TRadiobutton", font=("arial", 14, "bold"))
            rbn = Radiobutton(probe_type_frame, text=text, variable=self.probe_type,
                              value=value)
            rbn.pack(side=TOP, ipady=5)

        tk.Button(self.canvas_back, text='Continue', font=("Courier", 14), width=20, height=2,
                  command=self.to_devices).place(relx=0.82, rely=0.8, anchor=CENTER)

        tk.Button(self.canvas_back, text='Cancel', font=("Courier", 11),
                  command=self.back).place(relx=0.56, rely=0.8, anchor=CENTER)

        self.bind('<Return>', self.confm_btn_clicked)
        self.type_text = self.canvas_type.create_text(250, 20, text=" ", fill="black",
                                                      font=(OnScreenKeys.FONT_NAME, 8, "bold"))
        self.qty_text = self.canvas_qty.create_text(220, 20, text=" ", fill="black",
                                                    font=(OnScreenKeys.FONT_NAME, 8, "bold"))

        self.btn_1 = ttk.Button(self.canvas_type, text='Batch number: ',
                                command=lambda: [self.get_keys(), self.batch_entry()])
        self.btn_1.place(relx=0.21, rely=0.3, anchor=N)
        Label(self.canvas_type, text="-->").place(x=180, y=18)
        self.btn_2 = ttk.Button(self.canvas_qty, text='Batch Qty: ',
                                command=lambda: [self.get_keys(), self.qty_entry()])
        self.btn_2.place(relx=0.18, rely=0.3, anchor=N)
        Label(self.canvas_qty, text="-->").place(x=180, y=18)
        ttk.Label(self.canvas_qty, text=self.batchQty, font=("bold", 14)).place(relx=0.75, rely=0.3, width=140,
                                                                                anchor=N)
        self.text_area.config(state=NORMAL)
        self.text_area.insert('1.0', DS.get_username())
        self.text_area.insert('3.3', '\n\nPlease enter the batch number\nselect the probe type\nand batch quantity.')
        self.text_area.config(state=DISABLED)

    def get_keys(self):
        KY.get_keyboard()
        self.btn_1.config(state=DISABLED)
        self.btn_2.config(state=DISABLED)

    def batch_entry(self):
        data = self.wait_for_response(self.canvas_type, self.type_text)
        self.batchNumber = data
        self.btn_1.config(state=NORMAL)
        self.btn_2.config(state=NORMAL)

    def qty_entry(self):
        data = 0
        data = self.wait_for_response(self.canvas_qty, self.qty_text)
        self.batchQty = int(data)
        self.btn_1.config(state=NORMAL)
        self.btn_2.config(state=NORMAL)

    def wait_for_response(self, master, label):
        DS.write_to_from_keys("_")

        while 1:
            data = DS.get_keyboard_data()

            if len(data) > 0 and data[-1] == "+":
                data = data[:-1]
                break
            master.itemconfig(label, text=data, font=("bold", 14))
            Tk.update(master)
        return data

    def confm_btn_clicked(self):
        # create new batch
        batch = self.batchNumber
        qty = self.batchQty
        name = DS.get_username()
        batch_type = self.probe_type.get()
        check_qty = self.check_batch_qty(qty)
        check_batch = self.convert_batch_number(batch)
        if not check_qty and not check_batch:
            self.refresh_window()
        if not self.create_new_batch(check_batch, batch_type, qty, name):
            self.canvas_back.destroy()
            self.refresh_window()
        else:
            self.canvas_back.destroy()
            self.control.show_frame(CO.Connection)

    def check_batch_qty(self, qty):
        check = True
        if qty > 100:
            tm.showerror('Batch Error', "Enter a correct batch quantity\nYou can't have more than 100.")
            check = False
        if qty < 100:
            tm.showerror('Batch Error', "Enter a correct batch quantity\nYou can't have less than one.")
            check = False

        return check

    def create_new_batch(self, batch, batch_type, qty, name):
        newBatch = Batch(batch)
        newBatch.probe_type = batch_type
        newBatch.batchQty = qty
        check = True
        DAnswer = tm.askyesno(title='Confirm',
                              message=f'Are batch details correct?\n\n Batch number {batch} \n Batch Qty{self.batchQty}')
        if DAnswer:
            # create the batch file
            if not BM.CreateBatch(newBatch, name):
                tm.showerror('Error', 'Batch number not unique')
                check = False
            return check
        else:
            return False

    def convert_batch_number(self, batch):
        if self.check_batch_number(batch):
            batch_numbers = batch[:-1]
            batch_letter = batch[-1].upper()
            confirm_batch = batch_numbers + batch_letter
            return confirm_batch
        else:
            return False

    def check_batch_number(self, batch):
        check = False
        if len(batch) == 0:
            tm.showerror("error","Enter a batch number")
        check = [True for element in batch if element.isalpha()]
        if not check:
            tm.showerror("Error","Batch number in-complete")
        return check

    def back(self):
        self.canvas_type.destroy()
        self.canvas_qty.destroy()
        self.canvas_back.destroy()
        self.control.show_frame(SessionSelectWindow)

    def to_devices(self):
        self.canvas_type.destroy()
        self.canvas_qty.destroy()
        self.confm_btn_clicked()


class ContinueSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#B1D0E0')
        self.control = controller
        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 28, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 18)).place(relx=0.85, rely=0.15)

        self.text_area = tk.Text(self, font=("Courier", 14), height=5, width=38)
        self.text_area.place(x=40, y=70)

        ttk.Label(self, text='Choose a session to resume', font=("Courier", 18), background="#B1D0E0").place(relx=0.5,
                                                                                                             rely=0.05,
                                                                                                             anchor=CENTER)

        ttk.Label(self, text="Batch number", font=("Courier", 16), background="#B1D0E0").place(relx=0.28, rely=0.32)
        ttk.Label(self, text="Batch type", font=("Courier", 16), background="#B1D0E0").place(relx=0.58, rely=0.32)

        self.sessionListBox = Listbox(self)
        self.sessionListBox.place(relx=0.38, rely=0.45, anchor=CENTER)
        self.sessionListBox.config(height=4, width=20, font=("Courier", 18))

        self.probe_typeListBox = Listbox(self, font=("Courier", 12))
        self.probe_typeListBox.place(relx=0.65, rely=0.45, anchor=CENTER)
        self.probe_typeListBox.config(height=4, width=15, font=("Courier", 16))

        self.continue_btn = tk.Button(
            self, text='Continue Session', height=2, font=("Courier",14), command=self.continue_btn_clicked)
        self.continue_btn.place( relx=0.88, rely=0.82, anchor=E)

        self.cancel_btn = ttk.Button(
            self, text='Cancel', command=lambda: self.control.show_frame(SessionSelectWindow))
        self.cancel_btn.place(height=35, width=90, relx=0.62, rely=0.82, anchor=E)

    def refresh_window(self):
        # #create a list of the current users using the dictionary of users
        self.sessionList = []
        self.probe_typeList = []

        self.set_display()

        for item in self.get_available_batches():
            self.sessionList.append(item)
            self.get_batch_obj(item)
            self.probe_typeList.append(self.obj.probe_type)
            self.batch = None

        # clear the listbox
        self.sessionListBox.delete(0, END)
        self.probe_typeListBox.delete(0, END)

        # fill the listbox with the list of users
        for item in self.sessionList:
            self.sessionListBox.insert(END, item)

        for item in self.probe_typeList:
            self.probe_typeListBox.insert(END, item)
        self.probe_typeListBox.config(state=DISABLED)

    def continue_btn_clicked(self):
        lstid = self.sessionListBox.curselection()
        if len(lstid) != 0:
            lstBatch = self.sessionListBox.get(lstid[0])
            batch = BM.GetBatchObject(lstBatch)
            probe_data = P.Probes(batch.probe_type, batch.batchNumber, 0, batch.batchQty)
            DS.write_probe_data(probe_data)

            self.control.show_frame(CO.Connection)

    def set_display(self):
        self.text_area.config(state=NORMAL)
        self.text_area.insert('1.0', DS.get_username())
        self.text_area.insert('3.3', '\n\nPlease select a batch number\nto continue testing.')
        self.text_area.config(state=DISABLED)

    def get_available_batches(self):
        self.batches = BM.GetAvailableBatches()
        return self.batches

    def set_available_batches(self, batches):
        self.batches = batches

    def get_session_list_box(self):
        return self.sessionListBox

    def get_probe_type_list(self):
        return self.probe_typeList

    def get_batch_obj(self, item):
        self.obj = BM.GetBatchObject(item)

        self.set_batch_obj(self.obj.batchNumber)
        self.batch_obj.probe_type = self.obj.probe_type
        # self.batch_obj.probe_type = "DP12"

    def set_batch_obj(self, batch):
        self.batch_obj = Batch(batch)
