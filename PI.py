'''
Created on 28 Apr 2017
@author: jackw
'''

from time import gmtime, strftime


class ProbeData(object):
    '''
    Responsible for creating the full 256 bytes of EEPROM data.
    '''

    def __init__(self):
        '''
        '''
        self.probeData = False
        self.timeStamp = ''
        self.DP240TypeBytes = ['32', '46', '30', '44']
        self.DP12TypeBytes = ['32', '30', '43', '44']
        self.DP6TypeBytes = ['32', '30', '36', '44']
        self.I2CTypeBytes = ['36', '34', '38', '44']
        self.I2PTypeBytes = ['36', '31', '38', '44']
        self.I2STypeBytes = ['36', '30', '36', '44']
        self.KDP72TypeBytes = ['35', '34', '38', '44']
        self.Blank = ['00', '00', '00', '00', '00']
        # self.probeData = ['53A00910303030303030303050', '53A00918303030303030303050', '53A00920303030303030303050',
        #                   '53A00928303030303030300050', '53A009303001f00a3030303050', '53A00938303030303030303050',
        #                   '53A009402863292044656c7450', '53A009486578204d6564696350', '53A00950616c204c696d697450',
        #                   '53A00958656420323032310050', '53A00960303030303030303050', '53A00968303030303030303050',
        #                   '53A00970303030303030303050', '53A00978303030303030303050', '53A00980303030303030303050',
        #                   '53A00988303030303030303050', '53A00990303030303030303050', '53A00998303030303030303050',
        #                   '53A009a0303030303030303050', '53A009a8303030303030303050', '53A009b0303030303030303050',
        #                   '53A009b8303030303030303050', '53A009c0303030303030303050', '53A009c8303030303030303050',
        #                   '53A009d0303030303030303050', '53A009d8303030303030303050', '53A009e0303030303030303050',
        #                   '53A009e8303030303030303050', '53A009f0303030303030303050', '53A009f8303030303030303050']

    def GenerateDataString(self, probe_type, test):
        '''
        Pass in a probe type, returns the full 255 byte probe data including time stamped serial number

        The first 8 and last 2 values of each list item are for SC18IM configuration, the bytes inbetween are that actual data that is written
        '''
        probezeros = ['53A00900000000000000000050', '53A00908000000000000000050', '53A00910000000000000000050',
                      '53A00918000000000000000050', '53A00920000000000000000050', '53A00928000000000000000050',
                      '53A00930000000000000000050', '53A00938000000000000000050', '53A00940000000000000000050',
                      '53A00948000000000000000050', '53A00950000000000000000050', '53A00958000000000000000050',
                      '53A00960000000000000000050', '53A00968000000000000000050', '53A00970000000000000000050']
        probeones =  ['53A00900111111111111111150', '53A00908111111111111111150', '53A00910111111111111111150',
                      '53A00918111111111111111150', '53A00920111111111111111150', '53A00928111111111111111150',
                      '53A00930111111111111111150', '53A00938111111111111111150', '53A00940111111111111111150',
                      '53A00948111111111111111150', '53A00950111111111111111150', '53A00958111111111111111150',
                      '53A00960111111111111111150', '53A00968111111111111111150', '53A00970111111111111111150']
        # probeData = ['53A00910303030303030303050', '53A00918303030303030303050', '53A00920303030303030303050',
        #              '53A00928303030303030300050', '53A009303001f00a3030303050', '53A00938303030303030303050',
        #              '53A009402863292044656c7450', '53A009486578204d6564696350', '53A00950616c204c696d697450',
        #              '53A00958656420323032310050', '53A00960303030303030303050', '53A00968303030303030303050',
        #              '53A00970303030303030303050', '53A00978303030303030303050', '53A00980303030303030303050',
        #              '53A00988303030303030303050', '53A00990303030303030303050', '53A00998303030303030303050',
        #              '53A009a0303030303030303050', '53A009a8303030303030303050', '53A009b0303030303030303050',
        #              '53A009b8303030303030303050', '53A009c0303030303030303050', '53A009c8303030303030303050',
        #              '53A009d0303030303030303050', '53A009d8303030303030303050', '53A009e0303030303030303050',
        #              '53A009e8303030303030303050', '53A009f0303030303030303050', '53A009f8303030303030303050']
        SDprobeData = ['53A00910303030303030303050', '53A00918303030303030303050', '53A00920303030303030303050',
                       '53A00928303030303030300050', '53A0093030fafa1e3030303050', '53A00938303030303030303050',
                       '53A009402863292044656c7450', '53A009486578204d6564696350', '53A00950616c204c696d697450',
                       '53A00958656420323030370050', '53A00960303030303030303050', '53A00968303030303030303050',
                       '53A00970303030303030303050', '53A00978303030303030303050', '53A00980303030303030303050',
                       '53A00988303030303030303050', '53A00990303030303030303050', '53A00998303030303030303050',
                       '53A009a0303030303030303050', '53A009a8303030303030303050', '53A009b0303030303030303050',
                       '53A009b8303030303030303050', '53A009c0303030303030303050', '53A009c8303030303030303050',
                       '53A009d0303030303030303050', '53A009d8303030303030303050', '53A009e0303030303030303050',
                       '53A009e8303030303030303050', '53A009f0303030303030303050', '53A009f8303030303030303050']

        if probe_type == 'blank':
            return probezeros
        if probe_type == 'ones':
            return probeones
        # set the correct probe type bytes
        if 'DP240' in probe_type:
            typeBytes = self.DP240TypeBytes
        elif 'DP12' in probe_type:
            typeBytes = self.DP12TypeBytes
        elif 'DP6' in probe_type:
            typeBytes = self.DP6TypeBytes
        elif 'I2C' in probe_type:
            typeBytes = self.I2CTypeBytes
        elif 'I2S' in probe_type:
            typeBytes = self.I2STypeBytes
        elif 'I2P' in probe_type:
            typeBytes = self.I2PTypeBytes
        elif 'KDP' in probe_type:
            typeBytes = self.KDP72TypeBytes
        else:
            return False
        # create a 12 byte timestamp of the format
        timeStamp = strftime("%Y%m%d%H%M%S", gmtime())
        timeStampFormatted = timeStamp[2:]
        if not test:
            timestamp_failed = timeStampFormatted[2:-2]
            time_list = f"Fail{timestamp_failed}"
        else:
            time_list = timeStampFormatted
        # stick the type bytes and the timestamp together (good)
        serialNumber = typeBytes + self.convert_to_hex(time_list)
        return self.create_serial_data(serialNumber)

    def create_serial_data(self, serialNumber):
        # put them in a format that can be sent via the SC18IM
        ##############################################################
        # for using month and day on to probe use in upper [10:-2]   #
        # for using year and month on to probe use in upper [8:-4]  #
        ##############################################################
        probeData = ['53A00910303030303030303050', '53A00918303030303030303050', '53A00920303030303030303050',
                     '53A00928303030303030300050', '53A009303001f00a3030303050', '53A00938303030303030303050',
                     '53A009402863292044656c7450', '53A009486578204d6564696350', '53A00950616c204c696d697450',
                     '53A00958656420323032310050', '53A00960303030303030303050', '53A00968303030303030303050',
                     '53A00970303030303030303050', '53A00978303030303030303050', '53A00980303030303030303050']
        lower = serialNumber[0:8]
        upper = serialNumber[8:]

        firstStart = '53A00900'
        secondStart = '53A00908'
        end = '50'
        slower = ''.join(lower)
        supper = ''.join(upper)
        firstByte = firstStart + slower + end
        secondByte = secondStart + supper + end
        # add them to the probe data list
        probeData.insert(0, secondByte)
        probeData.insert(0, firstByte)
        return probeData

    def convert_to_hex(self, time_list):
        timeStampASCII = []
        for item in time_list:
            x = (ord(item))
            timeStampASCII.append(format(x, "x"))
        return timeStampASCII
