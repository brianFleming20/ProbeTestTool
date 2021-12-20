'''
Created on 28 Apr 2017

@author: jackw
'''

from time import gmtime, strftime
import time


# class PI(object):
#     """
#     SC18IM700 commands
    
#     S 53 I2C start
#     P 50 I2C stop
#     R 52 read SC18IM internal register
#     W 57 write to SC18IM internal register
#     I 49 read IO port
#     O 4F write to GPIO port
#     Z 5A power down
    
#     A0 write address
#     A1 read address

#     """
#     transfered all code to ProbeInterface module
 
   
   
class ProbeData(object):
    '''
    Responsible for creating the full 256 bytes of EEPROM data.
    '''
    
    
    def __init__(self):
        '''
        '''
        self.timeStamp = ''
        self.typeBytes = ''
        
        self.DP240TypeBytes = ['32','46','30','4a']
        self.DP12TypeBytes = ['32','30','43','4a']
        self.DP6TypeBytes = ['32','30','36','4a']
        self.I2CTypeBytes = ['36','34','38','4a']
        self.I2PTypeBytes = ['36','31','38','4a']
        self.I2STypeBytes = ['36','30','36','4a']
        self.KDP72TypeBytes = ['35','34','38','4a']
        self.SDP30TypeBytes = ['53','33','30','4a']


    
    def GenerateDataString(self, probeType):
        '''
        Pass in a probe type, returns the full 255 byte probe data including time stamped serial number
        
        The first 8 and last 2 values of each list item are for SC18IM configuration, the bytes inbetween are that actual data that is written
        '''
        probezeros = ['53A00900000000000000000050', '53A00908000000000000000050', '53A00910000000000000000050', '53A00918000000000000000050', '53A00920000000000000000050', '53A00928000000000000000050', '53A00930000000000000000050', '53A00938000000000000000050', '53A00940000000000000000050', '53A00948000000000000000050', '53A00950000000000000000050', '53A00958000000000000000050', '53A00960000000000000000050', '53A00968000000000000000050', '53A00970000000000000000050', '53A00978000000000000000050', '53A00980000000000000000050', '53A00988000000000000000050', '53A00990000000000000000050', '53A00998000000000000000050', '53A009a0000000000000000050', '53A009a8000000000000000050', '53A009b0000000000000000050', '53A009b8000000000000000050', '53A009c0000000000000000050', '53A009c8000000000000000050', '53A009d0000000000000000050', '53A009d8000000000000000050', '53A009e0000000000000000050', '53A009e8000000000000000050', '53A009f0000000000000000050', '53A009f8000000000000000050']
        probeData = ['53A00910303030303030303050', '53A00918303030303030303050', '53A00920303030303030303050', '53A00928303030303030300050', '53A009303001f00a3030303050', '53A00938303030303030303050', '53A009402863292044656c7450', '53A009486578204d6564696350', '53A00950616c204c696d697450', '53A00958656420323030370050', '53A00960303030303030303050', '53A00968303030303030303050', '53A00970303030303030303050', '53A00978303030303030303050', '53A00980303030303030303050', '53A00988303030303030303050', '53A00990303030303030303050', '53A00998303030303030303050', '53A009a0303030303030303050', '53A009a8303030303030303050', '53A009b0303030303030303050', '53A009b8303030303030303050', '53A009c0303030303030303050', '53A009c8303030303030303050', '53A009d0303030303030303050', '53A009d8303030303030303050', '53A009e0303030303030303050', '53A009e8303030303030303050', '53A009f0303030303030303050', '53A009f8303030303030303050']
        SDprobeData = ['53A00910303030303030303050', '53A00918303030303030303050', '53A00920303030303030303050', '53A00928303030303030300050', '53A0093030fafa1e3030303050', '53A00938303030303030303050', '53A009402863292044656c7450', '53A009486578204d6564696350', '53A00950616c204c696d697450', '53A00958656420323030370050', '53A00960303030303030303050', '53A00968303030303030303050', '53A00970303030303030303050', '53A00978303030303030303050', '53A00980303030303030303050', '53A00988303030303030303050', '53A00990303030303030303050', '53A00998303030303030303050', '53A009a0303030303030303050', '53A009a8303030303030303050', '53A009b0303030303030303050', '53A009b8303030303030303050', '53A009c0303030303030303050', '53A009c8303030303030303050', '53A009d0303030303030303050', '53A009d8303030303030303050', '53A009e0303030303030303050', '53A009e8303030303030303050', '53A009f0303030303030303050', '53A009f8303030303030303050']

        firstStart = '53A00900'
        secondStart = '53A00908'
        end = '50'
        
        if probeType == 'Blank':
            return probezeros
        
        #set the correct probe type bytes
        if probeType == 'DP240':
            typeBytes = self.DP240TypeBytes
        elif probeType == 'DP12':
            typeBytes = self.DP12TypeBytes
        elif probeType == 'DP6':
            typeBytes = self.DP6TypeBytes
        elif probeType == 'I2C':
            typeBytes = self.I2CTypeBytes
        elif probeType == 'I2S':
            typeBytes = self.I2STypeBytes
        elif probeType == 'I2P':
            typeBytes = self.I2PTypeBytes
        elif probeType == 'KDP72':
            typeBytes = self.KDP72TypeBytes
        elif probeType == 'I2P':
            typeBytes = self.I2PTypeBytes
        elif probeType == 'SDP30':
            typeBytes = self.SDP30TypeBytes
            
        #create a 12 byte timestamp of the format
        timeStamp = strftime("%Y%m%d%H%M%S", gmtime())
        timeStampFormatted = timeStamp[2:]
        timeStampASCII = []
        for item in timeStampFormatted:
            x = (ord(item))
            timeStampASCII.append(format((x), "x"))
        
        #stick the type bytes and the timestamp together 
        serialNumber = typeBytes + timeStampASCII
        
        #put them in a format that can be sent via the SC18IM
        lower  = serialNumber[0:8]
        upper = serialNumber[8:]
        slower = ''.join(lower)
        supper = ''.join(upper)
        firstByte = firstStart + slower + end
        secondByte = secondStart + supper + end
        
        #add them to the probe data list
        SDprobeData.insert(0, secondByte)
        SDprobeData.insert(0, firstByte)
        
        #create a single string of the actual data for error checking
        stripped = ''
        for item in SDprobeData:
            stripped = stripped + item[8:-2]
        return SDprobeData, stripped


# PI = PI()
# PD = ProbeData()
# PI.Connect('COM3')
# sn = PI.ProbeReadAllBytes()
# 
# print(sn)



