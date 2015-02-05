from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'RPVSt100tojj_13TeV_pythia8_EDMNtuple_PU40bx50_v2'
#config.General.workArea = 'crab_projects'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNtuples_cfg.py'
#config.JobType.pyCfgParams = [ 'outputLabel=RPVSt100tojj_13TeV_pythia8_EDMNtuple_PU40bx50.root' ]
config.JobType.allowNonProductionCMSSW = True

config.section_("Data")
config.Data.inputDataset = '/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-RPVSt100tojj_13TeV_pythia8_MiniAOD_v706_PU40bx50-b71e879835d2f0083a0e044b05216236/USER'
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
#NJOBS = 1
#config.Data.totalUnits = 1
config.Data.outLFN = '/store/user/algomez/'
#config.Data.ignoreLocality = True
config.Data.publication = True
config.Data.ignoreLocality = True
config.Data.publishDataName = 'RPVSt100tojj_13TeV_pythia8_EDMNtuple_PU40bx50_v2'
#config.Data.publishDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSWriter'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
