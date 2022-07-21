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
import codecs
from time import gmtime, strftime
import BatchManager
import InstrumentManager
from ProbeManager import ProbeManager
from ProbeManager import Probes as P
import NanoZND
import ODMPlus
import Sessions as SE
import FaultFinder as FF
import Datastore

# create instances
IM = InstrumentManager.InstrumentationManager()
BM = BatchManager.BatchManager()
PM = ProbeManager()
ZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()
DS = Datastore.Data_Store()

# define global variables
PTT_Version = 'Deltex Medical : XXXX-XXXX Probe Test Tool V1'
w = 800  # window width
h = 600  # window height
LARGE_FONT = ("Verdana", 14)
BTN_WIDTH = 30


# Assign as a command when I want to disable a button (double click prevention)
def ignore():
    return 'break'


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
        self.SD_data = IntVar()
        self.FTc_data = IntVar()
        self.PV_data = IntVar()
        self.user_admin = False
        self.probes_passed.set(0)
        self.lower_limit = 1.14
        self.upper_limit = 1.24
        ###############################################################
        # import and set up images for the screen                     #
        ###############################################################
        self.greenlight = (PhotoImage(file="GREEN.png"))
        self.amberlight = (PhotoImage(file="AMBER.png"))
        self.redlight = (PhotoImage(file="RED.png"))
        self.greylight = (PhotoImage(file="GREY.png"))
        self.complete_btn = (PhotoImage(file="completetesting.gif"))
        self.suspend_btn = (PhotoImage(file="suspend.gif"))
        self.back_colour = "#A6D1E6"

    def display_layout(self):
        #################################################################
        # Display main screen layout                                    #
        #################################################################
        self.text_area = tk.Text(self.canvas_back, height=5, width=40)
        self.text_area.place(x=40, y=70)
        ttk.Label(self.canvas_back, text="Deltex", background=self.back_colour, foreground="#003865",
                  font=('Helvetica', 24, 'bold'), width=12).place(x=850, y=25)
        ttk.Label(self.canvas_back, text="medical", background=self.back_colour, foreground="#A2B5BB",
                  font=('Helvetica', 14)).place(x=850, y=57)
        self.text_area.delete('1.0', 'end')
        ttk.Label(self.canvas_back, text='Batch number: ',background=self.back_colour).place(
            relx=0.1, rely=0.3, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.current_batch, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.3, rely=0.3, anchor='w')
        ttk.Label(self.canvas_back, text='Probe type: ',background=self.back_colour).place(
            relx=0.1, rely=0.45, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.probe_type, relief=SUNKEN, font="bold",
                  width=12).place(relx=0.3, rely=0.45, anchor='w')
        ttk.Label(self.canvas_back, text='Connected to: ',background=self.back_colour).place(
            relx=0.73, rely=0.2, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.device_details, relief=SUNKEN,
                  width=30).place(relx=0.7, rely=0.25, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.odm_details, relief=SUNKEN,
                  width=30).place(relx=0.7, rely=0.30, anchor='w')
        ttk.Label(self.canvas_back, text="Data from ODM",background=self.back_colour).place(
            relx=0.7, rely=0.42, anchor="w")
        ttk.Label(self.canvas_back, text="SD",background=self.back_colour).place(relx=0.70, rely=0.46, anchor="w")
        ttk.Label(self.canvas_back, text="FTc",background=self.back_colour).place(relx=0.77, rely=0.46, anchor="w")
        ttk.Label(self.canvas_back, text="PV",background=self.back_colour).place(relx=0.85, rely=0.46, anchor="w")
        ttk.Label(self.canvas_back, textvariable=self.SD_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.69, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.FTc_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.76, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.PV_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.84, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, text='Program/Test Status: ',background=self.back_colour).place(relx=0.1,
                                                            rely=0.58, anchor='w')
        self.status_image = ttk.Label(self.canvas_back, image=self.greylight)
        self.status_image.place(relx=0.53, rely=0.56, anchor=CENTER)
        ttk.Label(self.canvas_back, text='Probes Passed: ',background=self.back_colour).place(
            relx=0.1, rely=0.75, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.probes_passed, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.28, rely=0.75, anchor='w')
        ttk.Label(self, text='Probes to test: ',background=self.back_colour).place(
            relx=0.7, rely=0.75, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.left_to_test, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.83, rely=0.75, anchor='w')
        ttk.Label(self.canvas_back, text='Action: ',background=self.back_colour).place(relx=0.1, rely=0.9, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.action, background='yellow',
                  width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')
        #################################################################
        # Show interaction buttons                                      #
        #################################################################
        ttk.Button(self.canvas_back, text='Complete Session', image=self.complete_btn, command=lambda:
        self.cmplt_btn_clicked()).place(relx=0.68, rely=0.9, anchor=CENTER)
        self.ssp_btn = ttk.Button(self.canvas_back, text='Suspend Session', image=self.suspend_btn, command=lambda:
        self.suspnd_btn_clicked(self.control))
        self.ssp_btn.place(relx=0.85, rely=0.9, anchor=CENTER)
        self.session_on_going = True
        self.analyser_serial = None
        self.probes_passed.set(0)

        #########################################################
        # Complete button detected pressed                      #
        #########################################################

    def cmplt_btn_clicked(self):
        self.session_complete = True
        self.session_on_going = False
        if self.get_probes_left():
            current_batch = DS.get_current_batch()
            BM.CompleteBatch(current_batch)
            self.control.show_frame(SE.SessionSelectWindow)
        ###########################################################
        # Suspend button detected pressed                         #
        ###########################################################

    def suspnd_btn_clicked(self, controller):
        self.session_complete = False
        probe_data = P(self.probe_type.get(),self.current_batch.get(),self.probes_passed.get(),self.left_to_test.get())
        DS.write_probe_data(probe_data)
        BM.SuspendBatch(self.current_batch.get())
        self.session_on_going = False
        self.canvas_back.destroy()
        controller.show_frame(SE.SessionSelectWindow)
        ###########################################################
        # Retrieve amount of probes left to test                  #
        ###########################################################

    def get_probes_left(self):
        print(f"Probes left {self.left_to_test.get()}")
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

    def reset(self):
        self.canvas_back = Canvas(bg=self.back_colour,width=980,height=630)
        self.canvas_back.place(x=10, y=10)
        self.display_layout()
        time_now = strftime("%H:%M:%p", gmtime())
        if "AM" in time_now:
            self.text_area.insert('1.0', 'Good Morning ')
        else:
            self.text_area.insert('1.0', 'Good Afternoon ')
        self.display_layout()
        self.session_on_going = True
        current_user = DS.get_username()
        # user = Probe()
        self.user_admin = DS.get_user_data()['Over_rite']
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        current_batch = DS.get_current_batch()
        if current_batch == "000":
            print(f"Current batch is {current_batch}")
            self.text_area.insert('1.0', current_user)
            self.text_area.insert('2.0', '\nPlease continue testing batch ')
        else:
            self.text_area.insert('1.0', current_user)
            self.text_area.insert('2.0', '\nPlease continue testing batch ')
            self.text_area.insert('2.30', current_batch)
        self.left_to_test.set(DS.get_probes_left_to_test())  ## left to test should be from where you left off.
        self.probes_passed.set(DS.get_probe_data()['Passed'])
        self.probe_type.set(DS.get_current_probe_type())
        self.current_batch.set(DS.get_current_batch())
        self.current_user.set(current_user)
        self.RLLimit = -1  # pass criteria for return loss measurement
        self.programmed = False
        self.status_image.configure(image=self.greylight)
        ttk.Label(self.canvas_back, textvariable=self.action, background='yellow',
                  width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')

        ##############################
        # Collect analyser port data #
        ##############################
        ZND.flush_analyser_port()
        ZND.set_vna_controls()
        self.set_display()
        self.warning_text = {
            "overrite on": "Probe re-programming enabled.",
            "overrite off": "Probe re-programming disabled",
            "1": "Probe connected",
            "2": "Programmed Probe Detected",
            "3": "This probe is already programmed.\nDo you wish to re-program and test?",
            "4": "Information",
            "5": "Probe can't be re-programmed\n Do you wish to fault find the probe?",
            "6": "Connect New Probe",
            "7": "Batch Complete",
            "8": "Please press 'Complete Session' button.",
            "9": "Programming probe...",
            "10": "Testing probe...'",
            "11": "Programming error...",
            "12": "Unable to program\nPlease check probe chip. ",
            "13": "Probe Failed.",
            "14": "Do you wish to fault find this probe?",
            "15": "Probe passed",
            "16": "\nPlease remove probe..."
        }

        #############################################################
        # Display to screen the probe over-write status             #
        #############################################################

    def set_reprogram_status(self):
        if self.user_admin:
            self.display_message(self.warning_text["overrite on"])
        else:
            self.display_message(self.warning_text["overrite off"])

        ##############################################################
        # Check probe interface for a probe is inserted              #
        ##############################################################

    def check_probe_present(self):
        if not PM.ProbePresent() and self.session_on_going:
            ttk.Label(self.canvas_back, textvariable=self.action, background='yellow',
                      width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')
            return True
        else:
            return False

        ##############################################
        # Show if the external devices are connected #
        ##############################################

    def set_display(self):
        check = False
        odm = "ODM not running"
        device = "Not connected to analyser"
        if ZND.get_analyser_port_number(DS.get_devices()['Analyser']):
            device = " NanoNVA "
            check = True
        self.device_details.set(device)
        ODM.check_port_open()
        port_obj = ODM.get_port_obj()
        port = DS.get_devices()['ODM']
        if port_obj.port == port:
            odm = " ODM Monitor "
            check = True
        self.odm_details.set(odm)
        ODM.close_port()
        return check

        ###############################################################
        # Start off mai testing sequence                              #
        ###############################################################

    def refresh_window(self):
        self.reset()
        self.set_reprogram_status()

        ################################################################
        #                     Main loop                                #
        ################################################################
        while self.session_on_going:
            if self.left_to_test.get() == 0:
                self.session_on_going = False
                self.session_complete = True
            ttk.Label(self.canvas_back, textvariable=self.action, background='yellow',
                      width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')
            self.action.set(self.warning_text["6"])
            Tk.update(self)
            if not self.check_probe_present():
                if not self.program_blank_probe():
                #################################
                # Check for programmed probe    #
                # ask if admin is true, is so   #
                # reprogram and test probe      #
                #################################
                    self.over_write_probe()

            ##############################
            # Go to fault finding window #
            ##############################

        if self.session_complete:
            BM.CompleteBatch(BM.current_batch)
            tm.showinfo(title=self.warning_text["7"], message=self.warning_text["8"])

        ##############################
        # Perform program and test   #
        ##############################

    def do_program_and_test(self, batch):
        # Program and test probe #
        print("************")
        self.programmed = False
        self.action.set(self.warning_text["9"])
        snum = self.program_probe(DS.get_current_probe_type())
        results = self.test_probe()
        odm_data = self.update_odm_data()
        # Marker 3 data from the NanoVNA device #
        self.action.set(self.warning_text["10"])
        # If serial number is good, update results #
        if not results:
            snum = f"{snum}f"
        if len(snum) > 5:
            self.update_results(results, snum, odm_data, batch)
        return snum

        ###############################################################
        # Program a blank probe inserted into probe interface         #
        ###############################################################

    def program_blank_probe(self):
        if not PM.ProbeIsProgrammed() and self.session_on_going:
            self.set_reprogram_status()
            # PM.test_chip()
            self.action.set(self.warning_text["1"])
            self.show_green_text()
            self.update_odm_data()
            return self.do_program_and_test(self.current_batch.get())
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

        ############################
        # Program the probe        #
        ############################

    def program_probe(self, probe_type):
        self.show_amber_image()
        serialNumber = PM.ProgramProbe(probe_type)
        if not serialNumber:
            tm.showerror(self.warning_text["11"],
                         self.warning_text["12"])
            self.action.set(self.warning_text["13"])
            self.status_image.configure(image=self.redlight)
            ttk.Label(self.canvas_back, textvariable=self.action, background='orange',
                      width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')
            Tk.update(self)
            snum = False
        else:
            snum = str(codecs.decode(serialNumber, "hex"), 'utf-8')[:16]
            self.programmed = True
        return snum

        ##########################################################
        # Over-write a programmed probe detected                 #
        ##########################################################

    def over_write_probe(self):

        if self.session_on_going:
            if PM.ProbeIsProgrammed() and DS.get_user_data()['Over_rite']:
                    # ask for user input to reprogramme the probe #
                if tm.askyesno(self.warning_text["2"],
                                    self.warning_text["3"]):
                    self.do_program_and_test(self.current_batch.get())
                    self.set_reprogram_status()
                else:
                    tm.showinfo(title="Probe Inserted",message="Please remove inserted probe.")
                    return False
            else:
                    # If user admin is false, user can't reprogram the probe ask user to fault find #
                if tm.askyesno(title=self.warning_text["4"], message=self.warning_text["5"]):
                    self.session_on_going = False
                    self.ff_window()
                    self.refresh_window()
                else:
                    tm.showinfo(title="Probe Inserted", message="Please remove the inserted probe.")

                self.set_reprogram_status()
                # if PM.ZND.get_marker_values()[0] < self.RLLimit and PM.ZND.get_marker_values()[1] < self.RLLimit:
                Tk.update(self)

        ####################################
        # Redirect to fault finding window #
        ####################################

    def call_for_fault_find(self):
        self.status_image.configure(image=self.redlight)
        self.action.set(self.warning_text["13"])
        ask = tm.askyesno(title=self.warning_text["13"], message=self.warning_text["14"])
        if ask:
            self.ff_window()

        ################################
        # Show Fault find window       #
        ################################

    def ff_window(self):
        probe_data = P(self.probe_type.get(),self.current_batch.get(),self.probes_passed.get(),self.left_to_test.get())
        DS.write_probe_data(probe_data)
        self.canvas_back.destroy()
        self.control.show_frame(FF.FaultFindWindow)

        ##################################
        # Show probe state to user       #
        ##################################

    def show_green_image(self):
        self.status_image.configure(image=self.greenlight)
        ttk.Label(self.canvas_back, textvariable=self.action, background='#1fff1f',
                  width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')
        Tk.update(self)

    def show_amber_image(self):
        self.status_image.configure(image=self.amberlight)
        ttk.Label(self.canvas_back, textvariable=self.action, background='#FF7F3F',
                  width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')
        Tk.update(self)

    def show_red_light(self):
        self.display_message(self.warning_text["13"])
        self.status_image.configure(image=self.redlight)
        ttk.Label(self.canvas_back, textvariable=self.action, background='#FF7F3F',
                  width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')
        Tk.update(self)

    def show_gray_light(self):
        self.status_image.config(image=self.greylight)
        ttk.Label(self.canvas_back, textvariable=self.action, background='yellow',
                  width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')
        Tk.update(self)

    def show_blue_meaasge(self):
        self.action.set('Testing probe...')
        ttk.Label(self.canvas_back, textvariable=self.action, background='#548CFF',
                  width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')
        Tk.update(self)

    def show_green_text(self):
        ttk.Label(self.canvas_back, textvariable=self.action, background='#1fff1f',
                  width=40, relief=GROOVE).place(relx=0.3, rely=0.9, anchor='w')
        Tk.update(self)

        #######################
        # Test the probe      #
        #######################

    def test_probe(self):
        canvas_text = None
        self.show_blue_meaasge()
        results = False
        results = PM.TestProbe()
        if results:
            marker_data = TestProgramWindow.get_marker_data(self)
            # print(f"get marker data {marker_data}")
            if self.lower_limit < marker_data < self.upper_limit:
                self.show_green_image()
                canvas_text = Canvas(bg="#eae9e9", width=300, height=100)
                canvas_text.place(x=400, y=300)
                Label(canvas_text, text=self.warning_text["15"] + self.warning_text["16"], font=("Courier", 12)).place(
                    x=150, y=40, anchor=N)
            else:
                self.show_red_light()
                canvas_text = Canvas(bg="#eae9e9", width=300, height=100)
                canvas_text.place(x=400, y=280)
                self.call_for_fault_find()
                Label(canvas_text, text=self.warning_text["16"], font=("Courier", 12)).place(x=150, y=40, anchor=N)
        while PM.ProbePresent():
            pass

        self.show_gray_light()
        canvas_text.destroy()
        return results

        #############################
        # Returns cable length data #
        #############################

    def get_marker_data(self):
        ZND.flush_analyser_port()
        return ZND.tdr()

        ################################
        # Collect the ODM monitor data #
        ################################

    def update_odm_data(self):

        serial_results = ODM.ReadSerialODM()
        if serial_results == []:
            serial_results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.SD_data.set(serial_results[5])
        self.FTc_data.set(serial_results[6])
        self.PV_data.set(serial_results[9])

        return serial_results

        ######################################
        # Update the results to the CSV file #
        ######################################

    def update_results(self, results, snum, odm_data, batch):
        data_list_to_file = []
        odm_results = odm_data
        if odm_results is None:
            odm_to_file = "ODM not used"
        else:
            odm_to_file = str(odm_results[9])
        results_to_file = str(results)
        probes_left = self.left_to_test.get()
        probes_passed = self.probes_passed.get()
        self.left_to_test.set(probes_left - 1)
        self.probes_passed.set(probes_passed + 1)
        data_list_to_file.append(" ")  # by pass the batch number column
        data_list_to_file.append(snum)  # insert serial number
        data_list_to_file.append(self.probe_type.get())  # insert probe type
        data_list_to_file.append(" ")
        data_list_to_file.append(self.current_user.get())  # insert the logged in user
        data_list_to_file.append(odm_to_file)  # insert ODM data
        data_list_to_file.append(results_to_file)
        BM.saveProbeInfoToCSVFile(data_list_to_file, batch)  # save to file
