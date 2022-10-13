import unittest
from BatchManager import *
import Datastore
import Ports
import time

BM = BatchManager()
DS = Datastore.Data_Store()
P = Ports


class BatchTests(unittest.TestCase):
    
    def setUp(self):
        self.path = BM.path
        self.blank_data = None
    
    def test_create_new_batch(self):
        print("Create Batch")

        new_batch_number = 9876
        new_batch_type = "DP12"
        user = "brian"
        batch_qty = 100
        eachBatch = []
        print(f"path = {self.path}")

        batch = P.Batch(f"{new_batch_number}B")
        batch.probe_type = new_batch_type
        inProgressPath = os.path.join(self.path, "in_progress", "")
        fullPath = os.path.abspath(inProgressPath + batch.batchNumber + '.csv')
        result = BM.CreateBatch(batch,user)
        time.sleep(1)
        with open(fullPath, 'r') as csvfile:
            datareader = csv.reader(csvfile)

            for line in datareader:
                eachBatch.append(line)
        file_result = eachBatch[-1][0]
        
        self.assertEqual(result, False)
        self.assertTrue(file_result,new_batch_number)
        
        # Check for batch quantity of over 100 probes
        print("Test 101 batch qty")
        # new_batch_number += 1
        batch = P.Batch(f"{new_batch_number}B")
        batch.probe_type = new_batch_type
        batch_qty = 101
        result = BM.CreateBatch(batch,user)
        
        self.assertEqual(result,False)
        
        new_batch_number += 1
        batch = P.Batch(f"{new_batch_number}B")
        batch.probe_type = new_batch_type
        print("Test -1 batch qty")
        batch_qty = -1
        
        result = BM.CreateBatch(batch,user)
        
        self.assertEqual(result, False)

    def test_save_probe_info(self):
        # add batch number
        print("Save data to file")
        data_list_to_file = []
        batch = "9876B"
        snum = "20CD20220207141516"
        eachBatch = []

        inProgressPath = os.path.join(self.path, "in_progress", "")
        fullPath = os.path.abspath(inProgressPath + batch + '.csv')
        
        data_list_to_file.append(" ")                     # by pass the batch number column
        data_list_to_file.append(snum)                    # insert serial number
        data_list_to_file.append("DP12")   # insert probe type
        data_list_to_file.append(" ")
        data_list_to_file.append("brian") # insert the logged in user
        data_list_to_file.append("1.10")             # insert probe marker data           
        data_list_to_file.append(301)             # insert ODM data
        data_list_to_file.append(0)
        
        result = BM.saveProbeInfoToCSVFile(data_list_to_file, batch)
        
        with open(fullPath, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            
            for line in datareader: 
                eachBatch.append(line)   
       
        file_result = eachBatch[-1][1]

        self.assertEqual(result, True)
        
        self.assertEqual(file_result, snum)
    

if __name__ == '__main__':
    unittest.main()