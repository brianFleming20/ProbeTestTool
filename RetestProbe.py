"""
@author: Brian F
This screen is to retest a failed probe and either pass it or leave it as a failure.
If the probe is retested and passes, the serial number is reconstructed.
"""

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
from time import gmtime, strftime, sleep

P = Ports
BM = BatchManager.BatchManager()
PI = ProbeInterface.PRI()
PT = ProbeTest
DS = Datastore.DataStore()
CO = Connection
SE = Sessions
PM = ProbeManager.ProbeManager()

from_test = False


def sort_test_entry():
    global from_test
    from_test = True


def get_probe_type(probe_data):
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


def minutes_in_range(file_time, probe_time):
    result = False
    lower = file_time - 15
    upper = file_time + 15
    for tu in range(file_time, upper):
        if tu == probe_time:
            result = True
    for tl in range(lower, file_time):
        if tl == probe_time:
            result = True
    return result


def check_data(folder, probe_date):
    hrs = 0
    probe_hrs = 0
    result = None
    batch_list = []
    fail_text = "Fail"
    for file_loc in os.listdir(folder):
        lines = BM.CSVM.read_all_lines(folder, file_loc)
        for batch_line in lines:
            SN = batch_line[1]
            if len(SN) > 6:
                if fail_text in SN:
                    SN_date = SN[8:]
                else:
                    SN_date = SN[6:]
                mon = SN_date[:2]
                day = SN_date[2:4]
                probe_mon = probe_date[:2]
                probe_day = probe_date[2:4]
                if SN[4:6].isnumeric():
                    hrs = int(SN_date[4:6])
                if probe_date[4:6].isnumeric():
                    probe_hrs = int(probe_date[4:6])
                if mon == probe_mon:
                    if day == probe_day:
                        if minutes_in_range(hrs, probe_hrs):
                            batch_list.append(batch_line)
                result = [item for item in batch_list if len(item[2]) != 0]

    if len(batch_list) == 0:
        result = ["Not Found"]
    return result


class RetestProbe(tk.Frame):
    def __init__(self, Parent, Controller):
        tk.Frame.__init__(self, Parent)
        self.odm = None
        self.probe = None
        self.znd = None
        self.results = StringVar()
        self.scrapped = None
        self.control = Controller
        self.parent = Parent
        self.qty_passed = None
        self.failed_probe = None
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
        self.test_finished = False
        self.finish = 21
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.cent_x = self.ws / 2
        self.cent_y = self.hs / 2
        self.action = StringVar()
        self.timeout = IntVar()
        self.test = False

    def screen_layout(self):
        #################################################################
        # Display main screen layout                                    #
        #################################################################
        self.canvas_back = Canvas(bg=self.back_colour, width=self.ws - 10, height=self.hs - 10)
        self.canvas_back.place(x=5, y=5)
        Label(self, text="Deltex", background="#B1D0E0", foreground="#003865",
              font=('Helvetica', 30, 'bold'), width=12).place(relx=0.85, rely=0.1)
        Label(self, text="medical", background="#B1D0E0", foreground="#A2B5BB",
              font=('Helvetica', 16)).place(relx=0.88, rely=0.15)
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
        Label(self.canvas_back, text="Failure found: ", background=self.back_colour,
              font=("Courier", 14)).place(relx=0.58, rely=0.4)
        Label(self.canvas_back, textvariable=self.failures_found, relief=SUNKEN, font=("Courier", 14, "bold"),
              width=15).place(relx=0.75, rely=0.4)
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
        Label(self.canvas_back, textvariable=self.results, width=18,
              font=('Arial', 18), borderwidth=1, relief="solid").place(relx=0.22, rely=0.65)
        Label(self.canvas_back, text="ZND Analyser", background=self.back_colour).place(relx=0.15, rely=0.45)
        Label(self.canvas_back, text="Probe Interface", background=self.back_colour).place(relx=0.25, rely=0.45)
        Label(self.canvas_back, text="Monitor     ", background=self.back_colour).place(relx=0.35, rely=0.45)
        self.znd = Label(self.canvas_back, text="      ", background="#F7A76C")
        self.znd.place(relx=0.16, rely=0.5)
        self.probe = Label(self.canvas_back, text="      ", background="#F7A76C")
        self.probe.place(relx=0.26, rely=0.5)
        self.odm = Label(self.canvas_back, text="      ", background="#F7A76C")
        self.odm.place(relx=0.36, rely=0.5)
        Label(self.canvas_back, text="Time to end", background=self.back_colour, font=('Courier', 12)).place(relx=0.1,
                                                                                                             rely=0.2)
        Label(self.canvas_back, textvariable=self.timeout, background=self.back_colour, font=('Courier', 14)).place(
            relx=0.3, rely=0.2)

    def reset_display(self):
        blank = "---"
        self.serial_number.set(blank)
        self.found_batch_number.set(blank)
        self.found_qty.set("0")
        self.failures_found.set(" --- ")
        self.date_finished.set("--/--/----")
        self.testers.set(DS.get_username())
        self.found = False
        self.failed_probe = None
        self.info_canvas = None
        self.test_finished = False
        self.scrapped = ""
        self.results.set(blank)

    def refresh_window(self):
        self.finish = 21
        self.screen_layout()
        self.reset_display()
        if self.set_devices():
            P.probe_canvas(self, "\nPlease insert a failed probe.", False)
            self.check_for_probe()
        else:
            self.refresh_window()

    def set_devices(self):
        probe_port = CO.sort_probe_interface(self)
        analyser = CO.check_analyser()
        port = P.Ports(probe=probe_port, analyer=analyser, active=False)
        DS.write_device_to_file(port)
        ports = DS.get_devices()
        set_display = False
        if not ports['Analyser']:
            mb.showerror(title="Connection Error", message="Please connect all devices.")
            self.canvas_back.destroy()
            return False
        else:
            if len(ports['Analyser']) == 4:
                self.znd.config(background="#7FB77E")
                set_display = True
            else:
                self.znd.config(background="#EB1D36")
            if len(ports['ODM']) == 4:
                self.odm.config(background="#7FB77E")
                set_display = True
            else:
                self.odm.config(background="#EB1D36")

            if len(ports['Probe']) == 4:
                self.probe.config(background="#7FB77E")
                set_display = True
            else:
                self.probe.config(background="#EB1D36")
            return set_display

    def yes_answer(self):
        self.info_canvas = True
        P.text_destroy(self)

    def no_answer(self):
        self.info_canvas = False
        P.text_destroy(self)

    def sort_return(self):
        global from_test
        P.text_destroy(self)
        if not self.found:
            P.probe_canvas(self, "Probe has not been \nregistered with the system", True)
        self.canvas_back.destroy()
        if not from_test:
            if not self.test:
                self.control.show_frame(SE.SessionSelectWindow)
        else:
            from_test = False
            if not self.test:
                self.control.show_frame(PT.TestProgramWindow)

    def remove_probe(self):
        P.probe_canvas(self, "\n\nPlease remove the probe.", False)
        while PI.probe_present():
            pass
        P.text_destroy(self)
        self.reset_display()

    def check_for_probe(self):
        probe_type = self.check_for_failed_probe()
        if self.failed_probe:
            # P.text_destroy(self)
            filepath = DS.get_file_location()
            path = filepath['File']
            inProgressPath = os.path.join(path, "in_progress", "")
            completePath = os.path.join(path, "complete", "")
            if self.check_folder(inProgressPath, self.probe_date, probe_type):
                self.found_failed_probe()
                self.found = True
            if self.check_folder(completePath, self.probe_date, probe_type):
                self.found_failed_probe()
                self.found = True
        if self.finish < 1:
            self.sort_return()
        elif not self.test_finished:
            self.check_for_probe()

    def check_folder(self, folder, probe_date, probe_type):
        found = False
        last_line = check_data(folder, probe_date)[-1]
        if "Not Found" in last_line:
            last_line = False
        if last_line is not False:
            found = True
            self.display_probe_data(last_line)
            self.batch_from_file = last_line[0]
            scrap_line = self.find_scrapped(folder)
            self.scrapped = scrap_line[6]
            if self.scrapped == "<-Scrapped":
                self.failures_found.set(self.scrapped)
            else:
                self.failures_found.set("Failed")
            batch_info = f"{last_line[0]} : {get_probe_type(probe_type)}"
            self.found_batch_number.set(batch_info)
        return found

    def display_probe_data(self, last_line):
        if self.failed_probe:
            self.qty_passed = last_line[3]
            self.found_qty.set(self.qty_passed)
            failures = last_line[7]
            if type(failures) != int:
                failures = "---"
            self.failures_found.set(failures)
            date = last_line[8]
            if date.split()[0] == "On":
                self.date_finished.set(date[2:].split()[0])
            else:
                self.date_finished.set(date.split()[0])

    def found_failed_probe(self):
        if self.scrapped == "<-Scrapped":
            P.probe_canvas(self, "This probe has already \nbeen scrapped off.", False)
            sleep(3)
            P.text_destroy(self)
        else:
            P.probe_canvas(self, "Are these details correct?", True)
            if not self.info_canvas:
                self.failed_probe = False
                self.remove_probe()
            else:
                P.text_destroy(self)
                P.probe_canvas(self, f" ({self.batch_from_file}) \nRe-testing - {self.probe_type} - probe", False)
                self.results.set("  Testing probe")
                P.text_destroy(self)

                if PT.analyser:
                    P.probe_canvas(self, f" ({self.batch_from_file}) \n{self.probe_type} - Probe Passed", False)
                    self.passed_probe()
                    P.text_destroy(self)
                else:
                    self.failed_a_probe()
                    serial_number = self.serial_number.get()
                    time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    Stime_now = str(time_now)
                    batch_makeup = [self.batch_from_file, serial_number, self.probe_type, DS.get_probes_left_to_test(),
                                    DS.get_probe_data()['Passed'], DS.get_username(), "<-Scrapped", " ",
                                    f"On {Stime_now}"]
                    BM.CSVM.WriteListOfListsCSV(batch_makeup, self.batch_from_file)
        self.remove_probe()

    def check_for_failed_probe(self):
        self.failed_probe = False
        probe_type = False
        self.finish -= 1
        self.timeout.set(self.finish)
        if PM.ProbePresent():
            serial_number = PM.read_serial_number()
            self.serial_number.set(serial_number)
            probe_type = serial_number[:3]
            self.probe_date = serial_number[8:]
            if 'Fail' in serial_number:
                self.failed_probe = True
        Tk.update(self)
        if self.finish > 0:
            return probe_type
        else:
            self.test_finished = True

    def find_scrapped(self, folder):
        for line in BM.CSVM.read_all_lines(folder, f"{self.batch_from_file}.csv"):
            if line[6] == "<-Scrapped":
                return line
            else:
                return BM.CSVM.ReadLastLine(self.batch_from_file, False)

    def passed_probe(self):
        ####################################
        # Probe has been repaired and is   #
        # retested as passed.              #
        # Reconstructs probe data to give  #
        # full passed serial number        #
        ####################################
        construct = False
        SN_seperated = []
        limit = 16
        start = 0
        ##############################
        # Start hex for probe data   #
        ##############################
        dec_start = '53A00900'
        ##############################
        # End hex for probe data     #
        ##############################
        end = '50'
        ##############################
        # Get all probe bytes        #
        ##############################
        SN_bytes = PI.read_all_bytes()
        if len(SN_bytes) == 0:
            return construct
        else:
            while limit <= len(SN_bytes):
                ################################################
                # Reconstrusts original probe data             #
                # seperating each data set into 26 bytes       #
                ################################################
                makeup = dec_start + SN_bytes[start:limit] + end
                SN_seperated.append(makeup)
                limit += 16
                start += 16
            probe_type = SN_seperated[0][8:16]
            probe_sn = SN_seperated[1][8:-2]
            #####################################
            # Formats todays date into the data #
            # format for reconstructed probe    #
            #####################################
            year_hex = [format(ord(item), "x") for item in strftime("%Y", gmtime())[2:]]
            year = year_hex[0] + year_hex[1]
            secs = [format(ord(item), "x") for item in strftime("%S", gmtime())]
            seconds = secs[0] + secs[1]
            new_probe_sn = probe_type + year + probe_sn + seconds
            #####################################
            # Converts to hex                   #
            #####################################
            new_probe_bin = codecs.decode(new_probe_sn, 'hex')
            new_probe = new_probe_bin.decode('utf-8')
            ######################################
            # write new probe data               #
            ######################################
            PM.construct_new_serial_number(new_probe)

    def failed_a_probe(self):
        left_to_test = 0
        P.probe_canvas(self, f" ({self.batch_from_file}) \n{self.probe_type} - Probe Failed", False)
        self.results.set("  Probe Failed")
        sleep(2)
        P.text_destroy(self)
        P.probe_canvas(self, f" ({self.batch_from_file}) \n{self.probe_type} \n Probe Scrapped", False)
        sleep(3)
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
        P.text_destroy(self)

    def set_test_flag(self):
        self.test = True
