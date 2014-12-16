from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'RPVSt100tojj_13TeV_pythia8_EDMNtuple_PU40bx50'
config.General.workArea = 'crab_projects'

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'RUNtuples_cfg.py'
#config.JobType.pyCfgParams = [ 'outputLabel=RPVSt100tojj_13TeV_pythia8_EDMNtuple_PU40bx50.root' ]
#config.JobType.inputFiles = [ 'MuonEfficiencies_Run2012ReReco_53X.root' ]

config.section_("Data")
config.Data.inputDataset = '/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-RPVSt100tojj_13TeV_pythia8_MiniAOD_v706_PU40bx50-b71e879835d2f0083a0e044b05216236/USER'
#config.Data.inputDataset = '/QCD_HT_250To500_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'EventBased'
#config.Data.userInputFile = '/uscms_data/d3/algomez/Substructure/Analyzer/CMSSW_7_1_0_pre9/src/ttbarDM/TopPlusDMAna/test/files.txt'
config.Data.unitsPerJob = 10
config.Data.totalUnits = 1
config.Data.outLFN = '/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/'
config.Data.ignoreLocality = True
config.Data.publication = True
config.Data.publishDataName = 'test'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
