'''
Created on 3 May 2017
@author: jackw
@amended by Brian F
Naming convention
- Variables = no spaces, capitals for every word except the first : thisIsAVariable
- Local functions = prefixed with _, _ for spaces, no capitals : _a_local_function
Dependencies
-NI VISA Backend
-Non standard python modules
    pyvisa
    pyserial
to do:
-complete button on TPW doesn't work
-TPW freezes if a probe is inserted
-add SQ probe to list
#         s = ttk.Separator(self.root, orient=VERTICAL)
#         s.grid(row=0, column=1, sticky=(N,S))
'''

import pickle
import os
import tkinter.messagebox as tm
import json


class Data_Store():
    def __init__(self):
        self.file_data = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    ########################
    # Main data file read  #
    ########################
    #######################################

    def get_keyboard_data(self):
        try:
            with open('file.keys', 'rb') as load_keys:
                keys_data = pickle.load(load_keys)
        except FileNotFoundError:
            self.write_to_from_keys(" ")
        else:
            return keys_data

    ########################################

    def write_to_from_keys(self, keys):
        with open('file.keys', 'wb') as key_input:
            pickle.dump(keys, key_input)

    #########################################

    def user_admin_status(self):
        return self.get_user_data()['Admin']

    #########################################

    def get_username(self):
        return self.get_user_data()['Username']

    #########################################

    # def get_probes_state(self):
    #
    #     try:
    #         with open('file.probes', 'rb') as probes:
    #             probe_data = pickle.load(probes)
    #
    #     except FileNotFoundError as fileerror:
    #         print(f"{fileerror} file not found")
    #
    #     return probe_data

    #########################################

    def show_all_data(self):
        try:
            print(f"all data = main {self.get_user_data()['Name']}, batch {self.get_probe_data()['Probe_Type']}, "
                  f"admin {self.get_user_data()['Admin']}")
            print(f"Probe port {self.get_devices()['Probe']}, Analyser port {self.get_devices()['Analyser']}")
            print(f"ODM port {self.get_devices()['ODM']} , file location {self.get_file_location()['File']}")
        except FileNotFoundError:
            tm.showerror(title="File error", message="There are no files to show.")

    #########################################

    def get_probes_left_to_test(self):
        # return self.get_batch_file()[1]
        return self.get_probe_data()['Left_to_test']

    ###########################################

    def get_current_batch(self):
        # return self.get_batch_file()[0]
        return self.get_probe_data()['Batch']

    ############################################

    def get_current_probe_type(self):
        # return self.get_batch_file()[1]
        return self.get_probe_data()['Probe_Type']

    ############################################

    def get_plot_status(self):
        return self.get_user_data()['Plot']

    ############################################

    # def get_change_password_user(self):
    #     user = []
    #     user.extend(self.get_user_file())
    #     name = user[-1]
    #     user[-1] = ""
    #     return name

    ####################################################################

    def device_locations(self, data):
        devices = {
            "ODM": data.ODM,
            "Analyser": data.Analyser,
            "Probe": data.Probe,
            "Move": data.Move,
        }
        return devices

    def write_device_to_file(self, ports):
        filepath = os.path.join(self.file_data, "ports.json")
        port_data = self.device_locations(ports)
        try:
            with open(filepath, 'r') as user_file:
                data = json.load(user_file)
        except FileNotFoundError:
            with open(filepath, 'w') as user_file:
                json.dump(port_data, user_file, indent=4)
        else:
            data.update(port_data)
            with open(filepath, 'w') as user_file:
                json.dump(data, user_file, indent=4)
                return True

    def get_devices(self):
        filepath = os.path.join(self.file_data, "ports.json")
        try:
            with open(filepath, 'r') as load_user_file:
                load_data = json.load(load_user_file)
        except FileNotFoundError:
            pass
        else:
            return load_data

    def user_dict(self, user_data):
        user_dict = {
            "Username": user_data.Name,
            "Admin": user_data.Admin,
            "Plot": user_data.Plot,
            "Over_rite": user_data.Over_rite,
            "Change_password": user_data.Change_password,
        }
        return user_dict

    def write_user_data(self, user_data):
        filepath = os.path.join(self.file_data, "user.json")
        user_dict = self.user_dict(user_data)
        try:
            with open(filepath, 'r') as user_file:
                data = json.load(user_file)
        except FileNotFoundError:
            with open(filepath, 'w') as user_file:
                json.dump(user_dict, user_file, indent=4)
        else:
            data.update(user_dict)
            with open(filepath, 'w') as user_file:
                json.dump(data, user_file, indent=4)
                return True

    def get_user_data(self):
        filepath = os.path.join(self.file_data, "user.json")
        try:
            with open(filepath, 'r') as load_user_file:
                load_data = json.load(load_user_file)
        except FileNotFoundError:
            pass
        else:
            return load_data

    def probe_dict(self, probe_data):
        probe_dict = {
            "Probe_Type": probe_data.Probe_Type,
            "Batch": probe_data.Current_Batch,
            "Passed": probe_data.Passed,
            "Left_to_test": probe_data.Left,
        }
        return probe_dict

    def write_probe_data(self, probe_data):
        filepath = os.path.join(self.file_data, "probes.json")
        probe_dict = self.probe_dict(probe_data)
        try:
            with open(filepath, 'r') as user_file:
                data = json.load(user_file)
        except FileNotFoundError:
            with open(filepath, 'w') as user_file:
                json.dump(probe_dict, user_file, indent=4)
        else:
            data.update(probe_dict)
            with open(filepath, 'w') as user_file:
                json.dump(data, user_file, indent=4)
                return True

    def get_probe_data(self):
        filepath = os.path.join(self.file_data, "probes.json")
        try:
            with open(filepath, 'r') as load_user_file:
                load_data = json.load(load_user_file)
        except FileNotFoundError:
            pass
        else:
            return load_data

    def file_location(self, file):
        file_dict = {
            "File": file.File,
        }
        return file_dict

    def write_file_location(self,file):
        filepath = os.path.join(self.file_data, "location.json")
        location = self.file_location(file)
        try:
            with open(filepath, 'r') as user_file:
                data = json.load(user_file)
        except FileNotFoundError:
            with open(filepath, 'w') as user_file:
                json.dump(location, user_file, indent=4)
        else:
            data.update(location)
            with open(filepath, 'w') as user_file:
                json.dump(data, user_file, indent=4)
                return True

    def get_file_location(self):
        filepath = os.path.join(self.file_data, "location.json")
        try:
            with open(filepath, 'r') as load_user_file:
                load_data = json.load(load_user_file)
        except FileNotFoundError:
            pass
        else:
            return load_data