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
        self.device_details = ''
        self.analyser_data = []
        self.analyser_status = False
        self.port_info = None
        self.analyser_port = ""
        self.command = ""
        self.file_location = "C:/Users/Brian/python-dev/data_from_NanoNVA.csv"
        self._frequencies = None
        self.show_plot = False
        self.cable_length_calibration = 196
    
    def refresh_window(self):
        self.analyser_port = DS.get_ports()[1]
        self.port_info = serial.Serial(port = self.analyser_port, 
                                   baudrate=1152000,
                                   bytesize=8,
                                   timeout=0.05,
                                   parity = serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE)
        
        
        
        
    def ReadAnalyserData(self, analyser_port):
        port = analyser_port
        line = ""
        result = ""
        c = ""
        
        # analyser_port = self.SetAnalyserPort(port)
       
        time.sleep(0.05) #allow time for the data to be received  
        analyser_port.readline() # discard empty line
        while True:
            c = analyser_port.read().decode("utf-8")

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
        analyser_port.close() # Close port 
        # return self.analyser_data  
        return result
        
    
    
    # Set analyser port details
    def SetAnalyserPort(self, analyser_port):
       
        port_info = serial.Serial(port = analyser_port, 
                                   baudrate=115200,
                                   bytesize=8,
                                   timeout=0.05,
                                   parity = serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE)
        
        return port_info
        
   
    
    def get_vna_check(self):
        ports = DS.get_ports()
        all_ports = ports[:-1]
        port = None
        serial_port = None
        
        for p in all_ports:
                serial_port = self.SetAnalyserPort(p) 
                serial_port.write(f"echo\r".encode("ascii"))
                time.sleep(0.05)
                read = serial_port.read().decode("utf-8")
                if read == 'e':
                    port = p
        serial_port.close()
        return port
    
    def GetAnalyserPort(self):
        self.refresh_window()
        return self.port_info
    
    def get_marker_1_command(self, port_in):
        serial_port = self.SetAnalyserPort(port_in) 
        serial_port.write(f"marker 1\r".encode('ascii'))
        return self.ReadAnalyserData( serial_port)
        
        
    def get_marker_2_command(self, port_in):
        serial_port = self.SetAnalyserPort(port_in) 
        serial_port.write(f"marker 2\r".encode('ascii'))
        return self.ReadAnalyserData( serial_port)
    
        
    def get_marker_3_command(self, port_in):
        serial_port = self.SetAnalyserPort(port_in) 
      
        serial_port.write(f"marker 3\r".encode('ascii'))
        return self.ReadAnalyserData( serial_port)
    
    
   
    def dump(self, port):
        serial_port = self.SetAnalyserPort(port)
        data = serial_port.write("dump 0\r".encode('ascii'))
        
        return self.ReadAnalyserData(serial_port)
        
        
    def fetch_frequencies(self, port):
        port = self.SetAnalyserPort(port)
        port.write("data\r".encode('ascii'))
        data = self.ReadAnalyserData(port)
        port.close()
        x = []
        for line in data.split('\n'):
            if line:
                x.extend([float(d) for d in line.strip().split(' ')])
        result = np.array(x[0::2])
       
    
        return result
        
        
    def data(self, port_in):
        
        serial_port = self.SetAnalyserPort(port_in) 
        
        
        serial_port.write('data\r'.encode('ascii'))
        return self.ReadAnalyserData(serial_port)
    
        
       
     
        # x = []
        # for line in data.split('\n'):
        #     if line:
        #         d = line.strip().split(' ')
        #         x.append(float(d[0])+float(d[1])*1.j)
        # return np.array(x)
        # self.fetch_frequencies()
        
        
        
    

    def set_vna_controls(self, port):
        serial_port = self.SetAnalyserPort(port) 
        serial_port.write(f"sweep 3000000 5000000 1\r".encode('ascii')) 
        serial_port.close()
       
   
       
    def flush_analyser_port(self, port):
        serial_port = self.SetAnalyserPort(port) 
        serial_port.write("\r\n\r\n".encode("ascii")) # flush serial port  
        serial_port.close()
        
    def send_scan(self, start = 1e6, stop = 900e6, points = None):
        if points:
            self.send_command("scan %d %d %d\r"%(start, stop, points))
        else:
            self.send_command("scan %d %d\r"%(start, stop))
        
        
    def tdr(self, port):
        delay = 3
        data = self.fetch_frequencies(port)
        prop_speed =  78.6
        _prop_speed = prop_speed/100
        window = np.blackman(len(data))
        NFFT = 16384
        td = np.abs(np.fft.ifft(window * data , NFFT))
        min_freq = np.min(td)
    
        pk = np.max(td) # Maximum peak value
      
        # peak = pk - min_freq
        time_ = 1 / (data[2]  - data[0] )
        t_axis = np.linspace(0, time_, NFFT)
        d_axis = constants.speed_of_light * _prop_speed * (pk - min_freq)
       
        l = 1/(pk - min_freq) 
        cable_len = l/2 # cable length is 
        # idx_pk = np.where(td[1:] == peak)
    
        # cable_len = d_axis[idx_pk]/2
        show = DS.get_plot_status()
        if show == True:
            pl.plot(t_axis, td)
            pl.xlim(0, time_)
            pl.xlabel("time (s")
            pl.ylabel("magnitude")
           
            pl.show()
        else:
            pass
        
        return cable_len / self.cable_length_calibration
  
        
    # Return the analyser port number   
    def get_analyser_port_number(self, port):
        analyser_port_info = self.SetAnalyserPort(port)
        analyser_port = analyser_port_info.port
        analyser_port_info.close()
        if analyser_port == port:
            return True
        else:
            return False
    
   
      
    # Return the analyser data points 
    def Get_cable_length(self):
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