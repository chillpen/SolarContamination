import h5py
import numpy as np
import matplotlib.pyplot as plt
import HdfOperator as hdfOper
import Discrimination as discrimi
import matplotlib.collections as collections

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
        self._Discrim.SetCurrentHdfOper(self._hdfOper)
    
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
 
        contam = self._Discrim.Contamination(curveData)
        print(contam)
        type = contam[0]
        area = contam[1]
        fig, ax = plt.subplots()
        '''ax.plot(curveData)'''
       
        ax.plot(np.arange(0, 1800, 1), curveData, color='black')
        '''self.PlotCurve(curveData)'''
        collection = collections.BrokenBarHCollection.span_where(np.arange(area[0], area[1], 1), ymin=np.min(curveData), ymax=np.max(curveData), where=curveData>0, facecolor='green', alpha=0.5)
        ax.add_collection(collection)    
        print(area)
        plt.show()
                
        
def main():
    bba = BlackBodyAnalyse()
    bba.OpenFile('C:\\Data\\virr\\FY3C_VIRRX_GBAL_L1_20140620_0800_OBCXX_MS.HDF')
    dataset = bba.ReadData()  
    bba.Correction(dataset,3,2)
    

if __name__ == '__main__':
    main()