'''
Created on 1 May 2017
@author: jackw
Amended: BrianF
fix path variables
'''

import csv
import os
from time import gmtime, strftime
import Datastore
import Ports
from tkinter import messagebox as mb

DS = Datastore.Data_Store()
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

        self.CSVM = CSVManager()
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
                            self.blank_data, Stime_now]
                    self.CSVM.WriteCSVTitles(batch.batchNumber)  # create header #

                    self.CSVM.WriteListOfListsCSV(info, batch.batchNumber)  # create the CSV file
                    # self.availableBatchs = self.CSVM.GetFileNamesInProgress()  # update the list of available batchs
                    batch_data = P.Probes(batch.probe_type, batch.batchNumber, 0, int(batch.batchQty))
                    DS.write_probe_data(batch_data)
                    return True
                else:
                    return False
        else:
            return False

    def SuspendBatch(self, batchnumber):
        ################################################
        # tick                                         #
        # check if batch object is the current batch   #
        # makes the current_batch False                #
        ################################################
        self.CSVM = CSVManager()
        self.blank_data = " "

        batch_number = DS.get_probe_data()['Batch']
        probe_type = DS.get_probe_data()['Probe_Type']
        probes_left = DS.get_probe_data()['Left_to_test']

        user = DS.get_username()

        if batchnumber == batch_number:
            time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            Stime_now = str(time_now)
            info = [batchnumber, " Suspended Batch ", probe_type, probes_left, user, " ", " ", " On ", Stime_now]
            return self.CSVM.WriteListOfListsCSV(info, batchnumber)
        else:
            self.current_batch = False
            return False

    def updateBatchInfo(self):
        self.current_batch = self.GetBatchObject(DS.get_current_batch())

    def saveProbeInfoToCSVFile(self, data, batch):
        self.CSVM = CSVManager()
        data_list = []
        data_list.extend(data)
        time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        data_list.append(time_now)
        return self.CSVM.WriteListOfListsCSV(data_list, batch)

    def CompleteBatch(self, batch):
        ######################################################################
        # tick                                                               #
        # pass in a batch object, check this is the current batch, if so:    #
        # set current_batch = False,                                         #
        # move the batch file into the 'complete' folder                     #
        # refresh the current batch list                                     #
        ######################################################################
        # # Call load method to deserialze

        self.current_batch = DS.get_current_batch()

        if self.current_batch == batch:
            self.CSVM.MoveToCompleted(self.current_batch)
            # move the batch file to the complete folder
            try:
                self.availableBatchs = self.CSVM.GetFileNamesInProgress()
                # update the availableBaths list
            except FileExistsError:
                if not os.path.isdir(self.inProgressPath):
                    self.CSVM.check_directories()
            else:
                self.availableBatchs = self.CSVM.GetFileNamesInProgress()
                return True
        else:
            return False

    def GetAvailableBatches(self):
        batchList = []
        for item in self.CSVM.GetFileNamesInProgress():
            if item != 'FOO':
                batchList.append(item)

        return batchList

    def GetBatchObject(self, batchNumber):
        # get the batch's info list
        info = ['0','0','-','-']
        info_line = self.CSVM.ReadLastLine(batchNumber)
        for item in info_line:
            if batchNumber in item[0]:
                info = item[:]
        try:
            # get the batch's probe type
            probe_type = info[2]
            batchQty = info[3]
        except FileNotFoundError:
            probe_type = "000"
            batchQty = 0

        batch = Batch(batchNumber)
        batch.probe_type = probe_type
        batch.batchQty = batchQty

        return batch

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
        batch_info = [batch_number, " Completed by - ", user, " of ", probe_type, " On ", Stime_now,
                      f" Failed = {failures}", f"Passed = {passed}"]
        self.CSVM.WriteListOfListsCSV(batch_info, batch_number)


class CSVManager(object):
    ###############################################
    # A TaTT specific wrapper for the CSV Module  #
    ###############################################

    def __init__(self):
        # default_loc = "/PTT_Results"
        filepath = DS.get_file_location()
        if not filepath:
            self.path = os.path.join("C:\\Users", os.getenv('username'), "Documents\\PTT_Results", "")
        else:
            self.path = filepath['File']
        self.inProgressPath = os.path.join(self.path, "in_progress", "")
        self.completePath = os.path.join(self.path, "complete", "")
        self.check_directories()

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

    def GetFileNamesInProgress(self):
        ###############################
        # get in progress files       #
        ###############################

        batches = []
        try:
            a_list = os.listdir(self.inProgressPath)
        except FileNotFoundError:
            self.check_directories()
        else:
            for item in a_list:
                newItem = item[:-4]

                batches.append(newItem)

        return batches

    def get_file_names_completed(self):
        ########################
        # get completed files  #
        ########################
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
            newItem = item[2]
            newList.append(newItem)

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
        # pass in a file  name, move this file from the inprogress folder to the completed folder       #
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

    #

    def ReadLastLine(self, fileName):

        fullPath = os.path.abspath(self.inProgressPath + fileName + '.csv')
        batches = []
        eachBatch = []

        with open(fullPath, 'r') as csvfile:
            datareader = csv.reader(csvfile)

            for line in datareader:
                if "Batch No" in line:
                    pass
                elif not line:
                    pass
                else:
                    eachBatch.append(line)

            batches.append(eachBatch[-1])
        return batches

    # def ReadAllLines(self, fileName):
    #     ################################################################
    #     # pass in a filename string and a number of lines.             #
    #     # will return a list of lists with each list being a line      #
    #     ################################################################
    #     # originalPath = r"C:\Users\jackw\Dropbox\BSc (Hons) Engineering Studies\TaTT_results\in_progress\\"
    #
    #     fullPath = os.path.abspath(self.inProgressPath + fileName + '.csv')
    #
    #     with open(fullPath) as f:
    #         lis = [line.split() for line in f]  # create a list of lists
    #         return lis

    #             for i,x in enumerate(lis):              #print the list items
    #                 print (i,x)

    def read_all_lines(self, folder,batch):
        lines = []
        fullPath = os.path.abspath(folder + batch)
        with open(fullPath) as file:
            data_reader = csv.reader(file)
            for line in data_reader:
                lines.append(line)
        return lines


class Batch(object):
    ####################################
    # USed to create batch objects.    #
    ####################################

    def __init__(self, batchNumber):
        self.batchNumber = batchNumber
        self.probesProgrammed = 0
        self.batchQty = 0
        self.probe_type = ''
