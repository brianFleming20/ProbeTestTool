import unittest
import ProbeInterface
from tkinter import messagebox as mb
import Datastore
import PI
import ProbeManager

Pi = ProbeInterface.PRI()
DS = Datastore.Data_Store()
DATA = PI.ProbeData()
PM = ProbeManager.ProbeManager()


class ProbeInterfaceTest(unittest.TestCase):

    def setUp(self):
        Pi.get_serial_port()

    # def test_set_probe_port(self):
    #     print("Set probe port")
    #     probe_port = Pi.get_port_obj().port
    #
    #     port = DS.get_devices()['Probe']
    #     self.assertEqual(probe_port, port)
    #
    # def test_open_port(self):
    #     print("Open port")
    #     probe_port = Pi.get_port_obj()
    #
    #     Pi.open_port()
    #
    #     open_port = probe_port.isOpen()
    #
    #     self.assertTrue(open_port)
    #
    #
    # def test_close_port(self):
    #     print("Colse port")
    #     probe_port = Pi.get_port_obj()
    #     Pi.close_port()
    #     close_port = probe_port.isOpen()
    #
    #     self.assertFalse(close_port)
    #
    # def test_probe_present(self):
    #     print("Probe present")
    #     mb.showinfo(title="test", message="Remove any probes")
    #     probe_missing = Pi.probe_present()
    #     self.assertFalse(probe_missing)
    #     mb.showinfo(title="test", message="Insert any probe.")
    #
    #     probe_here = Pi.probe_present()
    #     self.assertTrue(probe_here)
    #
    # def test_read_first_byte(self):
    #     print("Read first byte")
    #     mb.showinfo(title="test", message="Remove any probes")
    #     mb.showinfo(title="test", message="Insert ant probe")
    #
    #     result = Pi.read_first_bytes()
    #     self.assertTrue(result)
    #
    # def test_read_serial_number(self):
    #     print("read serial number")
    #     mb.showinfo(title="test", message="Insert a programmed probe")
    #
    #     serial_number = Pi.read_serial_number()
    #     result = len(serial_number)
    #
    #     self.assertGreater(result, 8)
    #
    # def test_read_all_bytes(self):
    #     print("read all bytes")
    #     mb.showinfo(title="test", message="insert a programmed probe")
    #
    #     all_bytes = Pi.read_all_bytes()
    #     result = len(all_bytes[0])
    #     self.assertGreater(result, 0)
    #
    # def test_check_connection(self):
    #     print("check probe port")
    #     port = DS.get_devices()['Probe']
    #
    #     probe_port = Pi.check_probe_connection()
    #     self.assertEqual(port, probe_port)

    def test_a_write_probe(self):
        print("write probe serial number")
        mb.showinfo(title="test", message="Insert a probe to programme")
        probe_string = DATA.GenerateDataString("DP6", True)
        Pi.probe_write(probe_string)

        all_bytes = Pi.read_all_bytes()
        result = all_bytes[:32]
        first = probe_string[0][8:-2]
        second = probe_string[1][8:-2]
        expected = first + second
        self.assertEqual(result, expected)

        print("Match pass serial numbers")
        serial_number = Pi.read_serial_number()
        number_from_bytes = PM.get_converted_serial_number(result)
        print(f"{serial_number} :-> {number_from_bytes}")
        self.assertEqual(serial_number, number_from_bytes)

    def test_failed_probe(self):
        print("Test failed probe serial number")
        mb.showinfo(title="test", message="Use different probe")
        probe_string = DATA.GenerateDataString("DP12", False)
        Pi.probe_write(probe_string)

        all_bytes = Pi.read_all_bytes()
        result = all_bytes[:32]
        first = probe_string[0][8:-2]
        second = probe_string[1][8:-2]
        expected = first + second
        self.assertEqual(result, expected)

        print("Match fail serial numbers")
        serial_number = Pi.read_serial_number()
        number_from_bytes = PM.get_converted_serial_number(result)
        print(f"{serial_number} :-> {number_from_bytes}")
        self.assertEqual(serial_number, number_from_bytes)


if __name__ == '__main__':
    unittest.main()

