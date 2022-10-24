import unittest
from tkinter import messagebox as mb
import ProbeManager
import Datastore
import ProbeTest
import tkinter as tk
import Ports
import SecurityManager
import BatchManager
import Connection
import NanoZND

PM = ProbeManager.ProbeManager()
DS = Datastore.Data_Store()
PT = ProbeTest
P = Ports
SM = SecurityManager.SecurityManager()
U = SecurityManager
BM = BatchManager.BatchManager()
CO = Connection
ZN = NanoZND.NanoZND()


class ProbeTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.PT = PT.TestProgramWindow(self.parent, self.controller)
        self.CO = CO.Connection(self.parent, self.controller)
        self.batch = "12345H"
        self.type = "DP12"
        self.type2 = "DP240"
        self.qty = 10
        self.session_ongoing = True
        self.serial_number = None
        odm = P.Ports(probe='COM4', analyer='COM3', active=False)
        DS.write_device_to_file(odm)
        probes = P.Probes(self.type, self.batch, 0, 10)
        DS.write_probe_data(probes)
        if PM.ProbePresent():
            mb.showinfo(title="", message="remove any probes")
        self.PT.display_layout()

    def test_logged_in_user(self):
        username = "User3"
        password = "1234"
        user = P.User(username, password)
        SM.logIn(user)
        self.PT.reset()
        result = self.PT.current_user.get()
        self.assertEqual(result, username)

    # def test_inserted_probe_detected(self):
    #     expected_result_probe_out = False
    #     expected_result_probe_in = True
    #     # Test the bits for a probe has been inserted #
    #     result_probe_out = self.PT.check_probe_present()
    #     self.assertEqual(result_probe_out, expected_result_probe_out)
    #     mb.showinfo(title="Probe test", message="Insert a probe ")
    #     result_probe_in = self.PT.check_probe_present()
    #     self.assertEqual(result_probe_in, expected_result_probe_in)
    #     mb.showinfo(title="Probe test", message="Remove the probe")

    # Detect a probe that has a programmed with a serial number.
    def test_detect_programmed_probe_passed(self):
        print("Detect a programmed pass probe")
        probe_here = False
        # mb.showinfo(title="Probe programme test", message="Insert pass programmed probe")
        # if self.PT.check_probe_present():
        # probe_sn = PT.probe_programmed()
        # if len(probe_sn) > 1:
        #     probe_here = True
        # probe_is_programmed = PM.ProbeIsProgrammed()
        # self.assertEqual(probe_here, probe_is_programmed)

        # print("Detect a probe to pass")
        # result = True
        # self.PT.left_to_test.set(3)
        # self.PT.probe_type.set("DP240")
        # self.PT.programmed = True
        # self.serial_number = self.PT.program_probe(self.type2, True)
        # serial_number = PM.read_serial_number()
        # if "Fail" in self.serial_number:
        #     result = False
        # self.assertTrue(result)
        # ###########################################
        # # Program probe first to find good probe  #
        # ###########################################
        # self.PT.update_results(True, serial_number, "ODM not used", "12345H", 1.5)
        # self.assertEqual(self.serial_number, serial_number)

        # print("Test analyser")
        # result, one, two = self.PT.test_probe()
        # self.assertTrue(result)

        # print("Test analyser results")
        # PT.analyser = False
        # # ZN.flush_analyser_port()
        # # ZN.set_vna_controls()
        # users = P.Users("User3", True, plot=True)
        # DS.write_user_data(users)
        # PT.perform_probe_test()
        # result1 = PT.analyser
        # self.assertTrue(result1)

        # print("Test and program")
        # expected_passed = False
        # result_pass = self.PT.do_test_and_programme(self.batch, self.type)
        # self.assertEqual(result_pass, expected_passed)

        # print("Check over-write")
        # self.PT.current_user.set("User3")
        # self.PT.user_admin = True
        # user = P.Users("User3", True, over_right=True)
        # DS.write_user_data(user)
        # check_overwrite = DS.get_user_data()['Over_rite']
        # self.assertTrue(check_overwrite)

        # print("Passed probe to over-write")
        # over_write = self.PT.over_write_probe(self.batch, self.type)
        # check_reset = DS.get_user_data()['Over_rite']
        # self.assertFalse(check_reset)
        # self.assertTrue(over_write)

        # print("Known serial number")
        # found, sn = PT.detect_recorded_probe()
        # self.assertTrue(found)

    # Detect a completed batch.
    # def test_z_completed_batch(self):
    #     print("Detect a completed batch")
    #     newBatch = P.Batch("7733A")
    #     newBatch.probe_type = "I2C"
    #     newBatch.batchQty = 1
    #     BM.CreateBatch(newBatch, "User4")
    #     self.PT.reset()
    #     self.PT.session_complete = True
    #     self.PT.session_on_going = False
    #     self.PT.wait_for_probe()

    # def test_fail_probe_program(self):
    #     result = False
    #     self.PT.programmed = True
    #     mb.showinfo(title="Probe to fail", message="Insert a probe to fail")
    #     self.serial_number = self.PT.program_probe(self.type, False)
    #     serial_number = PM.read_serial_number()
    #     if "Fail" in self.serial_number:
    #         result = True
    #     self.assertTrue(result)
    #     self.assertEqual(self.serial_number, serial_number)

        # print("Test failed probe analyser")
        # PT.analyser = False
        # ZN.flush_analyser_port()
        # ZN.set_vna_controls()
        # users = P.Users("User3", True, plot=True)
        # DS.write_user_data(users)
        # PT.perform_probe_test()
        # result2 = PT.analyser
        # self.assertFalse(result2)

        # print("Test failed probe")
        # expected_fail = True
        # result_fail = self.PT.do_test_and_programme(self.batch, self.type)
        # print(result_fail)
        # self.assertEqual(result_fail, expected_fail)
        #
        # print("test failed over-write")
        # over_write = self.PT.over_write_probe(self.batch, self.type)
        # self.assertFalse(over_write)

    def test_z_reset_analyser(self):
        print("Reset analyser button")
        self.PT.reset_analyser()

    # def test_suspend_batch(self):
    #     print("Test suspend batch")
    #     self.PT.current_batch.set(self.batch)
    #     last_line = BM.CSVM.ReadLastLine(self.batch, False)
    #     before = last_line[1]
    #     result_before = "Suspended" not in before
    #     self.assertTrue(result_before)
    #
    #     self.PT.suspnd_btn_clicked()
    #
    #     last_line = BM.CSVM.ReadLastLine(self.batch, False)
    #     after = last_line[1]
    #     result_after = "Suspended" in after
    #     self.assertTrue(result_after)

    def test_different_batch_probe(self):
        print("Test different batch probe")



    # def test_reduce_probe_qty(self):
    #     print("Test reduce qty when probe tested")
    #     results = True
    #     left = 10
    #     test = 2
    #     snum = "test"
    #     odm_data = "ODM not used"
    #     batch = self.batch
    #     marker = "test"
    #     self.PT.left_to_test.set(left)
    #     self.PT.probes_passed.set(test)
    #     self.PT.update_results(results, snum, odm_data, batch, marker)
    #     last_line = BM.CSVM.ReadLastLine(self.batch, False)
    #     serial_number = last_line[1]
    #     result = snum in serial_number
    #     self.assertTrue(result)

    def test_qty_same_with_fail_probe(self):
        print("Failed probe qty same")

    # def test_non_human_probe(self):
    #     print("Test non human probe save to file test with passed probe")
    #     user = P.Users("Brian", True, non_human=True)
    #     DS.write_user_data(user)
    #     batch = "12345H"
    #     expected = "Animal Probe"
    #     mb.showinfo(title="test", message="Insert a passed probe")
    #     self.PT.do_test_and_programme(batch, "DP12")
    #
    #     data_line = BM.CSVM.ReadLastLine(batch, False)
    #     result = data_line[1]
    #     self.assertEqual(expected, result)
    #
    #     print("Test non human probe save to file with failed probe")
    #     user = P.Users("Brian", True, non_human=True)
    #     DS.write_user_data(user)
    #     batch = "12348D"
    #     expected = "Animal-Fail"
    #     mb.showinfo(title="test", message="Insert a failed probe")
    #     self.PT.do_test_and_programme(batch, "DP12")
    #
    #     data_line = BM.CSVM.ReadLastLine(batch, False)
    #     result = data_line[1][:11]
    #     self.assertEqual(expected, result)

    def test_KDP_probes(self):
        print("Test the KDP probes")
        probe_type = "KDP72"
        batch = "7531B"
        probe = P.Probes(probe_type=probe_type, current_batch=batch, passed=3, left_to_test=15)
        DS.write_probe_data(probe)
        self.PT.reset()
        mb.showinfo(title="test", message="Insert a passed KDP72 probe")
        probe_test = PT.perform_probe_test()
        print(probe_test)
        self.assertTrue(PT.analyser)

        result, marker, odm = self.PT.test_probe()

        self.assertTrue(result)
        PT.analyser = False

        print("Test KDP72 failed probe")
        mb.showinfo(title="test", message="Insert a failed KDP72 probe")
        probe_test = PT.perform_probe_test()
        print(probe_test)
        self.assertFalse(PT.analyser)
        result_fail, marker, odm = self.PT.test_probe()

        self.assertFalse(result_fail)




    def test_reflection_test(self):
        pass


if __name__ == '__main__':
    unittest.main()