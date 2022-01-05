'''
Created on 1 May 2017

@author: jackw
fix path variables
'''

import csv
import os
from time import gmtime, strftime
import NanoZND
import datastore

DS = datastore.DataStore()
ZND = NanoZND.NanoZND()


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
        
        
    
    def CreateBatch(self, batch, user):
        '''
        tick
        creates a new batch object and adds it to the availableSessions list and
        creates a new csv file in  the in progress folder
        '''
        
        
        #check the new batch number does not already exist
        if batch.batchNumber not in self.CSVM.GetFileNamesInProgress() and batch.batchNumber not in self.CSVM.GetFileNamesComplete():
            #set the current batch to this batch
            self.current_batch = batch
            #create the info list for the first row
            time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            Stime_now = str(time_now)
            info = [batch.batchNumber, batch.probe_type, batch.batchQty, user, Stime_now]
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
        makes the current_batch False
        '''
        batch_data = DS.get_batch()
        batch_number = batch_data[0]
        probe_type = batch_data[1]
        probesleft = batch_data[2]
       
        user_data = DS.get_user()
        user = user_data[0]

        if batchnumber == batch_number:
            time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            Stime_now = str(time_now)
            info = [batchnumber, probe_type, probesleft, user, Stime_now]
           
            self.CSVM.WriteListOfListsCSV(info, batchnumber) 
        self.current_batch = False
        
        
        
    def updateBatchInfo(self):
        session_data = []
  
        
        session_data.append(DS.get_batch())
        
       
        self.current_batch = self.GetBatchObject(session_data[0])
        
    def saveProbeInfoToCSVFile(self, list):
        data_list = []
        data_list.extend(list)
        time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        
        data_list.append(time_now)
        self.CSVM.WriteProbeDataToFile(data_list)
        
    def ResumeBatch(self, batch):
        '''
        tick
        pass in a batch object, check if this is in the availableBatchs list , if so: 
        make the batch the current_batch
        '''
        
        if batch.batchNumber in self.CSVM.GetFileNames():
            
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
    
        main_data = DS.get_batch()
        self.current_batch = main_data[0]
      
        
        if self.current_batch == batch:
            self.CSVM.MoveToCompleted(self.current_batch)        #move the batch file to the complete folder
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
       
        try:  
            #get the batch's probe type
            probe_type = info[1]
            batchQty = info[2]
        
        except:
            probe_type = "unable to read"
            batchQty = 0    
        
        batch = Batch(batchNumber)
        batch.probe_type = probe_type
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
        csvfile.close()
        
        
        
    def ReadProbeSerialNumber(self, batchNumber):
        info = self.GetBatchObject(batchNumber)
        
        
        
class CSVManager(object):
    '''
    A TaTT specific wrapper for the CSV Module
    '''
    
    def __init__(self):
        self.path = os.path.join("C:\\Users", os.getenv('username'), "Desktop\\PTT_Results", "")
        self.inProgressPath = os.path.join(self.path, "in_progress", "")
        self.completePath = os.path.join(self.path, "complete", "")
        self.save_path = ""
        
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
                
    
    def get_save_path(self):
        self.save_path = ZND.GetFileLocation()
        print(f"file location is {self.save_path}")
        print(f"set save path {self.path}")
                

    def GetFileNamesInProgress(self):
        '''
        tick
        return a list of batchs in the in progress folder
        '''
        batches = []
    
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
        
        
        
    def WriteProbeDataToFile(self, data_list):
        self.get_save_path()
        filename = DS.get_current_batch()
        
        fullPath = os.path.abspath(self.inProgressPath + filename + '.csv')
        # inputList = [serialNumber,fileName,analyserData,user,pv_data,time]
        
        with open(fullPath, 'a', newline='') as file:
            
            # write pribe data to existing in-progress file
            datawriter = csv.writer(file)
            
            datawriter.writerow(data_list)
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
        self.probe_type = ''
       




