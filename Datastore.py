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
from time import strftime, gmtime
import json
import Ports

P = Ports


class Data_Store():
    def __init__(self):
        self.file_data = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
    ########################
    # Main data file read  #
    ########################

    #########################################################
    # Reads the user input data from the on-screen keyboard #
    #########################################################
    def get_keyboard_data(self):
        filepath = os.path.join(self.file_data, "file.keys")
        try:
            with open(filepath, 'rb') as load_keys:
                keys_data = pickle.load(load_keys)
        except FileNotFoundError:
            self.write_to_from_keys(" ")
        else:
            return keys_data

    ##########################################################################
    # The key inputs from the user are saved to a JSON file for access later #
    # from the on-screen keyboard.                                           #
    ##########################################################################
    def write_to_from_keys(self, keys):
        filepath = os.path.join(self.file_data, "file.keys")
        with open(filepath, 'wb') as key_input:
            pickle.dump(keys, key_input)

    ####################################################################
    # Returns the administrator status of the currently logged-in user #
    ####################################################################
    def user_admin_status(self):
        return self.get_user_data()['Admin']

    ########################################################
    # Returns the username of the currently logged-in user #
    ########################################################
    def get_username(self):
        return self.get_user_data()['Username']

    ##############################################################
    # Returns the number of probes remaining in the batch number #
    ##############################################################
    def get_probes_left_to_test(self):
        return self.get_probe_data()['Left_to_test']

    ###################################################
    # Return the current batch number being worked on #
    ###################################################
    def get_current_batch(self):
        return self.get_probe_data()['Batch']

    ########################################################
    # Returns the current batch probe type being worked on #
    ########################################################
    def get_current_probe_type(self):
        return self.get_probe_data()['Probe_Type']

    ##################################################################################
    # Returns the current status of the plot graph from within the fault find screen #
    ##################################################################################
    def get_plot_status(self):
        return self.get_user_data()['Plot']

    #############################################################################
    # This method is not used, as an administrator can preform the same actions #
    #############################################################################
    def get_reset_password(self):
        return self.get_user_data()['reset_password']

    ##############################################################################
    # This method is not used, as the administrator can perform the same actions #
    ##############################################################################
    def get_reset_password_name(self):
        return self.get_user_data()['Change_password']

    #################################################################################
    # Returns the number of failed probes from the currently worked on batch number #
    #################################################################################
    def get_probes_failed(self):
        return self.get_probe_data()['Failures']

    ###################################################
    # Returns the ODM external monitor working status #
    ###################################################
    def get_monitor_setting(self):
        return self.get_devices()['odm_active']

    ######################################################################
    # Returns the setting for providing a probe with a new serial number #
    ######################################################################
    def get_overwrite_setting(self):
        return self.get_user_data()['Over_rite']

    ##########################################################
    # Returns the setting for a nun-human probe being tested #
    ##########################################################
    def get_animal_probe(self):
        return self.get_user_data()['Non_Human']

    ###################################################################
    # Returns true when a username is found in the removed users file #
    ###################################################################
    def get_current_use_user(self, username):
        # search in deleted json file for user, if not found user is not deleted
        if username in self.get_deleted_users():
            return True
        else:
            return False

    ############################################################
    # Creates a JSON object for the connected external devices #
    ############################################################
    def device_locations(self, data):
        devices = {
            "ODM": data.ODM,
            "Analyser": data.Analyser,
            "Probe": data.Probe,
            "Move": data.Move,
            "odm_active": data.ODM_Active,
        }
        return devices

    ###########################################################
    # Updates the external connected devices settings to file #
    ###########################################################
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

    ########################################################
    # Returns a list of connected external device settings #
    ########################################################
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

    ###################################################################
    # Creates a JSON object for the currently logged-in user settings #
    ###################################################################
    def user_dict(self, user_data):
        user_dict = {
            "Username": user_data.Name,
            "Admin": user_data.Admin,
            "Plot": user_data.Plot,
            "Over_rite": user_data.Over_rite,
            "Change_password": user_data.Change_password,
            "reset_password": user_data.reset_password,
            "Non_Human": user_data.Non_Human,
        }
        return user_dict

    #################################################
    # Updates the currently logged-in user settings #
    #################################################
    def write_user_data(self, user_data):
        filepath = os.path.join(self.file_data, "user.json")
        user_dict = self.user_dict(user_data)
        result = False
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
                result = True
        return result

    ###########################################################
    # Returns a list of the currently logged-in user settings #
    ###########################################################
    def get_user_data(self):
        filepath = os.path.join(self.file_data, "user.json")
        try:
            with open(filepath, 'r') as load_user_file:
                load_data = json.load(load_user_file)
        except FileNotFoundError:
            user_data = Ports.Users("", False)
            self.write_user_data(user_data)
            return self.user_dict(user_data)
        else:
            return load_data

    ############################################################################
    # Creates a JSON object for users that are not used within the system, but #
    # have been used in the past.                                              #
    ############################################################################
    def deleted_dict(self, name, date):
        deleted_user = {
            name: {
                "Date_removed": date,
            },
        }
        return deleted_user

    ##############################################################################
    # Updates the deleted users to file. When a user is removed from the system, #
    # it is not deleted but put into a file of previous users.                   #
    ##############################################################################
    def write_deleted_use(self, user_data):
        filepath = os.path.join(self.file_data, "deleted.json")
        date = strftime("%Y-%m-%d", gmtime())
        result = False
        delete_dict = self.deleted_dict(user_data.name, date)
        try:
            with open(filepath, 'r') as deleted_users:
                delete_data = json.load(deleted_users)
        except FileNotFoundError:
            with open(filepath, 'w') as deleted_users:
                json.dump(delete_dict, deleted_users, indent=4)
        else:
            delete_data.update(delete_dict)
            with open(filepath, 'w') as update_delete:
                json.dump(delete_data, update_delete, indent=4)
                result = True
        return result

    #################################################################
    # Returns a list of users that are no longer used in the system #
    #################################################################
    def get_deleted_users(self):
        filepath = os.path.join(self.file_data, "deleted.json")
        load_deleted = None
        try:
            with open(filepath, 'r') as file:
                load_deleted = json.load(file)
        except FileNotFoundError:
            date = strftime("%Y-%m-%d", gmtime())
            load_deleted = self.deleted_dict("Error", date)
        else:
            return load_deleted

    ###############################################################
    # Creates a JSON object for the batch and probe type settings #
    ###############################################################
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

    ################################################
    # Updates the batch and probe settings to file #
    ################################################
    def write_probe_data(self, probe_data):
        filepath = os.path.join(self.file_data, "probes.json")
        result = False
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
                result = True
        return result

    ##################################################################
    # Returns a list of currently worked on batch and probe settings #
    ##################################################################
    def get_probe_data(self):
        filepath = os.path.join(self.file_data, "probes.json")
        try:
            with open(filepath, 'r') as load_user_file:
                load_data = json.load(load_user_file)
        except FileNotFoundError:
            probe_data = Ports.Probes("", "", 0, 0)
            self.write_probe_data(probe_data)
            return self.probe_dict(probe_data)
        else:
            return load_data

    ##################################################################################
    # Creates a JSON object for the location of the in-progress and complete batches #
    ##################################################################################
    def file_location(self, file):
        file_dict = {
            "File": file.File,
        }
        return file_dict

    ###################################################################
    # Updates the file location for the in-progress and complete data #
    ###################################################################
    def write_file_location(self, file):
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

    ###############################################################################
    # Returns a single item list of location of the in-progress and complete file #
    ###############################################################################
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

    ###############################################################
    # Returns the user object of either a username or user object #
    ###############################################################
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
            print(e)
        else:
            for u in userDict:
                if u == user.name:
                    item = userDict[u]
                    password = item[0]
                    admin = item[1]
                    thisUser = P.User(u, password, admin)

        return thisUser

    #################################################################
    # Returns a list of the currently registered user to the system #
    #################################################################
    def getUserList(self):
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
            pass
        else:
            for user in userDict:
                password = userDict[user][0]
                admin = userDict[user][1]
                thisUser = P.User(user, password, admin)
                userList.append(thisUser)

        return userList

    #########################################
    # Registers a user object to the system #
    #########################################
    def putUser(self, user):
        '''
        tick
        Pass in a user object and update the CSV file with it
        '''
        filepath = os.path.join(self.file_data, "userfile.pickle")
        added = True
        # create details array
        details = ['', False]
        details[0] = user.password
        details[1] = user.admin

        try:
            with open(filepath, 'rb') as handle:
                userDict = pickle.load(handle)
        except FileNotFoundError:
            added = False
        else:
            userDict[user.name] = details
            with open(filepath, 'wb') as handle:
                pickle.dump(userDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return added

    ###########################################################
    # Registers a user to the removed users list.             #
    # Any user in this list cannot work on a batch number     #
    # If the user is held in the removed file and the system, #
    # the system is unable to see the user.                   #
    ###########################################################
    def removeUser(self, user):
        '''
        pass in a user object
        removes a given user from the user list
        '''
        filepath = os.path.join(self.file_data, "userfile.pickle")
        deleted = True
        try:
            # Loads the user pickle file
            with open(filepath, 'rb') as handle:
                userDict = pickle.load(handle)
        except FileNotFoundError:
            self.write_deleted_use(user)
        else:
            # Check if the user is held within the system
            # if so, the user is added to the delete file
            if user.name in userDict:
                if self.get_current_use_user(user.name):
                    deleted = False
                else:
                    self.write_deleted_use(user)
        return deleted

    ##################################
    # Removes a user from the system #
    ##################################
    def delete_user(self, username):
        filepath = os.path.join(self.file_data, "userfile.pickle")
        with open(filepath, 'rb') as handle:
            userDict = pickle.load(handle)
        userDict.pop(username)
        with open(filepath, 'wb') as handle:
            pickle.dump(userDict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #####################################################
    # Removes a user from the deleted file is that user #
    # is re-admitted to the system.                     #
    # When the user is removed from the deleted file,   #
    # the system is able to see the user again.         #
    #####################################################
    def remove_from_delete_file(self, username):
        filepath = os.path.join(self.file_data, "deleted.json")
        with open(filepath, 'r') as file:
            deleted_file = json.load(file)
        try:
            del deleted_file[username]
        except FileNotFoundError:
            pass
        with open(filepath, 'w') as file:
            json.dump(deleted_file, file, indent=4)
