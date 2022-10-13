import unittest
import Sessions
import Ports
from SecurityManager import *
import tkinter as tk


SE = Sessions
DS = Datastore.Data_Store()
P = Ports.Probes


class CreateSessionTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.S = SE.NewSessionWindow(self.parent, self.controller)
        self.batch = "12348D"
        self.type = "DP240"
        self.batch_qty = 100

    def test_batch_number(self):
        print("Test batch number")

        bad_batch = "12347b"
        expected = "12347B"
        numbers = "12345"
        empty = ""

        batch1 = self.S.convert_batch_number(bad_batch)
        batch2 = self.S.convert_batch_number(numbers)
        batch3 = self.S.convert_batch_number(empty)

        self.assertEqual(batch1,expected)
        self.assertEqual(batch2,False)
        self.assertEqual(batch3,False)



    def test_batch_qty(self):
        print("Test batch quantity")

        below_qty = 99
        good_batch = 100
        self.S.change_batch_qty(good_batch)

        result = SE.batch_qty
        self.assertEqual(result, good_batch)

        self.S.change_batch_qty(below_qty)
        result2 = SE.batch_qty
        self.assertEqual(result2, below_qty)

    def test_record_batch_object(self):
        print("Test save batch to file")

        save_batch = P(self.type,self.batch,0,self.batch_qty)
        DS.write_probe_data(save_batch)

        get_batch = DS.get_probe_data()

        self.assertEqual(get_batch["Probe_Type"],self.type)
        self.assertEqual(get_batch["Batch"],self.batch)
        self.assertEqual(get_batch["Left_to_test"],self.batch_qty)


if __name__ == '__main__':
    unittest.main()