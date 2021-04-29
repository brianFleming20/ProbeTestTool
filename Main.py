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
import tkinter.messagebox as tm
from tkinter import filedialog
import pyvisa as visa
import time


import PI
import SecurityManager
from SecurityManager import User
import BatchManager
from BatchManager import Batch
import InstrumentManager
import ProbeManager
from ProbeManager import Probe
from ProbeManager import ProbeManager
import NanoZND
import ODMPlus
import UserLogin as UL
import Sessions as SE



# create instances
SM = SecurityManager.SecurityManager()
IM = InstrumentManager.InstrumentationManager()
BM = BatchManager.BatchManager()
PM = ProbeManager()
NanoZND = NanoZND.NanoZND()
ODM = ODMPlus.ODMData()



# define global variables
PTT_Version = 'Deltex Medical : XXXX-XXXX Probe Test Tool V0.1'
w = 800  # window width
h = 600  # window height
LARGE_FONT = ("Verdana", 14)
BTN_WIDTH = 30


# Assign as a command when I want to disable a button (double click prevention)
def ignore():
    return 'break'


class WindowController(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title(PTT_Version)
        # get window width and height
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (UL.LogInWindow,
                  SE.SessionSelectWindow,
                  SE.NewSessionWindow,
                  SE.ContinueSessionWindow,
                  ConnectionWindow,
                  UL.AdminWindow,
                  UL.AddUserWindow,
                  TestProgramWindow):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(UL.LogInWindow)
       
       

    def show_frame(self, newFrame):

        frame = self.frames[newFrame]
        frame.tkraise()

        # Does the frame have a refresh method, if so call it.
        if hasattr(newFrame, 'refresh_window') and callable(getattr(newFrame, 'refresh_window')):
            self.frames[newFrame].refresh_window()



class TestProgramWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.sessionOnGoing = False
        self.sessionComplete = None
        self.action = StringVar()

        # define variables
        self.currentBatch = StringVar()
        self.currentUser = StringVar()
        self.probesPassed = IntVar()
        self.deviceDetails = StringVar()
        self.device = "Not connected to analyser"
        self.probeType = StringVar()
        self.SD_data = IntVar()
        self.FTc_data = IntVar()
        self.PV_data = IntVar()
        

        #import images
        self.greenlight = (PhotoImage(file="green128.gif"))
        self.amberlight = (PhotoImage(file="amber128.gif"))
        self.redlight = (PhotoImage(file="red128.gif"))
        self.greylight = (PhotoImage(file="grey128.gif"))
        

        ttk.Label(self, text='Batch number: ').place(
            relx=0.1, rely=0.05, anchor='w')
        ttk.Label(self, textvariable=self.currentBatch, relief=SUNKEN, font="bold",
                 width=10).place(relx=0.3, rely=0.05, anchor='w')

        ttk.Label(self, text='Probe type: ').place(
            relx=0.45, rely=0.05, anchor='w')
        ttk.Label(self, textvariable=self.probeType, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.6, rely=0.05, anchor='w')

        ttk.Label(self, text='User: ').place(relx=0.1, rely=0.15, anchor='w')
        ttk.Label(self, textvariable=self.currentUser, relief=SUNKEN, font="bold",
                  width=20).place(relx=0.3, rely=0.15, anchor='w')

        ttk.Label(self, text='Connected to: ').place(
            relx=0.1, rely=0.25, anchor='w')
        ttk.Label(self, textvariable=self.deviceDetails, relief=SUNKEN,
                  width=50).place(relx=0.3, rely=0.25, anchor='w')
        
        ttk.Label(self, text="Probe parameter data").place(
            relx=0.7, rely=0.4, anchor="w")
        ttk.Label(self, text="SD").place(relx=0.70, rely=0.44, anchor="w")
        ttk.Label(self, text="FTc").place(relx=0.77, rely=0.44, anchor="w")
        ttk.Label(self, text="PV").place(relx=0.85, rely=0.44, anchor="w")
        ttk.Label(self, textvariable=self.SD_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.69, rely=0.49, anchor='w')
        ttk.Label(self, textvariable=self.FTc_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.76, rely=0.49, anchor='w')
        ttk.Label(self, textvariable=self.PV_data, relief=SUNKEN, font="bold",
                  width=5).place(relx=0.84, rely=0.49, anchor='w')

        ttk.Label(self, text='Program/Test Status: ').place(relx=0.1,
                                            rely=0.5, anchor='w')
        self.status_image = ttk.Label(self, image=self.greylight)
        self.status_image.place(relx=0.5, rely=0.5, anchor=CENTER)

        ttk.Label(self, text='Probes Passed: ').place(
            relx=0.1, rely=0.7, anchor='w')
        ttk.Label(self, textvariable=self.probesPassed, relief=SUNKEN, font="bold",
                  width=10).place(relx=0.3, rely=0.7, anchor='w')

        ttk.Label(self, text='Action: ').place(relx=0.1, rely=0.8, anchor='w')
        ttk.Label(self, textvariable=self.action, background='yellow',
                  width=40, relief=GROOVE).place(relx=0.3, rely=0.8, anchor='w')
        self.action.set('Connect New Probe')

        ttk.Button(self, text='Complete Session', command=lambda: self.cmplt_btn_clicked(
            controller)).place(relx=0.4, rely=0.9, anchor=CENTER)
        ttk.Button(self, text='Suspend Session', command=lambda: self.suspnd_btn_clicked(
            controller)).place(relx=0.6, rely=0.9, anchor=CENTER)

    def cmplt_btn_clicked(self, controller):
        Tk.update(self)
        self.sessionComplete = True
        self.sessionOnGoing = False
        BM.CompleteBatch(BM.currentBatch)
        controller.show_frame(SE.SessionSelectWindow)

    def suspnd_btn_clicked(self, controller):
        self.sessionComplete = False
        self.sessionOnGoing = False
        controller.show_frame(SE.SessionSelectWindow)


    def refresh_window(self):
        self.sessionOnGoing = True
        serial_results = []
        analyser_data = []
        port = NanoZND.GetAnalyserPortNumber()
        # self.root.deiconify()
        self.probeType.set(BM.currentBatch.probeType)
        self.currentBatch.set(BM.currentBatch.batchNumber)
        self.probesPassed.set(0)
        self.currentUser.set(SM.loggedInUser.name)
        self.deviceDetails.set(self.device)
        self.RLLimit = -1  # pass criteria for return loss measurement
        
        ##############################
        # Collect analyser port data #
        ##############################
        
        try:
            # Check to see if the analyser port is connected
            if NanoZND.GetAnalyserStatus():
                # Get the analyser to generate data points and return them
                
                analyser_data = NanoZND.GetAnalyserData()
                # Print the analyser data points selected by 
                print(analyser_data[3:10])
                # Set the device connected name
                self.device = " NanoNVA "
                self.deviceDetails.set(self.device)
                
        except:
               tm.showerror(
                'Data Collection Error', 'Unable to collect the data from the NanoVNA Analyser. \nOr turn it on.')  
        # write data to .csv file
        
        try:
            batch = BM.currentBatch.batchNumber
            NanoZND.CVSOutPut(batch)
        except:
            tm.showerror(
                'Data write Error', 'Unable to start write the data from the NanoVNA Analyser. \n to file.')  
   
        #######################
        # Collect serial data #
        #######################
        try:
            serial_results = ODM.ReadSerialODM()
            # serial_results = IM.GetPatientParamerts()
            # self.SD_data.set(serial_results[0])
            # self.FTc_data.set(serial_results[1])
            # self.PV_data.set(serial_results[2])
           
            self.SD_data.set(serial_results[0][5])
            self.FTc_data.set(serial_results[0][6])
            self.PV_data.set(serial_results[0][9])
            Tk.update(self)
        except:
            tm.showerror(
                'Connection Error', 'Unable to collect the data from the ODM.')
                # controller.show_frame(ConnectionWindow)
        
        
        
        while(self.sessionOnGoing == True):
            Tk.update(self)
            if PM.ProbePresent() == True:
                self.action.set('Probe connected')
                self.status_image.configure(image=self.amberlight)
                ProbeIsProgrammed = PM.ProbeIsProgrammed()

                if ProbeIsProgrammed == False or tm.askyesno('Programmed Probe Detected', 'This probe is already programmed.\nDo you wish to re-program and test?'):
                    self.action.set('Programming probe')
                    serialNumber = PM.ProgramProbe(BM.currentBatch.probeType)
                    if serialNumber == False:
                        tm.showerror('Programming Error',
                                     'Unable to program\nPlease check U1')
                        self.action.set('Probe failed')
                        self.status_image.configure(image=self.redlight)
                    else:
                        Tk.update(self)
                        self.action.set('Testing probe...')
                            
                        results = PM.TestProbe(
                            serialNumber, BM.currentBatch.batchNumber, self.currentUser.get())
                        self.action.set('Testing complete. Disconnect probe')
                        # if PM.ZND.get_marker_values()[0] < self.RLLimit and PM.ZND.get_marker_values()[1] < self.RLLimit:
                        if self.RLLimit == -1: #check for crystal pass value, now pass every time
                            BM.UpdateResults(
                                results, BM.currentBatch.batchNumber)
                            self.probesPassed.set(self.probesPassed.get() + 1)
                            self.status_image.configure(image=self.greenlight)
                            Tk.update(self)
                        else:
                            self.status_image.configure(image=self.redlight)
                            tm.showerror('Return Loss Error',
                                         'Check crystal connections')
                            Tk.update(self)
                        
                        # Collect serial data
                        while PM.ProbePresent() == True:
                            # serial_results = IM.GetPatientParamerts()
                            try:
                                
                                serial_results = IM.ReadPortODM()
                            # print(serial_results)
                            # self.SD_data.set(serial_results[0])
                            # self.FTc_data.set(serial_results[1])
                            # self.PV_data.set(serial_results[2])
                            # Tk.update(self)
                            
                                self.SD_data.set(serial_results[0][5])
                                self.FTc_data.set(serial_results[0][6])
                                self.PV_data.set(serial_results[0][9])
                                Tk.update(self)
                            except:
                                tm.showerror(
                                        'Connection Error', 'Unable to collect the data from the ODM.')
 
                        
                while 1:
                    if PM.ProbePresent() == False:
                        # PM.ClearAnalyzer()
                        self.status_image.configure(image=self.greylight)
                        self.action.set('Connect New Probe')
                        break
        
       
                        
        # put something here to move csv?
        if self.sessionComplete == True:
            BM.CompleteBatch(BM.currentBatch)




class NewSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        self.batchNumber = StringVar()
        self.probeType = StringVar()

        # Details Screen
        tk.Frame.__init__(self, parent)

        batch_frame = tk.Frame(self, pady=3)
        probe_type_frame = tk.Frame(self, pady=3)
        button_frame = tk.Frame(self, pady=3)

        #batch_frame.grid(row=0, sticky="ew")
        probe_type_frame.grid(row=1, column=1, sticky="news")

        self.NSWL1 = ttk.Label(self, text='Batch number: ', justify=RIGHT)
        self.NSWL1.grid(row=0, column=0)

        self.NSWE1 = ttk.Entry(self, textvariable=self.batchNumber)
        self.NSWE1.grid(row=0, column=1)

        self.NSWL2 = ttk.Label(self, text='Select Probe Type: ')
        self.NSWL2.grid(row=1, column=0)

        tk.Radiobutton(probe_type_frame, text='SDP30 [Suprasternal Probe]',
                       variable=self.probeType, value='SDP30').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='DP240 [Doppler 10 Day]',
                       variable=self.probeType, value='DP240').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='DP12 [Doppler 12 Hour]',
                       variable=self.probeType, value='DP12').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='DP6 [Doppler 6 Hour]',
                       variable=self.probeType, value='DP6').pack(fill=X, ipady=5)
        tk.Radiobutton(probe_type_frame, text='I2C',
                       variable=self.probeType, value='I2C').pack(fill=X, ipady=5)
#        tk.Radiobutton(probe_type_frame, text='I2P', variable=self.probeType, value='I2P').pack(fill = X, ipady = 5)
#        tk.Radiobutton(probe_type_frame, text='I2S', variable=self.probeType, value='I2S').pack(fill = X, ipady = 5)
#        tk.Radiobutton(probe_type_frame, text='KDP', variable=self.probeType, value='KDP').pack(fill = X, ipady = 5)
        tk.Radiobutton(probe_type_frame, text='Blank',
                       variable=self.probeType, value='Blank').pack(fill=X, ipady=5)

        self.confm_btn = tk.Button(self, text='Confirm', padx=3, pady=3,
                                   width=BTN_WIDTH, command=lambda: self.confm_btn_clicked(controller))
        self.confm_btn.grid(row=2, column=0)

        self.cancl_btn = tk.Button(self, text='Cancel', padx=3, pady=3, width=BTN_WIDTH,
                                   command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.cancl_btn.grid(row=2, column=1)

        self.bind('<Return>', self.confm_btn_clicked)

    def confm_btn_clicked(self, controller):
        # create batch object
        newBatch = Batch(self.batchNumber.get())
        newBatch.probeType = self.probeType.get()

        DAnswer = tm.askyesno('Confirm', 'Are batch details correct?')
        if DAnswer == True:
            # create the batch file
            if BM.CreateBatch(newBatch, SM.loggedInUser.name) == False:
                tm.showerror('Error', 'Batch number not unique')
            else:
                BM.currentBatch = newBatch
                self.NSWE1.delete(0, 'end')
                controller.show_frame(ConnectionWindow)


class ContinueSessionWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        

        self.Label1 = ttk.Label(self, text='Choose a session to resume')
        self.Label1.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.sessionListBox = Listbox(self)
        self.sessionListBox.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.sessionListBox.config(height=14, width=20)

        self.continue_btn = ttk.Button(
            self, text='Continue Session', command=lambda: self.continue_btn_clicked(controller))
        self.continue_btn.place(relx=0.4, rely=0.9, anchor=CENTER)

        self.cancel_btn = ttk.Button(
            self, text='Cancel', command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.cancel_btn.place(relx=0.6, rely=0.9, anchor=CENTER)

        self.refresh_window()

    def refresh_window(self):
        # #create a list of the current users using the dictionary of users
        sessionList = []
        for item in BM.GetAvailableBatches():
            sessionList.append(item)

        # clear the listbox
        self.sessionListBox.delete(0, END)

        # fill the listbox with the list of users
        for item in sessionList:
            self.sessionListBox.insert(END, item)

    def continue_btn_clicked(self, controller):
        lstid = self.sessionListBox.curselection()

        try:
            lstBatch = self.sessionListBox.get(lstid[0])
            BM.currentBatch = BM.GetBatchObject(lstBatch)
            controller.show_frame(ConnectionWindow)
        except:
            tm.showerror('Error', 'Please select a batch from the batch list')


class ConnectionWindow(tk.Frame):
    def __init__(self, parent, controller):
        # define variables
        self.Monitor = StringVar()
        self.comPort = StringVar()
        self.AnalyserUSB = StringVar()
        self.file = StringVar()
        self.connectedToCom = False
        self.connectedToAnalyser = False
        self.odm_connection = False
        self.AnalyserUSB.set('COM4')
        self.comPort.set('COM3')
        self.Monitor.set('COM5')
        self.file.set(NanoZND.GetFileLocation())
        # create the window and frame
        tk.Frame.__init__(self, parent)

        # create the widgets
        self.label_1 = ttk.Label(self, text="ODM monitor port")
        self.label_2 = ttk.Label(self, text="Probe Interface Port")
        self.label_3 = ttk.Label(self, text="Analyser port")
        self.label_4 = ttk.Label(self, text="NanoZND file storage location")
        self.entry_1 = ttk.Entry(self, textvariable=self.Monitor,)
        self.entry_2 = ttk.Entry(self, textvariable=self.comPort, )
        self.entry_3 = ttk.Entry(self, textvariable=self.AnalyserUSB, )
        self.entry_4 = ttk.Entry(self, textvariable=self.file)
        
      

        self.label_1.place(relx=0.275, rely=0.2, anchor=CENTER)
        self.label_2.place(relx=0.275, rely=0.4, anchor=CENTER)
        self.label_3.place(relx=0.275, rely=0.3,anchor=CENTER)
        self.label_4.place(relx=0.25, rely=0.55, anchor=CENTER)
        self.entry_1.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.entry_2.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.entry_3.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.entry_4.place(relx=0.42, rely=0.55, width=250, anchor="w")
       
        self.browseBtn = ttk.Button(
            self, text="Browse", command=lambda: self._browse_btn_clicked(controller))
        self.browseBtn.grid(row=2, column=1)
        self.browseBtn.place(relx=0.8, rely=0.55, anchor=CENTER)
        self.bind('<Return>', self._connect_btn_clicked)
        
        self.connectBtn = ttk.Button(
            self, text="Connect", command=lambda: self._connect_btn_clicked(controller))
        self.connectBtn.grid(row=2, column=1)
        self.connectBtn.place(relx=0.4, rely=0.8, anchor=CENTER)
        self.bind('<Return>', self._connect_btn_clicked)

        self.cancelBtn = ttk.Button(
            self, text="Cancel",  command=lambda: controller.show_frame(SE.SessionSelectWindow))
        self.cancelBtn.place(relx=0.6, rely=0.8, anchor=CENTER)

        self.entry_1.focus_set()
        
      
    def _browse_btn_clicked(self, controller):
        filename = filedialog.askopenfilenames(initialdir = "/",title = "Select file",
                                               filetypes = ((".csv files","*.csv"),
                                                            ("all files","*.*")))     
        NanoZND.SetFileLocation(filename)
        self.file = NanoZND.GetFileLocation()
        print(self.file)
        
            

    def _connect_btn_clicked(self, controller):
        cp = self.comPort.get()
        odm = self.Monitor.get()
        usb = self.AnalyserUSB.get()
        
        
        try:
            NanoZND.SetAnalyserPort(usb)
            NanoZND.ReadAnalyserData()
            self.connectedToAnalyser = True
        except:
            self.connectedToAnalyser = False
            tm.showerror(
                'Connection Error', 'Unable to connect to Analyser Interface\nPlease check the nanoZND Port is correct or turned on.')
            
        try:
            PM.ConnectToProbeInterface(cp)
            self.connectedToCom = True
        except:
            self.connectedToCom = False
            tm.showerror(
                'Connection Error', 'Unable to connect to Probe Interface\nPlease check the Probe interface port is correct.')

        try:
           ODM.set_ODM_port_number(odm) 
           self.odm_connection = True
        except:
           self.odm_connection = False
           tm.showerror(
                'Connection Error', 'Unable to connect to Probe Interface\nPlease check the ODM port is correct and turned on.')
  

        if self.connectedToCom and self.connectedToAnalyser and self.odm_connection == True :
            controller.show_frame(TestProgramWindow)
              

app = WindowController()
app.mainloop()
