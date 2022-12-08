from Sessions import ContinueSessionWindow
import tkinter as tk
from Datastore import Data_Store


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
        DS = Data_Store()
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
