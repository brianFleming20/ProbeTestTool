import unittest
import Connection
import Datastore
import ProbeInterface
import ODMPlus
import NanoZND
import Ports
import tkinter as tk

CO = Connection
DS = Datastore.Data_Store()
PI = ProbeInterface.PRI()
ODM = ODMPlus.ODMData()
ZND = NanoZND.NanoZND()
P = Ports


class ConnectionTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.CO = CO.Connection(self.parent, self.controller)

    # Check the probe check from connection class
    def test_probe_connection(self):
        print("Test the probe port number")
        expected = "COM4"
        probe_port = PI.check_probe_connection()
        self.assertEqual(probe_port, expected)

    # accept data from ODM.
    def test_show_data_ODM(self):
        print("Test ODM port number")
        expected = "COM5"
        odm_port = ODM.check_odm_port()
        self.assertEqual(odm_port, expected)

    # Prove NanoZND device connection
    def test_znd_connection(self):
        print("Test the analyser port number")
        analyser = "COM3"
        analyser_port = ZND.get_vna_check()
        self.assertEqual(analyser_port, analyser)

    # record external device port to file.
    def test_ports_to_file(self):
        print("Record ports to file")
        probe = "COM4"
        ODM = "COM5"
        analyser = "COM3"
        move = "Not Used"
        ports = P.Ports(odm=ODM, probe=probe, analyer=analyser, move=move)
        DS.write_device_to_file(ports)

        devices = DS.get_devices()
        probe_check = devices['Probe']
        self.assertEqual(probe_check, probe)

        odm_check = devices['ODM']
        self.assertEqual(odm_check, ODM)

        analyser_check = devices['Analyser']
        self.assertEqual(analyser_check, analyser)

        move_check = devices['Move']
        self.assertEqual(move_check, move)

        active = devices['odm_active']
        self.assertTrue(active)

        set_active = P.Ports(active=False)
        DS.write_device_to_file(set_active)
        get_active = DS.get_devices()['odm_active']
        self.assertFalse(get_active)

    def test_check_ports_from_connection(self):
        print("Check ports from the connection window")
        # probe connection test
        expected_probe = "COM4"
        expected_analyser = "COM3"
        expected_odm = "COM5"
        result_probe = CO.sort_probe_interface(self)
        self.assertEqual(expected_probe, result_probe)

        result_analyser = self.CO.sort_znd_interface()
        self.assertEqual(expected_analyser, result_analyser)

        result_odm = self.CO.sort_odm_interface()
        self.assertEqual(expected_odm, result_odm)


if __name__ == '__main__':
    unittest.main()