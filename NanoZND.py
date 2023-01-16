'''
Created on 24 Apr 2017
@author: Brian F
'''

import serial
import numpy as np
from matplotlib import pyplot as plt
import time
import Datastore
import serial.tools.list_ports
from scipy.constants import speed_of_light
import Ports
from tkinter import messagebox as mb

DS = Datastore.Data_Store()
P = Ports

INDUCTANCE = 0.003526
TEST_CABLE = 0.59
BLANK_PROBE = 52140318.610617355


class NanoZND():
    '''
    Handles VNA operations. Primarily: configuring, refreshing traces and retrieving trace values
    '''

    def __init__(self):
        # self.file_location = "C:/Users/Brian/python-dev/data_from_NanoNVA.csv"
        self.show_plot = False
        self.analyser_port = None
        self.info_canvas = None
        self.ser_ana = None

    def get_serial_port(self):
        port = DS.get_devices()['Analyser']
        try:
            self.ser_ana = serial.Serial()
            self.ser_ana.port = port
            self.ser_ana.baudrate = 115200
            self.ser_ana.bytesize = 8
            self.ser_ana.timeout = 0.05
            # self.ser_ana.close()
        except IOError:
            return False

    def get_znd_obj(self):
        self.get_serial_port()
        return self.ser_ana

    def check_port_open(self):
        if self.ser_ana is None:
            self.get_serial_port()

    def close(self):
        self.ser_ana.close()

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
        if not result:
            mb.showerror(title="Analyser", message="Turn Analyser on")
        return result

    def fetch_s11(self):
        if not self.ser_ana.isOpen():
            self.ser_ana.open()
        self.send_data(f"data s11\r")
        data = self.ReadAnalyserData()
        x = []
        for line in data.split('\n'):
            if line:
                x.extend([float(d) for d in line.strip().split(' ')])
        s11_result = np.array(x[0::2])
        return s11_result

    def set_vna_controls(self):
        self.check_port_open()
        if not self.ser_ana.isOpen():
            self.ser_ana.open()
        self.send_data(f"sweep 3000000 5000000 1\r")
        self.ser_ana.close()  # close

    def flush_analyser_port(self):
        self.check_port_open()
        if not self.ser_ana.isOpen():
            self.ser_ana.open()
        self.send_data("\r\n\r\n")  # flush serial port
        self.ser_ana.close()  # close

    def get_marker3(self):
        if not self.ser_ana.isOpen():
            self.ser_ana.open()
        self.send_data("marker 3\r")
        data = self.ReadAnalyserData()
        return data

    def get_marker1(self):
        if not self.ser_ana.isOpen():
            self.ser_ana.open()
        self.send_data("marker 1\r")
        data = self.ReadAnalyserData()
        return data

    def reset_vna(self):
        self.get_serial_port()
        self.flush_analyser_port()
        self.set_vna_controls()
        return True
        # self.ser_ana.close()

    def tdr(self):
        # found in https://zs1sci.com/blog/nanovna-tdr/
        self.get_serial_port()
        self.set_vna_controls()
        if not self.ser_ana.isOpen():
            try:
                self.ser_ana.open()
            except IOError:
                pass
        t_axis = 1
        if not self.ser_ana.isOpen():
            mb.showinfo(title="Analyser", message="Ensure the analyser is turned on.")
        marker3 = int(self.get_marker3().split()[2])
        marker1 = int(self.get_marker1().split()[2])
        marker_total = marker1 - marker3
        raw_points = 101
        NFFT = 16384
        PROPAGATION_SPEED = 78.6  # For RG58U
        _prop_speed = PROPAGATION_SPEED / 100
        s11 = self.fetch_s11()
        # Read skrf docs
        step = marker_total
        window = np.blackman(raw_points)
        s11 = window * s11
        td = np.abs(np.fft.ifft(s11, NFFT))
        self.ser_ana.close()
        # Calculate maximum time axis
        try:
            t_axis = np.linspace(0, 1/step, NFFT)
        except ZeroDivisionError:
            marker3 = 2
            marker1 = 4
            marker_total = marker1 - marker3
            t_axis = np.linspace(0, 1 / marker_total, NFFT)
        d_axis = speed_of_light * _prop_speed * t_axis
        pk = np.max(td)
        #################################################
        # Probe value code calculated from length       #
        # divided by a blank probe value reading        #
        #################################################
        cable_code = (abs(1/pk) / 2) - 195.9
        td_10 = td * 1000
        plt.grid(True)
        show = DS.get_plot_status()
        plt.plot(d_axis, td_10)
        plt.xlabel("Distance (m) Length of cable(%.3fm)" % cable_code)
        plt.ylabel("Magnitude")
        plt.title("Return loss Time domain")
        if show:
            plt.show()
        else:
            plt.close('all')
        return cable_code

    def send_data(self, data):
        if not self.ser_ana.isOpen():
            self.ser_ana.open()
        data_ = (ord(character) for character in data)
        self.ser_ana.flush()
        self.ser_ana.write(data_)

    def read_data(self):
        return self.ser_ana.read().decode("utf-8")

