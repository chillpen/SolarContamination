import h5py
import numpy as np
import matplotlib.pyplot as plt
import HdfOperator as hdfOper
import os



class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
 
EnumContaminationType = Enum(["Enter", "Leave", "Mid", "Null"])



class Discrimination(object):
    
    EVCAziZenGroup = '/Geolocation'
    EVCAziZenDataset='EVC_Azi_Zen'
    EVCLonLatGoup = '/Geolocation'
    EVCLonLatDataset = 'EVC_Lon_Lat'
    _hdfOper = hdfOper.HdfOperator()
    _ContaminationType = EnumContaminationType.Null
    
    
    def __init__(self):
        '''
        Constructor
        '''
               
    def SetCurrentHdfOper(self,hdfOper):
        self._hdfOper = hdfOper
    
    def IsContamination(self,Data):
        Aze_Zen=self._hdfOper.ReadHdfDataset(self.EVCAziZenGroup, self.EVCAziZenDataset)
        Lon_Lat=self._hdfOper.ReadHdfDataset(self.EVCLonLatGoup, self.EVCLonLatDataset)
        zenith = Aze_Zen[:,1]*0.01
        lon = Lon_Lat[:,0]
        lat = Lon_Lat[:,1]
        isNorthern = self.IsNorthernHemisphere(lat)

        if isNorthern :
            dangerData = np.where((zenith>85) & (zenith <118))
        else:
            dangerData = np.where((zenith>93) & (zenith <123))
        
        if not np.size(dangerData)  > 0 :
            return False
        
        smoothData = self.Smooth(Data)
        stdValue=np.std(smoothData)
        
        if (isNorthern & (stdValue>0.4)) | (stdValue>0.7) :
            return True
                       
        return False
            
        
    
    def Contamination(self,Data):
        Aze_Zen=self._hdfOper.ReadHdfDataset(self.EVCAziZenGroup, self.EVCAziZenDataset)
        Lon_Lat=self._hdfOper.ReadHdfDataset(self.EVCLonLatGoup, self.EVCLonLatDataset)
        
        zenith = Aze_Zen[:,1]*0.01
        lon = Lon_Lat[:,0]
        lat = Lon_Lat[:,1]
        
        dataSize = np.size(zenith)
        
        '''zz=np.where(zenith<0)'''
        
        danger = False
        
        IsNorthern = self.IsNorthernHemisphere(lat)
        
        
        if not self.IsInLargeDiscrimRegion(zenith, IsNorthern):
            return [self._ContaminationTyp,[0,0]]
        
    
        discriminationArea = self.GetDiscriminationArea(Data,lat,zenith,IsNorthern)
        
        return [self._ContaminationType,discriminationArea]



                            
    def IsInLargeDiscrimRegion(self,zenith,isNorthern):
        result = False
        discrimRegion = []
        if isNorthern :
            discrimRegion = np.where((zenith>75) & (zenith <130))              
        else:
            discrimRegion = np.where((zenith>90) & (zenith <140))
            
        if np.size(discrimRegion) >0 :
            result = True
            
        return result
    
                    
            
    def GetDiscriminationArea(self,Data,lat,zenith,isNorthern):
        dangerData = []
        dataSize = np.size(zenith)
        enterPos =0
        leavePos =0
        
        if isNorthern :
            dangerData = np.where((zenith>85) & (zenith <118))
        else:
            dangerData = np.where((zenith>93) & (zenith <123))
        
        if not np.size(dangerData)  > 0 :
            return [0,0]
        
      
        
        smoothData = self.Smooth(Data)
        stdValue=np.std(smoothData)
        stdArray = []
        result = [enterPos,leavePos]  
        if (isNorthern & (stdValue>0.4)) | ((not isNorthern) &(stdValue>0.7)) :
            enterPos = np.min(dangerData)
            leavePos = np.max(dangerData)
            

            
            for i in range(100,dataSize-100,100):
                stdTmp = np.std(smoothData[i-100:i+99])
                stdArray.append(stdTmp)
                
            restd=((stdArray-np.mean(stdArray))/np.std(stdArray))
            
            std_1800=np.zeros(1800)
            
            for j in range(100,dataSize-100,100):
                std_1800[j] = restd[j/100-1]
                
            difIndex = np.where(np.abs(std_1800)>0.7)
                
            if (enterPos==0) & (leavePos==1799):
                self._ContaminationType = EnumContaminationType.Mid
                result = [0,1799]
            elif (enterPos==0) & (leavePos<1799):
                self._ContaminationType = EnumContaminationType.Enter
                result = [0,np.max(difIndex)+99]
               
            elif (enterPos>0) & (leavePos==1799):
                self._ContaminationType = EnumContaminationType.Leave
                result=[np.min(difIndex)-99,1799]
            else :
                self._ContaminationType =EnumContaminationType.Null
                '''result = [np.min(difIndex)-99,1799]'''
            '''   nz_l=1;nz_r=1800;  
            elseif (a==1 & b<1800)
                %nz_l=1;nz_r=max(kk)+15;  
                nz_l=1;nz_r=max(kk)+99;
             elseif (a>1 & b==1800);
                %nz_l=min(kk)-15;nz_r=1800;
                 nz_l=min(kk)-99;nz_r=1800;
             else
                nz_l=0;nz_r=0;
             end'''

        return result
    
  
        
    def Smooth(self,data):
        dataSize = np.size(data)
        step  = 50
        result = data[:]
        for i in range(step,dataSize-50,1):
            tempData = result[i-50:i+50]
            mean = np.mean(tempData)
            difLimit = mean*0.005
            if np.abs(result[i]- mean) >difLimit :
                result[i] = mean
        return result
        
    def IsNorthernHemisphere(self,latArray): 
        isNorthern = False
        region = np.where(latArray>0)
        if (np.size(region) / np.size(latArray)) > 0.9 :
            isNorthern = True
          
        return isNorthern
                
        

        
def main():
    hdfop = hdfOper.HdfOperator()
    hdfop.SetFile('C:\\Data\\virr\\FY3C_VIRRX_GBAL_L1_20140620_1335_OBCXX_MS.HDF')
    bbdataset =hdfop.ReadHdfDataset('/Calibration', 'Blackbody_View')
    disc = Discrimination()
    disc.SetCurrentHdfOper(hdfop)
    contam = disc.Contamination(bbdataset[2,:,3])
    
    print(contam)
    '''path = 'K:\\20140620'
    files = os.listdir(path)
    hdfop = hdfOper.HdfOperator()
    disc = Discrimination()
    disc.SetCurrentHdfOper(hdfop)
    contArray = []
    for file in files:
        hdfop.SetFile(path+'\\'+file)
        bbdataset = hdfop.ReadHdfDataset('/Calibration', 'Blackbody_View')
        if disc.IsContamination(bbdataset[2,:,3]):
            contArray.append(file)
    print(contArray) '''

    

if __name__ == '__main__':
    main()
        