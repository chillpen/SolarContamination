import h5py
import numpy as np
import matplotlib.pyplot as plt
import HdfOperator as hdfOper




class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
 
ContaminationType = Enum(["Enter", "Leave", "MId", "Null"])


class Discrimination(object):
    
    EVCAziZenGroup = '/Geolocation'
    EVCAziZenDataset='EVC_Azi_Zen'
    EVCLonLatGoup = '/Geolocation'
    EVCLonLatDataset = 'EVC_Lon_Lat'
    _hdfOper = hdfOper.HdfOperator()
    
    
    def __init__(self):
        '''
        Constructor
        '''
               
    def SetCurrentHdfOper(self,hdfOper):
        self._hdfOper = hdfOper
    
    def IsContamination(self):
        
        return True
    
    def Contamination(self,Data):
        Aze_Zen=self._hdfOper.ReadHdfDataset(self.EVCAziZenGroup, self.EVCAziZenDataset)
        Lon_Lat=self._hdfOper.ReadHdfDataset(self.EVCLonLatGoup, self.EVCLonLatDataset)
        
        zenith = Aze_Zen[:,1]
        lon = Lon_Lat[:,0]
        lat = Lon_Lat[:,1]
        
        dataSize = np.size(zenith)
        
        '''zz=np.where(zenith<0)'''
        
        danger = False
        
        '''IsNorthern = self.IsNorthernHemisphere(lat)'''
        for i in range(dataSize):
            if lat[i]>0 :
                if zenith>75 & zenith<130:
                    danger = True
            else :
                if zenith>90 & zenith<140:
                    danger = True
        
        
        if danger :
            
             
        

        
    def IsNorthernHemisphere(self,latArray): 
        dataSize = np.size(latArray)
        for i in range(dataSize):
            if latArray[i]>0 :
                return True
        return False
                
        

        
def main():
    hdfop = hdfOper.HdfOperator()
    hdfop.SetFile('C:\\Data\\virr\\20150429_0504\\FY3C_VIRRX_GBAL_L1_20150428_0615_OBCXX_MS.HDF')
    disc = Discrimination()
    disc.SetCurrentHdfOper(hdfop)
    disc.Contamination()

    

if __name__ == '__main__':
    main()
        