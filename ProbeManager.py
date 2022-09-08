'''
Created on 28 Apr 2017
@author: jackw
'''
import PI
import InstrumentManager
import NanoZND
import Datastore
import ProbeInterface
import codecs

PF = ProbeInterface.PRI()
DS = Datastore.Data_Store()
IM = InstrumentManager


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
        self.debugResults = [[1, 1, 1, ], [2, 2, 2], [3, 3, 3]]
        self.serial = None
        self.dev = dev
        self.show = False

    def TestProbe(self):

        return True

    def ProgramProbe(self, probe_type, test):
        '''
        pass in a string containing the probe type
        program the probe as that type
        returns the probes serial number if programming was succesful, False if not
        '''
        result = False

        if self.test_chip():
            probeData = self.PD.GenerateDataString(probe_type, test)

        ######################################################
        # get first two lots of 8 bights for error checking  #
        # write the data to the probe                        #
        ######################################################
            if not probeData:
                result = False
            else:
                PF.probe_write(probeData[0])
        ##############################################
        # check to see if programming was successful #
        ##############################################
            pd = ''.join(probeData[1])
            check = PF.read_all_bytes()
            if check == pd:
                result = PF.read_serial_number()

            return result

    def test_chip(self):
        check = True
        data = self.PD.GenerateDataString("blank",True)
        PF.probe_write(data)
        result = PF.read_all_bytes()
        for num in result:
            if not num == '0':
                check = False
        return check

    def ProbePresent(self):
        '''
        returns True of a probe is inserted into Probe Interface, false if not
        '''
        if PF.probe_present():
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

    def construct_new_serial_number(self,serial_number, test):
        converted = self.PD.convert_to_hex(serial_number)
        data,stripped = self.PD.create_serial_data(converted,test)
        PF.probe_write(data)
        # pcb_serial_number = PF.read_serial_number()
        # binary_str = codecs.decode(pcb_serial_number, "hex")
        # print(f"serial number now = {str(binary_str)[2:18]}")

    def blank_probe(self):
        data = self.PD.GenerateDataString("blank", True)
        PF.probe_write(data)


