'''
Created on 1 May 2017

@author: jackw
fix path variables
'''

import csv
import os
from time import gmtime, strftime
import pickle
import pdb


class BatchManager(object):
    

    def __init__(self):
        '''
        Constructor
        '''
        self.CSVM = CSVManager()
        self.currentBatch = None
        self.batchQty = 0
        
        self.availableBatchs = []
        self.path = os.path.join("C:\\Users", os.getenv('username'), "Desktop\\PTT_Results", "")
        self.inProgressPath = os.path.join(self.path, "in_progress", "")
        self.inProgressPathTest = os.path.join(self.path, "in_progressTest")
        self.completePath = os.path.join(self.path, "complete", "")
        
        
    
    def CreateBatch(self, batch, user):
        '''
        tick
        creates a new batch object and adds it to the availableSessions list and
        creates a new csv file in  the in progress folder
        '''
        
        
        #check the new batch number does not already exist
        if batch.batchNumber not in self.CSVM.GetFileNamesInProgress() and batch.batchNumber not in self.CSVM.GetFileNamesComplete():
            #set the current batch to this batch
            self.currentBatch = batch
            #create the info list for the first row
            timeNow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            StimeNow = str(timeNow)
            info = [batch.batchNumber, batch.probeType, batch.batchQty, user, StimeNow]
            testBatch = "222test"
            
            self.CSVM.WriteCSVTitles(batch.batchNumber)    #create header
            
            self.CSVM.WriteListOfListsCSV(info, batch.batchNumber)    #create the CSV file
            self.availableBatchs = self.CSVM.GetFileNamesInProgress() #update the list of available batchs
            
        else:
            return False
            
    def SuspendBatch(self, batchnumber):
        '''
        tick
        check if batch object is the current batch
        makes the currentBatch False
        '''
        with open("file_batch", "rb") as file:
            myvar = pickle.load(file)
            batchNumber = myvar[0]
            probetype = myvar[1]
            probesleft = myvar[2]
        file.close()
        with open('file.ptt','rb') as file:
            myvar = pickle.load(file)
        
            user = myvar[0]
        file.close()    
        if batchnumber == batchNumber:
            timeNow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            StimeNow = str(timeNow)
            info = [batchnumber, probetype, probesleft, user, timeNow]
           
            self.CSVM.WriteListOfListsCSV(info, batchnumber) 
        self.currentBatch = False
        
    def updateBatchInfo(self):
        session_data = []
        with open('file.ptt', 'rb') as file:
            myvar = pickle.load(file)
        session_data.extend(myvar)
        file.close()
       
        self.currentBatch = self.GetBatchObject(session_data[2])
        
    def saveProbeInfoToCSVFile(self, serialNumber, analyserData, user, batchNumber):
       
        self.CSVM.WriteProbeDataToFile(serialNumber,analyserData,user, batchNumber)
        
    def ResumeBatch(self, batch):
        '''
        tick
        pass in a batch object, check if this is in the availableBatchs list , if so: 
        make the batch the currentBatch
        '''
        if batch.batchNumber in self.CSVM.GetFileNames():
            
            self.currentBatch = batch
        
    def CompleteBatch(self, batch):
        '''
        tick
        pass in a batch object, check this is the current batch, if so: 
        set currentBatch = False, 
        move the batch file into the 'complete' folder 
        refresh the current batch list
        '''  
        
        
        with open('file.ptt', 'rb') as file:
      
        # Call load method to deserialze
            myvar = pickle.load(file)
            self.currentBatch = ''.join(myvar[2])
            
        file.close()
      
        
        if self.currentBatch == batch:
            self.CSVM.MoveToCompleted(self.currentBatch)        #move the batch file to the complete folder
            self.availableBatchs = self.CSVM.GetFileNamesInProgress()     #update the availableBaths list
        else:
            return False
        
        
    def GetAvailableBatches(self):
        batchList = []
        for item in self.CSVM.GetFileNamesInProgress():
            if item != 'FOO':
                batchList.append(item)
                 
        return batchList
    
    
    
    def GetBatchObject(self, batchNumber):
        #get the batch's info list
      
        info = self.CSVM.ReadLastLine(batchNumber)
        
        for item in info:
                
            if batchNumber in item[0]:
                info = item[:]
                    
        
        
        
        
           
        
        #get the batch's probe type
        probeType = info[1]
        batchQty = info[2]
        
        #get the batch's probes programmed value
        #probesProgrammed = int(info[2])
        
        batch = Batch(batchNumber)
        batch.probeType = probeType
        batch.batchQty = batchQty
        
        return batch
        

    def UpdateResults(self, results, batchNumber):
        '''
        Updates the batch's CSV file with a list of results
        '''
        self.CSVM.WriteListOfListsCSV(results, batchNumber)   #create the CSV file
        
    def testCSVRead(self, batchNumber):
        fullPathTest = os.path.abspath(self.inProgressPathTest + batchNumber + '.csv')
        with open(fullPathTest, 'rb') as csvfile:
            datareader = csv.reader(csvfile)
            print("data in {}".format(datareader))
        csvfile.close()
        
    def ReadProbeSerialNumber(self, batchNumber):
        info = self.GetBatchObject(batchNumber)
        print("serial Number = {}".format(info))
        
        
class CSVManager(object):
    '''
    A TaTT specific wrapper for the CSV Module
    '''
    
    def __init__(self):
        self.path = os.path.join("C:\\Users", os.getenv('username'), "Desktop\\PTT_Results", "")
        self.inProgressPath = os.path.join(self.path, "in_progress", "")
        self.completePath = os.path.join(self.path, "complete", "")
        
        #os.rmdir(self.inProgressPath)
        #os.rmdir(self.completePath)
        
        '''
        Check that the directories exist, if not create them        
        '''
        if not os.path.isdir(self.path):
            try:
                os.makedirs(self.path, 0o777)
            except OSError:
                print ("Creation of the directory %s failed" % self.path)
            else:
                print ("Successfully created the directory %s" % self.path)

        if not os.path.isdir(self.inProgressPath):
            try:
                os.makedirs(self.inProgressPath, 0o777)
            except OSError:
                print ("Creation of the directory %s failed" % self.inProgressPath)
            else:
                print ("Successfully created the directory %s" % self.inProgressPath)

        if not os.path.isdir(self.completePath):
            try:
                os.makedirs(self.completePath, 0o777)
            except OSError:
                print ("Creation of the directory %s failed" % self.completePath)
            else:
                print ("Successfully created the directory %s" % self.completePath)

    def GetFileNamesInProgress(self):
        '''
        tick
        return a list of batchs in the in progress folder
        '''
        #get a list of all the files in the in_progress folder
        # list = os.listdir(self.inProgressPath)
        
        batches = []
        #strip the '.csv' bit off the end
        # newList = []
        
        # for item in list:
        #     newItem = item[:-4]
        #     newList.append(newItem)
            
        
        list = os.listdir(self.inProgressPath) 
       
        for item in list:
            newItem = item[:-4]
            batches.append(newItem)
        
        return batches
    
    def GetFileNamesComplete(self):
        '''
        tick
        return a list of batchs in the complete folder
        '''
        #get a list of all the files in the in_progress folder
        list = os.listdir(self.completePath)
        
        #strip the '.csv' bit off the end
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
        #create the full path
        fullPath = os.path.abspath(self.inProgressPath + fileName + '.csv')
        
        #write the list to the CSV file
        with open(fullPath, 'a', newline='') as file:
            
            # Create a writer object from csv module
            datawriter = csv.writer(file)
            # Add contents of list as last row in the csv file
            datawriter.writerow(inputList)
        file.close()
        
    def WriteProbeDataToFile(self, serialNumber, analyserData, user, fileName):
        # print("saved")    
        # print("serial number {}".format(serialNumber))
        # print("analyser data {}".format(analyserData))
        # print("user {}".format(user))
        # print("batch {}".format(fileName))
        
        
        fullPath = os.path.abspath(self.inProgressPath + fileName + '.csv')
        inputList = [serialNumber,fileName,analyserData,user]
        with open(fullPath, 'a', newline='') as file:
            
            # write pribe data to existing in-progress file
            datawriter = csv.writer(file)
            
            datawriter.writerow(inputList)
        file.close()

    def WriteCSVTitles(self, fileName):
        '''
        tick
        pass in a list, save each item in the list as a new row in the csv file. Can also handle a list of lists
        '''
        #create the full path
        fullPath = os.path.abspath(self.inProgressPath + fileName + '.csv')
        header = ['Batch No','Batch Type','Batch Qty','Username','Date and Time Tested']
        #write the list to the CSV file
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
        #originalPath = r"C:\Users\jackw\Dropbox\BSc (Hons) Engineering Studies\TaTT_results\in_progress\\" 
        
        fullPath = os.path.abspath(self.inProgressPath + fileName + '.csv')
        
        with open(fullPath) as f:
            lis=[line.split() for line in f] 
        return lis[0]
#             print(lis)       # create a list of lists
#             for i,x in enumerate(lis):              #print the list items 
#                 print (i,x)


    def ReadLastLine(self, fileName):
        
        fullPathTest = os.path.abspath(self.inProgressPath + fileName + '.csv')
        batches = []
        eachBatch = []
        
        with open(fullPathTest, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            
            for line in datareader:
                
                if "Batch No" in line:
                    pass
                elif line == []:
                    pass
                else:
                    eachBatch.append(line)
                    
            batches.append(eachBatch[-1])
            
                    
                
        csvfile.close()   
        
       
        return batches
        
    
    
    def ReadAllLines(self, fileName):
        '''
        pass in a filename string and a number of lines.
        will return a list of lists with each list being a line
        '''
        #originalPath = r"C:\Users\jackw\Dropbox\BSc (Hons) Engineering Studies\TaTT_results\in_progress\\" 
        
        fullPath = os.path.abspath(self.inProgressPath + fileName + '.csv')
        
        with open(fullPath) as f:
            lis=[line.split() for line in f] # create a list of lists
            return[lis]
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
        self.probeType = ''
       




