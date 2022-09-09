import unittest
import Ports
import RetestProbe
import tkinter as tk
from tkinter import messagebox as mb
import ProbeTest
import Datastore
import Connection
import os

RT = RetestProbe
P = Ports.Probes
U = Ports.Users
DS = Datastore.Data_Store()
PT = ProbeTest
CO = Connection


class SearchProbeTests(unittest.TestCase):

    def setUp(self):
        self.tk = tk.Tk()
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.C = RT.RetestProbe(self.parent, self.controller)
        self.cent_x = 10
        self.cent_y = 10

    def yes_answer(self):
        pass

    def no_answer(self):
        pass

    def back_to_session(self):
        self.result = True

    def test_search_known_probe(self):
        print("Test search known probe serial number")
        type_probe_DP240 = "DP240"
        type_probe_DP12 = "DP12"
        type_probe_DP6 = "DP6"
        non_type = "---"

        check_type_DP240 = self.C.get_probe_type("2F0")
        self.assertEqual(type_probe_DP240,check_type_DP240)

        check_type_DP12 = self.C.get_probe_type("20C")
        self.assertEqual(type_probe_DP12,check_type_DP12)

        check_type_DP6 = self.C.get_probe_type("206")
        self.assertEqual(type_probe_DP6,check_type_DP6)

        error = self.C.get_probe_type("2F5")
        self.assertEqual(error,non_type)

    def test_search_serial_number(self):
        print("Test check for failed probe")

        mb.showinfo(title="Probe",message="Insert failed probe")
        probe = self.C.check_for_failed_probe()
        test1 = self.C.check
        self.assertEqual(test1, True)

        mb.showinfo(title="Probe", message="Insert passed probe")
        probe = self.C.check_for_failed_probe()
        test2 = self.C.check
        self.assertEqual(test2, False)

    def test_check_probe_dates(self):
        print("Test search un known probe serial number")
        SN = "2F0DFail09010729"
        filepath = DS.get_file_location()
        path = filepath['File']
        inProgressPath = os.path.join(path, "in_progress", "")
        completePath = os.path.join(path, "complete", "")
        probe_date = SN[8:]
        probe_type = SN[:3]
        self.C.check = True

        result = self.C.check_folder(inProgressPath, probe_date, probe_type)
        self.assertEqual(result, True)

    def test_found_failed_probe(self):
        print("Test found failed probe")
        self.C.found = True


if __name__ == '__main__':
    unittest.main()
