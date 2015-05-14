import BlackBodyAnalyse as BBA

bba = BBA
bba.OpenFile('C:\\Data\\virr\\20150429_0504\\FY3C_VIRRX_GBAL_L1_20150428_0610_OBCXX_MS.HDF')
dataset = bba.ReadHdfDataset()

bba.Correction(dataset,3)