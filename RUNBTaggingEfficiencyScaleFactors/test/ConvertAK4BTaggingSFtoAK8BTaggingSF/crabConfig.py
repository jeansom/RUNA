from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.requestName = ''
config.General.workArea = 'crab_projects'
config.section_('JobType')
config.JobType.psetName = '/uscms_data/d3/jsomalwa/CMSSW_7_6_3_patch2/src/BTagSFTool/MiniAnalyzer/test/crab_projects/SFPlotsStopStopjbDeltaR3/cfg_files/MiniAOD_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.pyCfgParams = ['wantSummary=True']
config.JobType.inputFiles = [ 'EfficiencyMapsAK4.root','EfficiencyMapsAK8.root','CSV.csv','JECs']
config.section_('Data')
config.Data.inputDataset = '/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15DR76_MiniAOD_Asympt25ns-928d46295c808b28c2560dd199b08897/USER'
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.publication = False
config.Data.unitsPerJob = 11
config.Data.splitting = 'FileBased'
config.Data.outputDatasetTag = 'RPVStopStopToJetsAK4toAK8SFbDeltaR3'
config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'
