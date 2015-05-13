import h5py
import numpy as np
import matplotlib.pyplot as plt
import HdfOperator

class BlackBodyAnalyse(object):
    
    FilePath = ''
    GoupPath = '/Calibration'
    DatasetPath = 'Blackbody_View'
    
    
    def __init__(self):
        '''
        Constructor
        '''
        
        
    def SetFileName(self,filePath):
        self.FilePath = filePath
    
    def ReadData(self):
        return HdfOperator.ReadHdfDataset(self.FilePath, self.GoupPath, self.DatasetPath)
              
   
    def PlotCurve(self,hdfdataset,chn,detector):
        drawdata = hdfdataset[detector,:,chn]
        plt.plot(drawdata)
        plt.show()
        
    def Correction(self,dataset,chn,detector):
        mean = np.mean(dataset[detector,:,chn])
        self.PlotCurve(dataset,chn,detector)
        
  
        
def main():
    bba = BlackBodyAnalyse()
    bba.SetFileName('e:\\FY3C_VIRRX_GBAL_L1_20150428_0615_OBCXX_MS.HDF')
    dataset = bba.ReadHdfDataset()
    bba.Correction(dataset,3,2)

if __name__ == '__main__':
    main()