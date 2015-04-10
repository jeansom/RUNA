from CRABClient.UserUtilities import config
config = config()

version = 'v03'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNtuples_cfg.py'
#config.JobType.pyCfgParams = [ 'outputLabel=RPVSt100tojj_13TeV_pythia8_EDMNtuple_PU40bx50.root' ]
config.JobType.allowNonProductionCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#NJOBS = 1
#config.Data.totalUnits = 1
config.Data.outLFN = '/store/user/algomez/'
config.Data.publication = True
config.Data.ignoreLocality = True
#config.Data.publishDataName = 'RUNA_PHYS14_PU20bx25_'+version
config.Data.publishDataName = 'RUNA_PHYS14_PU40bx50_'+version

config.Site.storageSite = 'T3_US_FNALLPC'

if __name__ == '__main__':

	from CRABAPI.RawCommand import crabCommand

	QCDHT = [ 
			#### CSA14
			#'/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-RPVSt100tojj_13TeV_pythia8_MiniAOD_v706_PU40bx50-b71e879835d2f0083a0e044b05216236/USER'
			#### PHYS14
			'/RPVSt100tojj_13TeV_pythia8/algomez-MiniAOD_PHYS14_v720_PU40bx50-159f4f639b95c6d4636b9f3013c28473/USER'
			#'/RPVSt100tojj_13TeV_pythia8/algomez-MiniAOD_PHYS14_v720-b1b44dbfc276814daa37c582f825184d/USER',
			#'/RPVSt100tobj_pythia8_13TeV/algomez-MiniAOD_PHYS14_v720_PU20bx25-b1b44dbfc276814daa37c582f825184d/USER'
			#'/RPVSt350tojj_13TeV_pythia8/algomez-MiniAOD_PHYS14_v720_PU20bx25-b1b44dbfc276814daa37c582f825184d/USER'
			]
	
	for dataset in QCDHT:
		config.Data.inputDataset = dataset
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-', '').split('-')[0]+'_RUNtuples_'+version
		config.General.requestName = procName
		config.General.requestName = dataset.replace('/','_')+'_RUNtuples_'+version
		crabCommand('submit', config = config)
