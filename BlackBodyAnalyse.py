import h5py
import numpy as np
import matplotlib.pyplot as plt
import HdfOperator as hdfOper
import Discrimination as discrimi

class BlackBodyAnalyse(object):
    
    m_FilePath = ''
    m_GoupPath = '/Calibration'
    m_DatasetPath = 'Blackbody_View'
    m_hdfOper = hdfOper.HdfOperator()
    m_Discrim = discrimi.Discrimination()
    
    def __init__(self):
        '''
        Constructor
        '''
        
        
    def OpenFile(self,filePath):
        self.m_FilePath = filePath
        self.m_hdfOper.SetFile(filePath)

    
    def ReadData(self):
        return self.m_hdfOper.ReadHdfDataset(self.m_GoupPath, self.m_DatasetPath)
              
   
    def PlotCurve(self,hdfdataset,chn,detector):
        drawdata = hdfdataset[detector,:,chn]
        plt.plot(drawdata)
        plt.show()
        
    def Correction(self,dataset,chn,detector):
        if self.m_Discrim.IsContamination()!=True:
            return
        mean = np.mean(dataset[detector,:,chn])
        self.PlotCurve(dataset,chn,detector)
        
  
        
def main():
    bba = BlackBodyAnalyse()
    bba.OpenFile('C:\\Data\\virr\\20150429_0504\\FY3C_VIRRX_GBAL_L1_20150428_0615_OBCXX_MS.HDF')
    dataset = bba.ReadData()
    bba.Correction(dataset,3,2)

if __name__ == '__main__':
    main()