##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from httplib import HTTPException
config = config()

name = 'RUNA'
version = 'v08'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNtuples_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 1
config.Data.publication = True
config.Data.ignoreLocality = True

config.Site.storageSite = 'T3_US_FNALLPC'

def submit(config):

	try:
		crabCommand('submit', config = config)
	except HTTPException, hte:
		print 'Cannot execute commend'
		print hte.headers

if __name__ == '__main__':

	from CRABAPI.RawCommand import crabCommand

	Samples = [ 
			#### DATA
			#'/JetHT/Run2015B-PromptReco-v1/MINIAOD',
			#'/JetHT/Run2015C-PromptReco-v1/MINIAOD',
			'/JetHT/Run2015D-PromptReco-v4/MINIAOD',
			#'/MET/Run2015B-PromptReco-v1/MINIAOD',
			##'/SingleMu/Run2015B-PromptReco-v1/MINIAOD',
			]
	
	from multiprocessing import Process
	for dataset in Samples:
		config.Data.inputDataset = dataset
		config.JobType.pyCfgParams = [ 'DataProcessing=Data25ns' ]
		config.JobType.inputFiles = [ 'Summer15_25nsV5_DATA.db' ]
		if 'Run2015B' in dataset: config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-255031_13TeV_PromptReco_Collisions15_50ns_JSON_v2.txt'
		else: config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-258159_13TeV_PromptReco_Collisions15_25ns_JSON_v3.txt'
		config.General.requestName = dataset.split('/')[1]+"_"+dataset.split('/')[2]+'_'+name+'_'+version
		config.Data.publishDataName = dataset.split('/')[2]+'_'+name+'_'+version
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
