import unittest
import Ports
import ProbeTest
import tkinter as tk
import BatchManager
import Datastore
import os

PT = ProbeTest
P = Ports
U = Ports.Users
DS = Datastore.Data_Store()
BM = BatchManager.BatchManager()
B = BatchManager


class SuspendSessionTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.T = PT.TestProgramWindow(self.parent, self.controller)
        self.B = BatchManager.CSVManager()
        self.batch = "12348D"
        self.type = "DP240"
        self.batch_qty = 45
        self.inProgressPath = None


    def test_batch_number(self):
        print("Identify in-progress batch number")

        batch = P.Probes(self.type, self.batch, 55, self.batch_qty)
        DS.write_probe_data(batch)

        user = U("John",False)
        DS.write_user_data(user)

        self.T.reset()

        batch = self.T.current_batch.get()
        self.assertEqual(batch,self.batch)

        probe_type = self.T.probe_type.get()
        self.assertEqual(probe_type,self.type)

        qty_left = self.T.left_to_test.get()
        self.assertEqual(qty_left, self.batch_qty)


    def test_save_to_file(self):
        print("Test sent batch data to file")
        user = U("John", False)
        batch = P.Batch(self.batch)
        batch.probe_type = self.type
        batch.batchQty = 100
        BM.CreateBatch(batch,user.Name)
        expected_text = " Suspended Batch "
        batch = P.Probes(self.type, self.batch, 55, self.batch_qty)
        DS.write_probe_data(batch)

        location = DS.get_file_location()
        file_list = os.listdir(f"{location['File']}/in_progress")
        B.CSVManager()
        self.inProgressPath = f"{location['File']}/in_progress/"
        self.T.reset()
        self.T.suspnd_btn_clicked()

        for file in file_list:
            if file[:-4] == self.batch:
                result_line = self.B.ReadLastLine(file[:-4], False)
                print(result_line)
                result_batch = result_line[0]
                result_probe = result_line[2]
                result_name = result_line[4]
                result_text = result_line[1]

                self.assertEqual(result_batch,self.batch)
                self.assertEqual(result_probe,self.type)
                self.assertEqual(result_name,user.Name)
                self.assertEqual(result_text,expected_text)


if __name__ == '__main__':
    unittest.main()