from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'NAME_GENSIM_v720'
#config.General.workArea = 'crab_projects'

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.generator = 'lhe'
config.JobType.psetName = 'test'

config.section_("Data")
config.Data.primaryDataset = 'NAME'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 100
NJOBS = 1000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.publishDataName = 'NAME_GENSIM_v720'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'

