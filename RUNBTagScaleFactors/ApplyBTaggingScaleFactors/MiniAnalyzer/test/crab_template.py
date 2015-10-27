from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.requestName = 'REQUESTED NAME'
config.section_('JobType')
config.JobType.psetName = 'cfg_files/CMSSW_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.pyCfgParams = []
config.JobType.inputFiles = [ 'EfficiencyMaps.root','CSV.csv']
config.section_('Data')
config.Data.inputDataset = 'DATASET'
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/DBS_INSTANCE/DBSReader/'
config.Data.publication = False
config.Data.unitsPerJob = 50
config.Data.splitting = 'FileBased'
config.Data.publishDataName = 'PUBLICATION_NAME'
config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'
