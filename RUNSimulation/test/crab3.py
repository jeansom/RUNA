from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'NAME'
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'PrivateMC'
config.JobType.generator = 'lhe'
config.JobType.psetName = 'test'

config.Data.outputPrimaryDatasett = 'NAME'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 100
NJOBS = 1000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'GENSIM_RunIISpring15DR74'
config.Site.storageSite = 'T3_US_FNALLPC'

##### For hexfarm... but it does not work yet
#config.Data.outLFN = '/store/user/algomez/data23/'	### only for hexfarm
#config.Site.storageSite = 'T3_US_Rutgers'
