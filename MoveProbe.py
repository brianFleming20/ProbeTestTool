'''
Created on 24 Apr 2017

@author: Brian F
'''

import pyvisa as visa
import serial

class MoveProbe():
    
    def __init__(self):
        self.patient = ["name", "age", "height", "weight"]
        self.step_acheived = False
        self.g_code_setup = "G90 G21 G17"
        self.setup = False
        self.Probe_grip = False
        self.probe_in_place = True
        
    def MoveProbeClockwise(self):
        # Check port access in 10 degrees
        step_acheved = False
        g_code_setup = "G90 G21 G17"
        g_code_move = "G68 X0 Y0 R5"
        port_control = "COM6"
        serial_port_control = self.AccessPortControl(port_control)
        
                
        if self.setup == False:
            serial_port_control.write(g_code_setup)
            self.setup = True
                
        if self.setup == True and self.probe_grip == True:
            serial_port_control.write(g_code_move)
            step_acheved = True
            
            
        # access serial port with own port number
        # try / catch move motor 10 degrees
        # step acheved as true
        
        return step_acheved
    
    
    def MoveProbeAnticlockwise(self):
        # Check port access in 10 degrees
        step_acheved = False
        g_code_move = "G68 X0 Y0 R-5"
        port_control = "COM6"
        serial_port_control = self.AccessPortControl(port_control)
        
                
        if self.setup == False:
            serial_port_control.write(g_code_setup)
            self.setup = True
                
        if self.setup == True and self.probe_grip == True:
            serial_port_control.write(g_code_move)
            step_acheved = True
        
        # access serial port with own port number
        # try / catch move motor 10 degrees
        # step acheved as true
        
        return step_acheved
    
    
    def ProbeGrip(self):
        # check port access
        port_command = "M10"
        port_control = "COM6"
        serial_port_control = self.AccessPortControl(port_control)
        
        if self.Probe_grip == False:
            serial_port_control.write(port_command)
            self.probe_in_place = True
            
        return probe_in_place
       
        
        
    def Release_tool(self):
        # check port access
        port_command = "M11"
        port_control = "COM6"
        serial_port_control = self.AccessPortControl(port_control)
        
        if self.Probe_grip == True:
            serial_port_control.write(port_command)
            self.probe_in_place = False
            
        return probe_in_place
    
