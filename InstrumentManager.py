'''
Created on 24 Apr 2017
@author: jackw
'''

# import pyvisa as visa
import serial
import time
# import ProbeManager as PM


class InstrumentationManager(object):
    """
    Not sure why I gave this it's own class, fix it. give ZND 'isConnected' bool
    """
    # rm = visa.ResourceManager()
    # rm.list_resources()

    def __init__(self):
        self.connectedinstrument = False


class ZND(object):
    def __init__(self):
        self.device_details = ''
        # self.rm = visa.ResourceManager('@py')
        self.HISLIPAddress = ''

        self.znd = False
        self.RxRL = None
        self.TxRL = None
        self.RxMinFreq = None
        self.RxMinMag = None
        self.TxMinFreq = None
        self.TxMinMag = None
        self.IM = InstrumentationManager()

    def SetAddress(self, USBAddress):
        '''
        Pass in the IP address of the VNA, Sets the HISLIP address
        '''
        print("inside set address" + USBAddress)
        # dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)
        # self.HISLIPAddress = 'TCPIP::' + IPAddress + '::HISLIP0'
        # self.HISLIPAddress = 'USB::' + USBAddress + '::INSTR'

    def TestConnection(self):
        '''
        Tests the connection to the VNA, returns the VNA's ID
        '''
        # self.znd = self.rm.open_resource(self.HISLIPAddress)
        # self.device_details = self.znd.query("*IDN?")[:-2]
        # self.znd.close()

    # def Reset(self):
    #     '''
    #     Reset the analyser to a fixed state
    #     '''
    #     self.znd = self.rm.open_resource(self.HISLIPAddress)
    #     #initial instrument configuration
    #     self.znd.write("*RST") #resets the instrument
    #     self.znd.write("*CLS") # clears the error queue
    #     self.znd.close()

    def Configure(self):
        '''
        Configures the analyser with the following windows:
        Window 1: S12, S21 dBmag
        Window 2: S11, S22 Smith
        Window 3: S11, S22 dBmag
        '''
        self.znd = self.rm.open_resource(self.HISLIPAddress)
        # initial instrument configuration
        self.znd.write("*RST")  # resets the instrument
        self.znd.write("*CLS")  # clears the error queue
        self.znd.write("INITiate:CONTinuous:ALL OFF")  # put it in single sweep mode
        self.znd.write("CALC1:PAR:DEL:ALL")  # clear the default trace
        self.znd.write("FREQ:STAR 3MHz")  # set start frequency value
        self.znd.write("FREQ:STOP 5MHz")  # set stop frequency value

        # configure each window
        # config window1 as S12, S21 dBmag
        self.znd.write("DISP:WIND1:STAT ON")  # create a window area no.1
        self.znd.write("CALC1:PAR:SDEF 'Ch1Tr1', 'S21'")  # create an S21 trace on channel 1
        self.znd.write("DISP:WIND1:TRAC1:FEED 'CH1TR1'")  # place the trace in the window
        self.znd.write("CALC1:PAR:SDEF 'Ch1Tr2', 'S12'")  # create an S12 trace on channel 1
        self.znd.write("DISP:WIND1:TRAC2:FEED 'CH1TR2'")  # place the trace in the window

        # config window2 as S22, S11 smith
        self.znd.write("DISP:WIND2:STAT ON")  # create a window area no.2
        self.znd.write("CALC2:PAR:SDEF 'Ch2Tr1', 'S22'")  # create an S22 trace on channel 2
        self.znd.write("CALCulate2:FORMat SMITh")
        self.znd.write("DISP:WIND2:TRAC3:FEED 'CH2Tr1'")  # display the trace in window 2
        self.znd.write("CALC3:PAR:SDEF 'Ch2Tr2', 'S11'")  # create an S11 trace on channel 2
        self.znd.write("CALCulate3:FORMat SMITh")
        self.znd.write("DISP:WIND2:TRAC4:FEED 'CH2Tr2'")  # display the trace in window 2

        # config window3 as S11, S22 dBmag
        self.znd.write("CALC4:PAR:SDEF 'Ch3Tr1', 'S22'")  # create an S22 trace on channel 3
        self.znd.write("CALC4:PAR:SDEF 'Ch3Tr2', 'S11'")  # create an S11 trace on channel 3
        self.znd.write("DISP:WIND3:STAT ON")  # create a window area no.3
        self.znd.write("DISP:WIND3:TRAC5:FEED 'CH3TR1'")  # display the trace in the window
        self.znd.write("DISP:WIND3:TRAC6:FEED 'CH3TR2'")  # display the trace in the window
        self.znd.write("DISP:WIND3:TRAC5:Y:PDIV 2")  # change scale to 2db per div
        self.znd.write("DISP:WIND3:TRAC6:Y:PDIV 2")  # change scale to 2db per div

        self.znd.close()

    # def refresh_traces(self):
    #     self.znd = self.rm.open_resource(self.HISLIPAddress)
    #     #refresh calc 1 and update traces
    #     self.znd.write("INITiate1:IMMediate; *WAI")
    #     self.znd.write("CALCulate1:PARameter:SELect 'CH1TR1'") #select trace for marker
    #     self.znd.write("CALCulate1:MARKer1:STATe ON") #set marker to center of sweep range
    #     self.znd.write("CALCulate1:MARKer1:FUNCtion:EXECute MIN") #Use the delta marker to search for the minimum of the trace and query the result. the query returns the stimulus and the response value at the marker position
    #     self.znd.write("CALCulate1:MARKer1:DELTa:STATe ON") #this command also creates the reference marker # make this on the trough
    #     self.znd.write("CALCulate1:MARKer1:REFerence:X 4.02 MHz") #set the  delta reference marker to the beginning of the sweep range
    #     self.znd.write("CALCulate1:PARameter:SELect 'CH1TR2'") #select trace for marker
    #     self.znd.write("CALCulate1:MARKer1:STATe ON") #set marker to center of sweep range
    #     self.znd.write("CALCulate1:MARKer1:FUNCtion:EXECute MIN") #Use the delta marker to search for the minimum of the trace and query the result. the query returns the stimulus and the response value at the marker position
    #     self.znd.write("CALCulate1:MARKer1:DELTa:STATe ON") #this command also creates the reference marker # make this on the trough
    #     self.znd.write("CALCulate1:MARKer1:REFerence:X 4.02 MHz") #set the  delta reference marker to the beginning of the sweep range

    #     #refresh calc 2 and update traces
    #     self.znd.write("INITiate2:IMMediate; *WAI")
    #     self.znd.write("CALCulate2:PARameter:SELect 'CH2TR1'") #select trace for marker
    #     self.znd.write("CALCulate2:MARKer1:STATe ON") #set marker to center of sweep range
    #     self.znd.write("CALCulate2:MARKer1:REFerence:X 4.02 MHz") #set the  delta reference marker to the beginning of the sweep range

    #     #refresh calc 3
    #     self.znd.write("INITiate3:IMMediate; *WAI")
    #     self.znd.write("CALCulate3:PARameter:SELect 'CH2TR2'") #select trace for marker
    #     self.znd.write("CALCulate3:MARKer1:STATe ON") #set marker to center of sweep range
    #     self.znd.write("CALCulate3:MARKer1:REFerence:X 4.02 MHz") #set the  delta reference marker to the beginning of the sweep range

    #     #refresh calc 4
    #     self.znd.write("INITiate4:IMMediate; *WAI")
    #     self.znd.write("CALCulate4:PARameter:SELect 'CH3TR1'") #select trace for marker
    #     self.znd.write("CALCulate4:MARKer2:STATe ON") #set marker to center of sweep range
    #     self.znd.write("CALCulate4:MARKer2:FUNCtion:EXECute MIN") #Use the delta marker to search for the minimum of the trace and query the result. the query returns the stimulus and the response value at the marker position
    #     self.znd.write("CALCulate4:MARKer1:STATe ON") #this command also creates the reference marker # make this on the trough
    #     self.znd.write("CALCulate4:MARKer1:X 4.02 MHz") #set the  delta reference marker to the beginning of the sweep range
    #     self.RxRL = self.znd.query("CALCulate4:MARKer1:Y?")
    #     self.RxMinFreq = self.znd.query("CALCulate4:MARKer2:X?")
    #     self.RxMinMag = self.znd.query("CALCulate4:MARKer2:Y?")

    #     self.znd.write("CALCulate4:PARameter:SELect 'CH3TR2'") #select trace for marker
    #     self.znd.write("CALCulate4:MARKer2:STATe ON") #set marker to center of sweep range
    #     self.znd.write("CALCulate4:MARKer2:FUNCtion:EXECute MIN") #Use the delta marker to search for the minimum of the trace and query the result. the query returns the stimulus and the response value at the marker position
    #     self.znd.write("CALCulate4:MARKer1:STATe ON") #this command also creates the reference marker # make this on the trough
    #     self.znd.write("CALCulate4:MARKer1:X 4.02 MHz") #set the  delta reference marker to the beginning of the sweep range
    #     self.TxRL = self.znd.query("CALCulate4:MARKer1:Y?")
    #     self.TxMinFreq = self.znd.query("CALCulate4:MARKer2:X?")
    #     self.TxMinMag = self.znd.query("CALCulate4:MARKer2:Y?")

    #     self.znd.close()

    def get_trace_values(self):
        '''
        This returns a list of lists, with each sub list containing a string of y values for a trace and information about that trace such as:
        -An individual reference number within the batch
        -The start frequency of the sweep
        -The stop frequency of the sweep
        Note: strings returned from the ZND are usually postfixed with a '\n', [:-1] has been used throughout this method to remove this unwanted
        postfix.

        '''
        # self.znd = self.rm.open_resource(self.HISLIPAddress)
        # CH1TR1_Data = []
        # CH1TR2_Data = []
        # CH2TR1_Data = []
        # CH2TR2_Data = []
        # CH3TR1_Data = []
        # CH3TR2_Data = []

        # # startFrequency = self.znd.query("FREQ:STAR?")
        # startFrequency =
        # startFrequency = startFrequency[:-1]

        # # stopFrequency = self.znd.query("FREQ:STOP?")
        # stopFrequency = self.znd.query("FREQ:STOP?")
        # stopFrequency = stopFrequency[:-1]

        # user += ','
        # probeID += ','
        # startFrequency += ','
        # stopFrequency += ','

        # RxRL = self.RxRL[:-1]
        # RxMinFreq = self.RxMinFreq[:-1]
        # RxMinMag = self.RxMinMag[:-1]
        # TxRL = self.TxRL[:-1]
        # TxMinFreq = self.TxMinFreq[:-1]
        # TxMinMag = self.TxMinMag[:-1]
        # RxRL += ','
        # RxMinFreq += ','
        # RxMinMag += ','
        # TxRL += ','
        # TxMinFreq += ','
        # TxMinMag += ','

        # CH1TR1_Data.append(user)
        # CH1TR1_Data.append(probeID)
        # CH1TR1_Data.append('Tx-Rx Insertion Loss,')
        # CH1TR1_Data.append(startFrequency)
        # CH1TR1_Data.append(stopFrequency)
        # CH1TR1_Data.append(self.znd.query("CALC:DATA:TRAC? 'CH1TR1', FDAT")[:-2])

        # CH1TR2_Data.append(user)
        # CH1TR2_Data.append(probeID)
        # CH1TR2_Data.append('Rx-Tx Insertion Loss,')
        # CH1TR2_Data.append(startFrequency)
        # CH1TR2_Data.append(stopFrequency)
        # CH1TR2_Data.append(self.znd.query("CALC:DATA:TRAC? 'CH1TR2', FDAT")[:-2])

        # CH2TR1_Data.append(user)
        # CH2TR1_Data.append(probeID)
        # CH2TR1_Data.append('Rx Smith,')
        # CH2TR1_Data.append(startFrequency)
        # CH2TR1_Data.append(stopFrequency)
        # CH2TR1_Data.append(self.znd.query("CALC:DATA:TRAC? 'CH2TR1', FDAT")[:-2])

        # CH2TR2_Data.append(user)
        # CH2TR2_Data.append(probeID)
        # CH2TR2_Data.append('Tx Smith,')
        # CH2TR2_Data.append(startFrequency)
        # CH2TR2_Data.append(stopFrequency)
        # CH2TR2_Data.append(self.znd.query("CALC:DATA:TRAC? 'CH2TR2', FDAT")[:-2])

        # CH3TR1_Data.append(user)
        # CH3TR1_Data.append(probeID)
        # CH3TR1_Data.append('Rx Return Loss,')
        # CH3TR1_Data.append(startFrequency)
        # CH3TR1_Data.append(stopFrequency)
        # CH3TR1_Data.append(RxRL)
        # CH3TR1_Data.append(RxMinFreq)
        # CH3TR1_Data.append(RxMinMag)
        # CH3TR1_Data.append(self.znd.query("CALC:DATA:TRAC? 'CH3TR1', FDAT")[:-2])

        # CH3TR2_Data.append(user)
        # CH3TR2_Data.append(probeID)
        # CH3TR2_Data.append('Tx Return Loss,')
        # CH3TR2_Data.append(startFrequency)
        # CH3TR2_Data.append(stopFrequency)
        # CH3TR2_Data.append(TxRL)
        # CH3TR2_Data.append(TxMinFreq)
        # CH3TR2_Data.append(TxMinMag)
        # CH3TR2_Data.append(self.znd.query("CALC:DATA:TRAC? 'CH3TR2', FDAT")[:-2])

        rlist = True

        # rlist.append(CH1TR1_Data)
        # rlist.append(CH1TR2_Data)
        # rlist.append(CH2TR1_Data)
        # rlist.append(CH2TR2_Data)
        # rlist.append(CH3TR1_Data)
        # rlist.append(CH3TR2_Data)
        # self.znd.close()
        return rlist

    def get_marker_values(self):
        '''
        Returns a 2 item list of the 4.02MHz return loss values of the format [<Tx>,<Rx>]
        '''
        if len(self.TxRL) < 3 or len(self.RxRL) < 3:
            return 999, 999
        return float(self.TxRL[:-2]), float((self.RxRL[:-2]))

# ZND = ZND()
# ZND.SetAddress('192.168.0.78')
# ZND.Configure()
# ZND.refresh_traces()
# print(ZND.get_marker_values())