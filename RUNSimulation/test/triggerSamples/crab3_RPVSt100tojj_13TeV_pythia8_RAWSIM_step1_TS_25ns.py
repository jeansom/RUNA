from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'RPVSt100tojj_13TeV_pythia8_RunIISpring15DR74_RAWSIM_TS_25ns'
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step1_DIGI_L1_DIGI2RAW_HLT_PU.py'

config.Data.inputDataset = '/RPVSt100tojj_13TeV_pythia8/algomez-GENSIM_RunIISpring15DR74_v2-8163b2d36efe3a5ba985d564c88e2b1e/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
NJOBS = 1000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.publishDataName = 'RunIISpring15DR74_RAWSIM_TS_25ns'
config.Data.ignoreLocality = True

config.Site.storageSite = 'T3_US_FNALLPC'

#### Only for hexfarm.. it still does not work
#config.Data.outLFN = '/store/user/algomez/data23/'	### only for hexfarm
#config.Site.storageSite = 'T3_US_Rutgers'

