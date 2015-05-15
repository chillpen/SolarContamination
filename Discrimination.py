import h5py
import numpy as np
import matplotlib.pyplot as plt
import HdfOperator as hdfOper


class Discrimination(object):
    
    EVCAziZenGroup = '/Geolocation'
    EVCAziZenDataset='EVC_Azi_Zen'
    EVCLonLatGoup = '/Geolocation'
    EVCLonLatDataset = 'EVC_Lon_Lat'
    m_hdfOper = hdfOper.HdfOperator()
    
    
    def __init__(self):
        '''
        Constructor
        '''
               
    def SetCurrentHdfOper(self,hdfOper):
        self.m_hdfOper = hdfOper
    
    def IsContamination(self):
        Aze_Zen=self.m_hdfOper.ReadHdfDataset(self.EVCAziZenGroup, self.EVCAziZenDataset)
        Lon_Lat=self.m_hdfOper.ReadHdfDataset(self.EVCLonLatGoup, self.EVCLonLatDataset)
        
        return True