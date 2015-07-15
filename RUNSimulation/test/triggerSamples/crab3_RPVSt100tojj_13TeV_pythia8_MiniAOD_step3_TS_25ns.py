from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'RPVSt100tojj_13TeV_pythia8_RunIISpring15DR74_MiniAOD_TS_25ns'
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step3_PAT.py'

config.Data.inputDataset = 'ADD_YOUR_DATASET_HERE'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
NJOBS = 1000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.publishDataName = 'RunIISpring15DR74_MiniAOD_TS_25ns'
config.Data.ignoreLocality = True

config.Site.storageSite = 'T3_US_FNALLPC'

#### Only for hexfarm.. it still does not work
#config.Data.outLFN = '/store/user/algomez/data23/'	### only for hexfarm
#config.Site.storageSite = 'T3_US_Rutgers'

