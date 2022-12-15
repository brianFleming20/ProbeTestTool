import Connection
import tkinter as tk
import Datastore

DS = Datastore.Data_Store()


class TestConnection:

    def test_sort_probe_interface(self):
        parent = tk.Tk()
        controller = tk.Tk()
        CO = Connection.Connection(parent, controller)
        expected = "COM4"
        check = CO.probe_working
        assert check is False
        result = Connection.sort_probe_interface(CO)
        assert result == expected

        check_true = CO.probe_working
        assert check_true is True

    def test_check_analyser(self):
        expected = "COM3"
        result = Connection.check_analyser()
        if not result:
            result = Connection.check_analyser()
        assert result == expected

    def test_sort_znd_interface(self):
        parent = tk.Tk()
        controller = tk.Tk()
        CO = Connection.Connection(parent, controller)
        expected = True
        analyser_working_before = CO.znd_working
        assert analyser_working_before is False
        CO.sort_znd_interface()
        analyser_working_after = CO.znd_working
        assert analyser_working_after == expected

    def test_refresh_window(self):
        parent = tk.Tk()
        controller = tk.Tk()
        CO = Connection.Connection(parent, controller)
        CO.set_test()
        expected_probe = "COM4"
        expected_analyser = "COM3"
        CO.refresh_window()
        ports = DS.get_devices()
        probe = ports['Probe']
        analyser = ports['Analyser']
        assert probe == expected_probe
        assert analyser == expected_analyser


