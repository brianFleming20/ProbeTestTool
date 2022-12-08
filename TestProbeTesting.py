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
import RetestProbe
import os

PM = ProbeManager.ProbeManager()
DS = Datastore.Data_Store()
PT = ProbeTest
P = Ports
SM = SecurityManager.SecurityManager()
U = SecurityManager
BM = BatchManager.BatchManager()
CO = Connection
ZN = NanoZND.NanoZND()
RT = RetestProbe


class ProbeTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.PT = PT.TestProgramWindow(self.parent, self.controller)
        self.CO = CO.Connection(self.parent, self.controller)
        self.RT = RT.RetestProbe(self.parent, self.controller)
        self.batch = "12345H"
        self.type = "DP12"
        self.type2 = "DP240"
        self.qty = 10
        self.user = "User3"
        self.path = os.path.join("C:\\Users", os.getenv('username'), "Documents\\PTT_Results", "")
        odm = P.Ports(probe='COM4', analyer='COM3', odm='COM5', active=False)
        DS.write_device_to_file(odm)
        probes = P.Probes(self.type, self.batch, 0, 10)
        DS.write_probe_data(probes)
        self.PT.set_test_flag()
        if PM.ProbePresent():
            mb.showinfo(title="", message="remove any probes")
        self.PT.display_layout()

    # Identify a logged-in username
    def test_logged_in_user(self):
        username = "User3"
        user = P.Users(username, False)
        DS.write_user_data(user)
        self.PT.reset()
        result = self.PT.current_user.get()
        self.assertEqual(result, username)

    # Detect an inserted probe
    def test_inserted_probe_detected(self):

        # Test the bits for a probe has been inserted #
        mb.showinfo(title="Probe test", message="Insert a probe ")
        result_probe_in = self.PT.check_probe_present()
        self.assertTrue(result_probe_in)

        mb.showinfo(title="Probe test", message="Remove the probe")
        result_probe_out = self.PT.check_probe_present()
        self.assertFalse(result_probe_out)

    def test_detect_programmed_probe_passed(self):
        print("Detect a programmed pass probe")
        mb.showinfo(title="Probe test", message="Insert a programmed passed probe")
        self.PT.set_test_flag()
        expected = False
        result = self.PT.program_blank_probe()
        self.assertEqual(expected, result)

    # Detect a completed batch.
    def test_completed_batch(self):
        print("Detect a completed batch")
        newBatch = "7733A"
        probe_type = "I2C"
        batchQty = 0
        self.PT.set_test_flag()
        inProgressPath = os.path.join(self.path, "in_progress", "")
        completePath = os.path.join(self.path, "complete", "")
        probe_data = P.Probes(probe_type, newBatch, 95, batchQty)
        DS.write_probe_data(probe_data)
        expected_text = " Completed by - "
        self.PT.reset()
        self.PT.wait_for_probe()
        finish_ongoing = self.PT.session_on_going
        finish_complete = self.PT.session_complete
        qty = DS.get_probes_left_to_test()
        self.assertFalse(finish_ongoing)
        self.assertTrue(finish_complete)
        self.assertEqual(qty, 0)
        result = BM.CSVM.ReadLastLine(newBatch, True)[1]
        self.assertEqual(expected_text, result)
        originalPath = os.path.abspath(completePath + newBatch + '.csv')
        destinationPath = os.path.abspath(inProgressPath + newBatch + '.csv')
        os.renames(originalPath, destinationPath)

    def test_detect_a_passed_probe(self):
        print("Detect a analyser passed probe, tested")
        mb.showinfo(title="Probe test", message="Insert a probe to pass")
        self.PT.set_test_flag()
        result, one, two = self.PT.test_probe()
        self.assertTrue(result)

    # Identify a failed probe
    def test_fail_probe_program(self):
        result = False
        self.PT.programmed = True
        mb.showinfo(title="Probe to fail", message="Insert a probe to fail")
        self.serial_number = self.PT.program_probe(self.type, False)
        serial_number = PM.read_serial_number()
        if "Fail" in self.serial_number:
            result = True
        self.assertTrue(result)
        self.assertEqual(self.serial_number, serial_number)

        print("Test failed probe analyser")
        PT.analyser = False
        users = P.Users("User3", True, plot=True)
        DS.write_user_data(users)
        PT.perform_probe_test()
        result2 = PT.analyser
        self.assertFalse(result2)

        print("Test failed probe")
        expected_fail = False
        result_fail = self.PT.do_test_and_programme(self.batch, self.type)
        self.assertEqual(result_fail, expected_fail)

    # Suspend a batch
    def test_suspend_batch(self):
        print("Test suspend batch")
        expected = " Suspended Batch "
        for file in BM.GetAvailableBatches():
            if file[:-4] == self.batch:
                contents = BM.get_batch_line(self.batch, False)
                self.assertEqual(contents[0], self.batch)

        self.PT.probe_type.set(self.type2)
        self.PT.current_batch.set(self.batch)
        self.PT.probes_passed.set(80)
        self.PT.left_to_test.set(self.qty)
        self.PT.suspnd_btn_clicked()
        result = BM.get_batch_line(self.batch, False)[1]
        self.assertEqual(expected, result)

    # Identify a programmed probe from same batch
    def test_different_batch_probe(self):
        print("Test different batch probe")
        probe = P.Probes(self.type, self.batch, self.qty, 80)
        DS.write_probe_data(probe)
        mb.showinfo(title="Probe test", message="Insert a probe from different batch")
        sn = PM.read_serial_number()
        probe_type = sn[:3]
        probe_date = sn[8:]
        inProgressPath = os.path.join(self.path, "in_progress", "")
        result = self.RT.check_folder(inProgressPath, probe_type, probe_date)
        self.assertFalse(result)

    # Check reduce batch qty after passed probe
    def test_reduce_probe_qty(self):
        print("Test reduce qty when probe tested")
        results = True
        left = 10
        tested = 2
        snum = "test"
        odm_data = "ODM not used"
        marker = "test"
        mb.showinfo(title="Probe test", message="Insert a passed probe")
        self.PT.left_to_test.set(left)
        self.PT.probes_passed.set(tested)
        # Save to file check
        self.PT.update_results(results, snum, odm_data, self.batch, marker)
        last_line = BM.CSVM.ReadLastLine(self.batch, False)
        serial_number = last_line[1]
        result = snum in serial_number
        self.assertTrue(result)
        ####################################
        # check for probe number altered   #
        # test for passed probes increased #
        # test for left to test reduced    #
        # test for failed probes same      #
        ####################################
        passed = self.PT.probes_passed.get()
        left = self.PT.left_to_test.get()
        failed = DS.get_probes_failed()
        self.PT.do_test_and_programme(self.batch, self.type2)
        passed_after = self.PT.probes_passed.get()
        left_after = self.PT.left_to_test.get()
        failed_after = DS.get_probes_failed()
        self.assertGreater(passed_after, passed)
        self.assertGreater(left, left_after)
        self.assertEqual(failed, failed_after)
        #######################################
        # check changed in file               #
        #######################################
        last_line_pass = BM.CSVM.ReadLastLine(self.batch, False)
        print(last_line_pass)
        mb.showinfo(title="Probe test", message="Remove test probe")
        ####################################
        # check for failed probe           #
        # test for passed probes stay same #
        # test for left to test reduced    #
        # test for failed increased        #
        ####################################
        mb.showinfo(title="Probe test", message="Insert a failed probe")
        collect_passed = self.PT.probes_passed.get()
        collect_failed = DS.get_probes_failed()
        collect_left = self.PT.left_to_test.get()
        self.PT.do_test_and_programme(self.batch, self.type2)
        collect_passed_after = self.PT.probes_passed.get()
        collect_failed_after = DS.get_probes_failed()
        left_after_fail = self.PT.left_to_test.get()
        self.assertEqual(collect_passed_after, collect_passed)
        self.assertGreater(collect_left, left_after_fail)
        self.assertGreater(collect_failed_after, collect_failed)
        last_line_fail = BM.CSVM.ReadLastLine(self.batch, False)
        print(last_line_fail)

    # Detect a non-human probe
    def test_non_human_probe(self):
        print("Test non human probe save to file test with passed probe")
        animal_probe = DS.get_animal_probe()
        if not animal_probe:
            user = P.Users("Brian", True, non_human=True)
            DS.write_user_data(user)
        batch = "12345H"
        expected = "Animal Probe"
        mb.showinfo(title="test", message="Insert a passed probe for animal")
        self.PT.do_test_and_programme(batch, "DP12")

        data_line = BM.CSVM.ReadLastLine(batch, False)
        result = data_line[1]
        self.assertEqual(expected, result)

        print("Test non human probe save to file with failed probe")
        user = P.Users("Brian", True, non_human=True)
        DS.write_user_data(user)
        batch = "12348D"
        expected = "Animal-Fail"
        mb.showinfo(title="test", message="Insert a failed probe")
        self.PT.do_test_and_programme(batch, "DP12")

        data_line = BM.CSVM.ReadLastLine(batch, False)
        result = data_line[1][:11]
        self.assertEqual(expected, result)

    def test_KDP_probes(self):
        print("Test the KDP probes")
        probe_type = "KDP72"
        batch = "7531B"
        probe = P.Probes(probe_type=probe_type, current_batch=batch, passed=3, left_to_test=15)
        DS.write_probe_data(probe)
        self.PT.reset()
        mb.showinfo(title="test", message="Insert a passed KDP72 probe")
        probe_test = PT.perform_probe_test()
        self.assertTrue(PT.analyser)

        result, marker, odm = self.PT.test_probe()

        self.assertTrue(result)
        PT.analyser = False

        print("Test KDP72 failed probe")
        mb.showinfo(title="test", message="Insert a failed KDP72 probe")
        probe_test = PT.perform_probe_test()
        self.assertFalse(PT.analyser)
        result_fail, marker, odm = self.PT.test_probe()

        self.assertFalse(result_fail)

    # Record a successfully repaired probe
    def test_pass_probe(self):
        print("Detect a passed probe")
        mb.showinfo(title="Probe Test", message="Insert failed probe for repair")
        fail_text = "Fail"
        check = False
        check_for_fault = PM.read_serial_number()
        if fail_text in check_for_fault:
            check = True
        self.assertTrue(check)

    # Check not reduce qty after probe overwrite
    def test_overwrite_not_reduce_qty(self):
        print("Test not reduce qty after overwrite")
        overwrite = DS.get_overwrite_setting()
        if not overwrite:
            user_overwrite = P.Users(self.user, True, over_right=True)
            DS.write_user_data(user_overwrite)

        qty = 10
        self.PT.left_to_test.set(qty)
        self.PT.probes_passed.set(qty)
        self.PT.do_test_and_programme(self.batch, self.type2)
        result = self.PT.left_to_test.get()
        self.assertEqual(result, qty)

    # Test the probe overwrite flag
    def test_overwrite_flag(self):
        print("Test overwrite flag")
        self.PT.current_user.set("User3")
        self.PT.user_admin = True
        user = P.Users("User3", True, over_right=True)
        DS.write_user_data(user)
        check_overwrite = DS.get_user_data()['Over_rite']
        self.assertTrue(check_overwrite)
        from_probe_test = self.PT.check_overwrite()
        self.assertEqual(from_probe_test, check_overwrite)

    # Test the monitor not required flag
    def test_not_monitor_flag(self):
        print("Test monitor flag")
        not_used = "Not used"
        used = 0
        monitor = P.Ports(active=True)
        DS.write_device_to_file(monitor)
        monitor_on = self.PT.update_odm_data()[0]
        self.assertEqual(monitor_on, used)
        monitor = P.Ports(active=False)
        DS.write_device_to_file(monitor)
        monitor_off = self.PT.update_odm_data()
        self.assertEqual(monitor_off, not_used)

    # Test the length code
    def test_probe_length(self):
        print("Test the probe length")
        limit_lower = 0.8
        limit_upper = 1.8
        result = PT.perform_probe_test()
        self.assertGreater(result, limit_lower)
        self.assertGreater(limit_upper, result)

    def test_bad_chip(self):
        print("Test for bad chip")
        expected = False
        mb.showinfo(title="Probe Test", message="Insert a known bad chip probe")
        check = PM.ProgramProbe(self.type, True)
        self.assertEqual(expected, check)


    # Reflection test
    def test_reflection_test(self):
        pass


if __name__ == '__main__':
    unittest.main()