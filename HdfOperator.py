import h5py

class HdfOperator(object):
    
    m_file = ''
    m_hdfHandle = h5py.File
    
    def __init__(self):
        '''
        Constructor
        '''
    def SetFile(self,filename):
        self.m_hdfHandle = h5py.File(filename,'r')
        
    def ReadHdfDataset(self,groupPath,datasetPath):
                   
        hdfgroup = self.m_hdfHandle[groupPath]
        dataset = hdfgroup[datasetPath]
        return dataset