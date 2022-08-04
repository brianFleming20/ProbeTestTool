import unittest
import Connection
import Datastore
import ProbeInterface
import ODMPlus
import NanoZND
import tkinter as tk

CO = Connection
DS = Datastore.Data_Store()
PI = ProbeInterface.PRI()
ODM = ODMPlus.ODMData()
ZND = NanoZND.NanoZND()


class ConnectionTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.CO = CO.Connection(self.parent, self.controller)
        
        
    # Check the probe check from connection class
    def test_probe_connection(self):
        print("Test the connection class")

        expected_ports = "COM4"
        
        read3 = self.CO.sort_probe_interface()
        
        self.assertEqual(read3, expected_ports)
        
        
     
        
    # detect the port number of the ODM monitor.
    def test_detect_ODM_monitor(self):
        print("Detect ODM")
        
        expected_port = "COM5"
        
        ODM.get_odm_port("COM5")
        
        port = ODM.get_port_obj()
        
        result = port.port
        
        self.assertEqual(result, expected_port)
        
        
    # accept data from ODM.
    def test_show_data_ODM(self):
        print("Show ODM data")

        while len(ODM.ReadSerialODM()) < 5:
            data = ODM.ReadSerialODM()
            print(data)
        data = ODM.ReadSerialODM()
        
        print(f"ODM data {data}")
        
        result = len(data)
        
        self.assertGreater(result, 0)
        
        
    #  cable length from the NanoVNA external device.
    # def test_cable_length(self):
    #     print("Show cable length")

    #     ZND.NanoZND()
        
    #     length = ZND.NanoZND.tdr(self)
        
    #     result = len(length)
        
    #     self.assertGreater(result, 0)
    # To be tested in the probe tests
        
        
        
    # Prove NanoZND device connection
    def test_znd_connection(self):
        print("Prove ZND connection")

        expected_ports = "COM3"
        
        read3 = self.CO.sort_znd_interface()
        
        self.assertEqual(read3, expected_ports)
        
        
        
        
    # record external device port to file.
    def test_ports_to_file(self):
        print("Record ports to file")
        
        expected_probe_port = "COM3"
        expected_odm_port = "COM5"
        expected_znd_port = "COM4"

        ports = DS.get_devices()
        print(ports)
        probe_result = ports['Probe']
        odm_result = ports['ODM']
        znd_result = ports['Analyser']
        
        self.assertEqual(probe_result, expected_probe_port)
        self.assertEqual(odm_result, expected_odm_port)
        self.assertEqual(znd_result, expected_znd_port)
    
    
    
    
    
if __name__ == '__main__':
    unittest.main()