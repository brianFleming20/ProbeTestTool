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
        probe = P.Ports(probe="COM4", analyer="COM3")
        DS.write_device_to_file(probe)
        self.FF.set_test()
    
    # serial number from probe.
    # def test_serial_no_probe(self):
    #     print("Show serial number from probe")
    #     mb.showinfo(title="Probe test", message="Insert a probe")
    #     serial_number = self.FF.get_probe_serial_number()
    #     result = len(serial_number)
    #     self.assertGreater(result, 5)

    # fault codes from a set of known fault limits
    def test_fault_codes(self):
        print("Match fault codes to probes")
        mb.showinfo(title="Probe Test", message="Insert a probe to test")
        data_collected = []
        for item in range(1,10):
            result = self.FF.get_cable_code()
            data_collected.append(result)
        print(data_collected)


    # cable length code
    # def test_cable_length_code(self):
    #     print("Cable length code")
    #     good = 0.8
    #     fail = 2.8
    #     mb.showinfo(title="Probe Test", message="Insert a good probe")
    #     result_good = self.FF.get_cable_length()
    #     self.assertGreater(result_good, good)
    #     self.assertLess(result_good, fail)
    #
    #     mb.showinfo(title="Probe Test", message="Insert a failed probe")
    #     result_fail = self.FF.get_cable_length()
    #     # self.assertGreater(result_fail, fail)
    #     self.assertLess(result_fail, good)

    # test fault limits
    # def test_fault_limits(self):
    #     print("Test fault limits")
    #     upper = PT.UPPER_LIMIT
    #     lower = PT.LOWER_LIMIT
    #     result_upper = self.FF.get_upper_limit()
    #     result_lower = self.FF.get_lower_limit()
    #     self.assertEqual(upper, result_upper)
    #     self.assertEqual(lower, result_lower)

    # Detect monitor connection flag
    # def test_monitor_connection(self):
    #     print("Test monitor connection")

    # Detect monitor parameters
    # def test_monitor_parameters(self):
    #     print("Test monitor parameters")
    
    # Set and show a loss return graph
    # def test_show_loss_return_graph(self):
    #     print("Show loss return graph")
    #     expected = "Unknown"
    #     self.FF.show_plot()
    #     result = self.FF.test_probe()


if __name__ == '__main__':
    unittest.main()