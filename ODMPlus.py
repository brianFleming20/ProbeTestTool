'''
Created on 24 Apr 2017

@author: Brian F
'''


import tkinter.messagebox as tm
import serial
import datastore
import time
from bitstring import BitArray
import binascii

DS= datastore.DataStore()

class ODMData(object):
    
    def __init__(self):
        self.connectedinstrument = False
        self.port_read = ""
        self.port_control = ""
        self.monitor_port = ""
        self.odm_port = None
        
  
    def access_odm_port(self, port_number):
            
        self.odm_port = serial.Serial(port = port_number,
                                    baudrate=9600,
                                    bytesize=8,
                                    timeout=1,
                                    parity= serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE)

    
        
    def ReadSerialODM(self):
        # initalise parameters
        found_item = "A"
        stop_item = "\n"
        ignor_bit = ","
        serial_result = []
        temp_add = []
        temp = ""
        
        # ======================
        # Set up port connection
        #=======================
        self.access_odm_port(DS.get_ODM_port())
        # ===========================
        # Access the ODM via the port
        # ===========================
        try:
            parameter = self.odm_port.read().decode('ascii')
            while parameter != found_item:                     # Test for start of parameters
                 parameter = self.odm_port.read().decode('ascii')
        
          
            
            while parameter != stop_item:                      # Test for end of parameters
                parameter = self.odm_port.read().decode('ascii')
                temp = temp + parameter                        # Collect one parameters data
                if parameter == ignor_bit:                     # Test for seperation between parameters
                    temp_add.append(temp[:-1])                 # Add to collection list
                    temp= ""
                serial_result.extend(temp_add)  
        except:
            return False 
                                                            
        self.odm_port.close()                            
        return serial_result                             


    
    def get_monitor_port(self):
        read = ["not_connected"]
        read_wait = "not_connected"
        read_check = ""
        try:
            read = self.ReadSerialODM()
            while read_wait in read:
                read = self.ReadSerialODM()
        except:
            print("odm data error")
        if read_check in read:
            return True
        else:
            return read[0]
        
    
    
    
    #======================================================
    
    # Detecting patient parameters from ODM extended
    
        
    def GetODMParameters(self):
        packet = bytearray()
        
        found_item = "r"
        stop_item = ""
        serial_result = []
        port = "COM5"
        # Access port at 19200 Baud in ODM extebded mode
        serialPort = serial.Serial(port = port, 
                                   baudrate=19200,
                                   bytesize=8,
                                   timeout=4,
                                   parity = serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE)
        # Send command for patient info
        packet.append(0x1B)
        packet.append(0x52)
        packet.append(0x50)
        packet.append(0x0D)
        packet.append(0x0A)
        
        serialPort.write(packet)
        parameter = serialPort.read().decode('Ascii')
        # Collect the patient info into a list
        while parameter != found_item:
            parameter = serialPort.read().decode('Ascii')
            
        while parameter != stop_item:
            parameter = serialPort.read().decode('Ascii')
            serial_result.append(parameter)
            
        serialPort.close()
        # print(serial_result)
        
    def GetPatientParamerts(self):
        packet_select = bytearray()
        packet_read = bytearray()
        
        found_item = "-"
        stop_item = "\r"
        ignor_bit = ","
        error_bit = "\n"
        serial_result = []
        serial_temp = ""
        port = "COM5"
        # Access port at 19200 Baud in ODM extended mode
        serialPort = serial.Serial(port = port, 
                                   baudrate=19200,
                                   bytesize=8,
                                   timeout=4,
                                   parity = serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE)
        # Send command for selecting parameters 
        packet_select.append(0x1B)
        packet_select.append(0x53)
        packet_select.append(0x20)
        packet_select.append(0x53)
        packet_select.append(0x44)
        packet_select.append(0x2C)
        packet_select.append(0x46)
        packet_select.append(0x54)
        packet_select.append(0x2C)
        packet_select.append(0x50)
        packet_select.append(0x56)
        packet_select.append(0x0D)
        packet_select.append(0x0A)
        # command for reading the selected parameters returned
        packet_read.append(0x1B)
        packet_read.append(0x52)
        packet_read.append(0x4C)
        packet_read.append(0x44)
        packet_read.append(0x0D)
        packet_read.append(0x0A)
        # sending commands to ODM extended version
        serialPort.write(packet_select)
        parameter = serialPort.read(2).decode('Ascii')
        # print(parameter)
        # pause between commands sent
        
        serialPort.write(packet_read)
        temp = serialPort.read().decode('Ascii')
       
        # Collect the patient info into a list
        while temp != found_item:
            temp = serialPort.read().decode('Ascii')
            
        parameter = serialPort.read(40).decode('Ascii')
        parameter = parameter[1:]
        parameter = parameter + ignor_bit
        # print(parameter)

        for str in parameter:
            if str != ignor_bit:
                serial_temp = serial_temp + str
                if str == error_bit:
                    serial_temp = serial_temp[:-2]
            else:
                serial_result.append(serial_temp)
                serial_temp = ""       
        
        serial_result.pop(0)
        serialPort.close()
        # print(serial_result)
        return serial_result
    
    
    
    def check_odm_port(self, port):
        self.access_odm_port(port)
        if self.odm_port.port == port:
            self.odm_port.close()
            return True
        else:
            self.odm_port.close()
            return False
        
        
       
        