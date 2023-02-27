import ProbeInterface
import Ports
import Datastore
from tkinter import messagebox as mb
import time

PI = ProbeInterface.PRI()
P = Ports
DS = Datastore.DataStore()


def set_port():
    ports = P.Ports(probe="COM4")
    DS.write_device_to_file(ports)


def insert_probe():
    mb.showinfo(title="Insert a probe", message="Insert any probe")


def remove_probe():
    mb.showinfo(title="Remove", message="Remove any probes")


def insert_programmed():
    mb.showinfo(title="Insert a probe", message="Insert a Programmed probe")


probeones =  ['53A00900111111111111111150', '53A00908111111111111111150', '53A00910111111111111111150',
                      '53A00918111111111111111150', '53A00920111111111111111150', '53A00928111111111111111150',
                      '53A00930111111111111111150', '53A00938111111111111111150', '53A00940111111111111111150',
                      '53A00948111111111111111150', '53A00950111111111111111150', '53A00958111111111111111150',
                      '53A00960111111111111111150', '53A00968111111111111111150', '53A00970111111111111111150',
                      '53A00978111111111111111150', '53A00980111111111111111150', '53A00988111111111111111150',
                      '53A00990111111111111111150', '53A00998111111111111111150', '53A009a0111111111111111150',
                      '53A009a8111111111111111150', '53A009b0111111111111111150', '53A009b8111111111111111150',
                      '53A009c0111111111111111150', '53A009c8111111111111111150', '53A009d0111111111111111150',
                      '53A009d8111111111111111150', '53A009e0111111111111111150', '53A009e8111111111111111150',
                      '53A009f0111111111111111150', '53A009f8111111111111111150']


class TestProbeSerialInterface:

    def test_get_serial_port(self):
        port = "COM4"
        set_port()

        PI.get_serial_port()
        result = PI.get_port_obj().port
        assert result == port

    def test_send_probe_bits(self):
        set_port()
        expected_out = '1'
        expected_in = '0'
        remove_probe()
        result1 = PI.send_probe_bits()
        assert result1 == expected_out
        insert_probe()
        result2 = PI.send_probe_bits()
        assert result2 == expected_in
        remove_probe()

    def test_probe_present(self):
        set_port()
        expected_out = False
        expected_in = True
        result1 = PI.probe_present()
        assert result1 == expected_out
        insert_probe()

        result2 = PI.probe_present()
        assert result2 == expected_in
        remove_probe()

    def test_read_first_bytes(self):
        set_port()
        insert_programmed()
        result = PI.read_first_bytes()
        print(result)
        assert result is True
        remove_probe()

    def test_read_serial_number(self):
        set_port()
        insert_programmed()
        result = len(PI.read_serial_number())
        assert result > 10
        remove_probe()

    def test_read_all_bytes(self):
        set_port()
        insert_programmed()
        result = len(PI.read_all_bytes())
        assert result == 512
        remove_probe()

    def test_check_probe_connection(self):
        set_port()
        port = "COM4"
        result = PI.check_probe_connection()
        assert result == port

    def test_send_data(self):
        set_port()
        data = ['32', '36', '35']
        result = PI.send_data(b'53A0010053A10150')
        if result in data:
            assert True

    def test_read_data(self):
        set_port()
        PI.get_serial_port()
        result = PI.send_data(b'4950')
        time.sleep(0.1)
        result1 = PI.read_data()
        assert result == 2
        assert result1 == '20'

    def test_probe_write(self):
        set_port()
        PI.get_serial_port()
        insert_programmed()
        result = PI.probe_write(probeones)
        assert result == 13

        all_bytes = PI.read_all_bytes()
        result2 = len(all_bytes)
        assert result2 == 512
