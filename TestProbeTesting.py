import unittest
from tkinter import messagebox as mb
from tkinter import *
import ProbeInterface
import Datastore
import ProbeTest
import PI
import tkinter as tk
import Ports
import SecurityManager
import BatchManager
import Connection

PRI = ProbeInterface.PRI()
DS = Datastore.Data_Store()
PT = ProbeTest
P = PI
SER = Ports
SM = SecurityManager.SecurityManager()
U = SecurityManager
BM = BatchManager.BatchManager()
CO = Connection

class ProbeTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.PT = PT.TestProgramWindow(self.parent, self.controller)
        self.CO = CO.Connection(self.parent,self.controller)
        self.batch = "12568B"
        self.type = "DP12"
        self.qty = 10

    # detect an inserted probe. 
    def test_inserted_probe(self):
        print("Detect an inserted probe")
        ports = SER.Ports(probe="COM4")
        DS.write_device_to_file(ports)
        self.PT.display_layout()
        expected_result_probe_in = True
        expected_result_probe_out = False
        mb.showinfo(title="test", message="Remove any probes.")
        # Test the bits for a probe has been inserted #
        result_probe_out = self.PT.check_probe_present()
        self.assertEqual(result_probe_out, expected_result_probe_out)

        mb.showinfo(title="Probe test", message="Insert a probe")

        result_probe_in = self.PT.check_probe_present()
        self.assertEqual(result_probe_in, expected_result_probe_in)

        mb.showinfo(title="Probe test", message="Remove the probe")
        # Test the probe present method which intergrates the bits detected #
        probe_present = PRI.probe_present()

        self.assertEqual(probe_present, expected_result_probe_out)

        mb.showinfo(title="Probe test", message="Insert a probe")

        probe_present = PRI.probe_present()
        mb.showinfo(title="test",message="Remove any probes.")
        self.assertEqual(probe_present, expected_result_probe_in)


    # Detect a probe that has a programmed with a serial number.
    def test_probe_programmed(self):
        print("Detect a programmed probe")
        ports = SER.Ports(probe="COM4")
        DS.write_device_to_file(ports)
        self.PT.display_layout()
        P = PI.ProbeData()
        self.PT.reset()

        # PD.get_serial_port()

        probe_is_programmed = True
        probe_type = "DP240"
        mb.showinfo(title="Probe programme test", message="Insert a probe")

        result_probe_in = PRI.read_first_bytes()
        self.assertEqual(result_probe_in, probe_is_programmed)

    # Detect a completed batch.
    def test_z_completed_batch(self):
        print("Detect a completed batch")
        batch = SER.Probes(self.type,self.batch,1,self.qty)
        DS.write_probe_data(batch)
        user = SER.Users("brian",False)
        DS.write_user_data(user)

        self.PT.reset()
        self.PT.left_to_test.set(0)
        result = self.PT.cmplt_btn_clicked()

        self.assertEqual(result, True)
        
    # Detect a passed probe.
    def test_detect_passed_probe(self):
        print("Detect a passed probe")
        expected = 'Pass'
        odm = SER.Ports(analyer='COM3',active=False)
        DS.write_device_to_file(odm)
        self.PT.reset()
        mb.showinfo(title="test",message="Insert a passed probe.")
        result,marker_data, odm_data = self.PT.test_probe()
        print(f"{result} , {marker_data} , {odm_data}")

        self.assertEqual(result, expected)


    # Detect a failed probe.
    def test_detect_failed_probe(self):
        print("Detect a failed probe")
        expected = 'Fail'
        odm = SER.Ports(analyer='COM3',active=False)
        DS.write_device_to_file(odm)
        self.PT.reset()
        mb.showinfo(title="test",message="Insert a failed probe.")
        result, marker_data, odm_data = self.PT.test_probe()
        print(f"{result} , {marker_data} , {odm_data}")

        self.assertEqual(result, expected)

    def test_programme_good_probe(self):
        print("Test do program and test a passed probe")
        expected = True
        odm = SER.Ports(probe='COM4',analyer='COM3', active=False)
        DS.write_device_to_file(odm)
        self.PT.reset()
        mb.showinfo(title="test", message="Insert a passed probe.")
        result = self.PT.do_program_and_test(self.batch)

        self.assertEqual(result,expected)

    def test_program_fail_probe(self):
        print("Test do program and test a fail probe")
        expected = False
        odm = SER.Ports(probe='COM4',analyer='COM3', active=False)
        DS.write_device_to_file(odm)
        self.PT.reset()
        mb.showinfo(title="test", message="Insert a failed probe.")
        result = self.PT.do_program_and_test(self.batch)

        self.assertEqual(result, expected)

    def test_logged_in_user(self):
        print("Test logged in user")
        username = "User3"
        password = "1234"
        user = U.User(username,password)

        SM.logIn(user)

        self.PT.reset()
        result = self.PT.current_user.get()

        self.assertEqual(result,username)

    def test_suspend_batch(self):
        print("Test suspend batch")
        self.PT.probe_type.set(self.type)
        self.PT.current_batch.set(self.batch)
        self.PT.probes_passed.set(40)
        self.PT.left_to_test.set(self.qty)
        self.PT.suspnd_btn_clicked()

        last_line = BM.CSVM.ReadLastLine(self.batch)[0]

        print(last_line)

        result_batch = last_line[0]
        result_type = last_line[2]
        result_qty = int(last_line[3])

        self.assertEqual(result_batch, self.batch)
        self.assertEqual(result_type,self.type)
        self.assertEqual(result_qty,self.qty)

    def test_repair_probe(self):
        print("Test repair probe")

    def test_scrap_probe(self):
        print("Double fail probe")

    def test_different_batch_probe(self):
        print("Test different batch probe")

    def test_reduce_probe_qty(self):
        print("Test reduce qty when probe tested")

    def test_qty_same_with_fail_probe(self):
        print("Failed probe qty same")

    def test_probe_length(self):
        print("Test probe length")


    def test_reflection_test(self):
        pass



if __name__ == '__main__':
    unittest.main()