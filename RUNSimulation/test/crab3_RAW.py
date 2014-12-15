from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'NAME'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'test.py'

config.section_("Data")
config.Data.inputDataset = 'None'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
NJOBS = 500
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.publishDataName = 'NAME'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'

