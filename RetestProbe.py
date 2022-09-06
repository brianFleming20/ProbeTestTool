'''
This screen is to retest a failed probe and either pass it or leave it as a failure.
'''
import tkinter as tk
from tkinter import *
import Ports
import BatchManager
import ProbeManager
import ProbeInterface
import ProbeTest
import Datastore
import Connection
import Sessions
import codecs
import os


P = Ports
BM = BatchManager.BatchManager()
PI = ProbeInterface.PRI()
PT = ProbeTest
DS = Datastore.Data_Store()
CO = Connection
SE = Sessions
PM = ProbeManager.ProbeManager()


class RetestProbe(tk.Frame):
    def __init__(self, Parent, Controller):
        tk.Frame.__init__(self, Parent)
        self.found = False
        self.probe_date = None
        self.probe_type = None
        self.batch_from_file = None
        self.info_canvas = None
        self.canvas_back = None
        self.control = Controller
        self.parent = Parent
        self.back_colour = "#A6D1E6"
        self.serial_number = StringVar()
        self.found_batch_number = StringVar()
        self.found_qty = StringVar()
        self.failures_found = StringVar()
        self.date_finished = StringVar()
        self.testers = StringVar()

    def screen_layout(self):
        #################################################################
        # Display main screen layout                                    #
        #################################################################
        blank = "---"

        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        self.canvas_back = Canvas(bg=self.back_colour, width=ws - 10, height=hs - 10)
        self.canvas_back.place(x=5, y=5)
        self.cent_x = ws / 2
        self.cent_y = hs / 2
        self.results_canvas = Canvas(bg="#9FC9F3", width=180, height=40)
        self.results_canvas.place(x=300, y=580)
        Label(self.canvas_back, text="Deltex", background=self.back_colour, foreground="#003865",
                  font=('Helvetica', 28, 'bold'), width=12).place(relx=0.79, rely=0.1)
        Label(self.canvas_back, text="medical", background=self.back_colour, foreground="#A2B5BB",
                  font=('Helvetica', 18)).place(relx=0.85, rely=0.15)
        Label(self.canvas_back, text="Probe Re-test", background=self.back_colour,
              font=("Courier", 24, "bold")).place(relx=0.4, rely=0.05)
        Label(self.canvas_back, text='Serial Number: ', background=self.back_colour, font=("Courier", 14)).place(
            relx=0.1, rely=0.3, anchor='w')
        Label(self.canvas_back, textvariable=self.serial_number, relief=SUNKEN, font=("Courier", 14, "bold"),
            width=22).place(relx=0.25, rely=0.3, anchor='w')
        Label(self.canvas_back, text="Found Batch Number: ",background=self.back_colour,font=("Courier", 14)).place(
            relx=0.58,rely=0.28)
        Label(self.canvas_back, textvariable=self.found_batch_number, relief=SUNKEN, font=("Courier", 14, "bold"),
              width=15).place(relx=0.75,rely=0.3, anchor='w')
        Label(self.canvas_back, text="Batch found Qty.", background=self.back_colour,
              font=("Courier", 14)).place(relx=0.58, rely=0.34)
        Label(self.canvas_back, textvariable=self.found_qty, relief=SUNKEN,
              font=("Courier", 14, "bold"), width=8).place(relx=0.75, rely=0.35, anchor='w')
        Label(self.canvas_back, text="Failures found: ", background=self.back_colour,
              font=("Courier", 14)).place(relx=0.58, rely=0.4)
        Label(self.canvas_back, textvariable=self.failures_found, relief=SUNKEN, font=("Courier", 14, "bold"),
              width=8).place(relx=0.75, rely=0.4)
        Label(self.canvas_back, text="Date batch finished: ", background=self.back_colour,
              font=("Courier", 14)).place(relx=0.58, rely=0.45)
        Label(self.canvas_back, textvariable=self.date_finished, relief=SUNKEN, font=("Courier", 14, "bold"),
              width=15).place(relx=0.75, rely=0.45)
        Label(self.canvas_back, text="Testers: ", background=self.back_colour,
              font=("Courier", 14)).place(relx=0.58,rely=0.5)
        Label(self.canvas_back, textvariable=self.testers, relief=SUNKEN, font=("Courier", 14, "bold"),
              width=18).place(relx=0.75, rely=0.5)
        Label(self.canvas_back, text="Test Result ", background=self.back_colour,
              font=("Courier", 14, "bold")).place(relx=0.1, rely=0.65)
        self.results = self.results_canvas.create_text(80,20, text=" ", fill="black", font=("Courier", 18, "bold"))
        self.results_canvas.itemconfig(self.results, text="Pass")
        self.results_canvas.config(bg="#7FB77E")
        Label(self.canvas_back, text="ZND Analyser", background=self.back_colour).place(relx=0.15, rely=0.45)
        Label(self.canvas_back, text="Probe Interface", background=self.back_colour).place(relx=0.25, rely=0.45)
        Label(self.canvas_back, text="Monitor     ", background=self.back_colour).place(relx=0.35, rely=0.45)
        self.znd = Label(self.canvas_back,text="      ", background="#F7A76C")
        self.znd.place(relx=0.16, rely=0.5)
        self.probe = Label(self.canvas_back, text="      ", background="#F7A76C")
        self.probe.place(relx=0.26, rely=0.5)
        self.odm = Label(self.canvas_back, text="      ", background="#F7A76C")
        self.odm.place(relx=0.36, rely=0.5)
        self.retest_btn = Button(self.canvas_back, text="Re-test",
                                 background="#42855B",font=("Courier", 16), command=self.retest_probe)
        self.retest_btn.place(relx=0.78,rely=0.75)
        Button(self.canvas_back, text="Return to Sessions", font=("Courier", 14), command=self.back_to_session).place(relx=0.12,rely=0.77)
        Button(self.canvas_back, text="Return to Probe Test", font=("Courier", 14), command=self.back_to_test).place(relx=0.35, rely=0.77)
        self.znd.config(background="#7FB77E")
        self.probe.config(background="#7FB77E")
        self.odm.config(background="#7FB77E")
        self.serial_number.set(blank)
        self.found_batch_number.set(blank)
        self.found_qty.set("0")
        self.failures_found.set("0")
        self.date_finished.set("--/--/----")
        self.testers.set(DS.get_username())
        self.check_for_probe()

        PT.probe_canvas(self,"Are these details correct? ",True)

    def refresh_window(self):
        self.screen_layout()

    def retest_probe(self):
        probe_port = CO.sort_probe_interface(self)
        port = P.Ports(probe=probe_port)
        DS.write_device_to_file(port)
        print("Re testing probe")

    def back_to_test(self):
        self.canvas_back.destroy()
        self.results_canvas.destroy()
        self.control.show_frame(PT.TestProgramWindow)

    def back_to_session(self):
        self.canvas_back.destroy()
        self.results_canvas.destroy()
        self.control.show_frame(SE.SessionSelectWindow)

    def yes_answer(self):
        self.info_canvas = True
        print("Yes")
        PT.text_destroy(self)

    def no_answer(self):
        self.info_canvas = False
        PT.text_destroy(self)
        self.remove_probe()

    def remove_probe(self):
        PT.probe_canvas(self, "Please remove the probe.",False)
        while PI.probe_present():
            pass

        print("Thanks")
        PT.text_destroy(self)

    def check_for_probe(self):
        PT.probe_canvas(self, "Please insert a failed probe.",False)
        while not PI.probe_present():
            pass
        PT.text_destroy(self)

        binary_str = codecs.decode(PI.read_serial_number(), "hex")
        serial_number = str(binary_str)[2:18]
        self.serial_number.set(serial_number)
        probe_type = serial_number[:4]
        self.probe_date = serial_number[8:]
        filepath = DS.get_file_location()
        path = filepath['File']
        inProgressPath = os.path.join(path, "in_progress", "")
        completePath = os.path.join(path, "complete", "")
        if self.probe_date:
            PT.probe_canvas(self, "Checking in-progress folder", False)
            self.check_folder(inProgressPath, self.probe_date, probe_type)
            PT.text_destroy(self)
        elif self.probe_date:
            PT.probe_canvas(self, "Checking Complete folder", False)
            self.check_folder(completePath, self.probe_date, probe_type)
            PT.text_destroy(self)
        else:
            self.passed_probe()

    def check_folder(self, folder, probe_date, probe_type):
        print(f"from folder {folder}")
        for file_loc in os.listdir(folder):
            print(f"file location {file_loc[:-4]}")
            lines = BM.CSVM.ReadAllLines(file_loc[:-4])
            for batch in lines:
                self.batch_from_file = file_loc[:-4]
                SN = batch[0][1:-1]
                if len(SN) > 5:
                    if 'Fail' in SN:
                        print(f"Fail {SN} probe sn is {probe_date}")
                        self.probe_type = self.get_probe_type(probe_type[:-1])
                        print(f"Probe type {self.probe_type}")
                        if probe_date in SN:
                            last_line = BM.CSVM.ReadLastLine(self.batch_from_file)[0]
                            batch_info = f"{self.batch_from_file}  {self.probe_type}"
                            self.found_batch_number.set(batch_info)
                            print(last_line)
                            qty_failed = last_line[7]
                            qty_passed = last_line[3]
                            date_complete = last_line[8][:-9]
                            self.found_qty.set(qty_passed)
                            self.failures_found.set(qty_failed)
                            self.date_finished.set(date_complete)
                    # else:
                    #     PT.text_destroy(self)
        # if self.found:
        #     batch_info = f"{self.batch_from_file}  {self.probe_type}"
        #     self.found_batch_number.set(batch_info)


        #     if retest:
        #         PT.probe_canvas(self, f" ({self.batch_from_file}) \nRe-testing - {self.probe_type} - probe", False)
        #         results, marker_data, odm_data = PT.TestProgramWindow.test_probe(self)
        #
        #         PT.text_destroy(self)
        #
        #         PT.probe_canvas(self, f" ({self.batch_from_file}) \n{self.probe_type} - probe passed", False)
        #         if results:
        #             SN_seperated = []
        #             limit = 16
        #             start = 0
        #             dec_start = '53A00900'
        #             end = '50'
        #             # pcb_serial_number = PM.read_serial_number()
        #             # binary_str = codecs.decode(pcb_serial_number, "hex")
        #             # print(f"serial number = {str(binary_str)[2:18]}")
        #             SN_bytes = PI.read_all_bytes()
        #             while limit <= len(SN_bytes):
        #                 makeup = dec_start + SN_bytes[start:limit] + end
        #                 SN_seperated.append(makeup)
        #                 limit += 16
        #                 start += 16
        #             probe_type = SN_seperated[0][8:16]
        #             probe_sn = SN_seperated[1][8:-2]
        #             new_probe_sn = probe_type + '3232' + probe_sn + '3031'
        #             new_probe_bin = codecs.decode(new_probe_sn, 'hex')
        #             new_probe = new_probe_bin.decode('utf-8')
        #             PM.construct_new_serial_number(new_probe, True)
        #
        #         PT.text_destroy(self)
        #         self.remove_probe()
        # else:
        #     return False

    def get_probe_type(self, probe_data):
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

    def passed_probe(self):
        self.info_canvas = False
        PT.probe_canvas(self, "Please remove the probe.\n\nInsert a failed probe.", False)
        while PI.probe_present():
            pass
        PT.text_destroy(self)
