from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'test_Matching'
config.General.workArea = 'crab_projects'
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'simpleMatching.py'

config.Data.inputDataset = '/RPVSt100tojj_13TeV_pythia8/algomez-RunIISpring15DR74_AODSIM_Asympt25ns-fb358e8852a60e2ae7f5961d9ec35138/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
NJOBS = 1000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.publishDataName = 'SimpleMatching'
config.Data.ignoreLocality = True

config.Site.storageSite = 'T3_US_FNALLPC'

#### Only for hexfarm.. it still does not work
#config.Data.outLFN = '/store/user/algomez/data23/'	### only for hexfarm
#config.Site.storageSite = 'T3_US_Rutgers'

