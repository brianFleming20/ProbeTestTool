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
from ProbeManager import Probes as P
import SecurityManager
import UserLogin as UL
import Connection as CO
import AdminUser as AU
import Datastore
import OnScreenKeys
from time import gmtime, strftime

BM = BatchManager.BatchManager()
SM = SecurityManager.SecurityManager()
DS = Datastore.Data_Store()
KY = OnScreenKeys.Keyboard()


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
        tk.Frame.__init__(self, parent, bg='#B1D0E0')
        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 24, 'bold'), width=12).place(x=850, y=25)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 14)).place(x=850, y=57)
        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(x=40, y=70)
        time_now = strftime("%H:%M:%p", gmtime())
        ################################
        # Window title                 #
        ################################
        self.NSWL1 = ttk.Label(self, text='Session Sellection Window. ', justify=RIGHT, font=("Courier", 20, "bold"))
        self.NSWL1.place(relx=0.5, rely=0.05, anchor=CENTER)
        ################################
        # Start a new batch session    #
        ################################
        ttk.Button(self, text='Start a new session', command=lambda:
        controller.show_frame(NewSessionWindow),
                   width=BTN_WIDTH).place(height=35, width=180, x=200, y=180)
        ################################
        # Continue a suspended batch   #
        ################################
        self.SSW_b2 = ttk.Button(self, text='Continue a previous session',
                                 command=lambda: controller.show_frame(ContinueSessionWindow), width=BTN_WIDTH)
        self.SSW_b2.place(height=35, width=180, x=500, y=180)
        ################################
        # Display completed batches    #
        ################################
        ttk.Button(self, text='Completed Batches', command=lambda:
        self.completed_btn_clicked(),
                   width=BTN_WIDTH).place(height=35, width=180, x=200, y=350)
        ################################
        # Access admin window          #
        ################################
        self.SSW_b4 = ttk.Button(self, text='Admin area', command=lambda:
        controller.show_frame(AU.AdminWindow), width=BTN_WIDTH)
        self.SSW_b4.place(height=35, width=180, x=500, y=350)
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        if "AM" in time_now:
            self.text_area.insert('1.0', 'Good Morning ')
        else:
            self.text_area.insert('1.0', 'Good Afternoon ')
        self.text_area.config(state=DISABLED)
        self.SSW_b3 = ttk.Button(self, text='Log Out', command=lambda:
        [SM.logOut(), controller.show_frame(UL.LogInWindow)], width=BTN_WIDTH)
        self.SSW_b3.place(height=35, width=180, x=850, y=530, anchor=E)

    def refresh_window(self):
        ####################################################
        # Refresh window on navigation from another window #
        ####################################################
        # Check user status for admin of logged in user #

        user_info = DS.user_admin_status()

        if user_info == False:
            self.SSW_b4.config(state=DISABLED)
        else:
            self.SSW_b4.config(state=NORMAL)
        if len(BM.GetAvailableBatches()) == 0:
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
        self.complete_canvas.place(x=730, y=180)
        self.complete_canvas.create_text(100, 20, text="Probes Completed", fill="black",
                                         font=(OnScreenKeys.FONT_NAME, 12, "bold"))
        ttk.Button(self.complete_canvas, text="Close", command=lambda:
        self.complete_canvas.destroy()).place(relx=0.80, rely=0.9, anchor=N)
        item = 0
        for probes in BM.get_completed_batches():
            position = (item * 20) + 50
            item += 1
            self.complete_canvas.create_text(80, position, text=f"{probes}", fill="black",
                                             font=(OnScreenKeys.FONT_NAME, 10))


class NewSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.batchNumber = None
        self.probe_type = StringVar()
        self.batchQty = 0
        self.control = controller


    def refresh_window(self):
        self.canvas_back = Canvas(bg='#B1D0E0',width=980,height=600)
        self.canvas_back.place(x=10,y=10)
        self.canvas_type = Canvas(width=300, height=45)
        self.canvas_type.place(x=400, y=250)
        self.canvas_qty = Canvas(width=300, height=45)
        self.canvas_qty.place(x=400, y=350)
        probe_type_frame = tk.Frame(self.canvas_back, pady=3, padx=50, bg='#E0FFFF')

        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 24, 'bold'), width=12).place(x=850, y=25)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 14)).place(x=850, y=57)

        self.text_area = tk.Text(self.canvas_back, height=5, width=38)
        self.text_area.place(x=40, y=70)

        probe_type_frame.place(relx=0.25, rely=0.55, anchor=CENTER)

        self.NSWL1 = ttk.Label(self.canvas_back, text='Probe selection window. ', justify=RIGHT, font=("Courier", 20, "bold"))
        self.NSWL1.place(relx=0.5, rely=0.05, anchor=CENTER)

        ttk.Label(self.canvas_back, text='Select Probe Type: ').place(x=180, y=190)

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
            Radiobutton(probe_type_frame, text=text, variable=self.probe_type,
                        value=value).pack(side=TOP, ipady=5)

        self.confm_btn = tk.Button(self.canvas_back, text='Confirm', padx=2, pady=3,
                                   width=BTN_WIDTH, command=lambda:
            [self.canvas_type.destroy(), self.canvas_qty.destroy(), self.confm_btn_clicked()])
        self.confm_btn.place(relx=0.85, rely=0.88, anchor=CENTER)

        self.cancl_btn = tk.Button(self.canvas_back, text='Cancel', padx=2, pady=3, width=BTN_WIDTH,
                                   command=lambda:
                                   [self.canvas_type.destroy(), self.canvas_qty.destroy(),self.canvas_back.destroy(),
                                    self.control.show_frame(SessionSelectWindow)])
        self.cancl_btn.place(relx=0.65, rely=0.88, anchor=CENTER)

        self.bind('<Return>', self.confm_btn_clicked)
        self.type_text = self.canvas_type.create_text(200, 20, text=" ", fill="black",
                                                      font=(OnScreenKeys.FONT_NAME, 16, "bold"))
        self.qty_text = self.canvas_qty.create_text(200, 20, text=" ", fill="black",
                                                    font=(OnScreenKeys.FONT_NAME, 14, "bold"))

        self.btn_1 = ttk.Button(self.canvas_type, text='Batch number: ',
                                command=lambda: [self.get_keys(), self.batch_entry()])
        self.btn_1.place(relx=0.21, rely=0.3, anchor=N)
        Label(self.canvas_type, text="-->").place(x=170, y=12)
        self.btn_2 = ttk.Button(self.canvas_qty, text='Batch Qty: ',
                                command=lambda: [self.get_keys(), self.qty_entry()])
        self.btn_2.place(relx=0.18, rely=0.3, anchor=N)
        Label(self.canvas_qty, text="-->").place(x=170, y=12)
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
            master.itemconfig(label, text=data)
            ttk.Label(master, text=data, font=("bold", 15)).place(relx=0.75, rely=0.3, width=100,anchor=N)
            Tk.update(master)
        return data

    def check_batch_qty(self, qty):
        check = True
        if qty > 100:
            tm.showerror('Batch Error', "Enter a correct batch quantity\nYou can't have more than 100.")
            check = False
        if qty < 1:
            tm.showerror('Batch Error', "Enter a correct batch quantity\nYou can't have less than one.")
            check = False
        return check

    def check_batch_number(self, number):
        check = True
        if len(number) == 0:
            tm.showerror('Error', 'Enter a batch number')
            check = False
        return check

    def create_new_batch(self, batch, batch_type, qty, name):
        check = False
        DAnswer = False
        confirm_batch = self.convert_batch_number(batch)
        newBatch = Batch(confirm_batch)
        newBatch.probe_type = batch_type
        newBatch.batchQty = qty
        check = True
        DAnswer = tm.askyesno('Confirm', 'Are batch details correct?')
        if DAnswer == True:
            # create the batch file
            if BM.CreateBatch(newBatch, name, qty) == False:
                tm.showerror('Error', 'Batch number not unique')
                check = False
                newBatch = None
        return check

    def convert_batch_number(self, batch):
        batch_numbers = batch[:-1]
        batch_letter = batch[-1].upper()
        confirm_batch = batch_numbers + batch_letter
        return confirm_batch

    def confm_btn_clicked(self):
        # create new batch
        batch = self.batchNumber
        qty = self.batchQty
        name = DS.get_username()
        batch_type = self.probe_type.get()
        check_qty = self.check_batch_qty(qty)
        check_batch = self.check_batch_number(batch)
        if check_qty and check_batch:
            self.create_new_batch(batch, batch_type, qty, name)
            self.control.show_frame(CO.Connection)
        else:
            self.refresh_window()


class ContinueSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#B1D0E0')

        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 24, 'bold'), width=12).place(x=850, y=25)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 14)).place(x=850, y=57)

        self.text_area = tk.Text(self, height=5, width=38)
        self.text_area.place(x=40, y=70)

        ttk.Label(self, text='Choose a session to resume').place(relx=0.5,
                                                                 rely=0.05, anchor=CENTER)

        ttk.Label(self, text="Batch number").place(relx=0.35, rely=0.3)
        ttk.Label(self, text="Batch type").place(relx=0.55, rely=0.3)

        self.sessionListBox = Listbox(self)
        self.sessionListBox.place(relx=0.4, rely=0.4, anchor=CENTER)
        self.sessionListBox.config(height=4, width=20)

        self.probe_typeListBox = Listbox(self)
        self.probe_typeListBox.place(relx=0.6, rely=0.4, anchor=CENTER)
        self.probe_typeListBox.config(height=4, width=15)

        self.continue_btn = ttk.Button(
            self, text='Continue Session', command=lambda: self.continue_btn_clicked(controller))
        self.continue_btn.place(height=35, width=180, x=880, y=530, anchor=E)

        self.cancel_btn = ttk.Button(
            self, text='Cancel', command=lambda: controller.show_frame(SessionSelectWindow))
        self.cancel_btn.place(height=30, width=80, x=625, y=530, anchor=E)

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

    def continue_btn_clicked(self, controller):
        batch_data = []
        try:

            lstid = self.sessionListBox.curselection()

            lstBatch = self.sessionListBox.get(lstid[0])
            batch = BM.GetBatchObject(lstBatch)
            probe_data = P(batch.probe_type,batch.batchNumber,0,batch.batchQty)
            DS.write_probe_data(probe_data)

            controller.show_frame(CO.Connection)
        except:
            tm.showerror('Select a batch',
                         'Unable to continue testing until you select a batch.')

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