"""
@Author: Brian F
Creates separate screen for issuing a serial number to a black PCB or probe without testing.
Checks to see if the batch number exists and that the probe type matches the batch number.
"""
from tkinter import Canvas, Label, Radiobutton, Button, IntVar
import OnScreenKeys
import ProbeManager
import BatchManager
import GetAuth
import Datastore

PM = ProbeManager.ProbeManager()
KY = OnScreenKeys.Keyboard()
K = OnScreenKeys
GA = GetAuth
GAU = GA.GetAuth()
DS = Datastore.DataStore()
BM = BatchManager.CSVManager()


def probe_present():
    return PM.ProbePresent()


def get_keyboard():
    KY.display()
    KY.shift()


def set_admin_auth():
    GA.set_auth(False)


class ProgramPCB:
    def __init__(self):
        self.lab1 = None
        self.lab2 = None
        self.error = None
        self.mnt_btn2 = None
        self.mnt_btn1 = None
        self.var = None
        self.canvas_prog = None
        self.has_program = False
        self.serial_number = None
        self.probe_type = None
        self.batch_number = None
        self.clicked = False
        self.present = False
        self.auth = None
        self.back_to_test = False
        self.count = 0
        self.paused = False
        self.back_colour = "#FCFFE7"

    def show_screen(self):
        self.canvas_prog = Canvas(bg=self.back_colour, width=500, height=280)
        self.canvas_prog.place(x=350, y=300)
        self.batch_number = DS.get_current_batch()
        self.probe_type = DS.get_current_probe_type()
        self.setup()

    def setup(self):
        Label(self.canvas_prog, text="New Serial Number", font=(K.FONT_NAME, 18, 'bold')).place(relx=0.2, rely=0.05)
        self.var = IntVar()
        Radiobutton(self.canvas_prog, text=f"Same batch ({self.batch_number} , {self.probe_type})", variable=self.var, value=0,
                    command=self.diff).place(relx=0.2, rely=0.2)
        Radiobutton(self.canvas_prog, text="Different batch", variable=self.var, value=1, command=self.diff).place(
            relx=0.2, rely=0.3)
        self.error = self.canvas_prog.create_text(150, 240)
        btn1 = Button(self.canvas_prog, text="OK", width=10, background="#A6D1E6", font=(K.FONT_NAME, 10, 'bold'),
                      command=self.get_auth)
        btn1.place(relx=0.8, rely=0.8)
        cancel = Button(self.canvas_prog, text="Cancel", width=12, font=(K.FONT_NAME, 10, 'bold'), command=self.end)
        cancel.place(relx=0.55, rely=0.8)
        self.paused = True

    def program_pcb(self):
        if self.auth:
            serial_number = PM.ProgramProbe(self.probe_type, False)
            self.canvas_prog.itemconfig(self.error, text=f"Complete \n{serial_number}",
                                        font=(K.FONT_NAME, 14, 'bold'))
        else:
            self.canvas_prog.itemconfig(self.error, text="Not Authorised", font=(K.FONT_NAME, 14, 'bold'))
        self.canvas_prog.after(1500, self.end)

    def end(self):
        self.paused = False
        self.canvas_prog.destroy()

    def get_auth(self):
        self.count = 0
        if probe_present():
            self.canvas_prog.itemconfig(self.error, text=" ", font=(K.FONT_NAME, 14, 'bold'))
            if DS.user_admin_status():
                self.auth = True
                self.prog_message()
                self.program_pcb()
            elif not GA.authenticate_user():
                GAU.show_screen()
                self.check()
        else:
            self.canvas_prog.itemconfig(self.error, text="Insert a PCB \nand press 'OK'", font=(K.FONT_NAME, 14, 'bold'))

    def diff(self):
        y = 135
        width = 205
        height = 40
        self.canvas_prog.itemconfig(self.error, text="")
        if self.var.get() == 1:
            self.mnt_btn1 = self.canvas_prog.create_rectangle(30, y, 30 + width, y + height, fill="#C2B6BF")
            self.lab1 = self.canvas_prog.create_text(80, 155)
            self.canvas_prog.itemconfig(self.lab1, text="Batch No.", font=(K.FONT_NAME, 10, 'bold'))

            self.mnt_btn2 = self.canvas_prog.create_rectangle(250, y, 250 + width + 30, y + height, fill="#C2B6BF")
            self.lab2 = self.canvas_prog.create_text(300, 155)
            self.canvas_prog.itemconfig(self.lab2, text="Probe type", font=(K.FONT_NAME, 10, 'bold'))

            get_keyboard()
            data_batch = K.wait_for_response(self.canvas_prog, self.batch_number, False, 0.35, 0.5)

            if data_batch == "":
                KY.end_keyboard('+')
                self.remove_screen()
                self.setup()
            else:
                get_keyboard()
                data_type = K.wait_for_response(self.canvas_prog, self.probe_type, False, 0.8, 0.5)
                progress = BM.get_file_names("in_progress")
                complete = BM.get_file_names("complete")
                if data_batch in progress:
                    last_line_inprogress = BM.ReadLastLine(data_batch, False)
                    if data_type in last_line_inprogress:
                        self.probe_type = data_type
                    else:
                        self.probe_type = last_line_inprogress[2]
                else:
                    if data_batch in complete:
                        last_line_complete = BM.ReadLastLine(data_batch, True)
                        if data_type in last_line_complete:
                            self.probe_type = data_type
                        else:
                            self.probe_type = last_line_complete[2]
                self.prog_message()
                self.program_pcb()
        else:
            KY.end_keyboard('+')
            self.remove_screen()
            self.setup()

    def check(self):
        if not self.clicked:
            self.clicked = GAU.get_clicked()
            self.canvas_prog.after(300, self.check)

        if self.clicked and self.count < 1:
            self.count += 1
            self.auth = GA.authenticate_user()
            self.prog_message()
            self.program_pcb()

    def get_pause(self):
        return self.paused

    def remove_screen(self):
        self.canvas_prog.delete(self.mnt_btn1)
        self.canvas_prog.delete(self.mnt_btn2)
        self.canvas_prog.delete(self.lab1)
        self.canvas_prog.delete(self.lab2)

    def prog_message(self):
        self.canvas_prog.itemconfig(self.error, text="Programming...", font=(K.FONT_NAME, 14, 'bold'))
