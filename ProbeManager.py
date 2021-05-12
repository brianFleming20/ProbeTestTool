'''
Created on 28 Apr 2017

@author: jackw
'''
import PI
import InstrumentManager as IM
import BatchManager
import serial
from serial.tools import list_ports
import struct
import NanoZND


BM = BatchManager.BatchManager()

class ProbeManager(object):
    '''
    classdocs
    '''
   

    def __init__(self, dev=None):
        '''
        Constructor
        '''
        self.PI = PI.PI()
        self.PD = PI.ProbeData()
        self.NanoZND = NanoZND.NanoZND()
        self.ZND = IM.ZND()
        self.testResults = []
        self.debugResults = [[1,1,1,],[2,2,2],[3,3,3]]
        self.serial = None
        self.dev = dev 
        
     
  
    def ConnectToProbeInterface(self, comPort):
        '''
        Pass in a com port ID (COMX) and connect to that comport.
        '''
        
        self.PI.Connect(comPort)
        
    
    def ConnectToAnalyzer(self, port):
        self.NanoZND.SetAnalyserPort(port)
        # self.NanoZND.AccessPortRead()
         
        
    def set_sweep(self, start, stop):
        if start is not None:
            self.send_command("sweep start %d\r" % start)
        if stop is not None:
            self.send_command("sweep stop %d\r" % stop)
    
   
    
    def ConfigureVNA(self):
        self.ZND.Configure()
        
    
    # def ClearAnalyzer(self):
    #     self.ZND.refresh_traces()
    

    
    def TestProbe(self, serialNumber, batchNumber, user):
        # self.ZND.refresh_traces()
        r = self.ZND.get_trace_values(serialNumber, user)
        
        return r
        
    def ProgramProbe(self, probeType):
        '''
        pass in a string containing the probe type
        program the probe as that type
        returns the probes serial number if programming was succesful, False if not
        '''
        probeData = self.PD.GenerateDataString(probeType)
        # get first two lots of 8 bights for error checking

        #write the data to the probe
        self.PI.ProbeWrite(probeData[0])
        
        #check to see if programming was succesful
        pd = ''.join(probeData[1])
        check = self.PI.ProbeReadAllBytes()
        if check == pd:
            sn = self.PI.ProbeReadSerialNumber()
            return sn
        else:
            return False
        
    def ProbePresent(self):
        '''
        returns True of a probe is inserted into PI, false if not
        '''
        if self.PI.ProbePresent() == True:
            return True
        else:
            return False
    
    def ProbeIsProgrammed(self):
        '''
        Checks to see if the first byte of the eeprom is programmed with the probe type byte,
        returns true if it is, false if not
        '''
        x = self.PI.ReadFirstByte()

        if x in ['48','49','50','51','52','53','54','55','56','57']: #Probe type codes in decimal
            return True
        else:
            return False



class Probe(object):
    
    def __init__(self):
        pass


        
