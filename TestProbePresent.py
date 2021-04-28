'''
Created on 12 Jan 2019

@author: jackw
'''
import serial
import codecs
import binascii
import time
from bitstring import BitArray



class PI(object):
    """
    Top level object for Probe Interface interaction
    """
    
    def __init__(self):
        self.loggedInUser = False
        self.SM = SerialManager()
    
    def Connect(self, comPort):
        '''
        pass in comport number, configures port. 
        '''
        self.ser = self.SM.ConfigurePort(comPort)

    def ProbePresent(self):
        '''
        Returns True if a probe is present, False if not
        '''          
        #get the IO byte
        self.SM.OpenPort()
        self.SM.Send(b'4950')   
        time.sleep(0.05) #allow time for the data to be received  
        IOByte = self.SM.Read()
        self.SM.ClosePort()
        #get the relevant bit
        bits = BitArray(hex=IOByte)
        bit = bits.bin[2:3]
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
   

class SerialManager(object):
    '''
    A wrapper for TaTT specific PySerial usage.
    '''
    
    def __init__(self):
        self.ser = False
        
    def ConfigurePort(self, port):
        self.ser = serial.Serial(port = port, baudrate = 9600, \
            parity = serial.PARITY_NONE, \
            stopbits = serial.STOPBITS_ONE, \
            bytesize  = serial.EIGHTBITS, \
            timeout  = 0, \
             )

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
    
    def OpenPort(self):
        '''
        Opens the port
        '''
        self.ser.open()
    
    def ClosePort(self):
        '''
        Closes the port
        '''
        self.ser.close()


PI = PI()
PI.Connect('COM7')
pp = None
while(1):
    pp = PI.ProbePresent()
    print(pp)
    time.sleep(2)    
    


