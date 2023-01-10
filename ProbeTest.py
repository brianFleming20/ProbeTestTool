'''
Created on 3 May 2017
Updated on 22 Dec 2021
@author: jackw
@amended: by Brian F
Naming convention
- Variables = no spaces, capitals for every word except the first : thisIsAVariable
- Local functions = prefixed with _, _ for spaces, no capitals : _a_local_function
Dependencies
-NI VISA Backend not used
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
import BatchManager
from ProbeManager import ProbeManager
from ProbeInterface import PRI
import NanoZND
import ODMPlus
import Sessions
import FaultFinder
import Datastore
import Ports
import time
import RetestProbe
import os

# create instances
BM = BatchManager.BatchManager()
PM = ProbeManager()
ZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
DS = Datastore.Data_Store()
P = Ports
SE = Sessions
FF = FaultFinder
PR = PRI()
RT = RetestProbe

# define global variables
PTT_Version = 'Deltex Medical : XXXX-XXXX Probe Test Tool V1'
w = 800  # window width
h = 600  # window height
LARGE_FONT = ("Verdana", 14)
BTN_WIDTH = 30
LOWER_LIMIT = 162.0
UPPER_LIMIT = 220.0
KDP_LOWER = 145.0

warning_text = {
    "overrite on": "Probe serial number re-issue enabled.",
    "overrite off": "Probe serial number re-issue disabled.",
    "1": " Probe connected  ",
    "2": "Programmed Probe  ",
    "3": "   New Serial Number ?        ",
    "4": "Information",
    "5": "   Fault Find Probe ?       ",
    "6": "Connect New Probe ",
    "7": "Batch Complete.",
    "8": "\nRemove probe.",
    "9": "Programming probe ",
    "10": "Testing probe...  ",
    "11": "\nProgramming error",
    "12": "\nUnable to program, \nPlease check probe chip. ",
    "13": " Probe Failed... ",
    "14": "\n\nFault finding this probe.",
    "15": "\nProbe passed ...",
    "16": "\nPlease remove probe...",
    "17": "\n Passed Analyser  ",
    "18": "\nPassed reflection "
}

analyser = False


def perform_probe_test():
    global analyser
    marker = round(ZND.tdr(), 3)
    lower_limit = LOWER_LIMIT
    if DS.get_probe_data()['Probe_Type'] == "KDP72":
        lower_limit = KDP_LOWER
    if PM.ProbePresent():
        if lower_limit < marker < UPPER_LIMIT:
            # Also check marker data from analyser too
            analyser = True
            # P.AnalyserResult().set_analyser_result(marker, analyser)
    return marker


def probe_programmed():
    return PM.read_serial_number()


def detect_recorded_probe():
    found = None
    fail = "Fail"
    not_found = "Not Found"
    filepath = DS.get_file_location()
    path = filepath['File']
    inProgressPath = os.path.join(path, "in_progress", "")
    completePath = os.path.join(path, "complete", "")
    serial_number = PM.read_serial_number()
    if fail in serial_number:
        search = serial_number[8:]
    else:
        search = serial_number[6:]
    found_in_progress = RT.check_data(inProgressPath, search)[0]

    if found_in_progress == not_found:
        found_complete = RT.check_data(completePath, search)[0]
        if found_complete == not_found:
            found = not_found
        else:
            found = found_complete[0]
    else:
        found = found_in_progress[0]

    return found, serial_number


class TestProgramWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # define variables
        self.control = controller
        self.session_on_going = True
        self.session_complete = False
        self.action = StringVar()
        self.left_to_test = IntVar()
        self.current_batch = StringVar()
        self.current_user = StringVar()
        self.probes_passed = IntVar()
        self.device_details = StringVar()
        self.odm_details = StringVar()
        self.probe_type = StringVar()
        self.reflection = StringVar()
        self.show_serial_number = StringVar()
        self.SD_data = IntVar()
        self.FTc_data = IntVar()
        self.PV_data = IntVar()
        self.user_admin = False
        self.probes_passed.set(0)
        self.info_canvas = None
        self.test = False
        self.serial_number = None
        self.reset_ana = None
        self.file_data = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')

        ###############################################################
        # import and set up images for the screen                     #
        ###############################################################
        self.greenlight = (PhotoImage(file=os.path.join(self.file_data, "PTT_Icons/GREEN.png")))
        self.amberlight = (PhotoImage(file=os.path.join(self.file_data, "PTT_Icons/AMBER.png")))
        self.redlight = (PhotoImage(file=os.path.join(self.file_data, "PTT_Icons/RED.png")))
        self.greylight = (PhotoImage(file=os.path.join(self.file_data, "PTT_Icons/GREY.png")))
        self.back_colour = "#A6D1E6"

    def display_layout(self):
        #################################################################
        # Display main screen layout                                    #
        #################################################################
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        self.canvas_back = Canvas(bg=self.back_colour, width=ws - 10, height=hs - 10)
        self.canvas_back.place(x=5, y=5)
        self.cent_x = ws / 2
        self.cent_y = hs / 2
        self.text_area = tk.Text(self.canvas_back, font=("Courier", 14), height=5, width=40)
        self.text_area.place(relx=0.07, rely=0.1)
        ttk.Label(self.canvas_back, text="Deltex", background=self.back_colour, foreground="#003865",
                  font=('Helvetica', 30, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self.canvas_back, text="medical", background=self.back_colour, foreground="#A2B5BB",
                  font=('Helvetica', 16)).place(relx=0.88, rely=0.15)
        self.text_area.delete('1.0', 'end')
        ttk.Label(self.canvas_back, text="Probe Test", background=self.back_colour,
                  font=("Courier", 24, "bold")).place(relx=0.45, rely=0.05)
        ttk.Label(self.canvas_back, text='Batch number: ', background=self.back_colour, font=("Courier", 14)).place(
            relx=0.1, rely=0.3, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.current_batch, relief=SUNKEN, font=('Arial', 18, 'bold'),
                  width=10).place(relx=0.25, rely=0.3, anchor='w')
        ttk.Label(self.canvas_back, text='Probe type: ', background=self.back_colour, font=("Courier", 14)).place(
            relx=0.1, rely=0.45, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.probe_type, relief=SUNKEN, font=('Arial', 18, 'bold'),
                  width=12).place(relx=0.25, rely=0.45, anchor='w')
        ttk.Label(self.canvas_back, text='Connected to: ', background=self.back_colour, font=("Courier", 14)).place(
            relx=0.73, rely=0.2, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.device_details, relief=SUNKEN,
                  width=30).place(relx=0.7, rely=0.25, anchor='w')
        self.reset_ana = Button(self.canvas_back, text="Reset Analyser", background="#FF731D", font=('Arial', 12),
               command=self.reset_analyser)
        self.reset_ana.place(relx=0.85, rely=0.23)
        ttk.Label(self.canvas_back, textvariable=self.odm_details, relief=SUNKEN,
                  width=30).place(relx=0.7, rely=0.30, anchor='w')
        ttk.Label(self.canvas_back, text="Data from ODM", background=self.back_colour, font=("Courier", 14)).place(
            relx=0.7, rely=0.42, anchor="w")
        ttk.Label(self.canvas_back, text="SD", background=self.back_colour, font=("Courier", 14)).place(relx=0.70,
                                                                                                        rely=0.46,
                                                                                                        anchor="w")
        ttk.Label(self.canvas_back, text="FTc", background=self.back_colour, font=("Courier", 14)).place(relx=0.77,
                                                                                                         rely=0.46,
                                                                                                         anchor="w")
        ttk.Label(self.canvas_back, text="PV", background=self.back_colour, font=("Courier", 14)).place(relx=0.85,
                                                                                                        rely=0.46,
                                                                                                        anchor="w")
        ttk.Label(self.canvas_back, text="Serial Number of Probe Inserted",
                  background=self.back_colour, font=('Courier', 14)).place(relx=0.68, rely=0.58)
        ttk.Label(self.canvas_back, textvariable=self.show_serial_number, relief=SUNKEN,
                  font=('Arial', 14, 'bold'), width=23).place(relx=0.7, rely=0.62)
        ttk.Label(self.canvas_back, textvariable=self.SD_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.69, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.FTc_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.76, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.PV_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.84, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, text='Program/Test Status: ',
                  background=self.back_colour, font=("Courier", 14)).place(relx=0.45, rely=0.32)
        ttk.Label(self.canvas_back, text='Probes Passed: ', background=self.back_colour, font=("Courier", 14)).place(
            relx=0.1, rely=0.6, anchor='w')
        ttk.Label(self.canvas_back, text="Reflection Test", font="bold",
                  background=self.back_colour).place(relx=0.1, rely=0.72)
        ttk.Label(self.canvas_back, textvariable=self.reflection, font=("Courier", 14), relief=SUNKEN,
                  width=20).place(relx=0.25, rely=0.72)
        ttk.Label(self.canvas_back, textvariable=self.probes_passed, relief=SUNKEN, font=('Arial', 18, 'bold'),
                  width=10).place(relx=0.25, rely=0.6, anchor='w')
        ttk.Label(self.canvas_back, text='Probes to test: ', background=self.back_colour, font=("Courier", 14)).place(
            relx=0.7, rely=0.75, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.left_to_test, relief=SUNKEN, font=('Arial', 18, 'bold'),
                  width=8).place(relx=0.85, rely=0.75, anchor='w')
        ttk.Label(self.canvas_back, text='Action: ', background=self.back_colour,
                  font=("Courier", 14)).place(relx=0.1, rely=0.83)

        #################################################################
        # Show interaction buttons                                      #
        #################################################################
        self.ssp_btn = Button(self.canvas_back, text='  Suspend Batch  ',
                              font=("Courier", 14, "bold"), background="#EF5B0C",
                              highlightthickness=0, command=self.suspnd_btn_clicked)
        self.ssp_btn.place(relx=0.85, rely=0.9, anchor=CENTER)
        self.retest = Button(self.canvas_back, text=" Re-test Failed Probe", font=("Courier", 15, "bold"),
                             background="#A8E890", command=self.retest_probe)
        self.retest.place(relx=0.5, rely=0.825)

        self.session_on_going = True
        self.analyser_serial = None
        self.probes_passed.set(0)

        #########################################################
        # Complete button detected pressed                      #
        #########################################################

    def retest_probe(self):
        self.session_on_going = False
        self.session_complete = False
        self.canvas_back.destroy()
        RT.sort_test_entry()
        self.control.show_frame(RT.RetestProbe)

    def reset_analyser(self):
        if ZND.reset_vna():
            self.reset_ana.config(background="#82CD47")

    def suspnd_btn_clicked(self):
        self.session_on_going = False
        if tm.askyesno(title="Batch Info", message="    Suspend Batch ?         "):
            probe_data = P.Probes(self.probe_type.get(), self.current_batch.get(), self.probes_passed.get(),
                                  self.left_to_test.get())
            DS.write_probe_data(probe_data)
            BM.SuspendBatch(self.current_batch.get())
            self.canvas_back.destroy()
            if not self.test:
                self.to_sessions()
        else:
            self.session_on_going = True
            self.wait_for_probe()
        ###########################################################
        # Retrieve amount of probes left to test                  #
        ###########################################################

    def get_probes_left(self):
        if int(self.left_to_test.get()) < 1:
            return True
        else:
            return False
        ###########################################################
        # Set the number rof probes left to test to the display   #
        ###########################################################

    def set_probes_left(self, qty):
        self.left_to_test.set(qty)
        ############################################################
        # Reset all display and data for next probe to be tested   #
        ############################################################

    def set_test(self):
        self.test = True

    def to_sessions(self):
        self.control.show_frame(SE.SessionSelectWindow)

    def reset(self):
        self.display_layout()
        self.session_on_going = True
        current_user = DS.get_username()
        self.user_admin = DS.user_admin_status()
        # self.user_admin = DS.get_user_data()['Over_rite']
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        if DS.get_current_batch() == "000":
            self.text_area.insert('1.0', current_user.title())
            self.text_area.insert('3.0', '\nPlease continue testing batch ')
        else:
            self.text_area.insert('1.0', current_user.title())
            self.text_area.insert('2.0', '\nPlease continue testing batch ')
            self.text_area.insert('2.30', DS.get_current_batch())
        self.left_to_test.set(DS.get_probes_left_to_test())
        self.probes_passed.set(DS.get_probe_data()['Passed'])
        self.probe_type.set(DS.get_current_probe_type())
        self.current_batch.set(DS.get_current_batch())
        self.current_user.set(DS.get_username())
        # self.RLLimit = -1
        self.canvas_back.pack()
        self.reflection.set("--->")
        self.show_serial_number.set("      ---")

        #############################################################
        # Display to screen the probe over-write status             #
        #############################################################
    def set_reprogram_status(self):
        if self.user_admin and self.check_overwrite():
            self.display_message(warning_text["overrite on"])
        else:
            self.display_message(warning_text["overrite off"])

        ##############################################################
        # Check probe interface for a probe is inserted              #
        ##############################################################
    def check_probe_present(self):
        if not PM.ProbePresent():
            if self.session_on_going:
                ttk.Label(self.canvas_back, textvariable=self.action, background='yellow',
                          relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
            return False
        else:
            return True

    def check_overwrite(self):
        return DS.get_user_data()['Over_rite']

        ##############################################
        # Show if the external devices are connected #
        ##############################################
    def set_display(self):
        check = False
        odm = "ODM not running"
        device = "Not connected to analyser"
        vna = ZND.get_znd_obj().port
        if vna == DS.get_devices()['Analyser']:
            device = " NanoNVA "
            check = True
        self.device_details.set(device)
        if DS.get_devices()['odm_active']:
            try:
                ODM.check_port_open()
                port_data = ODM.ReadSerialODM()
            except IOError:
                port_data = "000"
            else:
                if len(port_data) > 5:
                    odm = " ODM Monitor "
                    check = True
                    ODM.close_port()
        self.odm_details.set(odm)
        ZND.flush_analyser_port()
        ZND.set_vna_controls()
        return check

        ###############################################################
        # Start off mai testing sequence                              #
        ###############################################################
    def refresh_window(self):
        self.reset()
        self.set_display()
        self.info_canvas = None
        self.set_reprogram_status()
        self.show_gray_light()
        self.wait_for_probe()

        ################################################################
        #                     Main loop                                #
        ################################################################
    def wait_for_probe(self):
        # self.test = False
        if self.get_probes_left():
            self.session_on_going = False
            self.session_complete = True
        while self.session_on_going:
            # if self.get_probes_left():
            #     self.session_on_going = False
            #     self.session_complete = True
            self.show_gray_light()
            Tk.update(self)
            if self.check_probe_present():
                if not self.program_blank_probe():
                    #################################
                    # Check for programmed probe    #
                    # ask if admin is true, is so   #
                    # reprogram and test probe      #
                    #################################
                    if self.over_write_probe(DS.get_current_batch(), DS.get_current_probe_type()):
                        self.remove_probe()
                    self.set_reprogram_status()
                    if self.test:
                        return True
            ##############################
            # Go to fault finding window #
            ##############################
        if self.session_complete and not self.check_probe_present():
            if self.get_probes_left():
                P.probe_canvas(self, f"{warning_text['7']} {warning_text['8']}", False)
                time.sleep(2)
                P.text_destroy(self)
                self.complete_batch()

    def do_test_and_programme(self, current_batch, probe_type):
        self.info_canvas = None
        found, sn = detect_recorded_probe()
        if not found and not self.check_overwrite():
            self.show_serial_number.set(sn)
            P.probe_canvas(self, f"Probe not recognised\nCurrent batch {current_batch}", True)
            return False
        if current_batch != found and not self.check_overwrite():
            P.probe_canvas(self, f"Batch number {found} - error\n\ndoes not match current {current_batch}", True)
            if not self.test:
                return False
        failure = False
        ##############################################
        # Perform test and programing probe, if the  #
        # testing from the analyser fails the serial #
        # number has 'Fail' inserted into it. If the #
        # programming of the probe fails, the probe  #
        # is not given a serial number.              #
        ##############################################
        self.show_blue_meaasge()
        self.show_amber_image()
        Tk.update(self)
        ##############################################
        # Get number of failures so far during this  #
        # batch number.                              #
        ##############################################
        non_human = DS.get_animal_probe()
        ##############################################
        # Do the analyser testing of the probe.      #
        ##############################################
        result, marker, odm_data = self.test_probe()
        #################################################
        # If the analyser passes the probe, the probe   #
        # is given a serial number, or a fault text.    #
        # Check to see if the probe type is non-human   #
        #################################################

        if not non_human:
            serial_num = self.program_probe(probe_type, result)
        else:
            serial_num = "Animal Probe"
        ################################################
        # If the probe cannot be given a serial number #
        ################################################
        if not serial_num or not result:
            failure = True
            serial_num = "PCB failure"
        ########################################
        # Show serial number to screen         #
        ########################################
        self.show_serial_number.set(serial_num)
        ###########################################
        # Update number of probes being processed #
        ###########################################
        # if not self.check_overwrite():
        probes_passed = self.probes_passed.get() + 1
        self.probes_passed.set(probes_passed)
        probes_left = self.left_to_test.get() - 1
        if probes_left < 0:
            self.left_to_test.set(0)
        self.left_to_test.set(probes_left)

        Tk.update(self)
        #################################################
        # If the probe fails the analyser test, the     #
        # probe is failed and may be re-worked.         #
        #################################################
        if not result:
            failure = True
            ##################################################
            # Ask user if they want to fault find the failed #
            # probe. If not record probe results.            #
            ##################################################
            P.probe_canvas(self, f"{warning_text['13']} {warning_text['14']}", True)
            if self.info_canvas:
                self.session_on_going = False
                P.text_destroy(self)
                self.ff_window()
            if not self.info_canvas:
                self.session_on_going = True
                P.text_destroy(self)
        if result and not failure:
            self.show_green_image()
        else:
            self.show_red_light()
        Tk.update(self)
        #########################################################
        # Whatever the probe test outcome, the results are sent #
        # to the batch number file in-progress.                 #
        #########################################################
        if self.update_results(result, serial_num, odm_data, current_batch, marker):
            self.save_probe_data(current_batch, failure)
        self.remove_probe()
        self.show_gray_light()
        return failure

    def save_probe_data(self, batch, failure):
        failed = DS.get_probe_data()['Failures']
        if failure:
            failed += 1
        probe_data = P.Probes(self.probe_type.get(),
                              batch, int(self.probes_passed.get()), int(self.left_to_test.get()), failed=failed)
        DS.write_probe_data(probe_data)

    def remove_probe(self):
        P.probe_canvas(self, "Please remove probe.", False)
        while PM.ProbePresent():
            pass
        P.text_destroy(self)
        self.show_serial_number.set("      ---")

    def non_human_probe(self):
        return DS.get_user_data()['Non_Human']

    def program_blank_probe(self):
        ###############################################################
        # Program a blank probe inserted into probe interface         #
        ###############################################################
        if not probe_programmed():
            self.set_reprogram_status()
            self.action.set(warning_text["1"])
            return self.do_test_and_programme(self.current_batch.get(), self.probe_type.get())
        else:
            return False

        ###############################################
        # Display any messages to the user info box   #
        ###############################################

    def display_message(self, message):
        if self.session_on_going:
            self.text_area.config(state=NORMAL)
            self.text_area.delete('3.0', 'end')
            self.text_area.insert('3.0', "\n\n" + message)
            self.text_area.config(state=DISABLED)

        #################################################
        # Test the inserted probe                       #
        #################################################

    def program_probe(self, probe_type, test):
        programmed = True
        fail_message = "Chip fault"
        self.action.set(warning_text["9"])
        serial_number = PM.ProgramProbe(probe_type, test)
        if not serial_number:
            ttk.Label(self.canvas_back, textvariable=self.action, background='orange',
                      relief=GROOVE, font=("Courier", 16)).place(relx=0.25, rely=0.83)
            self.action.set(warning_text["13"])
            self.show_red_light()
            P.probe_canvas(self, f"{warning_text['13']} {warning_text['12']} ", False)
            time.sleep(1.8)
            P.text_destroy(self)
            programmed = False
            Tk.update(self)
        if programmed:
            self.action.set(warning_text['15'])
            Tk.update(self)
            return serial_number
        else:
            return fail_message

        ##########################################################
        # Over-write a programmed probe detected                 #
        ##########################################################

    def over_write_probe(self, current_batch, probe_type):
        # print(f"Before current user {self.current_user.get()} - user admin {self.user_admin} - {self.check_overwrite()}")
        self.info_canvas = None
        over_write = False
        found, serial_number = detect_recorded_probe()
        probe_type_ = RT.get_probe_type(serial_number[:3])
        self.show_serial_number.set(serial_number)
        if found == "Not Found":
            P.probe_canvas(self, f"Location of {probe_type_} not found.", False)
            time.sleep(2)
            P.text_destroy(self)
        else:
            P.probe_canvas(self, f"This probe is from {probe_type_}\n \nbatch number {found}", False)
            time.sleep(2)
            P.text_destroy(self)

        if self.check_overwrite():
            ###############################################
            # ask for user input to reprogramme the probe #
            ###############################################
            if tm.askyesno(title=warning_text["2"], message=warning_text['3']):
                over_write = True
                if not self.do_test_and_programme(current_batch, probe_type):
                    self.action.set(warning_text["15"])
                else:
                    self.action.set(warning_text["13"])
            reset_rewrite = P.Users(self.current_user.get(), self.user_admin, over_right=False)
            DS.write_user_data(reset_rewrite)
            # print(f"After current user {self.current_user.get()} - user admin {self.user_admin} - {self.check_overwrite()}")
            # self.remove_probe()
        else:
            P.probe_canvas(self, warning_text["14"], True)
            if self.info_canvas:
                self.session_on_going = False
                P.text_destroy(self)
                if not self.test:
                    self.ff_window()
            else:
                self.session_on_going = True
                P.text_destroy(self)
                self.remove_probe()
        return over_write

        ################################
        # Show Fault find window       #
        ################################

    def ff_window(self):
        probe_data = P.Probes(self.probe_type.get(), self.current_batch.get(), self.probes_passed.get(),
                              self.left_to_test.get())
        DS.write_probe_data(probe_data)
        self.session_on_going = False
        self.canvas_back.destroy()
        if not self.test:
            self.control.show_frame(FF.FaultFindWindow)

        ##################################
        # Show probe state to user       #
        ##################################

    def show_green_image(self):
        self.canvas_back.create_image(self.cent_x, self.cent_y, image=self.greenlight)
        self.canvas_back.pack()
        ttk.Label(self.canvas_back, textvariable=self.action, background='#1fff1f',
                  relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
        Tk.update(self)

    def show_amber_image(self):
        self.canvas_back.create_image(self.cent_x, self.cent_y, image=self.amberlight)
        self.canvas_back.pack()
        ttk.Label(self.canvas_back, textvariable=self.action, background='#FF7F3F',
                  relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
        Tk.update(self)

    def show_red_light(self):
        self.canvas_back.create_image(self.cent_x, self.cent_y, image=self.redlight)
        self.canvas_back.pack()
        self.display_message(warning_text["13"])
        ttk.Label(self.canvas_back, textvariable=self.action, background='#FF7F3F',
                  relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
        Tk.update(self)

    def show_gray_light(self):
        self.canvas_back.create_image(self.cent_x, self.cent_y, image=self.greylight)
        self.canvas_back.pack()
        self.action.set(warning_text["6"])
        ttk.Label(self.canvas_back, textvariable=self.action, background='yellow',
                  relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
        Tk.update(self)

    def show_blue_meaasge(self):
        self.action.set('Testing probe...')
        ttk.Label(self.canvas_back, textvariable=self.action, background='#548CFF',
                  relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
        Tk.update(self)

    def show_green_text(self):
        ttk.Label(self.canvas_back, textvariable=self.action, background='#1fff1f',
                  width=25, relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
        Tk.update(self)

        #######################
        # Test the probe      #
        #######################

    def test_probe(self):
        global analyser
        analyser = False
        pass_analyser = False
        pass_reflection = False
        self.action.set(warning_text["10"])  # Testing probe message
        odm_data = self.update_odm_data()  # Returns monitor data
        ###################################################
        # Probe passed                                    #
        ###################################################
        marker_data = perform_probe_test()
        if analyser:
            pass_analyser = True
            self.action.set(warning_text["17"]) # Passed analyser message
            Tk.update(self)
        if self.do_reflection_test():
            pass_reflection = True
            self.action.set(warning_text["18"]) # Passed reflection message
            Tk.update(self)
        if pass_analyser and pass_reflection:
            pass_tests = True
        else:
            self.action.set(warning_text["13"]) # Failed probe message
            self.show_red_light()
            pass_tests = False
        Tk.update(self)
        return pass_tests, marker_data, odm_data

    ################################
    # Collect the ODM monitor data #
    ################################

    def update_odm_data(self):
        if DS.get_devices()['odm_active']:
            serial_results = ODM.ReadSerialODM()
            if not serial_results:
                serial_results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            self.SD_data.set(serial_results[5])
            self.FTc_data.set(serial_results[6])
            self.PV_data.set(serial_results[9])

            return serial_results
        else:
            return "Not used"

        ######################################
        # Update the results to the CSV file #
        ######################################

    def update_results(self, results, snum, odm_data, batch, marker):
        data_list_to_file = []
        odm_to_file = "ODM not used"
        if DS.get_devices()['odm_active']:
            odm_to_file = str(odm_data[9])
        data_list_to_file.append(batch)  # by pass the batch number column
        data_list_to_file.append(snum)  # insert serial number
        data_list_to_file.append(self.probe_type.get())
        data_list_to_file.append(self.left_to_test.get())
        data_list_to_file.append(self.current_user.get())  # insert the logged in user
        data_list_to_file.append(results)  # results of reflection test
        data_list_to_file.append(marker)  # results of analyser data
        data_list_to_file.append(odm_to_file)
        return BM.saveProbeInfoToCSVFile(data_list_to_file, batch)

    def complete_batch(self):
        current_batch = DS.get_current_batch()
        BM.competed_text(DS.get_username(), DS.get_current_probe_type(),
                         current_batch, DS.get_probes_failed(), self.probes_passed.get())
        BM.CompleteBatch(current_batch)
        self.canvas_back.destroy()
        self.to_sessions_window()

    def yes_answer(self):
        self.info_canvas = True
        P.text_destroy(self)

    def no_answer(self):
        self.info_canvas = False
        P.text_destroy(self)

    def do_reflection_test(self):
        return True

    def to_sessions_window(self):
        if not self.test:
            self.control.show_frame(SE.SessionSelectWindow)

    def set_test_flag(self):
        self.test = True
