import unittest
import Ports
import Sessions
import tkinter as tk
import BatchManager
import Datastore
import csv
import os

SE = Sessions
P = Ports.Probes
U = Ports.Users
DS = Datastore.Data_Store()
BM = BatchManager.BatchManager()
B = BatchManager


class ContinueSessionTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.C = SE.ContinueSessionWindow(self.parent, self.controller)
        self.batch = "12348D"
        self.type = "DP240"
        self.batch_qty = '45'

    def test_in_progress_batch(self):
        print("In progress batch")
        self.C.refresh_window()
        batches = self.C.get_available_batches()
        location = DS.get_file_location()
        file_list = os.listdir(f"{location['File']}/in_progress")
        B.CSVManager()
        self.inProgressPath = f"{location['File']}/in_progress/"
        for info in batches:
            if info == self.batch:
                for file in file_list:
                    if file[:-4] == self.batch:
                        result_line = B.CSVManager.ReadLastLine(self, file[:-4])[0]
                        print(result_line)

                        result_batch = result_line[0]
                        result_probe = result_line[2]
                        result_left = result_line[3]
                        self.assertEqual(result_batch, self.batch)
                        self.assertEqual(result_probe,self.type)
                        self.assertEqual(result_left,self.batch_qty)



if __name__ == '__main__':
    unittest.main()