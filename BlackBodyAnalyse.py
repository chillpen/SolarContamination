import h5py
import numpy as np
import matplotlib.pyplot as plt


class BlackBodyAnalyse(object):
    
    GoupPath = '/Calibration'
    DatasetPath = 'Blackbody_View'
    
    def __init__(self):
        '''
        Constructor
        '''
        
    
    def ReadData(self,file):
        hdfFile = h5py.File(file,'r')
        
        hdfgroup = hdfFile[self.GoupPath]
        dataset = hdfgroup[self.DatasetPath]
        
        return dataset
   
    def Draw(self,hdfdataset):
        plt.plot(hdfdataset)
        plt.show()
        
        