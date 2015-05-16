import h5py
import numpy as np
import matplotlib.pyplot as plt
import HdfOperator as hdfOper
import Discrimination as discrimi

class BlackBodyAnalyse(object):
    
    m_FilePath = ''
    m_GoupPath = '/Calibration'
    m_DatasetPath = 'Blackbody_View'
    _hdfOper = hdfOper.HdfOperator()
    _Discrim = discrimi.Discrimination()
    
    def __init__(self):
        '''
        Constructor
        '''
        
        
    def OpenFile(self,filePath):
        self.m_FilePath = filePath
        self._hdfOper.SetFile(filePath)

    
    def ReadData(self):
        return self._hdfOper.ReadHdfDataset(self.m_GoupPath, self.m_DatasetPath)
              
   
    '''def PlotCurve(self,hdfdataset,chn,detector):
        drawdata = hdfdataset[detector,:,chn]
        plt.plot(drawdata)
        plt.smagnet:?xt=1urn:btih:7c6b1b5b590b23c964d360425334469935ce7d58&xl=52478050790how()'''
        
    def PlotCurve(self,curveData):
        plt.plot(curveData)
        plt.show()
        
    def Correction(self,dataset,chn,detector):
        '''if self._Discrim.IsContamination()!=True:
            return'''
        curveData = dataset[detector,:,chn]
        dataSize = np.size(curveData)
 
        self._Discrim.Contamination(curveData)
        self.PlotCurve(curveData)
        

                
        
def main():
    bba = BlackBodyAnalyse()
    bba.OpenFile('C:\\Data\\virr\\20150429_0504\\FY3C_VIRRX_GBAL_L1_20150428_0615_OBCXX_MS.HDF')
    dataset = bba.ReadData()  
    bba.Correction(dataset,3,2)
    

if __name__ == '__main__':
    main()