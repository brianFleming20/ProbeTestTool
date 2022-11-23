import unittest
import Ports
import Sessions
import tkinter as tk
import BatchManager
import Datastore
import os

SE = Sessions
P = Ports.Probes
U = Ports.Users
DS = Datastore.Data_Store()
B = BatchManager


class ContinueSessionTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.C = SE.ContinueSessionWindow(self.parent, self.controller)
        self.BS = B.CSVManager()
        self.BM = B.BatchManager()
        self.batch = "12345A"
        self.type = "DP240"
        self.batch_qty = '95'
        self.filename = os.path.expanduser('~') + '\Documents\PTT_Results\in_progress'

    def test_in_progress_batch(self):
        print("Access in progress batch")
        suspend_text = " Suspended Batch "
        result = self.BS.ReadLastLine(self.batch, False)
        file = self.filename + f"\{self.batch}.csv"
        probe_data = P(self.type,self.batch,45,55)
        DS.write_probe_data(probe_data)
        suspend = self.BM.SuspendBatch(self.batch)
        self.assertTrue(suspend)

        for file in self.filename:
            if file[:-4] == self.batch:
                self.assertEqual(result[0], self.batch)
                self.assertEqual(suspend_text, result[1])
                self.assertEqual(result[3], 55)


if __name__ == '__main__':
    unittest.main()