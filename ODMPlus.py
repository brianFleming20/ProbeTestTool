'''
Created on 24 Apr 2017

@author: Brian F
'''


import tkinter.messagebox as tm
import serial
import datastore
from bitstring import BitArray

DS= datastore.DataStore()

class ODMData(object):
    
    def __init__(self):
        self.connectedinstrument = False
        self.port_read = ""
        self.port_control = ""
        self.monitor_port = ""
        self.odm_port = None
        
  
    def get_odm_port(self):
        port_number = DS.get_ODM_port()
        self.odm_port = serial.Serial()
        self.odm_port.baudrate = '9600'
        self.odm_port.port = port_number
        self.odm_port.bytesize = 8
        self.odm_port.timeout = 1
        
        
        
    def close_port(self):
        self.odm_port.close()
        
        
    def check_port_open(self):
        if self.odm_port == None:
            self.get_odm_port() 

    
        
    def ReadSerialODM(self):
        # initalise parameters
        ignor_bit = 44
        odm_result = []
        temp = ""
        parameters = ''
        # Set up port connection
        self.check_port_open()
        self.odm_port.open()
        
        parameters = self.odm_port.readline() # read line of ODM
        for data in parameters:
            temp += chr(data)
            if data == ignor_bit:
                odm_result.append(temp[:-1])
                temp = ""                              
        self.close_port()                     
        return odm_result                             


    
    def get_monitor_port(self):
        # read = [0,0,0,0,"not_connected"]
        read = self.ReadSerialODM()
        if read == []:
            return False
        else:
            if isinstance(read[3], int):
                return True
      
    # def GetODMParameters(self):
    #     packet = bytearray()
        
    #     found_item = "r"
    #     stop_item = ""
    #     serial_result = []
    #     port = "COM5"
    #     # Access port at 19200 Baud in ODM extebded mode
    #     serialPort = serial.Serial(port = port, 
    #                                baudrate=19200,
    #                                bytesize=8,
    #                                timeout=4,
    #                                parity = serial.PARITY_NONE,
    #                                stopbits=serial.STOPBITS_ONE)
    #     # Send command for patient info
    #     packet.append(0x1B)
    #     packet.append(0x52)
    #     packet.append(0x50)
    #     packet.append(0x0D)
    #     packet.append(0x0A)
        
    #     serialPort.write(packet)
    #     parameter = serialPort.read().decode('Ascii')
    #     # Collect the patient info into a list
    #     while parameter != found_item:
    #         parameter = serialPort.read().decode('Ascii')
            
    #     while parameter != stop_item:
    #         parameter = serialPort.read().decode('Ascii')
    #         serial_result.append(parameter)
            
    #     serialPort.close()
    #     # print(serial_result)
        
    # def GetPatientParamerts(self):
    #     packet_select = bytearray()
    #     packet_read = bytearray()
        
    #     found_item = "-"
    #     stop_item = "\r"
    #     ignor_bit = ","
    #     error_bit = "\n"
    #     serial_result = []
    #     serial_temp = ""
    #     port = "COM5"
    #     # Access port at 19200 Baud in ODM extended mode
    #     serialPort = serial.Serial(port = port, 
    #                                baudrate=19200,
    #                                bytesize=8,
    #                                timeout=4,
    #                                parity = serial.PARITY_NONE,
    #                                stopbits=serial.STOPBITS_ONE)
    #     # Send command for selecting parameters 
    #     packet_select.append(0x1B)
    #     packet_select.append(0x53)
    #     packet_select.append(0x20)
    #     packet_select.append(0x53)
    #     packet_select.append(0x44)
    #     packet_select.append(0x2C)
    #     packet_select.append(0x46)
    #     packet_select.append(0x54)
    #     packet_select.append(0x2C)
    #     packet_select.append(0x50)
    #     packet_select.append(0x56)
    #     packet_select.append(0x0D)
    #     packet_select.append(0x0A)
    #     # command for reading the selected parameters returned
    #     packet_read.append(0x1B)
    #     packet_read.append(0x52)
    #     packet_read.append(0x4C)
    #     packet_read.append(0x44)
    #     packet_read.append(0x0D)
    #     packet_read.append(0x0A)
    #     # sending commands to ODM extended version
    #     serialPort.write(packet_select)
    #     parameter = serialPort.read(2).decode('Ascii')
    #     # print(parameter)
    #     # pause between commands sent
        
    #     serialPort.write(packet_read)
    #     temp = serialPort.read().decode('Ascii')
       
    #     # Collect the patient info into a list
    #     while temp != found_item:
    #         temp = serialPort.read().decode('Ascii')
            
    #     parameter = serialPort.read(40).decode('Ascii')
    #     parameter = parameter[1:]
    #     parameter = parameter + ignor_bit
    #     # print(parameter)

    #     for str in parameter:
    #         if str != ignor_bit:
    #             serial_temp = serial_temp + str
    #             if str == error_bit:
    #                 serial_temp = serial_temp[:-2]
    #         else:
    #             serial_result.append(serial_temp)
    #             serial_temp = ""       
        
    #     serial_result.pop(0)
    #     serialPort.close()
    #     # print(serial_result)
    #     return serial_result
    
    
    
    def check_odm_port(self, port):
        self.get_odm_port()
        if self.odm_port.port == port:
            self.close_port()
            return True
        else:
            self.close_port()
            return False
        
        
    def read_data(self):
        return self.odm_port.read().decode('ascii')
    
    
        