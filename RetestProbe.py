'''
This screen is to retest a failed probe and either pass it or leave it as a failure.
'''
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
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
import time

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
        self.qty_passed = None
        self.check = None
        self.found = False
        self.probe_date = None
        self.probe_type = None
        self.batch_from_file = None
        self.info_canvas = None
        self.canvas_back = None
        self.control = Controller
        self.back_colour = "#A6D1E6"
        self.serial_number = StringVar()
        self.found_batch_number = StringVar()
        self.found_qty = StringVar()
        self.failures_found = StringVar()
        self.date_finished = StringVar()
        self.testers = StringVar()
        self.test_finished = True
        self.finish = 0
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.cent_x = self.ws / 2
        self.cent_y = self.hs / 2
        self.action = StringVar()

    def screen_layout(self):
        #################################################################
        # Display main screen layout                                    #
        #################################################################
        # blank = "---"

        self.canvas_back = Canvas(bg=self.back_colour, width=self.ws - 10, height=self.hs - 10)
        self.canvas_back.place(x=5, y=5)
        self.results_canvas = Canvas(bg="#9FC9F3", width=200, height=40)
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
        Label(self.canvas_back, text="Found Batch Number: ", background=self.back_colour, font=("Courier", 14)).place(
            relx=0.58, rely=0.28)
        Label(self.canvas_back, textvariable=self.found_batch_number, relief=SUNKEN, font=("Courier", 14, "bold"),
              width=15).place(relx=0.75, rely=0.3, anchor='w')
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
              font=("Courier", 14)).place(relx=0.58, rely=0.5)
        Label(self.canvas_back, textvariable=self.testers, relief=SUNKEN, font=("Courier", 14, "bold"),
              width=18).place(relx=0.75, rely=0.5)
        Label(self.canvas_back, text="Test Result ", background=self.back_colour,
              font=("Courier", 14, "bold")).place(relx=0.1, rely=0.65)
        self.results = self.results_canvas.create_text(80, 20, text=" ", fill="black", font=("Courier", 18, "bold"))
        self.results_canvas.config(bg=self.back_colour)
        Label(self.canvas_back, text="ZND Analyser", background=self.back_colour).place(relx=0.15, rely=0.45)
        Label(self.canvas_back, text="Probe Interface", background=self.back_colour).place(relx=0.25, rely=0.45)
        Label(self.canvas_back, text="Monitor     ", background=self.back_colour).place(relx=0.35, rely=0.45)
        self.znd = Label(self.canvas_back, text="      ", background="#F7A76C")
        self.znd.place(relx=0.16, rely=0.5)
        self.probe = Label(self.canvas_back, text="      ", background="#F7A76C")
        self.probe.place(relx=0.26, rely=0.5)
        self.odm = Label(self.canvas_back, text="      ", background="#F7A76C")
        self.odm.place(relx=0.36, rely=0.5)

        Button(self.canvas_back, text="Return to Sessions", font=("Courier", 14), command=self.back_to_session).place(
            relx=0.12, rely=0.77)
        # ports = DS.get_devices()
        # if ports['']
        # self.znd.config(background="#7FB77E")
        # self.probe.config(background="#7FB77E")
        # self.odm.config(background="#7FB77E")
        self.reset_display()

    def reset_display(self):
        blank = "---"
        self.serial_number.set(blank)
        self.found_batch_number.set(blank)
        self.found_qty.set("0")
        self.failures_found.set("0")
        self.date_finished.set("--/--/----")
        self.testers.set(DS.get_username())
        self.results_canvas.itemconfig(self.results, text=blank)

    def refresh_window(self):
        self.screen_layout()
        self.retest_probe()
        self.finish = 0
        PT.probe_canvas(self, "Please insert a failed probe.", False)
        self.check_for_probe()

    def retest_probe(self):
        probe_port = CO.sort_probe_interface(self)
        analyser = CO.Connection.check_analyser(self)
        port = P.Ports(probe=probe_port, analyer=analyser, active=False)
        DS.write_device_to_file(port)
        ports = DS.get_devices()
        if len(ports['Analyser']) == 4:
            self.znd.config(background="#7FB77E")
        else:
            self.znd.config(background="#EB1D36")
        if len(ports['ODM']) == 4:
            self.odm.config(background="#7FB77E")
        else:
            self.odm.config(background="#EB1D36")
        if len(ports['Probe']) == 4:
            self.probe.config(background="#7FB77E")
        else:
            self.probe.config(background="#EB1D36")


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
        PT.text_destroy(self)

    def no_answer(self):
        self.info_canvas = False
        PT.text_destroy(self)
        self.remove_probe()

    def remove_probe(self):
        PT.probe_canvas(self, "\n\nPlease remove the probe.", False)
        while PI.probe_present():
            pass
        PT.text_destroy(self)
        self.results_canvas.config(bg=self.back_colour)

    def check_probe_present(self):
        if not PM.ProbePresent():
            return False
        else:
            return True

    def check_for_probe(self):
        # PT.probe_canvas(self, "Please insert a failed probe.", False)
        probe_type = self.check_for_failed_probe()
        if self.check:
            PT.text_destroy(self)
            filepath = DS.get_file_location()
            path = filepath['File']
            inProgressPath = os.path.join(path, "in_progress", "")
            completePath = os.path.join(path, "complete", "")
            PT.probe_canvas(self, "Checking folders ", False)
            if self.check:
                if self.check_folder(inProgressPath, self.probe_date, probe_type):
                    self.found_failed_probe()
                if self.check_folder(completePath, self.probe_date, probe_type):
                    self.found_failed_probe()
                PT.text_destroy(self)
            else:
                self.test_finished = True
                self.refresh_window()
        else:
            if self.finish > 20:
                PT.text_destroy(self)
                self.back_to_session()
            else:
                Tk.update(self)
                # PT.text_destroy(self)
                self.check_for_probe()
        self.finish += 1

    def check_folder(self, folder, probe_date, probe_type):
        hrs = 0
        probe_hrs = 0
        result = False
        for file_loc in os.listdir(folder):
            lines = BM.CSVM.read_all_lines(folder, file_loc)
            for batch in lines:
                SN = batch[1][8:]
                if len(SN) > 6:
                    mon = SN[:2]
                    day = SN[2:4]
                    probe_mon = probe_date[:2]
                    probe_day = probe_date[2:4]
                    try:
                        hrs = int(SN[4:6])
                        probe_hrs = int(probe_date[4:6])
                    except:
                        pass
                    if mon == probe_mon and day == probe_day:
                        if self.minutes_in_range(hrs,probe_hrs):

                            last_line = BM.CSVM.ReadLastLine(file_loc[:-4])[0]
                            self.display_probe_data(last_line)
                            self.probe_type = self.get_probe_type(probe_type)
                            self.found = True
                            self.batch_from_file = file_loc[:-4]
                            batch_info = f"{self.batch_from_file} : {self.probe_type}"
                            self.found_batch_number.set(batch_info)
                            result = True
        return result

    def display_probe_data(self, last_line):
        if self.check:
            qty_failed = last_line[7]
            self.qty_passed = last_line[3]
            date_complete = last_line[8][:-9]
            self.found_qty.set(self.qty_passed)
            self.failures_found.set(qty_failed)
            self.date_finished.set(date_complete)
        else:
            PT.probe_canvas(self, "This probe has not failed.", False)
            time.sleep(2)
            PT.text_destroy(self)
            self.remove_probe()
            self.refresh_window()

    def found_failed_probe(self):
        if self.found:
            left_to_test = 0
            PT.text_destroy(self)
            PT.probe_canvas(self,"Are these details correct?",True)
            if not self.info_canvas:
                self.check = False
                self.reset_display()
            if self.info_canvas:
                PT.text_destroy(self)
                PT.probe_canvas(self, f" ({self.batch_from_file}) \nRe-testing - {self.probe_type} - probe", False)
                self.results_canvas.itemconfig(self.results, text="  Testing probe")
                PT.TestProgramWindow.warnings(self)
                results, marker_data, odm_data = PT.TestProgramWindow.test_probe(self)
                PT.text_destroy(self)

                if results == "Pass":
                    PT.probe_canvas(self, f" ({self.batch_from_file}) \n{self.probe_type} - Probe Passed", False)
                    self.results_canvas.config(background='#7FB77E')
                    SN_seperated = []
                    limit = 16
                    start = 0
                    dec_start = '53A00900'
                    end = '50'
                    # pcb_serial_number = PM.read_serial_number()
                    # binary_str = codecs.decode(pcb_serial_number, "hex")
                    # print(f"serial number = {str(binary_str)[2:18]}")
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
                    PT.text_destroy(self)
                    self.remove_probe()
                if results == "Fail":
                    PT.probe_canvas(self, f" ({self.batch_from_file}) \n{self.probe_type} - Probe Failed", False)
                    self.results_canvas.itemconfig(self.results, text="  Probe Failed")
                    self.results_canvas.config(background='#EB1D36')
                    time.sleep(2)
                    PT.text_destroy(self)
                    PT.probe_canvas(self, f" ({self.batch_from_file}) \n{self.probe_type} \n Probe Scrapped", False)
                    time.sleep(3)
                    failed = DS.get_probe_data()['Failures']
                    scraped = DS.get_probe_data()['Scrapped']
                    if DS.get_probe_data()['Batch'] == self.batch_from_file:
                        left_to_test = DS.get_probe_data()['Left_to_test']
                    if failed > 0:
                        failed -= 1
                        scraped += 1
                    probe_data = P.Probes(self.probe_type, self.batch_from_file,
                                          self.qty_passed, left_to_test, failed=failed, scrap=scraped)
                    DS.write_probe_data(probe_data)
                    PT.text_destroy(self)
                    if scraped > 0:
                        answer = mb.askyesno(title="Batch Quantity",
                                             message=f"You need to adjust at end.\nBatch number {self.batch_from_file} to 100.")
                        batch_makeup = ["Scrapped","acknowledged",answer,DS.get_probe_data()['Passed'],"Passed, Scrapped = ",scraped,"Failed", failed]
                        BM.CSVM.WriteListOfListsCSV(batch_makeup, self.batch_from_file)
            self.reset_display()
            self.remove_probe()

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

    def minutes_in_range(self, file_time, probe_time):
        result = False
        lower = file_time - 15
        upper = file_time + 15
        for tu in range(file_time,upper):
            if tu == probe_time:
                result = True
        for tl in range(lower, file_time):
            if tl == probe_time:
                result = True
        return result

    def check_for_failed_probe(self):
        self.check = False
        probe_type = None
        self.finish += 1
        if self.check_probe_present():
            self.test_finished = False
        else:
            self.test_finished = True
        if not self.test_finished:
            binary_str = codecs.decode(PI.read_serial_number(), "hex")
            serial_number = str(binary_str)[2:18]
            self.serial_number.set(serial_number)
            probe_type = serial_number[:3]
            self.probe_date = serial_number[8:]
            if 'Fail' in serial_number:
                self.check = True
        return probe_type
