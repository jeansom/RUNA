from CRABClient.UserUtilities import config
config = config()

name = 'RunIISpring15DR74_RUNA_Asympt25ns_'
version = 'v01'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNtuples_cfg.py'
#config.JobType.pyCfgParams = [ 'is74XSample=0' ]
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#NJOBS = 1
#config.Data.totalUnits = 1
config.Data.publication = True
config.Data.ignoreLocality = True
config.Data.publishDataName = name+'_'+version

config.Site.storageSite = 'T3_US_FNALLPC'

def submit(config):

	try:
		crabCommand('submit', config = config)
	except HTTPException, hte:
		print 'Cannot execute commend'
		print hte.headers

if __name__ == '__main__':

	from CRABAPI.RawCommand import crabCommand
	from multiprocessing import Process

	QCDHT = [ 
			#### CSA14
			#'/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-RPVSt100tojj_13TeV_pythia8_MiniAOD_v706_PU40bx50-b71e879835d2f0083a0e044b05216236/USER'
			#### PHYS14
			#'/RPVSt100tojj_13TeV_pythia8/algomez-MiniAOD_PHYS14_v720_PU40bx50-159f4f639b95c6d4636b9f3013c28473/USER'
			#'/RPVSt100tojj_13TeV_pythia8/algomez-MiniAOD_PHYS14_v720-b1b44dbfc276814daa37c582f825184d/USER',
			#'/RPVSt100tobj_pythia8_13TeV/algomez-MiniAOD_PHYS14_v720_PU20bx25-b1b44dbfc276814daa37c582f825184d/USER',
			#'/RPVSt350tojj_13TeV_pythia8/algomez-MiniAOD_PHYS14_v720_PU20bx25-b1b44dbfc276814daa37c582f825184d/USER'
			##### RunIISpring15DR74
			'/RPVSt100tojj_13TeV_pythia8/algomez-RunIISpring15DR74_MiniAOD_v2-fb89f44b0d6970d718ed21d513cd1c9d/USER',
			'/RPVSt200tojj_13TeV_pythia8/algomez-RunIISpring15DR74_MiniAOD_Asympt25ns-aaa2c03e98f1a25cd2e28ba65d8e2a63/USER',
			'/RPVSt350tojj_13TeV_pythia8/algomez-RunIISpring15DR74_MiniAOD_Asympt25ns-aaa2c03e98f1a25cd2e28ba65d8e2a63/USER',
			]
	
	for dataset in QCDHT:
		config.Data.inputDataset = dataset
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-', '').split('-')[0]+name+'_'+version
		config.General.requestName = procName
		#crabCommand('submit', config = config)
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
