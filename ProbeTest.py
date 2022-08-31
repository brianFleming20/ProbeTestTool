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
import BatchManager
from ProbeManager import ProbeManager
from ProbeInterface import PRI
import NanoZND
import ODMPlus
import Sessions
import FaultFinder
import Datastore
import sys
import Ports
import time

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

# define global variables
PTT_Version = 'Deltex Medical : XXXX-XXXX Probe Test Tool V1'
w = 800  # window width
h = 600  # window height
LARGE_FONT = ("Verdana", 14)
BTN_WIDTH = 30


# Assign as a command when I want to disable a button (double click prevention)
def ignore():
    return 'break'


LOWER_LIMIT = 0.9
UPPER_LIMIT = 1.5


def probe_canvas(self, message, btn):
    self.canvas_text = Canvas(bg="#eae9e9", width=350, height=180)
    self.canvas_text.place(x=self.cent_x - 150, y=self.cent_y - 20)
    Label(self.canvas_text, text=message, font=("Courier", 12)).place(
        x=50, y=20)
    btn1 = Button(self.canvas_text, text="Continue", command=self.yes_answer, width=10, height=2)
    btn2 = Button(self.canvas_text, text="Cancel", command=self.no_answer, width=10, height=2)
    Tk.update(self)
    while btn and self.info_canvas is None:
        btn1.place(x=90, y=120)
        btn2.place(x=190, y=120)
        Tk.update(self)


def text_destroy(self):
    self.canvas_text.destroy()



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
        self.SD_data = IntVar()
        self.FTc_data = IntVar()
        self.PV_data = IntVar()
        self.user_admin = False
        self.probes_passed.set(0)
        self.info_canvas = None
        self.test = False

        ###############################################################
        # import and set up images for the screen                     #
        ###############################################################
        sys.path.append('./PTT_Icons')
        self.greenlight = (PhotoImage(file="./PTT_Icons/GREEN.png"))
        self.amberlight = (PhotoImage(file="./PTT_Icons/AMBER.png"))
        self.redlight = (PhotoImage(file="./PTT_Icons/RED.png"))
        self.greylight = (PhotoImage(file="./PTT_Icons/GREY.png"))
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
        self.text_area = tk.Text(self.canvas_back, font=("Courier",14),height=5, width=40)
        self.text_area.place(relx=0.07, rely=0.07)
        ttk.Label(self.canvas_back, text="Deltex", background="#B1D0E0", foreground="#003865",
                  font=('Helvetica', 28, 'bold'), width=12).place(relx=0.85, rely=0.1)
        ttk.Label(self.canvas_back, text="medical", background="#B1D0E0", foreground="#A2B5BB",
                  font=('Helvetica', 18)).place(relx=0.85, rely=0.15)
        self.text_area.delete('1.0', 'end')
        ttk.Label(self.canvas_back, text='Batch number: ', background=self.back_colour, font=("Courier",14)).place(
            relx=0.1, rely=0.3, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.current_batch, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.25, rely=0.3, anchor='w')
        ttk.Label(self.canvas_back, text='Probe type: ', background=self.back_colour, font=("Courier",14)).place(
            relx=0.1, rely=0.45, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.probe_type, relief=SUNKEN, font="bold",
                  width=12).place(relx=0.25, rely=0.45, anchor='w')
        ttk.Label(self.canvas_back, text='Connected to: ', background=self.back_colour, font=("Courier",14)).place(
            relx=0.73, rely=0.2, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.device_details, relief=SUNKEN,
                  width=30).place(relx=0.7, rely=0.25, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.odm_details, relief=SUNKEN,
                  width=30).place(relx=0.7, rely=0.30, anchor='w')
        ttk.Label(self.canvas_back, text="Data from ODM", background=self.back_colour, font=("Courier",14)).place(
            relx=0.7, rely=0.42, anchor="w")
        ttk.Label(self.canvas_back, text="SD", background=self.back_colour, font=("Courier",14)).place(relx=0.70, rely=0.46, anchor="w")
        ttk.Label(self.canvas_back, text="FTc", background=self.back_colour, font=("Courier",14)).place(relx=0.77, rely=0.46, anchor="w")
        ttk.Label(self.canvas_back, text="PV", background=self.back_colour, font=("Courier",14)).place(relx=0.85, rely=0.46, anchor="w")
        ttk.Label(self.canvas_back, textvariable=self.SD_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.69, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.FTc_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.76, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.PV_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.84, rely=0.51, anchor='w')
        ttk.Label(self.canvas_back, text='Program/Test Status: ',
                  background=self.back_colour, font=("Courier", 14)).place(relx=0.4,rely=0.32)
        ttk.Label(self.canvas_back, text='Probes Passed: ', background=self.back_colour, font=("Courier",14)).place(
            relx=0.1, rely=0.6, anchor='w')
        ttk.Label(self.canvas_back, text="Reflection Test", font="bold",
                  background=self.back_colour).place(relx=0.1,rely=0.72)
        ttk.Label(self.canvas_back, textvariable=self.reflection,font=("Courier", 14), relief=SUNKEN,
                  width=20).place(relx=0.25, rely=0.72)
        ttk.Label(self.canvas_back, textvariable=self.probes_passed, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.25, rely=0.6, anchor='w')
        ttk.Label(self.canvas_back, text='Probes to test: ', background=self.back_colour, font=("Courier",14)).place(
            relx=0.7, rely=0.75, anchor='w')
        ttk.Label(self.canvas_back, textvariable=self.left_to_test, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.83, rely=0.75, anchor='w')
        ttk.Label(self.canvas_back, text='Action: ', background=self.back_colour,
                  font=("Courier",14)).place(relx=0.1, rely=0.83)

        #################################################################
        # Show interaction buttons                                      #
        #################################################################
        self.ssp_btn = Button(self.canvas_back, text='  Suspend Batch  ',
                              font=("Courier", 14, "bold"), background="#EF5B0C",
                              highlightthickness=0,command=self.suspnd_btn_clicked)
        self.ssp_btn.place(relx=0.85, rely=0.88, anchor=CENTER)
        self.session_on_going = True
        self.analyser_serial = None
        self.probes_passed.set(0)

        #########################################################
        # Complete button detected pressed                      #
        #########################################################

    def cmplt_btn_clicked(self):
        if self.get_probes_left():
            self.session_complete = True
            self.session_on_going = False
            current_batch = DS.get_current_batch()
            self.complete_batch(current_batch)
            complete = BM.CompleteBatch(current_batch)

            self.canvas_back.destroy()
            try:
                self.control.show_frame(SE.SessionSelectWindow)
            except:
                pass
            return complete
        ###########################################################
        # Suspend button detected pressed                         #
        ###########################################################

    def suspnd_btn_clicked(self):
        if tm.askyesno(title="Batch Info", message="    Suspend Batch ?         "):
            self.session_complete = False
            self.session_on_going = False
            probe_data = P.Probes(self.probe_type.get(), self.current_batch.get(), self.probes_passed.get(),
                                  self.left_to_test.get())
            DS.write_probe_data(probe_data)
            BM.SuspendBatch(self.current_batch.get())
            if not self.test:
                self.canvas_back.destroy()
                self.control.show_frame(SE.SessionSelectWindow)

        else:
            self.refresh_window()
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

    def reset(self):
        self.display_layout()
        self.set_display()
        self.session_on_going = True
        current_user = DS.get_username()
        self.user_admin = DS.get_user_data()['Over_rite']
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        current_batch = DS.get_current_batch()
        if current_batch == "000":
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
        self.canvas_back.pack()
        self.reflection.set("--->")
        ##############################
        # Collect analyser port data #
        ##############################
        ZND.flush_analyser_port()
        ZND.set_vna_controls()
        self.warning_text = {
            "overrite on": "Probe re-programming enabled.",
            "overrite off": "Probe re-programming disabled",
            "1": "Probe connected",
            "2": "Programmed Probe Detected",
            "3": "   New Serial Number ?        ",
            "4": "Information",
            "5": "   Fault Find Probe ?       ",
            "6": "  Connect New Probe",
            "7": "Batch Complete.",
            "8": "\nRemove probe.",
            "9": "Programming probe...",
            "10": "Testing probe...'",
            "11": "\nProgramming error...",
            "12": "\nUnable to program, \nPlease check probe chip. ",
            "13": "Probe Failed.",
            "14": "\n\nFault finding this probe.",
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
        if PM.ProbePresent() and self.session_on_going:
            ttk.Label(self.canvas_back, textvariable=self.action, background='yellow',
                      width=25, relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
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
        vna = ZND.get_vna_check()
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
        return check

        ###############################################################
        # Start off mai testing sequence                              #
        ###############################################################

    def refresh_window(self):
        self.reset()
        self.set_reprogram_status()
        self.show_gray_light()
        ################################################################
        #                     Main loop                                #
        ################################################################
        while self.session_on_going:
            # self.info_canvas = True
            if self.left_to_test.get() == 0:
                self.session_on_going = False
                self.session_complete = True
            self.action.set(self.warning_text["6"])
            self.programmed = False
            Tk.update(self)
            if self.check_probe_present():
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

        if self.session_complete and not self.check_probe_present():
            probe_canvas(self,f"{self.warning_text['7']} {self.warning_text['8']}", False)
            time.sleep(2)
            text_destroy(self)
            self.cmplt_btn_clicked()

    def do_program_and_test(self, batch):
        ################################
        # Program and test probe       #
        ################################
        self.programmed = False
        results, marker, odm_data = self.test_probe()
        # pcb_serial_number = PM.read_serial_number()
        # binary_str = codecs.decode(pcb_serial_number, "hex")
        # print(f"serial number = {str(binary_str)[2:19]}")
        snum = self.program_probe(DS.get_current_probe_type(),results)
        self.update_results(results, snum, odm_data, batch, marker)
        if not results:
            return True
        else:
            return False

    def program_blank_probe(self):
        ###############################################################
        # Program a blank probe inserted into probe interface         #
        ###############################################################
        if PM.ProbePresent() and not PM.ProbeIsProgrammed():
            self.set_reprogram_status()
            self.action.set(self.warning_text["1"])
            self.show_green_text()
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

        #################################################
        # Test the inserted probe                       #
        #################################################

    def program_probe(self, probe_type, test):
        self.action.set(self.warning_text["9"])
        self.show_amber_image()
        serialNumber = PM.ProgramProbe(probe_type, test)

        if not serialNumber:
            self.canvas_back.create_image(520, 350, image=self.redlight)
            self.canvas_back.pack()
            ttk.Label(self.canvas_back, textvariable=self.action, background='orange',
                        width=25, relief=GROOVE, font=("Courier", 16)).place(x=270, y=550)
            self.action.set(self.warning_text["13"])
            probe_canvas(self,f"{self.warning_text['13']} {self.warning_text['12']} {self.warning_text['8']}", True)
            text_destroy(self)
            self.show_gray_light()
            self.programmed = False
            return False
        else:
            self.programmed = True
            return str(codecs.decode(serialNumber, "hex"), 'utf-8')[:16]



        ##########################################################
        # Over-write a programmed probe detected                 #
        ##########################################################

    def over_write_probe(self):
        # SN_seperated = []
        # limit = 16
        # start = 0
        # dec_start = '53A00900'
        # end = '50'
        # pcb_serial_number = PM.read_serial_number()
        # binary_str = codecs.decode(pcb_serial_number, "hex")
        # print(f"serial number = {str(binary_str)[2:18]}")
        # SN_bytes = PR.read_all_bytes()
        # while limit <= len(SN_bytes):
        #     makeup = dec_start + SN_bytes[start:limit] + end
        #     SN_seperated.append(makeup)
        #     limit += 16
        #     start += 16
        # probe_type = SN_seperated[0][8:16]
        # probe_sn = SN_seperated[1][8:-2]
        # new_probe_sn = probe_type + '3232' + probe_sn + '3031'
        # new_probe_bin = codecs.decode(new_probe_sn, 'hex')
        # new_probe = new_probe_bin.decode('utf-8')
        # PM.construct_new_serial_number(new_probe,True)

        if PM.ProbeIsProgrammed() and PM.ProbePresent():
            self.programmed = True
            self.action.set(self.warning_text["2"])
            Tk.update(self)
        if DS.get_user_data()['Over_rite']:
            # ask for user input to reprogramme the probe #
            if self.programmed and tm.askyesno(title=self.warning_text["2"], message=self.warning_text["3"]):
                self.do_program_and_test(self.current_batch.get())
                self.set_reprogram_status()
                # self.session_on_going = False
                # self.ff_window()
        else:
            probe_canvas(self,"Do you want to Fault Find.", True)
            if self.info_canvas:
                self.session_on_going = False
                text_destroy(self)
                self.ff_window()
            else:
                self.session_on_going = True
                text_destroy(self)
                self.refresh_window()

        ################################
        # Show Fault find window       #
        ################################

    def ff_window(self):
        probe_data = P.Probes(self.probe_type.get(), self.current_batch.get(), self.probes_passed.get(),
                              self.left_to_test.get())
        DS.write_probe_data(probe_data)
        self.session_on_going = False
        self.canvas_back.destroy()
        self.control.show_frame(FF.FaultFindWindow)

        ##################################
        # Show probe state to user       #
        ##################################

    def show_green_image(self):
        self.canvas_back.create_image(self.cent_x, self.cent_y, image=self.greenlight)
        self.canvas_back.pack()
        ttk.Label(self.canvas_back, textvariable=self.action, background='#1fff1f',
                  width=25, relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.75)
        Tk.update(self)

    def show_amber_image(self):
        self.canvas_back.create_image(self.cent_x, self.cent_y, image=self.amberlight)
        self.canvas_back.pack()
        ttk.Label(self.canvas_back, textvariable=self.action, background='#FF7F3F',
                  width=25, relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
        Tk.update(self)

    def show_red_light(self):
        self.canvas_back.create_image(self.cent_x, self.cent_y, image=self.redlight)
        self.canvas_back.pack()
        self.display_message(self.warning_text["13"])
        ttk.Label(self.canvas_back, textvariable=self.action, background='#FF7F3F',
                  width=25, relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
        Tk.update(self)

    def show_gray_light(self):
        self.canvas_back.create_image(self.cent_x, self.cent_y, image=self.greylight)
        self.canvas_back.pack()
        ttk.Label(self.canvas_back, textvariable=self.action, background='yellow',
                  width=25, relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
        Tk.update(self)

    def show_blue_meaasge(self):
        self.action.set('Testing probe...')
        ttk.Label(self.canvas_back, textvariable=self.action, background='#548CFF',
                  width=25, relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
        Tk.update(self)

    def show_green_text(self):
        ttk.Label(self.canvas_back, textvariable=self.action, background='#1fff1f',
                  width=25, relief=GROOVE, font=("Courier", 18)).place(relx=0.25, rely=0.83)
        Tk.update(self)

        #######################
        # Test the probe      #
        #######################

    def test_probe(self):
        self.action.set(self.warning_text["10"])
        self.show_blue_meaasge()
        odm_data = self.update_odm_data()
        results = PM.TestProbe()
        marker_data = ZND.tdr()
        ###################################################
        # Probe passed                                    #
        ###################################################
        if LOWER_LIMIT < results < UPPER_LIMIT:
            self.show_green_image()
            probe_canvas(self,f"{self.warning_text['15']} {self.warning_text['16']}", False)
            while self.check_probe_present():
                pass
            text_destroy(self)

        else:
            ####################################################
            # Probe failed                                     #
            ####################################################
            self.show_red_light()
            probe_canvas(self,f"{self.warning_text['13']} {self.warning_text['14']}", True)
            if self.info_canvas:
                self.session_on_going = False
                text_destroy(self)
                self.ff_window()
            else:
                self.session_on_going = True
                text_destroy(self)

        ###############################################
        # Reset probe testing                         #
        ###############################################
        self.show_gray_light()
        return results, marker_data, odm_data

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

        ######################################
        # Update the results to the CSV file #
        ######################################

    def update_results(self, results, snum, odm_data, batch, marker):
        data_list_to_file = []
        odm_to_file = "ODM not used"
        if DS.get_devices()['odm_active'] and self.programmed:
            odm_to_file = str(odm_data[9])
        results_to_file = str(results)
        probes_left = self.left_to_test.get()
        probes_passed = self.probes_passed.get()
        self.left_to_test.set(probes_left - 1)
        self.probes_passed.set(probes_passed + 1)
        data_list_to_file.append(" ")  # by pass the batch number column
        data_list_to_file.append(snum)  # insert serial number
        data_list_to_file.append(" ")
        data_list_to_file.append(probes_left)
        data_list_to_file.append(self.current_user.get())  # insert the logged in user
        data_list_to_file.append(results_to_file)  # insert ODM data
        data_list_to_file.append(marker)
        data_list_to_file.append(odm_to_file)
        BM.saveProbeInfoToCSVFile(data_list_to_file, batch)  # save to file

    def complete_batch(self,batch_number):
        print(f"{batch_number} completed")

        batch_qty = self.probes_passed.get()
        failures = 0
        scrapped = 100 - self.probes_passed.get()
        BM.competed_text(DS.get_username(),DS.get_current_probe_type(),batch_number,batch_qty,failures,scrapped)


    def yes_answer(self):
        self.info_canvas = True
        # text_destroy(self)
        # self.session_on_going = False
        # self.ff_window()

    def no_answer(self):
        self.info_canvas = False
        # text_destroy(self)
        # self.session_on_going = True
        # self.refresh_window()
