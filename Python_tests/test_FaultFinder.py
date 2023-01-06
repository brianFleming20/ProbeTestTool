import FaultFinder
import tkinter as tk
import Ports
import Datastore

FF = FaultFinder
P = Ports
DS = Datastore.Data_Store()


def setup():
    parent = tk.Tk()
    controller = tk.Tk()
    parent.config(width=800, height=550)
    analyser = "COM3"
    probe = "COM4"
    ana = P.Ports(analyer=analyser, probe=probe)
    DS.write_device_to_file(ana)
    return FF.FaultFindWindow(parent, controller)


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

    def test_setup(self):
        assert False

    def test_update_odm_data(self):
        assert False

    def test_fault_find_probe(self):
        assert False

    def test_test_probe(self):
        assert False
