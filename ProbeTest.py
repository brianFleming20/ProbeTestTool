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
import time
import pickle
import serial
from serial import Serial
import codecs
import binascii
from time import gmtime, strftime
import time
from bitstring import BitArray

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
        with open('file.ptt', 'rb') as file:
      
        # Call load method to deserialze
            myvar = pickle.load(file)
            currentBatch = ''.join(myvar[2])
       
        
        file.close()
        BM.CompleteBatch(currentBatch)
        controller.show_frame(SE.SessionSelectWindow)

    def suspnd_btn_clicked(self, controller):
        self.sessionComplete = False
        self.sessionOnGoing = False
        controller.show_frame(SE.SessionSelectWindow)


    def refresh_window(self):
        self.sessionOnGoing = True
        serial_results = []
        analyser_data = []
       
        
        # Open the file in binary mode
        with open('file.ptt', 'rb') as file:
      
        # Call load method to deserialze
            myvar = pickle.load(file)
            name = myvar[0]
            currentBatch = myvar[2]
            probeType = myvar[3]
            analyser_port = myvar[4][2]
        file.close()
        # self.root.deiconify()
        self.probeType.set(probeType)
        self.currentBatch.set(currentBatch)
        self.probesPassed.set(0)
        self.currentUser.set(name)
        self.deviceDetails.set(self.device)
        self.RLLimit = -1  # pass criteria for return loss measurement
        
        ##############################
        # Collect analyser port data #
        ##############################
      
        try:
            # Check to see if the analyser port is connected
            
            if analyser_port:
                # Get the analyser to generate data points and return them
                analyser_data = NanoZND.ReadAnalyserData(analyser_port)
                
                # Print the analyser data points selected by 
                print("Analyser data {}".format(analyser_data[3:10]))
                # Set the device connected name
                self.device = " NanoNVA "
                self.deviceDetails.set(self.device)
                
        except:
               tm.showerror(
                'Data Collection Error', 'Unable to collect the data from the NanoVNA Analyser. \nOr turn it on.')  
        # write data to .csv file
        
        try:
            
            NanoZND.CVSOutPut(currentBatch)
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
                    if ConnectToProbe().ProbePresent() == False:
                        # PM.ClearAnalyzer()
                        self.status_image.configure(image=self.greylight)
                        self.action.set('Connect New Probe')
                        break
        
       
                        
        # put something here to move csv?
        if self.sessionComplete == True:
            BM.CompleteBatch(BM.currentBatch)

class ConnectToProbe(object):
    def __init__(self):
        self.ser = False
        self.probePort = ""

    def ConnectToProbeInterface(self, comPort):
        '''
        Pass in a com port ID (COMX) and connect to that comport.
        '''
        self.ser = serial.Serial(port = comPort, baudrate = 9600, \
            parity = serial.PARITY_NONE, \
            stopbits = serial.STOPBITS_ONE, \
            bytesize  = serial.EIGHTBITS, \
            timeout  = 0, \
             )
        
        print(self.probePort)
        self.ser.close()
  
    def ProbePresent(self):
        '''
        Returns True if a probe is present, False if not
        '''   
             
        #get the IO byte
        self.OpenPort()
       
        self.Send(b'4950')   
        time.sleep(0.05) #allow time for the data to be received  
        IOByte = self.Read()
        print("IOByte {}".format(IOByte))
        self.ClosePort()
        
        #get the relevant bit
        bits = BitArray(hex=IOByte)
        bit = bits.bin[2:3]
        print("bits \n\n{}".format(bit))
        self.ser.close()
        #check to see if the pin is pulled low by the probe
        if bit == '0':
            return True
        else:
            return False    
        
    def OpenPort(self):
        '''
        Opens the port, readying it for communication
        '''
        
        self.ser.open()
    
    def ClosePort(self):
        '''
        Closes the port
        '''
        self.ser.close()
        
    def Send(self, input):
        '''
        pass in hex bytes, send the whole lot down the serial port.
        '''
        
        #flush the buffers
        self.ser.flushInput()   
        self.ser.flushOutput() 
        
        #convert the input to ASCII characters and send it
        self.ser.write(codecs.decode(input, "hex_codec"))
        
    def Read(self):
        '''
        reads the contents of the serial buffer and returns it as a string 
        of hex bytes
        '''
        serialData = ''

        while self.ser.inWaiting() > 0:
            b = binascii.hexlify(self.ser.read(1))
            serialData += codecs.decode(b) 
        
        return serialData

    
class PI(object):
    """
    SC18IM700 commands
    
    S 53 I2C start
    P 50 I2C stop
    R 52 read SC18IM internal register
    W 57 write to SC18IM internal register
    I 49 read IO port
    O 4F write to GPIO port
    Z 5A power down
    
    A0 write address
    A1 read address

    """
    
    def __init__(self):
        self.loggedInUser = False
        self.SM = SerialManager()
        self.PD = ProbeData()
        self.ser = None

    
    def Connect(self, comPort):
        self.ser = self.SM.ConfigurePort(comPort)
            
    def ProbeWrite(self, data):
        '''
        pass in a list of bytes, writes a byte at a time to the probe
        '''
        
        self.SM.OpenPort()
        print(data)
        for item in data:
            self.SM.Send(item)
            time.sleep(0.01)
        self.SM.ClosePort()
            
    def ProbeReadSerialNumber(self):
        '''
        Returns a 32 character string of the first 16 bytes of the probe's memory
        
        
        sends: I2c start, write address, number of bytes, data... , I2C start, read address, number of bytes, I2C stop
        sends:    53    ,        A0    ,       01       ,    00   ,    53    ,     A1      ,       10       ,    50
        '''   
        serialData = []
        self.SM.OpenPort()   
        
        for i in range(2): 
            self.SM.Send(b'53A0010053A11e50')
           #self.SM.Send(b'53A0010053A10150')   
            time.sleep(0.05) #allow time for the data to be received  
            
        serialData = self.SM.Read()
        self.SM.ClosePort()
        
        return serialData

    def ProbePresent(self):
        '''
        Returns True if a probe is present, False if not
        '''   
        try:        
        #get the IO byte
            self.SM.OpenPort()
            self.SM.Send(b'4950')   
            time.sleep(0.05) #allow time for the data to be received  
            IOByte = self.SM.Read()
            self.SM.ClosePort()
        except:
            print("unable to tell if probe is there")
        #get the relevant bit
        bits = BitArray(hex=IOByte)
        bit = bits.bin[2:3]
        print("bits \n\n{}".format(bit))
        #check to see if the pin is pulled low by the probe
        if bit == '0':
            return True
        else:
            return False
        
    def ReadFirstByte(self):
        '''
        returns a single byte as a 2 character string
        '''
        self.SM.OpenPort()         #open the port
        self.SM.Send(b'53A0010053A10150') #write data to request first byte from the probe EEPROM
        time.sleep(0.05) #allow time for the data to be received  
        firstByte = self.SM.Read() #read the first byte
        self.SM.ClosePort()

        return firstByte
    
    def ProbeReadAllBytes(self):
        '''
        Returns a 32 character string of the first 16 bytes of the probe's memory
        
        
        sends: I2c start, write address, number of bytes, data... , I2C start, read address, number of bytes, I2C stop
        sends:    53    ,        A0    ,       01       ,    00   ,    53    ,     A1      ,       10       ,    50
        '''   
        serialData = []
        self.SM.OpenPort()   
        

        self.SM.Send(b'53A0010053A11e50')  
        time.sleep(0.05) #allow time for the data to be received     
        serialData = self.SM.Read()
        
        self.SM.Send(b'53A0011e53A11e50')
        time.sleep(0.05)
        serialData = serialData + self.SM.Read()

        self.SM.Send(b'53A0013c53A11e50')
        time.sleep(0.05)
        serialData = serialData + self.SM.Read()
        
        self.SM.Send(b'53A0015A53A11e50')
        time.sleep(0.05)
        serialData = serialData + self.SM.Read()

        self.SM.Send(b'53A0017853A11e50')
        time.sleep(0.05)
        serialData = serialData + self.SM.Read()
        
        self.SM.Send(b'53A0019653A11e50')
        time.sleep(0.05)
        serialData = serialData + self.SM.Read()
        
        self.SM.Send(b'53A001B453A11e50')
        time.sleep(0.05)
        serialData = serialData + self.SM.Read()
        
        self.SM.Send(b'53A001D253A11e50')
        time.sleep(0.05)
        serialData = serialData + self.SM.Read()
        
        self.SM.Send(b'53A001F053A11050')
        time.sleep(0.05)
        serialData = serialData + self.SM.Read()
        
        self.SM.ClosePort()
        
        return serialData
   

class SerialManager(object):
    '''
    A wrapper for TaTT specific PySerial usage.
    '''
    
    def __init__(self):
        self.ser = False
        
    def ConfigurePort(self, port):
        session_data = []
       
        with open('file.ptt', 'rb') as file:
      
            # Call load method to deserialze
            myvar = pickle.load(file)
        session_data.extend(myvar)
        
        file.close()
        print("session data before{}".format(session_data))
        self.ser = serial.Serial(port = port, baudrate = 9600, \
            parity = serial.PARITY_NONE, \
            stopbits = serial.STOPBITS_ONE, \
            bytesize  = serial.EIGHTBITS, \
            timeout  = 0, \
             )
        
        
        self.ser.close()
        
        session_data.append(self.ser.port)

        with open('file.ptt', 'wb') as file:
            pickle.dump(session_data, file)
        file.close()
        print("session data after {}".format(session_data))

    def Send(self, input):
        '''
        pass in hex bytes, send the whole lot down the serial port.
        '''
        
        #flush the buffers
        self.ser.flushInput()   
        self.ser.flushOutput() 
        
        #convert the input to ASCII characters and send it
        self.ser.write(codecs.decode(input, "hex_codec"))

        
    def Read(self):
        '''
        reads the contents of the serial buffer and returns it as a string 
        of hex bytes
        '''
        serialData = ''

        while self.ser.inWaiting() > 0:
            b = binascii.hexlify(self.ser.read(1))
            serialData += codecs.decode(b) 
        
        return serialData
    
    def OpenPort(self):
        '''
        Opens the port, readying it for communication
        '''
        
        self.ser.open()
    
    def ClosePort(self):
        '''
        Closes the port
        '''
        self.ser.close()
    
    
class ProbeData(object):
    '''
    Responsible for creating the full 256 bytes of EEPROM data.
    '''
    pass
    
    def __init__(self):
        '''
        '''
        self.timeStamp = ''
        self.typeBytes = ''
        
        self.DP240TypeBytes = ['50','46','30','4a']
        self.DP12TypeBytes = ['50','30','43','4a']
        self.DP6TypeBytes = ['50','30','36','4a']
        self.I2CTypeBytes = ['50','34','38','4a']
        self.I2PTypeBytes = ['50','31','38','4a']
        self.I2STypeBytes = ['50','30','36','4a']
        self.KDP72TypeBytes = ['50','34','38','4a']
        self.SDP30TypeBytes = ['53','33','30','4a']

    
    def GenerateDataString(self, probeType):
        '''
        Pass in a probe type, returns the full 255 byte probe data including time stamped serial number
        
        The first 8 and last 2 values of each list item are for SC18IM configuration, the bytes inbetween are that actual data that is written
        '''
        probezeros = ['53A00900000000000000000050', '53A00908000000000000000050', '53A00910000000000000000050', '53A00918000000000000000050', '53A00920000000000000000050', '53A00928000000000000000050', '53A00930000000000000000050', '53A00938000000000000000050', '53A00940000000000000000050', '53A00948000000000000000050', '53A00950000000000000000050', '53A00958000000000000000050', '53A00960000000000000000050', '53A00968000000000000000050', '53A00970000000000000000050', '53A00978000000000000000050', '53A00980000000000000000050', '53A00988000000000000000050', '53A00990000000000000000050', '53A00998000000000000000050', '53A009a0000000000000000050', '53A009a8000000000000000050', '53A009b0000000000000000050', '53A009b8000000000000000050', '53A009c0000000000000000050', '53A009c8000000000000000050', '53A009d0000000000000000050', '53A009d8000000000000000050', '53A009e0000000000000000050', '53A009e8000000000000000050', '53A009f0000000000000000050', '53A009f8000000000000000050']
        probeData = ['53A00910303030303030303050', '53A00918303030303030303050', '53A00920303030303030303050', '53A00928303030303030300050', '53A009303001f00a3030303050', '53A00938303030303030303050', '53A009402863292044656c7450', '53A009486578204d6564696350', '53A00950616c204c696d697450', '53A00958656420323030370050', '53A00960303030303030303050', '53A00968303030303030303050', '53A00970303030303030303050', '53A00978303030303030303050', '53A00980303030303030303050', '53A00988303030303030303050', '53A00990303030303030303050', '53A00998303030303030303050', '53A009a0303030303030303050', '53A009a8303030303030303050', '53A009b0303030303030303050', '53A009b8303030303030303050', '53A009c0303030303030303050', '53A009c8303030303030303050', '53A009d0303030303030303050', '53A009d8303030303030303050', '53A009e0303030303030303050', '53A009e8303030303030303050', '53A009f0303030303030303050', '53A009f8303030303030303050']
        SDprobeData = ['53A00910303030303030303050', '53A00918303030303030303050', '53A00920303030303030303050', '53A00928303030303030300050', '53A0093030fafa1e3030303050', '53A00938303030303030303050', '53A009402863292044656c7450', '53A009486578204d6564696350', '53A00950616c204c696d697450', '53A00958656420323030370050', '53A00960303030303030303050', '53A00968303030303030303050', '53A00970303030303030303050', '53A00978303030303030303050', '53A00980303030303030303050', '53A00988303030303030303050', '53A00990303030303030303050', '53A00998303030303030303050', '53A009a0303030303030303050', '53A009a8303030303030303050', '53A009b0303030303030303050', '53A009b8303030303030303050', '53A009c0303030303030303050', '53A009c8303030303030303050', '53A009d0303030303030303050', '53A009d8303030303030303050', '53A009e0303030303030303050', '53A009e8303030303030303050', '53A009f0303030303030303050', '53A009f8303030303030303050']

        firstStart = '53A00900'
        secondStart = '53A00908'
        end = '50'
        
        if probeType == 'Blank':
            return probezeros
        
        #set the correct probe type bytes
        if probeType == 'DP240':
            typeBytes = self.DP240TypeBytes
        elif probeType == 'DP12':
            typeBytes = self.DP12TypeBytes
        elif probeType == 'DP6':
            typeBytes = self.DP6TypeBytes
        elif probeType == 'I2C':
            typeBytes = self.I2CTypeBytes
        elif probeType == 'I2S':
            typeBytes = self.I2STypeBytes
        elif probeType == 'I2P':
            typeBytes = self.I2PTypeBytes
        elif probeType == 'KDP72':
            typeBytes = self.KDP72TypeBytes
        elif probeType == 'I2P':
            typeBytes = self.I2PTypeBytes
        elif probeType == 'SDP30':
            typeBytes = self.SDP30TypeBytes
            
        #create a 12 byte timestamp of the format
        timeStamp = strftime("%Y%m%d%H%M%S", gmtime())
        timeStampFormatted = timeStamp[2:]
        timeStampASCII = []
        for item in timeStampFormatted:
            x = (ord(item))
            timeStampASCII.append(format((x), "x"))
        
        #stick the type bytes and the timestamp together 
        serialNumber = typeBytes + timeStampASCII
        
        #put them in a format that can be sent via the SC18IM
        lower  = serialNumber[0:8]
        upper = serialNumber[8:]
        slower = ''.join(lower)
        supper = ''.join(upper)
        firstByte = firstStart + slower + end
        secondByte = secondStart + supper + end
        
        #add them to the probe data list
        SDprobeData.insert(0, secondByte)
        SDprobeData.insert(0, firstByte)
        
        #create a single string of the actual data for error checking
        stripped = ''
        for item in SDprobeData:
            stripped = stripped + item[8:-2]
        return SDprobeData, stripped


# PI = PI()
# PD = ProbeData()
# PI.Connect('COM3')
# sn = PI.ProbeReadAllBytes()
# 
# print(sn)
