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
config.Data.publishDataName = 'RUNA_PHYS14_PU20bx25_'+version

config.Site.storageSite = 'T3_US_FNALLPC'

if __name__ == '__main__':

	from CRABAPI.RawCommand import crabCommand

	QCDHT = [ 
			#'/RPVSt100tojj_13TeV_pythia8/algomez-MiniAOD_PHYS14_v720-b1b44dbfc276814daa37c582f825184d/USER',
			#'/RPVSt100tobj_13TeV_pythia8/algomez-MiniAOD_PHYS14_v720-b1b44dbfc276814daa37c582f825184d/USER'
			'/RPVSt350tojj_13TeV_pythia8/algomez-MiniAOD_PHYS14_v720_PU20bx25-b1b44dbfc276814daa37c582f825184d/USER'
			]
	
	for dataset in QCDHT:
		config.Data.inputDataset = dataset
		config.General.requestName = dataset.replace('/','_')+'_RUNtuples_'+version
		crabCommand('submit', config = config)
