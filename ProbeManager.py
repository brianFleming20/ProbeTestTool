'''
Created on 28 Apr 2017

@author: jackw
'''
import PI
import InstrumentManager as IM
import BatchManager
import NanoZND
import ProbeInterface

BM = BatchManager.BatchManager()
PF = ProbeInterface.PRI()

class ProbeManager(object):
    '''
    classdocs
    '''
   

    def __init__(self, dev=None):
        '''
        Constructor
        '''
        self.PD = PI.ProbeData()
        self.NanoZND = NanoZND.NanoZND()
        self.ZND = IM.ZND()
        self.testResults = []
        self.debugResults = [[1,1,1,],[2,2,2],[3,3,3]]
        self.serial = None
        self.dev = dev 
        self.show = False
        
     
  
    def ConnectToProbeInterface(self, com_port):
        '''
        Check for the same port name as sent from the connection class to set 
        correct port number.
        '''
        return PF.check_port_number(com_port)
        
    

    
    def TestProbe(self):
        print("test probe in PM")
        try:
            r = self.ZND.get_trace_values()
            # r = True
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
        PF.probe_write(probeData[0])
            
        #check to see if programming was succesful
        pd = ''.join(probeData[1])
        check = PF.read_all_bytes()
        if check == pd:
                sn = PF.read_serial_number()
                return sn
        else:
                return False
      
        
    def ProbePresent(self):
        '''
        returns True of a probe is inserted into Probe Interface, false if not
        '''
        if PF.probe_present() == True:
            return True
        else:
            return False
    
    def ProbeIsProgrammed(self):
        '''
        Checks to see if the first byte of the eeprom is programmed with the probe type byte,
        returns true if it is, false if not
        '''
        return PF.read_first_bytes()

        

    def read_serial_number(self):
        return PF.read_serial_number()
    

class Probe(object):
    
    def __init__(self):
        pass


        
