from CRABClient.UserUtilities import config
config = config()

datasets = { 
	#	'JTB_MiniAOD_JEC':'/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-JTB_MiniAOD_JEC_PU40bx50_v0-b5d257f9cbd3d492dffbbae30fc8b5d0/USER',
		'JTB_MiniAOD_NOJEC':'/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-JTB_MiniAOD_NOJEC_PU40bx50_v0-73c0a97cd9d09caef3a40f297663be8a/USER',
	#	'JTB_AOD_JEC':'/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-JTB_AOD_JEC_PU40bx50_v0-e59098fe6877ec277c1517ed59783e8f/USER'
		}

for name, dataset in datasets.iteritems():

	from CRABClient.UserUtilities import config
	config = config()

	config.General.requestName = 'RPVSt100tojj_13TeV_pythia8_'+name+'_Plots_PU40bx50_v0'
	config.General.workArea = 'crab_projects'

	config.JobType.pluginName = 'Analysis'
	config.JobType.psetName = 'PUStudies_cfg.py'
	config.JobType.allowNonProductionCMSSW = True

	#config.Data.inputDataset = '/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-JTB_MiniAOD_JEC_PU40bx50_v0-b5d257f9cbd3d492dffbbae30fc8b5d0/USER'
	#config.Data.inputDataset = '/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-JTB_MiniAOD_NOJEC_PU40bx50_v0-73c0a97cd9d09caef3a40f297663be8a/USER'
	#config.Data.inputDataset = '/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-JTB_AOD_JEC_PU40bx50_v0-e59098fe6877ec277c1517ed59783e8f/USER'
	config.Data.inputDataset = dataset
	config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
	config.Data.splitting = 'FileBased'
	config.Data.unitsPerJob = 1
	config.Data.outLFN = '/store/user/algomez/'
	config.Data.ignoreLocality = True
	config.Data.publishDataName = name+'_Plots_PU40bx50_v0'

	config.Site.storageSite = 'T3_US_FNALLPC'

