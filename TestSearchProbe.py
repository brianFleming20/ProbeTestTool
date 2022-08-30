import unittest
import Ports
import Sessions
import tkinter as tk
import ProbeTest
import Datastore
import Connection
import os

SE = Sessions
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
        self.C = SE.SessionSelectWindow(self.parent, self.controller)
        self.cent_x = 0
        self.cent_y = 0

    def yes_answer(self):
        pass

    def no_answer(self):
        pass

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
        print("Test search serial number")
        SN = "2F0DFail22083010"
        probe = "DP240"
        probe_data = "2F0"
        filepath = DS.get_file_location()
        path = filepath['File']
        inProgressPath = os.path.join(path, "in_progress", "")
        completePath = os.path.join(path, "complete", "")
        canvas = PT.probe_canvas(self,"test",False)

        self.C.check_folder(inProgressPath,SN[8:],probe_data)

        test = self.C.test
        self.assertEqual(test,True)

        self.C.test = False

        self.C.check_folder(completePath,SN[8:],probe_data)
        test = self.C.test
        self.assertEqual(test,False)


    def test_search_unknown_probe(self):
        print("Test search un known probe serial number")
        SN = "2F0DFail22073020"
        probe_data = "20C"
        filepath = DS.get_file_location()
        path = filepath['File']
        inProgressPath = os.path.join(path, "in_progress", "")
        completePath = os.path.join(path, "complete", "")

        self.C.check_folder(inProgressPath, SN[8:], probe_data)

        test = self.C.test
        self.assertEqual(test, False)

        self.C.test = False

        self.C.check_folder(completePath, SN[8:], probe_data)
        test = self.C.test
        self.assertEqual(test, False)


    def test_search_passed_probe(self):
        print("Test search passed probe")
        SN = "20CD20220207141516"
        probe = "DP240"
        probe_data = "2F0"
        filepath = DS.get_file_location()
        path = filepath['File']
        inProgressPath = os.path.join(path, "in_progress", "")
        completePath = os.path.join(path, "complete", "")
        canvas = PT.probe_canvas(self, "test", False)

        result = self.C.check_folder(inProgressPath, SN[8:], probe_data)

        self.assertEqual(result, False)





if __name__ == '__main__':
    unittest.main()
