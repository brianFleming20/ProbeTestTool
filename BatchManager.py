'''
Created on 1 May 2017
@author: jackw
fix path variables
'''

import csv
import os
from time import gmtime, strftime
import Datastore

DS = Datastore.Data_Store()


class BatchManager(object):

    def __init__(self):
        '''
        Constructor
        '''
        self.CSVM = CSVManager()
        self.current_batch = None
        self.batchQty = 0

        self.availableBatchs = []
        self.path = os.path.join("C:\\Users", os.getenv('username'), "Desktop\\PTT_Results", "")
        self.inProgressPath = os.path.join(self.path, "in_progress", "")
        self.inProgressPathTest = os.path.join(self.path, "in_progressTest")
        self.completePath = os.path.join(self.path, "complete", "")

    def CreateBatch(self, batch, user, batch_qty):
        '''
        tick
        creates a new batch object and adds it to the availableSessions list and
        creates a new csv file in  the in progress folder
        '''

        self.CSVM = CSVManager()
        self.blank_data = " "
        batch_data = []

        # Check the batch quantity is not over 100 probes
        if batch_qty <= 100 and batch_qty > 0:

            # Check the new batch number does not already exist
            if batch.batchNumber not in self.CSVM.GetFileNamesInProgress() and batch.batchNumber not in self.CSVM.GetFileNamesComplete():
                # set the current batch to this batch

                self.current_batch = batch
                # create the info list for the first row
                time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                Stime_now = str(time_now)
                info = [batch.batchNumber, self.blank_data, batch.probe_type, batch.batchQty, user, self.blank_data,
                        self.blank_data, Stime_now]

                self.CSVM.WriteCSVTitles(batch.batchNumber)  # create header

                self.CSVM.WriteListOfListsCSV(info, batch.batchNumber)  # create the CSV file
                self.availableBatchs = self.CSVM.GetFileNamesInProgress()  # update the list of available batchs

                batch_data.append(batch.batchNumber)
                batch_data.append(batch.probe_type)
                batch_data.append(batch_qty)

                DS.write_to_batch_file(batch_data)
                return True
            else:
                return False
        else:
            return False

    def SuspendBatch(self, batchnumber):
        '''
        tick
        check if batch object is the current batch
        makes the current_batch False
        '''
        self.CSVM = CSVManager()
        self.blank_data = " "

        batch_number = DS.get_probe_data()['Batch']
        probe_type = DS.get_probe_data()['Probe_Type']
        probesleft = DS.get_probe_data()['Left_to_test']

        # user_data = DS.get_user_file()
        user = DS.get_username()

        if batchnumber == batch_number:
            time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            Stime_now = str(time_now)
            info = [batchnumber, self.blank_data, probe_type, probesleft, user, self.blank_data, self.blank_data,
                    self.blank_data, Stime_now]

            self.CSVM.WriteListOfListsCSV(info, batchnumber)
            return True
        else:
            self.current_batch = False
            return False

    def updateBatchInfo(self):
        session_data = []

        session_data.append(DS.get_batch_file())

        self.current_batch = self.GetBatchObject(session_data[0])

    def saveProbeInfoToCSVFile(self, list, batch):
        self.CSVM = CSVManager()
        data_list = []
        data_list.extend(list)
        time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        data_list.append(time_now)
        return self.CSVM.WriteProbeDataToFile(data_list, batch)

    def ResumeBatch(self, batch):
        '''
        tick
        pass in a batch object, check if this is in the availableBatchs list , if so:
        make the batch the current_batch
        '''

        if batch.batchNumber in self.CSVM.get_file_names():
            self.current_batch = batch

    def CompleteBatch(self, batch):
        '''
        tick
        pass in a batch object, check this is the current batch, if so:
        set current_batch = False,
        move the batch file into the 'complete' folder
        refresh the current batch list
        '''

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
        info_line = self.CSVM.ReadLastLine(batchNumber)

        for item in info_line:
            if batchNumber in item[0]:
                info = item[:]

        try:
            # get the batch's probe type
            probe_type = info[2]
            batchQty = info[3]

        except Exception as e:
            probe_type = "000"
            batchQty = 0

        batch = Batch(batchNumber)
        batch.probe_type = probe_type
        batch.batchQty = batchQty

        return batch

    def UpdateResults(self, results, batchNumber):
        '''
        Updates the batch's CSV file with a list of results
        '''
        self.CSVM.WriteListOfListsCSV(results, batchNumber)  # create the CSV file

    def testCSVRead(self, batchNumber):
        fullPathTest = os.path.abspath(self.inProgressPathTest + batchNumber + '.csv')
        with open(fullPathTest, 'rb') as csvfile:
            datareader = csv.reader(csvfile)

    def get_completed_batches(self):
        return self.CSVM.get_file_names_completed()

    def ReadProbeSerialNumber(self, batchNumber):
        info = self.GetBatchObject(batchNumber)


class CSVManager(object):
    '''
    A TaTT specific wrapper for the CSV Module
    '''

    def __init__(self):

        filepath = DS.get_file_location()['File']
        if filepath == False:
            self.path = os.path.join("C:\\Users", os.getenv('username'), "Desktop\\PTT_Results", "")
        else:
            self.path = filepath
        self.inProgressPath = os.path.join(self.path, "in_progress", "")
        self.completePath = os.path.join(self.path, "complete", "")
        self.check_directories()

        # os.rmdir(self.inProgressPath)
        # os.rmdir(self.completePath)

    def check_directories(self):

        '''
        Check that the directories exist, if not create them
        '''
        if not os.path.isdir(self.path):
            try:
                os.makedirs(self.path, 0o777)
            except OSError:
                print("Creation of the directory %s already exists." % self.path)
            else:
                print("Successfully created the directory %s" % self.path)

        if not os.path.isdir(self.inProgressPath):
            try:
                os.makedirs(self.inProgressPath, 0o777)
            except OSError:
                print("Creation of the directory %s failed" % self.inProgressPath)
            else:
                print("Successfully created the directory %s" % self.inProgressPath)

        if not os.path.isdir(self.completePath):
            try:
                os.makedirs(self.completePath, 0o777)
            except OSError:
                print("Creation of the directory %s failed" % self.completePath)
            else:
                print("Successfully created the directory %s" % self.completePath)

    def GetFileNamesInProgress(self):
        '''
        get in progress files

        '''

        # inprogress = "inprogress"
        batches = []
        try:
            list = os.listdir(self.inProgressPath)
        except FileNotFoundError:
            self.check_directories()
        else:
            for item in list:
                newItem = item[:-4]

                batches.append(newItem)

        return batches
        # return self.get_file_names(self, inprogress)

    def get_file_names_completed(self):
        '''
        get completed files

        '''
        batches = []

        try:
            list = os.listdir(self.completePath)
        except FileNotFoundError:
            self.check_directories()
        else:
            for item in list:
                newItem = item[:-4]

                batches.append(str(newItem))

        return batches
        # complete = "complete"
        # return self.get_file_names(self, complete)

    def get_file_names(self, file_type):
        '''
        tick
        return a list of batchs in the in specified folder
        '''
        type_ = None
        if file_type == "inprogresss":
            type_ = self.inProgressPath
        elif file_type == "complete":
            type_ = self.completePath

        batches = []
        try:
            list = os.listdir(type_)
        except FileNotFoundError:
            self.check_directories()
        else:
            for item in list:
                newItem = item[:-4]
                batches.append(newItem)

        return batches

    def GetFileNamesComplete(self):
        '''
        tick
        return a list of batchs in the complete folder
        '''
        # get a list of all the files in the in_progress folder
        list = os.listdir(self.completePath)

        # strip the '.csv' bit off the end
        newList = []
        for item in list:
            newItem = item[2]
            newList.append(newItem)

        return newList

    def WriteListOfListsCSV(self, inputList, fileName):
        '''
        tick
        pass in a list, save each item in the list as a new row in the csv file. Can also handle a list of lists
        '''
        # create the full path
        fullPath = os.path.abspath(self.inProgressPath + fileName + '.csv')

        # write the list to the CSV file
        with open(fullPath, 'a', newline='') as file:
            # Create a writer object from csv module
            datawriter = csv.writer(file)
            # Add contents of list as last row in the csv file
            datawriter.writerow(inputList)
        # file.close()

    def WriteProbeDataToFile(self, data_list, batch):
        filename = DS.get_current_batch()

        fullPath = os.path.abspath(self.inProgressPath + batch + '.csv')
        # inputList = [serialNumber,fileName,analyserData,user,pv_data,time]
        try:
            with open(fullPath, 'a', newline='') as file:

                # write pribe data to existing in-progress file
                datawriter = csv.writer(file)
                datawriter.writerow(data_list)
                return True
        except FileNotFoundError:
            return False

    def WriteCSVTitles(self, fileName):
        '''
        tick
        pass in a list, save each item in the list as a new row in the csv file. Can also handle a list of lists
        '''
        # create the full path
        fullPath = os.path.abspath(self.inProgressPath + fileName + '.csv')
        header = ['Batch No', 'Serial Number', 'Batch Type', 'Batch Qty', 'Username', 'Probe length data',
                  'NanoVNA marker3', ' Passed ', 'Date and Time Tested']
        # write the list to the CSV file
        with open(fullPath, 'a+', newline='') as csvfile:
            datawriter = csv.writer(csvfile)
            datawriter.writerow(header)
        csvfile.close()

    def MoveToCompleted(self, fileName):
        '''
        tick
        pass in a file name, move this file from the inprogress folder to the completed folder
        '''
        originalPath = os.path.abspath(self.inProgressPath + fileName + '.csv')
        destinationPath = os.path.abspath(self.completePath + fileName + '.csv')

        os.renames(originalPath, destinationPath)

    def ReadFirstLine(self, fileName):
        '''
        pass in a filename string and a number of lines.
        will return a list of lists with each list being a line
        '''
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
                elif line == []:
                    pass
                else:
                    eachBatch.append(line)

            batches.append(eachBatch[-1])
        return batches

    def ReadAllLines(self, fileName):
        '''
        pass in a filename string and a number of lines.
        will return a list of lists with each list being a line
        '''
        # originalPath = r"C:\Users\jackw\Dropbox\BSc (Hons) Engineering Studies\TaTT_results\in_progress\\"

        fullPath = os.path.abspath(self.inProgressPath + fileName + '.csv')

        with open(fullPath) as f:
            lis = [line.split() for line in f]  # create a list of lists
            return [lis]


#             for i,x in enumerate(lis):              #print the list items
#                 print (i,x)


class Batch(object):
    '''
    USed to create batch objects.
    '''

    def __init__(self, batchNumber):
        self.batchNumber = batchNumber
        self.probesProgrammed = 0
        self.batchQty = 0
        self.probe_type = ''