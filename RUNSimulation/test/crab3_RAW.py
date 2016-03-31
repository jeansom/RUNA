from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'NAME'
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'test.py'

config.Data.inputDataset = 'None'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
NJOBS = 1000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'PROC'
config.Data.ignoreLocality = True

config.Site.storageSite = 'T3_US_FNALLPC'

##### Only for hexfarm.. it still does not work
#config.Data.outLFN = '/store/user/algomez/data23/'	### only for hexfarm
#config.Site.storageSite = 'T3_US_Rutgers'
