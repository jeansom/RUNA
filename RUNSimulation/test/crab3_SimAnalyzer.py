from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8_SimAnalyzer'
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'SimAnalyzer_cfg.py'

config.Data.inputDataset = '/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15DR76_RAW_AODSIM_Asympt25ns-af0f65cd1e8cab3336e7e09ad24c411d/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'SimAnalyzer'
config.Data.ignoreLocality = True

config.Site.storageSite = 'T3_US_FNALLPC'

##### Only for hexfarm.. it still does not work
#config.Data.outLFN = '/store/user/algomez/data23/'	### only for hexfarm
#config.Site.storageSite = 'T3_US_Rutgers'
