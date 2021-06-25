'''
Created on 12 Jan 2019

@author: jackw

Tests communication with the probes EEPROM. 

Writes a series of ones and zeros and reads them back to make sure read/writes can be performed correctly.

Should print in a loop:

00000000000000
11111111111111


'''
import serial
import codecs
import binascii
import time



class PI(object):
    """
    Object for top level interaction with the PI
    """
    
    def __init__(self):
        self.loggedInUser = False
        self.SM = SerialManager()
    
    def Connect(self, com_port):
        self.ser = self.SM.ConfigurePort(com_port)
            
    def ProbeWrite(self, data):
        '''
        pass in a list of bytes, writes a byte at a time to the probe
        '''
        
        self.SM.OpenPort()

        for item in data:
            self.SM.Send(item)
            time.sleep(0.01)
        self.SM.ClosePort()
            
    def ProbeRead(self):
        '''
        Returns a string of the first 14 bytes of the probe's memory (modified from TaTT object ProbeReadSerialNumber)
        '''   
        serialData = []
        self.SM.OpenPort()   
        
        for i in range(2): 
            self.SM.Send(b'53A0010053A11050')   
            time.sleep(0.05) #allow time for the data to be received  
            
        serialData = self.SM.Read()
        self.SM.ClosePort()
        
        return serialData[2:16]

    
   

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
        Opens the port, readying it for communication
        '''
        self.ser.open()
    
    def ClosePort(self):
        '''
        Closes the port
        '''
        self.ser.close()
    
    


PI = PI()

zeros = ['53A00900500000000000000050']
ones = ['53A00900501111111111111150']


PI.Connect('COM7')

while(1):
    PI.ProbeWrite(zeros)
    print(PI.ProbeRead())
    time.sleep(1)
    PI.ProbeWrite(ones)
    print(PI.ProbeRead())
    time.sleep(1)



