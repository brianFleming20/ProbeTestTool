import unittest
import Datastore
import ProbeTest
import Ports
import FaultFinder
import ProbeManager
import tkinter as tk
from tkinter import messagebox as mb

DS = Datastore.Data_Store()
PT = ProbeTest
P = Ports
FF = FaultFinder
PM = ProbeManager.ProbeManager()


class AdminTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.FF = FF.FaultFindWindow(self.parent, self.controller)
        if PM.ProbePresent():
            mb.showinfo(title="Probe Test", message="Remove any probes")

    
    # serial number from probe.
    def test_serial_no_probe(self):
        print("Show serial number from probe")
        mb.showinfo(title="Probe test", message="Insert a probe")
        probe = P.Ports(probe="COM4")
        DS.write_device_to_file(probe)
        serial_number = self.FF.get_probe_serial_number()
        result = len(serial_number)
        self.assertGreater(result, 5)

    # fault codes from a set of known fault limits
    def test_fault_codes(self):
        print("Match fault codes to probes")

    # cable length code
    def test_cable_length_code(self):
        print("Cable length code")

    # test fault limits
    def test_fault_limits(self):
        print("Test fault limits")

    # Detect monitor connection flag
    def test_monitor_connection(self):
        print("Test monitor connection")

    # Detect monitor parameters
    def test_monitor_parameters(self):
        print("Test monitor parameters")
    
    # Set and show a loss return graph
    def test_show_loss_return_graph(self):
        print("Show loss return graph")


if __name__ == '__main__':
    unittest.main()