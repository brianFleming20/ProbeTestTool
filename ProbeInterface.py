'''
Created on 28 Apr 2017

@author: jackw
'''
import serial
from serial import Serial
import codecs
import binascii
from time import gmtime, strftime
import time
from bitstring import BitArray
import datastore
import pyvisa as visa
import PI



DS = datastore.DataStore()
PD = PI.ProbeData()

class PRI(object):
    
    def __init__(self):
        self.loggedInUser = False
        self.ser = None
        



    def get_serial_port(self):
        port = DS.get_probe_port()
        self.ser = serial.Serial(port = port, baudrate = 9600, \
                parity = serial.PARITY_NONE, \
                stopbits = serial.STOPBITS_ONE, \
                bytesize  = serial.EIGHTBITS, \
                timeout  = 0, \
                )
        
        
    
    def check_port_number(self, com_port):
        return True
        
        
        
        
        
    def probe_present(self):
        '''
        Returns True if a probe is present, False if not
        '''  
        self.get_serial_port()
        bit = self.send_probe_bits()
        self.ser.close()
        #check to see if the pin is pulled low by the probe
        if bit == '0':
            return True
        else:
            return False
        
    
    def send_probe_bits(self):
        self.send_data(b'4950')   
        time.sleep(0.05) #allow time for the data to be received  
        IOByte = self.read_data()
        bits = BitArray(hex=IOByte)
        bit = bits.bin[2:3]
        return bit
        
        
        
    def read_first_bytes(self):
        '''
        returns a single byte as a 2 character string
        '''
        self.get_serial_port()
        self.send_data(b'53A0010053A10150') #write data to request first byte from the probe EEPROM
        time.sleep(0.05) #allow time for the data to be received  
        first_byte = self.read_data() #read the first byte
        self.ser.close()
        if first_byte in ['30','32','34','35','36','38','46']: #Probe type codes in decimal
            return True
        else:
            return False

    
    
    def read_serial_number(self):
        '''
        returns a single byte as a 2 character string
        '''
        self.get_serial_port()
        self.send_data(b'53A0010053A11e50') #write data to request first byte from the probe EEPROM
        time.sleep(0.05) #allow time for the data to be received  
        sn = self.read_data() #read the first byte
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
        time.sleep(0.05) #allow time for the data to be received     
        serialData = self.read_data()

        self.send_data(b'53A0011e53A11e50') 
        time.sleep(0.05)
        serialData = serialData + self.read_data()

        self.send_data(b'53A0013c53A11e50')
        time.sleep(0.05)
        serialData = serialData + self.read_data()
        
        self.send_data(b'53A0015A53A11e50') # read 0's
        time.sleep(0.05)
        serialData = serialData + self.read_data()

        self.send_data(b'53A0017853A11e50') # read 0's
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
        
        self.send_data(b'53A001F053A11050') # read 0's
        time.sleep(0.05)
        serialData = serialData + self.read_data()
        
        self.ser.close()
        
        return serialData
    
    
    
    def check_probe_connection(self, ports):
        port = "not_connected"
        read_check = '1'
        for p in ports:
                self.ser = serial.Serial(port = p, baudrate = 9600, \
                parity = serial.PARITY_NONE, \
                stopbits = serial.STOPBITS_ONE, \
                bytesize  = serial.EIGHTBITS, \
                timeout  = 0, \
                    )
                probe_out = self.send_probe_bits()
                self.ser.close()
                if read_check == probe_out:
                    port = p
        return port         
        
        
        
    def send_data(self, data):
        '''
        pass in hex bytes, send the whole lot down the serial port.
        '''
        #flush the buffers
     
        self.ser.flushInput()   
        self.ser.flushOutput() 
      
        #convert the input to ASCII characters and send it
        sent = self.ser.write(codecs.decode(data, "hex_codec"))
       



    def read_data(self):
        '''
        reads the contents of the serial buffer and returns it as a string 
        of hex bytes
        '''
        serialData = ''

        while self.ser.inWaiting() > 0:
            b = binascii.hexlify(self.ser.read(1))
            serialData += codecs.decode(b) 
        
        return serialData
    
    
    