'''
Created on 24 Apr 2017
@author: Brian F
'''

import serial
import numpy as np
from matplotlib import pyplot as plt
import time
import tkinter.messagebox as tm
import Datastore
import csv
import serial.tools.list_ports

DS = Datastore.Data_Store()

INDUCTANCE = 0.003526
TEST_CABLE = 0.59


class NanoZND(object):
    '''
    Handles VNA operations. Primarily: configuring, refreshing traces and retrieving trace values
    '''

    def __init__(self):
        self.file_location = "C:/Users/Brian/python-dev/data_from_NanoNVA.csv"
        self.show_plot = False
        self.analyser_port = None
        self.ser_ana = None

    def get_serial_port(self):
        port = DS.get_devices()['Analyser']
        try:
            self.ser_ana = serial.Serial()
            self.ser_ana.port = port
            self.ser_ana.baudrate = '115200'
            self.ser_ana.bytesize = 8
            self.ser_ana.timeout = 0.05
        except IOError:
            return False

    def get_znd_obj(self):
        return self.ser_ana

    def check_port_open(self):
        if self.ser_ana is None:
            self.get_serial_port()

    def ReadAnalyserData(self):
        line = ""
        result = ""
        c = ""
        self.ser_ana.readline()  # discard empty line
        time.sleep(0.05)  # allow time for the data to be received
        while True:
            c = self.read_data()
            if c == chr(13):
                next  # ignore CR
            line += c
            if c == chr(10):
                result += line
                line = ''
                next
            if line.endswith('ch>'):
                # stop on prompt
                break

        return result

    def get_vna_check(self):
        result = False
        ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(ports):
            self.ser_ana = serial.Serial(port=port, baudrate='115200', bytesize=8, timeout=0.05)

            if "400" in hwid:
                result = self.ser_ana.port
        if self.ser_ana:
            self.ser_ana.close()
        return result

    def get_marker_3_command(self):
        result = None
        bottom,top = self.get_inv_markers()

        return bottom

    def get_inv_markers(self):
        s11, data = self.fetch_frequencies()
        value1 = 10
        value2 = 0
        for num in s11:
            # inv = 1 / num
            if num < value1:
                value1 = num
        for num in s11:
            # inv = 1/num
            if num > value2:
                value2 = num
        return value1,value2


    def fetch_frequencies(self):
        self.get_serial_port()
        if not self.ser_ana.isOpen():
            self.ser_ana.open()
        self.send_data(f"frequencies\r")

        freq_data = self.ReadAnalyserData()
        self.send_data(f"data s11\r")
        s11_data = self.ReadAnalyserData()
        self.ser_ana.close()
        x = []
        for line in freq_data.split('\n'):
            if line:
                x.extend([float(d) for d in line.strip().split(' ')])
        freq_result = np.array(x[0::2])

        x = []
        for line in s11_data.split('\n'):
            if line:
                x.extend([float(d) for d in line.strip().split(' ')])
        s11_result = np.array(x[0::2])
        s11_im = np.array(x[1::2])

        return s11_result, freq_result

    def set_vna_controls(self):
        self.check_port_open()
        self.ser_ana.open()
        self.send_data(f"sweep 3000000 5000000 1\r")
        self.ser_ana.close()  # close

    def flush_analyser_port(self):
        self.check_port_open()
        self.ser_ana.open()
        self.send_data("\r\n\r\n")  # flush serial port
        self.ser_ana.close()  # close

    def tdr(self):
        if not self.ser_ana.isOpen():
            self.ser_ana.open()
        c = 3 * 10**8
        v = 0.85
        s11, freq = self.fetch_frequencies()
        bottom,top = self.get_inv_markers()
        window = np.blackman(len(s11))
        step_size = s11[1] - s11[2]
        windowed_s11 = window * s11
        NFFT = 2 ** 8
        td = np.abs(np.fft.ifft(windowed_s11, NFFT))

        time_axis = np.linspace(0, 1 / step_size, NFFT)
        d_axis = time_axis * v * c
        time1 = 1/((top - bottom) * 10**6)
        value = (time1 * v * c * INDUCTANCE) / 2

        cable_len = value - TEST_CABLE
        td_10 = td * 1000
        plt.grid(True)
        show = DS.get_plot_status()
        plt.plot(d_axis, td_10)
        plt.xlabel("Distance (m) Length of cable(%.5fm)" % cable_len)
        plt.ylabel("Magnitude")
        plt.title("Return loss Time domain")
        if show:
            plt.show()
        else:
            plt.close('all')
        return cable_len

    # Collect the data points and send to a .csv file
    def CSV_output(self, batch):
        data = []
        # data = self.analyser_data
        b = []
        b.append(batch)

        file_to_output = open(self.file_location, mode='a', newline='')
        csv_writer = csv.writer(file_to_output, delimiter=',')
        try:

            csv_writer.writerows([b, data])

        except:
            tm.showerror(
                'Data writting Error', 'Unable to write data to file. \nCheck file path and analyser data.')

        file_to_output.close()

    def GetOutFileLocation(self):
        return self.file_location

    def send_data(self, data):
        # flush the buffers

        data_ = (ord(character) for character in data)
        self.ser_ana.flushInput()
        self.ser_ana.flushOutput()
        self.ser_ana.write(data_)

    def read_data(self):

        result = self.ser_ana.read().decode("utf-8")

        return result

