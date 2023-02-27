"""
Created on 1 May 2017
@author: jackw
@author: Brian F
Creates .csv files and reads the entire file contents or the last line of the required file.
"""

import csv
import os
from time import gmtime, strftime, sleep
import Datastore
import Ports

DS = Datastore.DataStore()
P = Ports


class BatchManager(object):

    def __init__(self):
        #####################
        # Constructor       #
        #####################
        self.CSVM = CSVManager()
        self.current_batch = None
        self.batchQty = 0
        self.blank_data = "-"
        self.availableBatchs = []
        self.path = os.path.join("C:\\Users", os.getenv('username'), "Documents\\PTT_Results", "")
        self.inProgressPath = os.path.join(self.path, "in_progress", "")
        self.inProgressPathTest = os.path.join(self.path, "in_progressTest")
        self.completePath = os.path.join(self.path, "complete", "")

    def CreateBatch(self, batch, user):
        ############################################################################
        # tick                                                                     #
        # creates a new batch object and adds it to the availableSessions list and #
        # creates a new csv file in  the in progress folder                        #
        #############################################################################
        complete = False
        #####################################################
        # Check the batch quantity is not over 100 probes   #
        #####################################################
        if 100 >= batch.batchQty > 0:
            ######################################################
            # Check the new batch number does not already exist  #
            ######################################################
            if batch.batchNumber not in self.CSVM.GetFileNamesComplete():
                if batch.batchNumber not in self.CSVM.GetFileNamesInProgress():
                    ##########################################
                    # set the current batch to this batch    #
                    # self.current_batch = batch             #
                    # create the info list for the first row #
                    ##########################################
                    time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    Stime_now = str(time_now)
                    info = [batch.batchNumber, self.blank_data, batch.probe_type, batch.batchQty, user, self.blank_data,
                            self.blank_data, self.blank_data, f"On {Stime_now}"]
                    self.CSVM.WriteCSVTitles(batch.batchNumber)  # create header #

                    self.CSVM.WriteListOfListsCSV(info, batch.batchNumber)  # create the CSV file
                    # self.availableBatchs = self.CSVM.GetFileNamesInProgress()  # update the list of available batchs
                    batch_data = P.Probes(batch.probe_type, batch.batchNumber, 0, int(batch.batchQty))
                    DS.write_probe_data(batch_data)
                    complete = True
        return complete

    def SuspendBatch(self, batch_number):
        ################################################
        # tick                                         #
        # check if batch object is the current batch   #
        # makes the current_batch False                #
        ################################################
        self.blank_data = " "
        batch_num = DS.get_probe_data()['Batch']
        probe_type = DS.get_probe_data()['Probe_Type']
        probes_left = DS.get_probe_data()['Left_to_test']
        user = DS.get_username()
        if batch_number == batch_num:
            time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            Stime_now = str(time_now)
            info = [batch_number, " Suspended Batch ", probe_type, probes_left, user, " ", " ", " ", f"On {Stime_now}"]
            return self.CSVM.WriteListOfListsCSV(info, batch_number)
        else:
            self.current_batch = False
            return False

    def saveProbeInfoToCSVFile(self, data, batch):
        ###############################################
        # Save probe data to file with appended date  #
        # format. This is saved to the batch number   #
        # file.                                       #
        ###############################################
        data_list = []
        data_list.extend(data)
        time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        data_list.append(f"On {time_now}")
        return self.CSVM.WriteListOfListsCSV(data_list, batch)

    def CompleteBatch(self, batch):
        ######################################################################
        # tick                                                               #
        # pass in a batch object, check this is the current batch, if so:    #
        # set current_batch = False,                                         #
        # move the batch file into the 'complete' folder                     #
        # refresh the current batch list                                     #
        ######################################################################
        check = True
        self.current_batch = DS.get_current_batch()
        for file in self.get_completed_batches():
            if file[:-4] == batch:
                check = False
        if self.current_batch == batch and check:
            self.CSVM.MoveToCompleted(batch)
        else:
            P.probe_canvas(self, f"Complete file contains {batch}", False)
            sleep(2)
            P.text_destroy(self)

    def GetAvailableBatches(self):
        return self.CSVM.GetFileNamesInProgress()

    def get_batch_line(self, batchNumber, complete):
        return self.CSVM.ReadLastLine(batchNumber, complete)

    def UpdateResults(self, results, batchNumber):
        ########################################################
        # Updates the batch's CSV file with a list of results  #
        ########################################################
        self.CSVM.WriteListOfListsCSV(results, batchNumber)  # create the CSV file

    def get_completed_batches(self):
        return self.CSVM.get_file_names_completed()

    def competed_text(self, user, probe_type, batch_number, failures, passed):
        time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        Stime_now = str(time_now)
        batch_info = [batch_number, " Completed by  ", user, " of ", probe_type, "-", f"On {Stime_now}",
                      f" Failed = {failures}", f"Passed = {passed}"]
        self.CSVM.WriteListOfListsCSV(batch_info, batch_number)


class CSVManager(object):
    ###############################################
    # A TaTT specific wrapper for the CSV Module  #
    ###############################################

    def __init__(self):
        self.inProgressPath = None
        self.completePath = None
        self.path = None
        self.check_file_location()

    def check_directories(self):
        #########################################################
        # Check that the directories exist, if not create them  #
        #########################################################
        if not os.path.isdir(self.path):
            try:
                os.makedirs(self.path, 0o777)
            except OSError:
                pass
        if not os.path.isdir(self.inProgressPath):
            try:
                os.makedirs(self.inProgressPath, 0o777)
            except OSError:
                pass
        if not os.path.isdir(self.completePath):
            try:
                os.makedirs(self.completePath, 0o777)
            except OSError:
                pass

    def check_file_location(self):
        filepath = DS.get_file_location()
        if not filepath:
            self.path = os.path.join("C:\\Users", os.getenv('username'), "Documents\\PTT_Results", "")
        else:
            self.path = filepath['File']
        self.inProgressPath = os.path.join(self.path, "in_progress", "")
        self.completePath = os.path.join(self.path, "complete", "")

    def GetFileNamesInProgress(self):
        ###############################
        # get in progress files       #
        ###############################
        self.check_file_location()
        batches = []
        try:
            a_list = os.listdir(self.inProgressPath)
        except FileNotFoundError:
            self.check_directories()
        else:
            for item in a_list:
                batches.append(item[:-4])
        return batches

    def get_file_names_completed(self):
        ########################
        # get completed files  #
        ########################
        self.check_file_location()
        batches = []
        try:
            a_list = os.listdir(self.completePath)
        except FileNotFoundError:
            self.check_directories()
        else:
            for item in a_list:
                newItem = item[:-4]
                batches.append(str(newItem))
        return batches

    def get_file_names(self, file_type):
        #########################################################
        # tick                                                  #
        # return a list of batchs in the in specified folder    #
        #########################################################
        type_ = None
        if file_type == "in_progress":
            type_ = self.inProgressPath
        elif file_type == "complete":
            type_ = self.completePath
        batches = []
        try:
            a_list = os.listdir(type_)
        except FileNotFoundError:
            self.check_directories()
        else:
            for item in a_list:
                newItem = item[:-4]
                batches.append(newItem)
        return batches

    def GetFileNamesComplete(self):
        #####################################################
        # tick                                              #
        # return a list of batches in the complete folder   #
        #####################################################
        # get a list of all the files in the in_progress folder
        a_list = os.listdir(self.completePath)
        # strip the '.csv' bit off the end
        newList = []
        for item in a_list:
            newList.append(item[2])
        return newList

    def WriteListOfListsCSV(self, inputList, fileName):
        #############################################################################################################
        # tick                                                                                                      #
        # pass in a list, save each item in the list as a new row in the csv file. Can also handle a list of lists  #
        #############################################################################################################
        # create the full path
        fullPath = os.path.abspath(self.inProgressPath + fileName + '.csv')
        try:
            with open(fullPath, 'a+', newline='') as file:
                data_writer = csv.writer(file)
                data_writer.writerow(inputList)
                return True
        except FileNotFoundError:
            return False

    def WriteCSVTitles(self, fileName):
        #############################################################################################################
        # tick                                                                                                      #
        # pass in a list, save each item in the list as a new row in the csv file. Can also handle a list of lists  #
        #############################################################################################################
        header = ['Batch No', 'Serial Number', 'Batch Type', 'Batch Qty', 'Username', 'Probe length (tdr)',
                  'NanoVNA marker3', ' ODM PV', 'Date and Time Tested']
        # write the list to the CSV file
        self.WriteListOfListsCSV(header, fileName)

    def MoveToCompleted(self, fileName):
        #################################################################################################
        # tick                                                                                          #
        # pass in a file  name, move this file from the in progress folder to the completed folder       #
        #################################################################################################
        originalPath = os.path.abspath(self.inProgressPath + fileName + '.csv')
        destinationPath = os.path.abspath(self.completePath + fileName + '.csv')
        os.renames(originalPath, destinationPath)

    def ReadFirstLine(self, fileName):
        ################################################################
        # pass in a filename string and a number of lines.             #
        # will return a list of lists with each list being a line      #
        ################################################################
        # originalPath = r"C:\Users\jackw\Dropbox\BSc (Hons) Engineering Studies\TaTT_results\in_progress\\"
        fullPath = os.path.abspath(self.inProgressPath + fileName + '.csv')
        with open(fullPath) as f:
            lis = [line.split() for line in f]
        return lis[0]

    def ReadLastLine(self, fileName, complete):
        if complete:
            path = self.completePath
        else:
            path = self.inProgressPath
        fullPath = os.path.abspath(path + fileName + '.csv')
        with open(fullPath,  "r", encoding="utf-8", errors="ignore") as csvfile:
            datareader = csvfile.readlines()[-1]
        return datareader.split(',')

    def read_all_lines(self, folder, batch):
        lines = []
        fullPath = os.path.abspath(folder + batch)
        with open(fullPath,  "r", encoding="utf-8", errors="ignore") as file:
            data_reader = csv.reader(file)
            for line in data_reader:
                lines.append(line)
        return lines

    def remove_batch(self, batch):
        path = self.inProgressPath
        a_list = os.listdir(path)
        file = os.path.abspath(path + batch + '.csv')
        find = f"{batch}.csv"
        if find in a_list:
            os.remove(file)
