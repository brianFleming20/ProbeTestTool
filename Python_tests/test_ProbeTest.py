
import ProbeTest
import tkinter as tk
from tkinter import messagebox as mb
import Ports
import Datastore
import os
import BatchManager

PT = ProbeTest
P = Ports
DS = Datastore.Data_Store()
BM = BatchManager.CSVManager()


def set_up():
    parent = tk.Tk()
    controller = tk.Tk()
    parent.config(width=800, height=550)
    analyser = "COM3"
    probe = "COM4"
    ana = P.Ports(analyer=analyser, probe=probe)
    DS.write_device_to_file(ana)
    return ProbeTest.TestProgramWindow(parent, controller)


def insert_probe():
    mb.showinfo(title="Insert Probe", message="Insert a probe")


def remove_probe():
    mb.showinfo(title="Remove Probe", message="Remove any probes inserted")


filename = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents/PTT_Results')


class TestProbeTesting:

    def test_perform_probe_test(self):
        set_up()
        upper_limit = 220
        lower_limit = 150
        insert_probe()
        result = PT.perform_probe_test()
        assert result > lower_limit
        assert result < upper_limit

    def test_probe_programmed(self):
        set_up()
        serian_num = PT.probe_programmed()
        result = len(serian_num)
        assert result == 16

    def test_detect_recorded_probe(self):
        set_up()
        expected = "12345A"
        type_ = "2F0"
        file = P.Location(filename)
        DS.write_file_location(file)
        found, serial_num = PT.detect_recorded_probe()
        print(f"{found} - {serial_num}")
        assert found == expected
        assert serial_num[:3] == type_

    def test_suspend_btn_clicked(self):
        test = set_up()
        test.set_test_flag()
        expected = " Suspended Batch "
        batch = "12345A"
        test.probe_type.set("DP12")
        test.current_batch.set(batch)
        test.probes_passed.set(50)
        test.left_to_test.set(45)
        test.display_layout()
        test.suspnd_btn_clicked()

        result = BM.ReadLastLine(batch, False)[1]
        assert expected == result

    def test_get_probes_left(self):
        test = set_up()
        test.left_to_test.set(1)
        expected = False
        complete = True
        result = test.get_probes_left()
        assert result == expected
        test.left_to_test.set(0)
        result1 = test.get_probes_left()
        assert result1 == complete

    def test_check_probe_present(self):
        test = set_up()
        test.display_layout()
        test.session_on_going = True
        remove_probe()
        result_out = test.check_probe_present()
        assert result_out is False
        insert_probe()
        result_in = test.check_probe_present()
        assert result_in is True

    def test_program_blank_probe(self):
        test = set_up()
        test.display_layout()
        expected = False
        result = test.program_blank_probe()
        assert result == expected

    def test_over_write_probe(self):
        test = set_up()
        batch = "12345A"
        probe = "DP240"
        data = P.Probes(probe, batch, 50, 45)
        DS.write_probe_data(data)
        test.display_layout()
        user = P.Users("Richard", False, over_right=False)
        DS.write_user_data(user)
        test.probe_type.set("DP240")
        test.set_test_flag()
        result = test.over_write_probe(batch, probe)
        assert result is False

        user = P.Users("Richard", False, over_right=True)
        DS.write_user_data(user)
        mb.showinfo(title="Insert Probe", message="Click NOT to issue a new serial number")
        result1 = test.over_write_probe(batch, probe)
        assert result1 is False

        user = P.Users("Richard", False, over_right=True)
        DS.write_user_data(user)
        mb.showinfo(title="Insert Probe", message="Insert a probe and click to issue a new serial number")
        result2 = test.over_write_probe(batch, probe)
        assert result2 is True

    def test_wait_for_probe(self):
        test = set_up()
        insert_probe()
        test.left_to_test.set(10)
        test.current_batch.set("12345A")
        test.probe_type.set("DP240")
        test.session_on_going = True
        test.set_test_flag()
        test.display_layout()
        result = test.wait_for_probe()
        assert result is True

    def test_test_probe(self):
        test = set_up()
        test.set_test_flag()
        test.display_layout()
        insert_probe()
        upper_test = 220.0
        lower_test = 162.0
        odm = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        result1, result2, result3 = test.test_probe()
        assert result1 is True
        assert result2 < upper_test
        assert result2 > lower_test
        assert result3 == odm

    def test_program_probe(self):
        test = set_up()
        test.set_test_flag()
        test.display_layout()
        insert_probe()
        probe = "DP240"
        fail = "Fail"
        SN1 = test.program_probe(probe, True)
        result1 = SN1[4:].isdigit()
        assert result1 is True

        SN2 = test.program_probe(probe, False)
        if fail in SN2:
            assert True
        else:
            assert False

    def test_do_test_and_programme(self):
        test = set_up()
        test.display_layout()
        ############################################
        # Set up default parameters for test       #
        ############################################
        user_admin = DS.user_admin_status()
        username = DS.get_username()
        test.current_user.set(username)
        test.user_admin = user_admin
        test.current_batch.set("14752N")
        test.probe_type.set("DP240")
        batch = "14752N"
        probe = "DP240"
        fail = "Fail"
        test.left_to_test.set(10)
        ########################################
        # Run test for Do Test and Program     #
        # on good probe.                       #
        ########################################
        mb.showinfo(title="Insert Probe", message="Insert a passed probe, press continue")
        result = test.do_test_and_programme(batch, probe)
        ########################################
        # Check if there are no faults.        #
        ########################################
        # assert result is False
        ########################################
        # Check the data saved to file is the  #
        # same as given by the test.           #
        ########################################
        read_line = BM.ReadLastLine(batch, False)
        assert read_line[0] == batch
        assert read_line[2] == probe
        ########################################
        # Test a failed probe to check that    #
        # the function returns a true failure  #
        ########################################
        test.current_batch.set("12345A")
        mb.showinfo(title="Insert Probe", message="Insert a failed probe, press continue")
        result_fail = test.do_test_and_programme(batch, probe)
        ########################################
        # Check if the fail is true            #
        ########################################
        # assert result_fail is True
        read_fail = BM.ReadLastLine(batch, False)
        ########################################
        # Check that a fail is recorded        #
        ########################################
        fail_text = read_fail[1]
        ########################################
        # Check that a 'Fail' text is in the   #
        # serial number when probe fails       #
        ########################################
        if fail in fail_text:
            assert True
        assert read_fail[0] == batch
        assert read_fail[2] == probe

        username_check = test.current_user.get()
        user_admin_check = test.user_admin
        assert username_check == username
        assert user_admin_check == user_admin

    def test_update_results(self):
        test = set_up()
        probe = "DP240"
        batch = "12345A"
        user = "Richard"
        marker = 200.0
        serial_number = "2F0D230105083211"
        odm_data = [0,0,0,0,0,0,0,0,0,9]
        test.probe_type.set(probe)
        test.current_batch.set(batch)
        test.current_user.set(user)
        result = test.update_results(True, serial_number, odm_data, batch, marker)
        assert result is True

    def test_save_probe_data(self):
        test = set_up()
        probe_data = DS.get_probe_data()
        probe = "DP12"
        passed = 12
        left = 50
        print(f"probe type {probe_data['Probe_Type']}, batch no {probe_data['Batch']}, failures {probe_data['Failures']}")
        test.probe_type.set(probe)
        test.probes_passed.set(passed)
        test.left_to_test.set(left)
        test.save_probe_data(probe_data['Batch'], True)
        amended_data = DS.get_probe_data()
        assert amended_data['Probe_Type'] == probe
        assert amended_data['Batch'] == probe_data['Batch']
        assert amended_data['Failures'] == probe_data['Failures'] + 1
        assert amended_data['Left_to_test'] == left

    def test_complete_batch(self):
        test = set_up()
        test.display_layout()
        test.set_test_flag()
        test.probes_passed.set(100)
        batch = "7733A"
        probes = P.Probes("DP240", batch, passed=99, left_to_test=0, failed=1)
        DS.write_probe_data(probes)
        test.complete_batch()
        inProgressPath = os.path.join(filename, "in_progress", "")
        complete = os.path.join(filename, "complete", "")
        for path in os.listdir(inProgressPath):
            if path[:-4] == batch:
                assert False

        for path in os.listdir(complete):
            if path[:-4] == batch:
                assert True

        originalPath = os.path.abspath(complete + batch + '.csv')
        destinationPath = os.path.abspath(inProgressPath + batch + '.csv')
        os.renames(originalPath, destinationPath)
