'''
Created on 28 Apr 2017

@author: jackw
'''
import PI
import InstrumentManager as IM
import BatchManager
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
        
     
  
    def ConnectToProbeInterface(self, com_port):
        '''
        Pass in a com port ID (COMX) and connect to that com_port.
        '''
        
        
        self.ser = self.PI.Connect(com_port)
      
        if com_port == self.ser.port:
            self.PI.SM.ClosePort(self.ser)
            return True
        else:
            return False
        
    
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
    

    
    def TestProbe(self):
        
        try:
            r = self.ZND.get_trace_values()
            r = True
        except:
            r = False
        
        return r
        
    def ProgramProbe(self, probe_type):
        '''
        pass in a string containing the probe type
        program the probe as that type
        returns the probes serial number if programming was succesful, False if not
        '''
        probeData = self.PD.GenerateDataString(probe_type)
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

        if x in ['30','32','34','35','36','38','46']: #Probe type codes in decimal
            return True
        else:
            return False

    def read_serial_number(self):
        return self.PI.ReadSerialNumber()

class Probe(object):
    
    def __init__(self):
        pass


        
