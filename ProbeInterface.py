'''
Created on 28 Apr 2017
@author: jackw
'''
import serial
import codecs
import binascii
import time
from bitstring import BitArray
import Datastore
import PI
import serial.tools.list_ports
import sys

DS = Datastore.Data_Store()
PD = PI.ProbeData()


class PRI(object):

    def __init__(self):
        self.loggedInUser = False
        self.ser = None

    def get_serial_port(self):
        port = DS.get_devices()['Probe']
        try:
            self.ser = serial.Serial(port=port)
            self.ser.baudrate = 9600
            self.ser.parity = serial.PARITY_NONE
            self.ser.stopbits = serial.STOPBITS_ONE
            self.ser.bytesize = serial.EIGHTBITS
            self.ser.timeout = 0.25
        except IOError:
            pass

    def get_port_obj(self):
        return self.ser

    def close_port(self):
        self.ser.close()

    def open_port(self):
        self.ser.open()

    def probe_present(self):
        '''
        Returns True if a probe is present, False if not
        '''
        self.get_serial_port()
        if not self.ser.isOpen():
            self.ser.open()

        bit = self.send_probe_bits()
        self.ser.close()
        # check to see if the pin is pulled low by the probe
        if bit == '0':
            return True
        else:
            return False

    def send_probe_bits(self):
        ################################
        # send data to probe interface #
        ################################
        self.send_data(b'4950')
        time.sleep(0.1)  # allow time for the data to be received
        IOByte = self.read_data()
        bits = BitArray(hex=IOByte)
        bit = bits.bin[2:3]
        return bit

    def read_first_bytes(self):
        '''
        returns a single byte as a 2 character string
        '''
        self.get_serial_port()

        ##########################################################
        # write data to request first byte from the probe EEPROM #
        ##########################################################
        self.send_data(b'53A0010053A10150')
        time.sleep(0.05)  # allow time for the data to be received
        #######################
        # read the first byte #
        ######################

        first_byte = self.read_data()
        self.ser.close()

        ###############################
        # Probe type codes in decimal #
        ###############################
        if first_byte in ['32', '36', '35']:
            return True
        else:
            return False

    def read_serial_number(self):
        '''
        returns a single byte as a 2 character string
        '''
        self.get_serial_port()
        #############################################################
        # write data to request serial number from the probe EEPROM #
        #############################################################
        self.send_data(b'53A0010053A11e50')
        time.sleep(0.05)  # allow time for the data to be received
        #######################
        # read the probe data #
        #######################
        sn = self.read_data()
        self.ser.close()

        return sn

    def probe_write(self, data):
        '''
        pass in a list of bytes, writes a byte at a time to the probe
        '''
        self.get_serial_port()
        for item in data:
            self.send_data(item)
            time.sleep(0.01)
        self.ser.close()

    def read_all_bytes(self):
        '''
        Returns a 32 character string of the first 16 bytes of the probe's memory


        sends: I2c start, write address, number of bytes, data... , I2C start, read address, number of bytes, I2C stop
        sends:    53    ,        A0    ,       01       ,    00   ,    53    ,     A1      ,       10       ,    50
        '''

        self.get_serial_port()
        serialData = []

        self.send_data(b'53A0010053A11e50')
        time.sleep(0.05)  # allow time for the data to be received
        serialData = self.read_data()

        self.send_data(b'53A0011e53A11e50')
        time.sleep(0.05)
        serialData = serialData + self.read_data()

        self.send_data(b'53A0013c53A11e50')
        time.sleep(0.05)
        serialData = serialData + self.read_data()

        self.send_data(b'53A0015A53A11e50')  # read 0's
        time.sleep(0.05)
        serialData = serialData + self.read_data()

        self.send_data(b'53A0017853A11e50')  # read 0's
        time.sleep(0.05)
        serialData = serialData + self.read_data()

        self.send_data(b'53A0019653A11e50')
        time.sleep(0.05)
        serialData = serialData + self.read_data()

        self.send_data(b'53A001B453A11e50')
        time.sleep(0.05)
        serialData = serialData + self.read_data()

        self.send_data(b'53A001D253A11e50')
        time.sleep(0.05)
        serialData = serialData + self.read_data()

        self.send_data(b'53A001F053A11050')  # read 0's
        time.sleep(0.05)
        serialData = serialData + self.read_data()

        self.ser.close()

        return serialData

    def check_probe_connection(self):
        result = False

        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):

            self.ser = serial.Serial(port=port, baudrate=9600, parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE,
                                     bytesize=serial.EIGHTBITS,
                                     timeout=0.5)

            if '0403' in hwid:
                result = self.ser.port
        if self.ser:
            self.ser.close()
        return result

    def send_data(self, data):
        '''
        pass in hex bytes, send the whole lot down the serial port.
        '''
        # flush the buffers
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.timeout = 0.2
        # convert the input to ASCII characters and send it
        self.ser.write(codecs.decode(data, "hex_codec"))

    def read_data(self):
        '''
        reads the contents of the serial buffer and returns it as a string
        of hex bytes
        '''
        serialData = ''

        self.ser.flush()
        while self.ser.inWaiting() > 0:
            b = binascii.hexlify(self.ser.readline())
            serialData += codecs.decode(b)
        return serialData

    def line_status(self):
        self.send_data(b'12')
        time.sleep(0.05)  # allow time for the data to be received
        #######################
        # read the first byte #
        ######################

        first_byte = self.read_data()
        print(first_byte)
