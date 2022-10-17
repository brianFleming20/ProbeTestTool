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
import Ports

P = Ports


class Data_Store():
    def __init__(self):
        self.file_data = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
        self.empty = None
    ########################
    # Main data file read  #
    ########################
    #######################################

    def get_keyboard_data(self):
        filepath = os.path.join(self.file_data, "file.keys")
        try:
            with open(filepath, 'rb') as load_keys:
                keys_data = pickle.load(load_keys)
        except FileNotFoundError:
            self.write_to_from_keys(" ")
        else:
            return keys_data

    ########################################

    def write_to_from_keys(self, keys):
        filepath = os.path.join(self.file_data, "file.keys")
        with open(filepath, 'wb') as key_input:
            pickle.dump(keys, key_input)

    #########################################

    def user_admin_status(self):
        return self.get_user_data()['Admin']

    #########################################

    def get_username(self):
        return self.get_user_data()['Username']

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
        return self.get_probe_data()['Left_to_test']

    ###########################################

    def get_current_batch(self):
        return self.get_probe_data()['Batch']

    ############################################

    def get_current_probe_type(self):
        return self.get_probe_data()['Probe_Type']

    ############################################

    def get_plot_status(self):
        return self.get_user_data()['Plot']

    ############################################

    def get_reset_password(self):
        return self.get_user_data()['reset_password']

    ############################################

    def get_probes_failed(self):
        return self.get_probe_data()['Failures']

    #############################################

    def device_locations(self, data):
        devices = {
            "ODM": data.ODM,
            "Analyser": data.Analyser,
            "Probe": data.Probe,
            "Move": data.Move,
            "odm_active": data.ODM_Active,
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
            device_data = Ports.Ports()
            self.write_device_to_file(device_data)

        else:
            return load_data

    def user_dict(self, user_data):
        user_dict = {
            "Username": user_data.Name,
            "Admin": user_data.Admin,
            "Plot": user_data.Plot,
            "Over_rite": user_data.Over_rite,
            "Change_password": user_data.Change_password,
            "reset_password": user_data.reset_password,
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
            user_data = Ports.Users("",False)
            self.write_user_data(user_data)
            return self.user_dict(user_data)
        else:
            return load_data

    def probe_dict(self, probe_data):
        probe_dict = {
            "Probe_Type": probe_data.Probe_Type,
            "Batch": probe_data.Current_Batch,
            "Passed": probe_data.Passed,
            "Left_to_test": probe_data.Left,
            "Failures": probe_data.failed,
            "Scrapped": probe_data.scrap,
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
            probe_data = Ports.Probes("","",0,0)
            self.write_probe_data(probe_data)
            return self.probe_dict(probe_data)
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
            loc = Ports.Location("")
            self.write_file_location(loc)
            return loc.File
        else:
            return load_data

    def getUser(self, user):
        '''
        tick
        pass in a username looks for given user in file
        if found, create a user object, fill it with the users data and return the object
        if not found, return False
        '''
        filepath = os.path.join(self.file_data, "userfile.pickle")
        thisUser = False

        if type(user) == str:
            name = user
            user = P.User(name, "*")
        try:
            with open(filepath, 'rb') as handle:
                userDict = pickle.load(handle)

        except FileExistsError as e:
            with open(filepath, 'w') as handle:
                pickle.dump(handle, self.empty)
                thisUser = False
        else:
            for u in userDict:
                if u == user.name:
                    item = userDict[u]
                    password = item[0]
                    admin = item[1]
                    thisUser = P.User(u, password, admin)
        return thisUser

    def getUserList(self, ):
        '''
        tick
        returns a list of all the user objects
        '''
        filepath = os.path.join(self.file_data, "userfile.pickle")
        userList = []
        try:
            with open(filepath, 'rb') as handle:
                userDict = pickle.load(handle)
        except FileNotFoundError:
            with open(filepath, 'wb') as handle:
                pickle.dump(handle, self.empty)
                return False
        else:
            for user in userDict:
                password = userDict[user][0]
                admin = userDict[user][1]
                thisUser = P.User(user, password, admin)
                userList.append(thisUser)

        return userList

    def putUser(self, user):
        '''
        tick
        Pass in a user object and update the CSV file with it
        '''
        filepath = os.path.join(self.file_data, "userfile.pickle")
        # create details array
        details = ['', False]
        details[0] = user.password
        details[1] = user.admin

        try:
            with open(filepath, 'rb') as handle:
                userDict = pickle.load(handle)

        except FileNotFoundError:
            with open(filepath, 'wb') as handle:
                userDict = {user.name: details}
                pickle.dump(userDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            userDict[user.name] = details
            with open(filepath, 'wb') as handle:
                pickle.dump(userDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
            return True

    def removeUser(self, user):
        '''
        pass in a user object
        removes a given user from the user list
        '''
        filepath = os.path.join(self.file_data, "userfile.pickle")
        with open(filepath, 'rb') as handle:
            userDict = pickle.load(handle)

        if user in userDict:
            userDict.pop(user)

        with open(filepath, 'wb') as handle:
            pickle.dump(userDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return True
