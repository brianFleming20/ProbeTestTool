"""
Created on 3 May 2017
@author: jackw
@author: Brian F
Naming convention
- Variables = no spaces, capitals for every word except the first : thisIsAVariable
- Local functions = prefixed with _, _ for spaces, no capitals : _a_local_function

User selectable items from onscreen options
New batches create new batch file with titles

"""
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter.messagebox as tm
import BatchManager
import SecurityManager
import UserLogin
import Connection
import AdminUser
import Datastore
import OnScreenKeys
import ProbeManager
from time import gmtime, strftime
import Ports
import ProbeTest
import ProbeInterface
import RetestProbe

BM = BatchManager.BatchManager()
SM = SecurityManager.SecurityManager()
DS = Datastore.DataStore()
KY = OnScreenKeys.Keyboard()
K = OnScreenKeys
P = Ports
UL = UserLogin
CO = Connection
AU = AdminUser
PT = ProbeTest
PI = ProbeInterface.PRI()
PM = ProbeManager.ProbeManager()
RP = RetestProbe


def ignore():
    return 'break'


BTN_WIDTH = 22
BTN_HEIGHT = 20
BATCH_QTY = 100


def set_qty(qty):
    global BATCH_QTY
    BATCH_QTY = qty


def get_qty():
    global BATCH_QTY
    return BATCH_QTY


class SessionSelectWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__()
        ##################################
        # create a choose session window #
        ##################################
        tk.Frame.__init__(self, parent, bg="#B1D0E0")
        self.cancel_btn = None
        self.label1 = None
        self.SSW_b3 = None
        self.SSW_b4 = None
        self.failed = None
        self.SSW_b2 = None
        self.NSWL1 = None
        self.text_area = None
        self.cent_y = None
        self.cent_x = None
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
                  font=('Helvetica', 30, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 16)).place(relx=0.88, rely=0.15)
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
        btn1 = tk.Button(self, text='Start a new session', background="#5FD068",
                         command=lambda: self.control.show_frame(NewSessionWindow))
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
        self.failed = tk.Button(self, text='Re-test Failed Probe.', background="#A8E890", command=self.failed_probe)
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
        ################################
        # User greeting                #
        ################################
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
        self.text_area.insert('2.0', DS.get_username().title())
        self.text_area.insert('3.3', '\n\nPlease choose an option.')
        self.text_area.config(state=DISABLED)

    def completed_btn_clicked(self):
        self.complete_canvas = Canvas(bg="#eae9e9", width=400, height=350)
        self.complete_canvas.place(relx=0.78, rely=0.28)
        scrollbar = Scrollbar(self.complete_canvas, orient=VERTICAL)
        complete_list = Listbox(self.complete_canvas, height=12, width=12)
        complete_list.place(x=0, y=50)
        scrollbar.pack(side=RIGHT, fill=Y)
        complete_list.config(font=("Arial", 14))
        for probe in BM.get_completed_batches():
            complete_list.insert(END, ' ' + probe)
        scrollbar.config(command=complete_list.yview)
        complete_list.config(yscrollcommand=scrollbar.set)
        complete_list.pack(side=LEFT)
        self.label1 = Label(self, text="Complete batches", background="#B1D0E0", font=("Courier", 16, "bold"))
        self.label1.place(relx=0.75, rely=0.23)
        self.cancel_btn = tk.Button(self, text="Close", font=("Courier", 16), command=self.canvas_go)
        self.cancel_btn.place(relx=0.82, rely=0.65)
        complete_list.config(state=DISABLED)

    def logout(self):
        try:
            self.canvas_go()
        except:
            pass
        SM.logOut()
        self.control.show_frame(UL.LogInWindow)

    def blank(self):
        probe = P.Ports(probe="COM4")
        DS.write_device_to_file(probe)
        tm.showinfo("test", "Insert a probe to blank")
        PM.blank_probe()

    def failed_probe(self):
        probe_port = CO.sort_probe_interface(self)
        port = P.Ports(probe=probe_port)
        DS.write_device_to_file(port)
        self.control.show_frame(RP.RetestProbe)

    def canvas_go(self):
        self.complete_canvas.destroy()
        self.cancel_btn.destroy()
        self.label1.destroy()


class NewSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.type_text = None
        self.cancel = None
        self.btn_2 = None
        self.btn_1 = None
        self.text_area = None
        self.canvas_qty = None
        self.canvas_type = None
        self.canvas_back = None
        self.batchNumber = None
        self.probe_type = StringVar()
        self.batchQty = BATCH_QTY
        self.control = controller
        self.test = False

    def refresh_window(self):
        global batch_qty
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        self.canvas_back = Canvas(bg='#B1D0E0', width=ws - 10, height=hs - 10)
        self.canvas_back.place(x=5, y=5)
        self.canvas_type = Canvas(width=400, height=50)
        self.canvas_type.place(relx=0.5, rely=0.4)
        ttk.Label(self.canvas_back, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 30, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self.canvas_back, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 16)).place(relx=0.88, rely=0.15)
        self.batchNumber = None
        self.probe_type.set("")
        self.text_area = tk.Text(self.canvas_back, font=("Courier", 14), height=5, width=38)
        self.text_area.place(x=40, y=70)
        ttk.Label(self.canvas_back, text='Probe selection window. ',
                  justify=RIGHT, font=("Courier", 20, "bold"), background="#B1D0E0").place(relx=0.5, rely=0.05,
                                                                                           anchor=CENTER)
        ttk.Label(self.canvas_back, text='Select Probe Type: ',
                  justify=RIGHT, font=("Courier", 18, "bold"), background="#B1D0E0").place(relx=0.12, rely=0.3)
        tk.Button(self.canvas_back, text='Continue', font=("Courier", 16), width=20, height=2,
                  command=self.to_devices).place(relx=0.82, rely=0.8, anchor=CENTER)
        self.cancel = tk.Button(self.canvas_back, text='Cancel', font=("Courier", 14), command=self.back)
        self.cancel.place(relx=0.56, rely=0.8, anchor=CENTER)
        self.type_text = self.canvas_type.create_text(250, 20, text=" ", fill="black",
                                                      font=(OnScreenKeys.FONT_NAME, 8, "bold"))
        self.btn_1 = Button(self.canvas_type, text='Batch number: ', command=self.batch_entry)
        self.btn_1.place(relx=0.21, rely=0.3, anchor=N)
        Label(self.canvas_type, text="-->").place(x=180, y=18)
        self.text_area.config(state=NORMAL)
        self.text_area.insert('1.0', DS.get_username().title())
        self.text_area.insert('3.3', '\n\nPlease enter the batch number\nselect the probe type\nand batch quantity.')
        self.text_area.config(state=DISABLED)
        if not self.test:
            self.fill_probe_types()

    def get_keys(self):
        KY.get_keyboard()
        if not self.test:
            self.btn_1.config(state=DISABLED)

    def batch_entry(self):
        self.get_keys()
        data = K.wait_for_response(self.canvas_type, self.type_text)
        self.batchNumber = data
        if not self.test:
            self.btn_1.config(state=NORMAL)

    def fill_probe_types(self):
        probe_type_frame = tk.Frame(self.canvas_back, pady=3, padx=50, bg='#E0FFFF')
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
        style = Style(probe_type_frame)
        style.configure("TButton", font=("arial", 14))
        self.canvas_qty = Canvas(width=400, height=50)
        self.canvas_qty.place(relx=0.5, rely=0.55)
        Label(self.canvas_qty, text="Batch Qty:", font=("bold", 14)).place(relx=0.18, rely=0.3, anchor=N)
        Label(self.canvas_qty, text="-->").place(x=180, y=18)
        ttk.Label(self.canvas_qty, text=get_qty(), font=("bold", 14)).place(relx=0.75, rely=0.3, width=140, anchor=N)

    def confm_btn_clicked(self):
        ######################
        # create new batch   #
        ######################
        batch = self.batchNumber
        user = DS.get_username()
        batch_type = self.probe_type.get()
        check_batch = self.convert_to_uppercase(batch)
        if not check_batch:
            self.back()
            self.refresh_window()
        elif not self.create_new_batch(check_batch, batch_type, BATCH_QTY, user):
            self.canvas_back.destroy()
            self.refresh_window()
        else:
            if not self.test:
                self.connection()
            else:
                return True

    def create_new_batch(self, batch_number, batch_type, qty, user):
        newBatch = P.Batch(batch_number)
        newBatch.probe_type = batch_type
        newBatch.batchQty = qty
        check = False
        DAnswer = tm.askyesno(title='Confirm',
                              message=f'Are batch details correct?\n\n Batch number {batch_number} \n Batch Qty{qty}')
        if DAnswer:
            # create the batch file
            if not BM.CreateBatch(newBatch, user):
                tm.showerror(title='Error', message='Batch number not unique')
            else:
                check = True
        return check

    def convert_to_uppercase(self, batch):
        result = False
        if len(batch) < 5:
            tm.showerror(title="Batch Error", message="This batch number is not correct.")
        else:
            if self.check_batch_number(batch):
                batch_numbers = batch[:-1]
                batch_letter = batch[-1].upper()
                confirm_batch = batch_numbers + batch_letter
                result = confirm_batch
        return result

    def check_batch_number(self, batch):
        check = False
        if len(batch) == 0:
            tm.showerror(title="error", message="Enter a batch number")
            return check
        end = batch[-1]
        start = batch[:-1]
        if end.isalpha() and start.isnumeric():
            check = True
        if not check:
            tm.showerror(title="Error", message="Batch number in-complete")
        return check

    def connection(self):
        self.canvas_back.destroy()
        self.control.show_frame(CO.Connection)

    def back(self):
        self.canvas_type.destroy()
        self.canvas_qty.destroy()
        self.canvas_back.destroy()
        self.control.show_frame(SessionSelectWindow)

    def to_devices(self):
        self.canvas_type.destroy()
        self.canvas_qty.destroy()
        self.confm_btn_clicked()

    def set_test(self):
        self.test = True


def get_available_batches():
    return BM.GetAvailableBatches()


class ContinueSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#B1D0E0')
        self.suspend_dict = None
        self.text_area = None
        self.control = controller
        self.index = 0
        self.batch_selected = ""
        self.test = False
        ttk.Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 30, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 16)).place(relx=0.88, rely=0.15)
        ttk.Label(self, text='Choose a session to resume', font=("Courier", 18), background="#B1D0E0").place(relx=0.5,
                                                                                                             rely=0.05,
                                                                                                             anchor=CENTER)
        ttk.Label(self, text="Batch number", font=("Courier", 16), background="#B1D0E0").place(relx=0.28, rely=0.32)
        ttk.Label(self, text="Batch type", font=("Courier", 16), background="#B1D0E0").place(relx=0.58, rely=0.32)
        self.sessionListBox = Listbox(self)
        self.sessionListBox.place(relx=0.38, rely=0.45, anchor=CENTER)
        self.sessionListBox.config(height=5, width=20, font=("Courier", 18))
        self.probe_typeListBox = Listbox(self, exportselection=False)
        self.probe_typeListBox.place(relx=0.65, rely=0.45, anchor=CENTER)
        self.probe_typeListBox.config(height=5, width=15, font=("Courier", 18))
        self.sessionListBox.focus_set()
        self.continue_btn = tk.Button(
            self, text='Continue Session', height=2, font=("Courier", 14), command=self.continue_btn_clicked)
        self.continue_btn.place(relx=0.88, rely=0.82, anchor=E)
        self.cancel_btn = ttk.Button(
            self, text='Cancel', command=lambda: self.control.show_frame(SessionSelectWindow))
        self.cancel_btn.place(height=35, width=90, relx=0.62, rely=0.82, anchor=E)
        btn_up = tk.Button(self, text="\u2191", font=("Courier", 30), command=lambda: self.up_arrow())
        btn_up.place(relx=0.8, rely=0.32)
        btn_down = tk.Button(self, text="\u2193", font=("Courier", 30), command=lambda: self.down_arrow())
        btn_down.place(relx=0.8, rely=0.52)

    def refresh_window(self):
        self.test = False
        self.text_area = tk.Text(self, font=("Courier", 14), height=5, width=38)
        self.text_area.place(x=40, y=70)
        self.text_area.delete(1.0, 'end')
        self.suspend_dict = {item: self.get_batch_type(item) for item in get_available_batches()}
        self.set_display()
        self.sessionListBox.delete(0, END)
        self.probe_typeListBox.delete(0, END)
        for batch, probe in self.suspend_dict.items():
            self.probe_typeListBox.insert(END, probe)
            self.sessionListBox.insert(END, batch)
        self.sessionListBox.itemconfig(self.index, {"bg": "#5CB8E4"})
        self.probe_typeListBox.itemconfig(self.index, {"bg": "#5CB8E4"})
        self.batch_selected = self.sessionListBox.get(self.index)

    def up_arrow(self):
        self.index -= 1
        if self.index < 0:
            self.index = 0
        self.sessionListBox.itemconfig(self.index, {"bg": "#5CB8E4"})
        self.probe_typeListBox.itemconfig(self.index, {"bg": "#5CB8E4"})
        self.sessionListBox.itemconfig(self.index + 1, {"bg": "#FEFCF3"})
        self.probe_typeListBox.itemconfig(self.index + 1, {"bg": "#FEFCF3"})
        self.batch_selected = self.sessionListBox.get(self.index)

    def down_arrow(self):
        self.index += 1
        if self.index > 4 or self.index > len(list(self.suspend_dict.keys())) - 1:
            self.index = 4
        self.sessionListBox.itemconfig(self.index, {"bg": "#5CB8E4"})
        self.probe_typeListBox.itemconfig(self.index, {"bg": "#5CB8E4"})
        self.sessionListBox.itemconfig(self.index - 1, {"bg": "#FEFCF3"})
        self.probe_typeListBox.itemconfig(self.index - 1, {"bg": "#FEFCF3"})
        self.batch_selected = self.sessionListBox.get(self.index)

    def continue_btn_clicked(self):
        batch = BM.get_batch_line(self.batch_selected, False)
        probe_data = P.Probes(batch[2], batch[0], 0, int(batch[3]))
        DS.write_probe_data(probe_data)
        if not self.test:
            self.control.show_frame(CO.Connection)

    def set_display(self):
        self.text_area.config(state=NORMAL)
        self.text_area.insert('1.0', DS.get_username().title())
        self.text_area.insert('3.3', '\n\nPlease select a batch number\nto continue testing.')
        self.text_area.config(state=DISABLED)

    def get_batch_type(self, batch_number):
        ########################################
        # get batch type from the batch number #
        # of probe serial number from file     #
        ########################################
        return BM.get_batch_line(batch_number, False)[2]

    def set_test(self):
        self.test = True
