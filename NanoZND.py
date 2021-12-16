'''
Created on 24 Apr 2017

@author: Brian F
'''


import serial
import numpy as np
import pylab as pl
import time
import tkinter.messagebox as tm
import datastore
import csv
from scipy import constants

DS = datastore.DataStore()



class NanoZND(object):
    '''
    Handles VNA operations. Primarily: configuring, refreshing traces and retrieving trace values
    '''
    
    def __init__(self):
        self.file_location = "C:/Users/Brian/python-dev/data_from_NanoNVA.csv"
        self.show_plot = False
        self.port_info = None
        self.cable_length_calibration = 196
        
    def get_serial_port(self):
        port = DS.get_analyser_port()
        self.port_info = serial.Serial(port = port, 
                                   baudrate=115200,
                                   bytesize=8,
                                   timeout=0.1,
                                   parity = serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE)  
        
        
    def close_analyser_port(self):
        self.port_info.close()
        
        
    
    def ReadAnalyserData(self):
       
        line = ""
        result = ""
        c = ""
      
        self.get_serial_port() # open
        self.port_info.readline() # discard empty line
        time.sleep(0.05) #allow time for the data to be received  
        while True:
            c = self.read_data()
            if c == chr(13):
                next # ignore CR
            line += c
            if c == chr(10):
                result += line
                line = ''
                next 
            if line.endswith('ch>'):
                # stop on prompt
                break
        self.port_info.close() # Close port 
 
        # return self.analyser_data  
        return result
        
    
    def get_vna_check(self, ports):
        port = "not_connected"
        
        for p in ports:
                self.port_info = serial.Serial(
                    port = p, 
                    baudrate=115200,
                    bytesize=8,
                    timeout=0.1,
                    parity = serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE) 
                self.send_data(f"echo\r")
                time.sleep(0.05)
                read = self.read_data()
                if read == 'e':
                    port = p
        self.port_info.close()
        return port
    
    
    
    def get_marker_1_command(self):
        self.get_serial_port() # open
        self.send_data(f"marker 1\r")
        self.port_info.close() #close
        return self.ReadAnalyserData()
        
        
    # def get_marker_2_command(self):
       
    #     self.port_info.write(f"marker 2\r".encode('ascii'))
    #     return self.ReadAnalyserData()
    
        
    def get_marker_3_command(self):
        self.get_serial_port() #open
        self.send_data("marker 3\r")
        self.port_info.close() # close
        analyser_data = self.ReadAnalyserData()
        x = []      
        for line in analyser_data.split('\n'):
            if line:
                x.extend([int(d, 16) for d in line.strip().split(' ')])
                result = np.array(x, dtype=np.int16)
        return result
    

        
        
    def fetch_frequencies(self):
        self.get_serial_port() # open
        self.send_data("data s11\r")
        self.close_analyser_port() # close
        data = self.ReadAnalyserData()
        x = []
        for line in data.split('\n'):
            if line:
                x.extend([float(d) for d in line.strip().split(' ')])
        result = np.array(x[0::2])
        return result

        
    

    def set_vna_controls(self):
        self.get_serial_port() # open
        self.send_data(f"sweep 3000000 5000000 101\r") 
        self.close_analyser_port() # close
       
   
       
    def flush_analyser_port(self):
        self.get_serial_port() # open
        self.send_data("\r\n\r\n") # flush serial port  
        self.close_analyser_port() # close

        
        
    def tdr(self):
        
        data = self.fetch_frequencies()
     
        window = np.blackman(len(data))
        NFFT = 16384
        td = np.abs(np.fft.ifft(window * data , NFFT))
        min_freq = np.min(td)
    
        pk = np.max(td) # Maximum peak value
        time_ = 1 / (data[1]  - data[0] )
        t_axis = np.linspace(0, time_, NFFT)
   
        l = 1/(pk - min_freq) 
        cable_len = l/2 # cable length is 
        td_10 = td * 1000
       
        show = DS.get_plot_status()
        if show == True:
            pl.plot(t_axis, td_10)
            pl.xlim(10, time_)
            pl.xlabel("time (s")
            pl.ylabel("magnitude")
           
            pl.show()
        else:
            pass
        
        return (cable_len / self.cable_length_calibration) - 1
  
        
    # Return the analyser port number   
    def get_analyser_port_number(self, port):
        analyser_port = ""
        self.get_serial_port() # open
        analyser_port = self.port_info.port
            
        if analyser_port == port:
            self.port_info.close() # close
            return True
        else:
            self.port_info.close() # close
            return False

  
    
    def GetFileLocation(self):
        return self.file_location
    
    def SetFileLocation(self, file):
        self.file_location = file
        
    
    # Collect the data points and send to a .csv file
    def CVSOutPut(self, batch):
        data = []
        data = self.analyser_data
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
    
    
    def send_data(self,data):
        #flush the buffers
        data_ = (ord(character) for character in data)
        self.port_info.flushInput()   
        self.port_info.flushOutput() 
        self.port_info.write(data_)
        
        
    def read_data(self):
        return self.port_info.read().decode("utf-8")