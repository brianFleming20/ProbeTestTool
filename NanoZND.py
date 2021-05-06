'''
Created on 24 Apr 2017

@author: Brian F
'''

import pyvisa as visa
import serial
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tm
from tkinter import filedialog
import pickle
import csv



class NanoZND(object):
    '''
    Handles VNA operations. Primarily: configuring, refreshing traces and retrieving trace values
    '''
    
    def __init__(self):
        self.deviceDetails = ''
        self.analyser_data = []
        self.analyser_port = ""
        self.analyser_status = False
        self.port_info = None
        self.file_location = "C:/Users/Brian/python-dev/data_from_NanoNVA.csv"
    
    
    def ReadAnalyserData(self, usb):
        port = str(usb)
        line = ''
        self.port_info = serial.Serial(port = port, 
                                   baudrate=1152000,
                                   bytesize=8,
                                   timeout=0.05,
                                   parity = serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE)
        
        self.port_info.write("data\r".encode('ascii'))
        while True:
            c = self.port_info.read().decode('utf-8')
            if c == chr(13):
                c=''
                next # ignore CR
            line += c
            if c == chr(10):
                c=''
                if line == 'data\n':
                    line='' # ignore data tag
                    next
                self.analyser_data.append(line[:-1])
                line = ''
                c = ''
                next
            if line.endswith('ch>'):
                # stop on prompt
                break
        self.port_info.close() # Close port 
        return self.analyser_data  
        

    
    # # Set analyser port details
    # def SetAnalyserPort(self, port):
    #     self.port_info = port
    #     # session_data = []
    #     # with open('file.ptt', 'rb') as file:
      
    #     #     # Call load method to deserialze
    #     #     myvar = pickle.load(file)
    #     # session_data.extend(myvar)
    #     # self.port_info = session_data[4][:-1]
    #     # file.close()
    #     self.port_info = serial.Serial(port = port, 
    #                                baudrate=1152000,
    #                                bytesize=8,
    #                                timeout=0.05,
    #                                parity = serial.PARITY_NONE,
    #                                stopbits=serial.STOPBITS_ONE)
    #     self.analyser_port = self.port_info.port
        # Set the analyser port connection status to true to show connection is available
        
        
        
    # Return the analyser port number   
    def GetAnalyserPortNumber(self):
        return self.analyser_port
     
    # Return the analyser data points 
    def GetAnalyserData(self):
        return self.analyser_data
    
    # Return the analyser connection status
    def GetAnalyserStatus(self):
        return self.analyser_status
    
    # Get the port details and start frequency scan
    def FrequencyStart(self):
        pass
    
    # Stop the frequency scan and close the port
    def FrequecyStop(self):
        pass
    
    def GetFileLocation(self):
        return self.file_location
    
    def SetFileLocation(self, file):
        self.file_location = file
        
    
    # Collect the data points and send to a .csv file
    def CVSOutPut(self, batch):
        data = self.GetAnalyserData()
        b = []
        b.append(batch)
        
        file_to_output = open(self.file_location, mode='a', newline='')
        csv_writer = csv.writer(file_to_output, delimiter=',')
        try:
            
            csv_writer.writerows([b,data])
            
        except:
            tm.showerror(
                'Data writting Error', 'Unable to write data to file. \nCheck file path and analyser data.')  
        
        file_to_output.close()
 
    def GetOutFileLocation(self):
        return self.file_location