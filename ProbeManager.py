'''
Created on 28 Apr 2017
@author: jackw
'''
import PI
import InstrumentManager
# import NanoZND
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

    def __init__(self):
        '''
        Constructor
        '''
        self.PD = PI.ProbeData()
        # self.NanoZND = NanoZND.NanoZND()
        # self.ZND = IM.ZND()
        # self.testResults = []
        # self.debugResults = [[1, 1, 1, ], [2, 2, 2], [3, 3, 3]]
        # self.serial = None

        # self.show = False

    def TestProbe(self):

        return True

    def ProgramProbe(self, probe_type, test):
        '''
        pass in a string containing the probe type
        program the probe as that type
        returns the probes serial number if programming was succesful, False if not
        '''
        ################################################
        # The probe serial number memory is checked    #
        # for errors by writing '0' to the chip. If    #
        # the probe's chip reads all 0's. The probe is #
        # given a serial number. When the serial       #
        # number is given, the probe's serial number   #
        # is read and matched against the first line   #
        # of the raw data.                             #
        ################################################
        if self.test_chip():
            probeData = self.PD.GenerateDataString(probe_type, test)
            if not probeData:
                return probeData
            else:
                PF.probe_write(probeData)
                return self.read_serial_number()
        else:
            return False

    def test_chip(self):
        check = True
        ################################################
        # Checks the probe chip storage by writing     #
        # '0' to the probe and then confining them by  #
        # reading the '0' back.                        #
        ################################################
        blank_data = self.PD.GenerateDataString("ones", True)
        PF.probe_write(blank_data)
        result1 = str(PF.read_all_bytes())
        for num in result1:
            if not num == '1':
                check = False
        blank_data = self.PD.GenerateDataString("blank", True)
        PF.probe_write(blank_data)
        result0 = str(PF.read_all_bytes())
        if len(result0) == 0:
            check = False
        for num in result0:
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
        if PF.probe_present():
            return PF.read_serial_number()
        else:
            return PF.reset_port()


    # def get_serial_number(self):
    #     # sn = self.read_serial_number()
    #     return self.get_converted_serial_number(self.read_serial_number())
    # 53A00900324630443232313050
    # 53A00900323043444661696c50

    def get_converted_serial_number(self, num):
        if not num:
            return num
        else:
            return codecs.decode(num, "hex")[:16].decode()

    def construct_new_serial_number(self, serial_number):
        converted = self.PD.convert_to_hex(serial_number)
        data = self.PD.create_serial_data(converted)
        return PF.probe_write(data)

    def blank_probe(self):
        data = self.PD.GenerateDataString("blank", True)
        PF.probe_write(data)


