from Sessions import ContinueSessionWindow, NewSessionWindow
import Sessions
import BatchManager
import tkinter as tk
from Datastore import DataStore

BM = BatchManager.BatchManager()
CSV = BatchManager.CSVManager()


class TestContinueSessions:

    def test_up_arrow(self):
        parent = tk.Tk()
        controller = tk.Tk()
        CS = ContinueSessionWindow(parent, controller)
        CS.refresh_window()

        CS.set_test()
        CS.index = 3
        batches = list(CS.suspend_dict.keys())
        CS.up_arrow()
        index = CS.index
        first = batches[index]
        batch1 = CS.batch_selected
        assert first == batch1
        assert index == 2

    def test_down_arrow(self):
        parent = tk.Tk()
        controller = tk.Tk()
        CS = ContinueSessionWindow(parent, controller)
        CS.refresh_window()

        CS.set_test()
        CS.index = 3
        batches = list(CS.suspend_dict.keys())
        CS.down_arrow()
        index = CS.index
        second = batches[index]
        batch2 = CS.batch_selected
        assert batch2 == second
        assert index == 4

    def test_continue_btn_clicked(self):
        parent = tk.Tk()
        controller = tk.Tk()
        CS = ContinueSessionWindow(parent, controller)
        DS = DataStore()
        CS.refresh_window()

        CS.set_test()
        CS.batch_selected = "12345A"
        CS.continue_btn_clicked()
        probe_data = DS.get_probe_data()
        result = probe_data['Batch']
        assert result == "12345A"

    def test_get_batch_type(self):
        parent = tk.Tk()
        controller = tk.Tk()
        CS = ContinueSessionWindow(parent, controller)
        CS.refresh_window()

        CS.set_test()
        expected = "DP12"
        result = CS.get_batch_type("9876B")
        assert result == expected

    def test_refresh_window(self):
        parent = tk.Tk()
        controller = tk.Tk()
        CS = ContinueSessionWindow(parent, controller)
        CS.refresh_window()
        CS.set_test()
        expected_batch = "9876B"
        expected_type = "DP12"
        CS.refresh_window()
        batch_keys = list(CS.suspend_dict.keys())
        batch_Values = list(CS.suspend_dict.values())
        assert expected_batch in batch_keys
        assert expected_type in batch_Values

    def test_batch_entry(self, capsys):
        parent = tk.Tk()
        controller = tk.Tk()
        CS = NewSessionWindow(parent, controller)
        CS.set_test()
        CS.refresh_window()
        expected = 'h'
        with capsys.disabled():
            print('Press the letter "H"')
        CS.batch_entry()
        result = CS.batchNumber
        assert result == expected

    # def test_change_batch_qty(self):
    #     assert False
    def test_convert_to_uppercase(self):
        parent = tk.Tk()
        controller = tk.Tk()
        CS = NewSessionWindow(parent, controller)
        CS.set_test()
        CS.refresh_window()
        batch = "12345b"
        expected = "12345B"
        result = CS.convert_to_uppercase(batch)
        assert result == expected

    def test_check_batch_number(self):
        parent = tk.Tk()
        controller = tk.Tk()
        CS = NewSessionWindow(parent, controller)
        CS.set_test()
        CS.refresh_window()
        expected_false = False
        Expected_true = True
        batch1 = ""
        batch2 = "12345"
        batch3 = "abcds"
        batch4 = "12345F"
        result1 = CS.check_batch_number(batch1)
        assert result1 == expected_false

        result2 = CS.check_batch_number(batch2)
        assert result2 == expected_false

        result3 = CS.check_batch_number(batch3)
        assert result3 == expected_false

        result4 = CS.check_batch_number(batch4)
        assert result4 == Expected_true

    def test_create_new_batch(self):
        parent = tk.Tk()
        controller = tk.Tk()
        CS = NewSessionWindow(parent, controller)
        CS.set_test()
        CS.refresh_window()
        expected_fail = False
        expected_pass = True
        batch_number_exist = "12345A"
        new_batch = "12348F"
        batch_type = "DP240"
        qty = 95
        user = "Brian"
        result1 = CS.create_new_batch(batch_number_exist, batch_type, qty, user)
        assert result1 == expected_fail

        result2 = CS.create_new_batch(new_batch, batch_type, qty, user)
        assert result2 == expected_pass

        batches = BM.GetAvailableBatches()
        if new_batch in batches:
            assert True
        else:
            assert False

        CSV.remove_batch(new_batch)

    def test_confm_btn_clicked(self):
        parent = tk.Tk()
        controller = tk.Tk()
        CS = NewSessionWindow(parent, controller)
        CS.set_test()
        CS.refresh_window()
        new_batch = "12348F"
        CS.batchNumber = new_batch
        CS.probe_type.set("DP12")
        result = CS.confm_btn_clicked()
        assert result is True

        CSV.remove_batch(new_batch)

    def test_get_available_batches(self):
        expected = 0
        result = len(Sessions.get_available_batches())
        assert result > expected
