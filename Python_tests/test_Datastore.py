import Datastore
import os
import Ports
import json

DS = Datastore.Data_Store()
P = Ports
file_data = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')


def read_from_file(file_type):
    filepath = os.path.join(file_data, file_type)
    with open(filepath, 'r') as load_user_file:
        load_data = json.load(load_user_file)
    return load_data


def write_to_file(file_type, dict, ports):
    filepath = os.path.join(file_data, file_type)
    port_data = dict(ports)
    with open(filepath, 'w') as user_file:
        json.dump(port_data, user_file, indent=4)


class TestDatastore:

    def test_write_device_to_file(self):
        probe = "COM4"
        port_data = P.Ports("Not used", probe, "COM3")
        result1 = DS.write_device_to_file(port_data)
        assert result1 is True
        read = read_from_file("ports.json")
        result2 = read['Probe']
        assert result2 == probe

    def test_get_devices(self):
        analyser = "TEST"
        port_data = P.Ports(analyer=analyser)
        write_to_file("ports.json", DS.device_locations, port_data)
        data = DS.get_devices()
        result = data['Analyser']
        assert result == analyser

    def test_write_user_data(self):
        user = "User"
        data = P.Users(user, False, non_human=True)
        result = DS.write_user_data(data)
        assert result is True

        read = read_from_file("user.json")
        result_user = read['Username']
        assert result_user == user

        result_admin = read['Admin']
        assert result_admin is False

        result_flag = read['Non_Human']
        assert result_flag is True

    def test_get_user_data(self):
        user = "User3"
        admin = True
        change_password = "Robert"
        data = P.Users(user, admin, pw_user=change_password)
        write_to_file("user.json", DS.user_dict, data)

        read = DS.get_user_data()
        result_user = read['Username']
        assert result_user == user

        result_admin = read['Admin']
        assert result_admin == admin

        result_password = read['Change_password']
        assert result_password == change_password

    def test_write_dateted_user(self):
        name = "Richard"
        user = P.User(name, False)
        result = DS.write_dateted_user(user)
        assert result is True

        read = read_from_file("deleted.json").keys()
        if name in read:
            assert True
        else:
            assert False

    def test_get_deleted_users(self):
        name = "Richard"
        result = DS.get_deleted_users().keys()
        if name in result:
            assert True
        else:
            assert False

    def test_write_probe_data(self):
        probe_type = "DP240"
        batch = "12345A"
        passed = 50
        left = 45
        probe = P.Probes(probe_type, batch, passed, left)
        result = DS.write_probe_data(probe)
        assert result is True

        read = read_from_file("probes.json")
        result1 = read['Probe_Type']
        assert result1 == probe_type

        result2 = read['Batch']
        assert result2 == batch

        result3 = read['Passed']
        assert result3 == passed

        result4 = read['Left_to_test']
        assert result4 == left

    def test_get_probe_data(self):
        probe_type = "DP240"
        batch = "12345b"
        passed = 45
        left = 50
        probe = P.Probes(probe_type, batch, passed, left)
        write_to_file("probes.json", DS.probe_dict, probe)

        read = DS.get_probe_data()
        result1 = read['Probe_Type']
        assert result1 == probe_type

        result2 = read['Batch']
        assert result2 == batch

        result3 = read['Passed']
        assert result3 == passed

        result4 = read['Left_to_test']
        assert result4 == left

    def test_get_file_location(self):
        save_location = DS.get_file_location()
        file = "Test file"
        File = P.Location(file=file)
        write_to_file('location.json', DS.file_location, File)
        read = DS.get_file_location()
        result = read['File']
        assert result == file

    def test_write_file_location(self):
        file = "Test file"
        File = P.Location(file=file)
        DS.write_file_location(File)

        read = read_from_file("location.json")
        result = read['File']
        assert result == file

    def test_get_user(self):
        assert False

    def test_get_user_list(self):
        assert False

    def test_put_user(self):
        assert False

    def test_remove_user(self):
        assert False

    def test_delete_user(self):
        assert False

    def test_get_keyboard_data(self):
        assert False

    def test_write_to_from_keys(self):
        assert False
