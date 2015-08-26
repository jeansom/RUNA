##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand
from multiprocessing import Process
config = config()

version = 'ts_v10'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNTriggerEfficiency_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.outLFNDirBase = '/store/user/algomez/'
config.Data.publication = False
config.Data.ignoreLocality = True

config.Site.storageSite = 'T3_US_FNALLPC'

def submit(config):
	try:
		crabCommand('submit', config = config)
	except HTTPException, hte:
		print 'Cannot execute commend'
		print hte.headers

if __name__ == '__main__':


	Samples = [ 
			'/JetHT/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v01p2-59a8f6968d1faf0a39f7c4c693699d7c/USER',
			#'/SingleMu/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v01p2-59a8f6968d1faf0a39f7c4c693699d7c/USER',
			'/MET/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v01p2-59a8f6968d1faf0a39f7c4c693699d7c/USER',
			#'/RPVSt100tojj_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_TS__v02-1886d118546a0d39f46d888ed262e31b/USER',  ### tmp 
			'/RPVSt100tojj_13TeV_pythia8/jsomalwa-RunIISpring15DR74_RUNA_Asympt25ns_v02p2-1886d118546a0d39f46d888ed262e31b/USER'
			]

	
	for dataset in Samples:
		#procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RUNA', '').split('-')[0]+'_'+version
		if 'RPV' in dataset:
			procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RunIISpring15DR74_RUNA', '').split('-')[0]+'_'+version
			config.Data.splitting = 'FileBased'
			config.Data.unitsPerJob = 1
		else:
			procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RunIISpring15DR74_RUNA_Asympt25ns', '_Asympt50ns').split('-')[0]+'_'+version
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 3
			#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-251252_13TeV_PromptReco_Collisions15_JSON.txt'
			config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON.txt'
		config.Data.inputDataset = dataset
		config.General.requestName = procName
		config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0' ]
		#crabCommand('submit', config = config)
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
