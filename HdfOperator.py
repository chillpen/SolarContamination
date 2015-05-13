import h5py

def ReadHdfDataset(self,filePath,groupPath,datasetPath):
    hdfFile = h5py.File(filePath,'r')
        
    hdfgroup = hdfFile[groupPath]
    dataset = hdfgroup[datasetPath]
        
    return dataset