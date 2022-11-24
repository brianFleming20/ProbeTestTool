import unittest
import RetestProbe
import tkinter as tk
from tkinter import messagebox as mb
import ProbeManager
import Ports
import Datastore
import BatchManager
import os

RT = RetestProbe
PM = ProbeManager.ProbeManager()
P = Ports
DS = Datastore.Data_Store()
BM = BatchManager.BatchManager()


class RetestTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.RT = RT.RetestProbe(self.parent, self.controller)
        self.probe_type = "DP240"
        self.probe_type2 = "DP12"
        self.batch = "12345H"
        self.batch2 = "7531B"
        port = P.Ports(probe="COM4", analyer="COM3")
        DS.write_device_to_file(port)
        self.RT.reset_display()
        if PM.ProbePresent():
            mb.showinfo(title="", message="remove any probes")

    # Identify a failed probe
    # def test_identify_failed_probe(self):
    #     print("Identify a failed probe")
    #     mb.showinfo(title="Probe Test", message="Insert a failed probe")
    #     result = self.RT.check_for_failed_probe()
    #     read_sn = PM.read_serial_number()[:3]
    #     self.assertEqual(result, read_sn)
    #
    # # Retest a failed probe
    # def test_retest_failed_probe(self):
    #     print("Retest a failed probe to pass")
    #     mb.showinfo(title="Probe test", message="Insert known good probe")
    #     probe = P.Probes(self.probe_type, self.batch, 50, 49, 1)
    #     DS.write_probe_data(probe)
    #     check = PM.ProgramProbe(self.probe_type, False)
    #     serial_number_fail = PM.read_serial_number()
    #     check_sn = serial_number_fail[8:]
    #     print(f"check  {check} : {len(serial_number_fail)}")
    #     self.RT.batch_from_file = self.batch
    #     self.RT.probe_type = self.probe_type
    #     result = self.RT.found_failed_probe()
    #
    # # Remove Fail from serial number test
    # def test_remove_fail_from_sn(self):
    #     print("Remove 'Fail' from serial number")
    #     expected = 13
    #     mb.showinfo(title="Probe Test", message="Insert failed probe for pass")
    #     # port = P.Ports(probe="COM4", analyer="COM3")
    #     # DS.write_device_to_file(port)
    #     serial_num = PM.ProgramProbe(self.probe_type, False)
    #     check = serial_num[8:]
    #     result = self.RT.passed_probe()
    #     self.assertEqual(expected, result)
    #     check_after = PM.read_serial_number()[6:-2]
    #     self.assertEqual(check, check_after)

    # Store passed probe to correct file
    def test_store_in_correct_file(self):
        print("Store in correct file")
        # find correct file
        filepath = DS.get_file_location()
        path = filepath['File']
        mb.showinfo(title="Probe data store", message="Insert a probe to find file data")
        sn = PM.read_serial_number()
        batch_data = []
        comp_line = "---"
        batch = None
        probe_date = sn[6:]
        inProgressPath = os.path.join(path, "in_progress", "")
        completePath = os.path.join(path, "complete", "")
        folder = None
        # searches folder and returns the probe entry for the batch
        inprog_line = RT.check_data(inProgressPath, probe_date)
        if not inprog_line:
            comp_line = RT.check_data(completePath, probe_date)
            comp_selected = [item for item in comp_line if item[1] == sn]
            batch = comp_selected[0]
            folder = "Complete"
        else:
            in_selected = [item[0] for item in inprog_line if item[1] == sn]
            batch = in_selected[0]
            folder = "In-progress"

        self.assertEqual(batch, self.batch)
        fail_text = "<-Scrapped"
        mb.showinfo(title="Probe Test", message="Insert a failed probe")
        serial_num = PM.ProgramProbe(self.probe_type2, False)

        # batch_data.append(self.batch2)
        # batch_data.append(serial_num)
        # batch_data.append(self.probe_type2)
        # batch_data.append("9")
        # batch_data.append("User1")
        # batch_data.append("result")
        # batch_data.append("1.3")
        # batch_data.append("ODM-not used")
        # BM.saveProbeInfoToCSVFile(batch_data, self.batch2)

        self.RT.probe_type = self.probe_type2
        self.RT.batch_from_file = self.batch2
        self.RT.serial_number.set(serial_num)
        self.RT.found_failed_probe()
        probe_date2 = serial_num[8:]
        read_line = RT.check_data(inProgressPath, probe_date2)
        selected = [item[1] for item in read_line if item[1] == serial_num]
        self.assertEqual(selected[0], serial_num)

        last_line = BM.GetBatchObject(self.batch2, False)
        results = last_line[1]
        self.assertEqual(results, serial_num)
        resultf = last_line[6]
        self.assertEqual(resultf, fail_text)


if __name__ == '__main__':
    unittest.main()
