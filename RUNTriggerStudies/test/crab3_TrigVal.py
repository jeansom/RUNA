##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from httplib import HTTPException

config = config()

name = 'RUNTriggerValidation'
version = 'v03p1'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNTriggerValidation_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.splitting = 'LumiBased'
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
			#'/JetHT/Run2015B-PromptReco-v1/MINIAOD',
			'/JetHT/Run2015C-PromptReco-v1/MINIAOD',
			##'/MET/Run2015B-PromptReco-v1/MINIAOD',
			##'/SingleMu/Run2015B-PromptReco-v1/MINIAOD',
			]
	
	from multiprocessing import Process
	for dataset in Samples:
		config.Data.inputDataset = dataset
		config.General.requestName = dataset.split('/')[1]+"_"+dataset.split('/')[2]+'_'+name+'_'+version
		if 'Run2015' in dataset: 
			config.JobType.pyCfgParams = [ 'RUN='+dataset.split('/')[1]+"_"+dataset.split('/')[2], 'local=0' ]
			if 'Run2015B' in dataset: config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-255031_13TeV_PromptReco_Collisions15_50ns_JSON.txt'
			elif 'Run2015C' in dataset: config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-255031_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt'
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
