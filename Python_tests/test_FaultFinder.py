import FaultFinder
import tkinter as tk
from tkinter import messagebox as mb
import Ports
import Datastore

FF = FaultFinder
P = Ports
DS = Datastore.DataStore()


def setup():
    parent = tk.Tk()
    controller = tk.Tk()
    parent.config(width=800, height=550)
    analyser = "COM3"
    probe = "COM4"
    ana = P.Ports(analyer=analyser, probe=probe)
    DS.write_device_to_file(ana)
    return FF.FaultFindWindow(parent, controller)


def insert_a_good_probe():
    mb.showwarning(title="Insert Probe", message="Insert a good probe")


class TestFaultFind:

    def test_show_plot(self):
        test = setup()
        plot = DS.get_plot_status()
        print(plot)
        assert plot is True
        test.show_plot()
        plot1 = DS.get_plot_status()
        print(plot1)
        assert plot1 is False

    def test_update_odm_data(self):
        test = setup()
        odm = P.Ports(odm="COM5", active=False)
        DS.write_device_to_file(odm)
        test.SD_data.set(1)
        test.FTc_data.set(1)
        test.PV_data.set(1)
        SD_data = 0
        FTc_data = 0
        PV_data = 0
        test.update_odm_data()
        assert test.SD_data.get() == SD_data
        assert test.FTc_data.get() == FTc_data
        assert test.PV_data.get() == PV_data

    def test_test_probe(self):
        test = setup()
        insert_a_good_probe()
        expected2 = "No Fault"
        result1 = test.test_probe()
        print(result1)
        assert result1 == expected2

        mb.showinfo(title="Probe", message="Insert a failed probe")
        expected = ""
        result2 = test.test_probe()
        print(result2)

    def test_fault_find_probe(self):
        test = setup()
        insert_a_good_probe()
        test.set_test()
        test.fault_find_probe()
        expected = "No Fault"
        result = test.fault_message.get()
        assert result == expected

        expected2 = ""
        mb.showinfo(title="Probe", message="Insert a failed probe")
        test.fault_find_probe()
        result1 = test.fault_message.get()
        print(result1)


