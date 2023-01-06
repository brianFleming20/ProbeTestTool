import RetestProbe
import tkinter as tk
from tkinter import messagebox as mb
import Datastore
import BatchManager
import os
import Ports
from time import gmtime, strftime
import ProbeManager

RT = RetestProbe
DS = Datastore.Data_Store()
BM = BatchManager.CSVManager()
P = Ports
PM = ProbeManager.ProbeManager()


def setup():
    parent = tk.Tk()
    controller = tk.Tk()
    parent.config(width=800, height=550)
    return RT.RetestProbe(parent, controller)


def insert_probe():
    mb.showinfo(title="Insert Probe", message="Insert a Probe")


def insert_failed_probe():
    mb.showinfo(title="Insert Probe", message="Insert a failed Probe")


class TestRetestProbe:

    def test_get_probe_type(self):
        probe_type1 = "2F0"
        probe_type3 = "648"
        probe_type2 = "20C"
        probe_type4 = "206"
        probe_type5 = "618"
        probe_type6 = "606"
        probe_type7 = "548"
        expected1 = "DP240"
        expected2 = "I2C"
        expected3 = "DP12"
        expected4 = "DP6"
        expected5 = "I2P"
        expected6 = "I2S"
        expected7 = "KDP72"
        result1 = RT.get_probe_type(probe_type1)
        assert result1 == expected1
        result2 = RT.get_probe_type(probe_type2)
        assert result2 == expected3
        result3 = RT.get_probe_type(probe_type3)
        assert result3 == expected2
        result4 = RT.get_probe_type(probe_type4)
        assert result4 == expected4
        result5 = RT.get_probe_type(probe_type5)
        assert result5 == expected5
        result6 = RT.get_probe_type(probe_type6)
        assert result6 == expected6
        result7 = RT.get_probe_type(probe_type7)
        assert result7 == expected7

    def test_minutes_in_range(self):
        file_mins = 20
        probe_mins = 22
        probe_mins_out = 55
        probe_mins_low = 2
        result1 = RT.minutes_in_range(file_mins, probe_mins)
        assert result1 is True

        result2 = RT.minutes_in_range(file_mins, probe_mins_out)
        assert result2 is False

        result3 = RT.minutes_in_range(file_mins, probe_mins_low)
        assert result3 is False

    def test_check_data(self):
        filepath = DS.get_file_location()
        path = filepath['File']
        inProgressPath = os.path.join(path, "in_progress", "")
        completePath = os.path.join(path, "complete", "")
        expected1 = "DP240"
        expected2 = "DP12"
        expected3 = "Not Found"
        probe_date1 = "2F0D230105102136"
        probe_date2 = "20CDFail11241400"
        probe_date3 = "20CDFail10241129"
        probe_date4 = "20CD220900000000"
        result1 = RT.check_data(inProgressPath, probe_date1[6:])[0]
        assert result1[2] == expected1

        result2 = RT.check_data(completePath, probe_date1[6:])[0]
        assert result2 == expected3

        result3 = RT.check_data(inProgressPath, probe_date2[8:])[0]
        assert result3[2] == expected1

        result4 = RT.check_data(completePath, probe_date2[8:])[0]
        assert result4 == expected3

        result5 = RT.check_data(inProgressPath, probe_date3[6:])[0]
        assert result5 == expected3

        result6 = RT.check_data(completePath, probe_date3[8:])[0]
        assert result6[2] == expected2

        result7 = RT.check_data(inProgressPath, probe_date4[6:])[0]
        assert result7 == expected3

        result8 = RT.check_data(completePath, probe_date4[6:])[0]
        assert result8 == expected3

    def test_set_devices(self):
        test = setup()
        test.screen_layout()
        result = test.set_devices()
        assert result is True

    def test_failed_a_probe(self):
        test = setup()
        ###################################
        # Set up test parameters          #
        ###################################
        test.batch_from_file = "12345A"
        test.probe_type = "DP240"
        test.screen_layout()
        failures = 2
        scrapped = 1
        probes = P.Probes("DP240", "12345A", 15, 82, failed=failures, scrap=scrapped)
        DS.write_probe_data(probes)
        test.failed_a_probe()
        probe_data1 = DS.get_probe_data()
        after_failures = probe_data1['Failures']
        after_scrapped = probe_data1['Scrapped']
        assert after_failures == 1
        assert after_scrapped == 2

    def test_check_folder(self):
        test = setup()
        ###################################
        # Set up parameters for test      #
        # set up file locations           #
        ###################################
        test.screen_layout()
        filepath = DS.get_file_location()
        path = filepath['File']
        inProgressPath = os.path.join(path, "in_progress", "")
        completePath = os.path.join(path, "complete", "")
        probe_date = "11241400"
        probe_type = "2F0"
        #####################################
        # Check batch number contains probe #
        #####################################
        result1 = test.check_folder(inProgressPath, probe_date, probe_type)
        assert result1 is True

        ######################################
        # Check that batch number is not in  #
        # complete folder                    #
        ######################################
        result2 = test.check_folder(completePath, probe_date, probe_type)
        assert result2 is False

    def test_check_for_failed_probe(self):
        test = setup()
        ###################################
        # Set up test parameters for a    #
        # failed text in serial number    #
        ###################################
        test.finish = 20
        test.failed_probe = False
        expected = "2F0"
        insert_probe()
        result = test.check_for_failed_probe()
        assert test.finish < 20
        assert len(test.probe_date) == 8
        assert result == expected

        test.finish = 1
        test.check_for_failed_probe()
        assert test.test_finished is True

    def test_found_failed_probe(self):
        test = setup()
        test.screen_layout()
        test.set_test_flag()
        test.scrapped = "<-Scrapped"
        test.found_failed_probe()

        batch = "12345A"
        test.batch_from_file = batch
        test.probe_type = "DP240"
        test.serial_number.set("test")
        insert_failed_probe()
        test.found_failed_probe()
        read_line = BM.ReadLastLine(batch, False)
        print(read_line)
        assert read_line[0] == batch
        assert read_line[6] == "<-Scrapped"

    def test_check_for_probe(self):
        test = setup()
        #################################
        # Set up test parameters        #
        #################################
        test.screen_layout()
        test.failed_probe = False
        test.finish = 10
        test.found = False
        test.test_finished = False
        test.set_test_flag()
        insert_failed_probe()
        #################################
        # run test for check for probe  #
        #################################
        test.check_for_probe()
        result = test.found
        print(result)
        assert result is True

        mb.showinfo(title="Insert Probe", message="Insert a passed Probe")
        test.screen_layout()
        test.found = False
        test.finish = 20
        test.failed_probe = False
        test.test_finished = False
        test.check_for_probe()
        result1 = test.found
        print(result1)
        assert result1 is False

    def test_find_scrapped(self):
        test = setup()
        ####################################
        # Searches for the word 'scrapped' #
        # in any line of the batch number  #
        # returns the first line or the    #
        # last line.                       #
        ####################################
        test.batch_from_file = "12345A"
        scrapped_text = "<-Scrapped"
        filepath = DS.get_file_location()
        path = filepath['File']
        inProgressPath = os.path.join(path, "in_progress", "")
        result = test.find_scrapped(inProgressPath)
        if scrapped_text in result:
            assert True
        else:
            assert False

        test.batch_from_file = "7733A"
        result1 = test.find_scrapped(inProgressPath)
        if scrapped_text in result1:
            assert False
        else:
            assert True

    def test_passed_probe(self):
        test = setup()
        fail_text = "Fail"
        insert_failed_probe()
        test.passed_probe()
        serial_number = PM.read_serial_number()
        if fail_text in serial_number:
            assert False
        else:
            assert True

    def test_test(self):
        secs = [format(ord(item), "x") for item in strftime("%S", gmtime())]
        print(secs)
        seconds = secs[0] + secs[1]
        print(seconds)
        print(type(seconds))
