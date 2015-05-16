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
    m_Discrim = discrimi.Discrimination()
    
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
        '''if self.m_Discrim.IsContamination()!=True:
            return'''
        curveData = dataset[detector,:,chn]
        dataSize = np.size(curveData)
        mean = np.mean(curveData)
        meanArray = np.ones(dataSize)*mean  
        diffData = curveData - meanArray
        diffData = diffData*diffData
        
        print(diffData)
        '''self.PlotCurve(dataset,chn,detector)'''
 
        self.Smooth(curveData)
        self.PlotCurve(curveData)
        
    def Smooth(self,data):
        dataSize = np.size(data)
        step  = 50
        
        for i in range(step,dataSize-50):
            tempData = data[i-50:i+50]
            mean = np.mean(tempData)
            difLimit = mean*0.005
            if np.abs(data[i]- mean) >difLimit :
                data[i] = mean
        
        print(data)
                
        
def main():
    bba = BlackBodyAnalyse()
    bba.OpenFile('C:\\Data\\virr\\20150429_0504\\FY3C_VIRRX_GBAL_L1_20150428_0615_OBCXX_MS.HDF')
    dataset = bba.ReadData()  
    bba.Correction(dataset,3,2)
    

if __name__ == '__main__':
    main()