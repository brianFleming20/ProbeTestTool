import unittest
import Sessions
import Ports
from SecurityManager import *
import tkinter as tk
from tkinter import *
import os
import BatchManager


SE = Sessions
DS = Datastore.Data_Store()
P = Ports.Probes
BM = BatchManager.CSVManager()


class CreateSessionTests(unittest.TestCase):

    def setUp(self):
        self.parent = tk.Tk()
        self.controller = tk.Tk()
        self.S = SE.NewSessionWindow(self.parent, self.controller)
        self.batch = "12348D"
        self.type = "DP240"
        self.batch_qty = 100
        self.filename = os.path.expanduser('~') + '\Documents\PTT_Results\in_progress'

    def test_batch_number(self):
        print("Test batch number is followed by a letter")

        bad_batch = "12347b"
        expected = "12347B"
        numbers = "12345"
        empty = ""

        batch1 = self.S.convert_to_uppercase(bad_batch)
        batch2 = self.S.convert_to_uppercase(numbers)
        batch3 = self.S.convert_to_uppercase(empty)

        self.assertEqual(batch1, expected)
        self.assertEqual(batch2, False)
        self.assertEqual(batch3, False)

    def test_batch_qty(self):
        print("Test batch quantity")

        below_qty = 99
        good_batch = 100
        above_qty = 101
        self.S.change_batch_qty(good_batch)

        result = SE.BATCH_QTY
        self.assertEqual(result, good_batch)

        self.S.change_batch_qty(below_qty)
        result2 = SE.BATCH_QTY
        self.assertEqual(result2, below_qty)

    def test_incorrect_batch_format(self):
        print("Test incorrect batch number format")
        batch_letters1 = "abcdefg"
        batch_letters2 = "ABCDEFG"
        batch_format = "1a2b3c"
        batch_numbers = "1234567"
        batch_empty = ""
        short_batch = "123b"
        good_batch = "12345a"
        expected = "12345A"
        if os.path.exists(self.filename + f'\{expected}.csv'):
            os.remove(self.filename + f'\{expected}.csv')

        # Convert batch number letter to uppercase
        result_short = self.S.convert_to_uppercase(short_batch)
        self.assertFalse(result_short)
        result = self.S.convert_to_uppercase(good_batch)
        self.assertEqual(expected, result)

        # Check batch number
        result_empty = self.S.check_batch_number(batch_empty)
        self.assertFalse(result_empty)
        result_numbers = self.S.check_batch_number(batch_numbers)
        self.assertFalse(result_numbers)
        result_format = self.S.check_batch_number(batch_format)
        self.assertFalse(result_format)
        result1 = self.S.check_batch_number(batch_letters1)
        self.assertFalse(result1)
        result2 = self.S.check_batch_number(batch_letters2)
        self.assertFalse(result2)
        result_good = self.S.check_batch_number(good_batch)
        self.assertTrue(result_good)

        # Create new batch number
        result_create = self.S.create_new_batch(expected, self.batch, self.batch_qty, "brian")
        self.assertTrue(result_create)

        for file in os.listdir(self.filename):
            if file[:-4] == expected:
                self.assertEqual(file[:-4], expected)
        if os.path.exists(self.filename + f'\{expected}.csv'):
            os.remove(self.filename + f'\{expected}.csv')

        # Continue button clicked
        self.S.batchNumber = expected
        self.S.batchQty = 100
        self.S.probe_type.set("DP240")
        self.S.test = True
        result = self.S.confm_btn_clicked()
        self.assertTrue(result)

    def test_record_batch_object(self):
        print("Test save batch to file")

        save_batch = P(self.type, self.batch, 0, self.batch_qty)
        DS.write_probe_data(save_batch)

        get_batch = DS.get_probe_data()

        self.assertEqual(get_batch["Probe_Type"], self.type)
        self.assertEqual(get_batch["Batch"], self.batch)
        self.assertEqual(get_batch["Left_to_test"], self.batch_qty)

    def test_changed_batch_qualtity(self):
        print("Test changed batch quantity")
        expected_qty = 95
        self.S.change_batch_qty(expected_qty)
        self.S.batchNumber = "12345B"
        self.S.probe_type.set("DP6")
        expected = "12345B"
        if os.path.exists(self.filename + f'\{expected}.csv'):
            os.remove(self.filename + f'\{expected}.csv')
        self.S.test = True
        create_batch = self.S.confm_btn_clicked()
        self.assertTrue(create_batch)
        for file in os.listdir(self.filename):
            if file[:-4] == expected:
                self.assertEqual(file[:-4], expected)

        result = BM.ReadLastLine(expected, False)
        qty = int(result[3])

        self.assertEqual(qty, expected_qty)
        if os.path.exists(self.filename + f'\{expected}.csv'):
            os.remove(self.filename + f'\{expected}.csv')


if __name__ == '__main__':
    unittest.main()
