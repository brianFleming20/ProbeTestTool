import unittest
from tkinter import messagebox as mb
import ProbeInterface
import Datastore
import ProbeTest
import PI
import tkinter as tk

PRI = ProbeInterface
DS = Datastore
PT = ProbeTest
P = PI


class ProbeTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.PT = PT.TestProgramWindow(self.parent, self.controller)

    # detect an inserted probe. 
    def test_inserted_probe(self):
        print("Detect an inserted probe")

        PI = PRI.PRI()

        # PI.get_serial_port()

        expected_result_probe_in = True
        expected_result_probe_out = False

        probe_in_bit = '0'
        probe_out_bit = '1'

        # Test the bits for a probe has been inserted #
        result_probe_out_bit = PI.send_probe_bits()
        self.assertEqual(result_probe_out_bit, probe_out_bit)

        mb.showinfo(title="Probe test", message="Insert a probe")

        result_probe_in_bit = PI.send_probe_bits()
        self.assertEqual(result_probe_in_bit, probe_in_bit)

        mb.showinfo(title="Probe test", message="Remove the probe")
        # Test the probe present method which intergrates the bits detected #
        probe_present = PI.probe_present()

        self.assertEqual(probe_present, expected_result_probe_out)

        mb.showinfo(title="Probe test", message="Insert a probe")

        probe_present = PI.probe_present()

        self.assertEqual(probe_present, expected_result_probe_in)

    # Detect a probe that has a programmed with a serial number.
    def test_programmed_probe(self):
        print("Detect a programmed probe")

        PD = PRI.PRI()
        P = PI.ProbeData()
        self.PT.reset()

        # PD.get_serial_port()

        probe_in_bit = '0'
        probe_type = "DP6"
        mb.showinfo(title="Probe programme test", message="Insert a probe")

        result_probe_in_bit = PD.send_probe_bits()
        self.assertEqual(result_probe_in_bit, probe_in_bit)

        probe_data = P.GenerateDataString(probe_type)

        data_result = len(probe_data)

        self.assertGreater(data_result, 0)

        PD.probe_write(probe_data[0])

        check = PD.read_all_bytes()

        serial_number = PD.read_serial_number()

        self.assertEqual(check, serial_number)

        # Check probe program from the 'TestProbe' metho#

        snum = self.PT.program_probe()

        self.assertEqual(snum, serial_number)

    # Detect a completed batch.
    def test_completed_batch(self):
        print("Detect a completed batch")

        self.PT.reset()

        result = self.PT.cmplt_btn_clicked()
        # Probe left to test variable from probe test class #
        passed = self.PT.left_to_test.get()

        self.assertEqual(result, )
        
    # Detect a passed probe.
    def test_detect_passed_probe(self):
        print("Detect a passed probe")

    # Detect a failed probe.
    def test_detect_failed_probe(self):
        print("Detect a failed probe")

    # Data generated is acceptable to the ODM monitor.
    def test_probe_data_type(self):
        print("Probe data type")

    # Collected data saved to CSV file.
    def test_data_to_CSV(self):
        print("Show that data is saved to CSV file")

    # Transfer in-progress file to a completed file.
    def test_inprogress_to_complete(self):
        print("In-progress file to complete file")


if __name__ == '__main__':
    unittest.main()