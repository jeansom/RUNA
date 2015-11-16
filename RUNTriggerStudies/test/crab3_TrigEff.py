##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand
from multiprocessing import Process
from httplib import HTTPException

config = config()

version = 'v02'

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
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

config.Site.storageSite = 'T3_US_FNALLPC'

def submit(config):
	try:
		crabCommand('submit', config = config)
	except HTTPException, hte:
		print 'Cannot execute commend'
		print hte.headers

if __name__ == '__main__':


	Samples = [ 
			#'/MET/alkahn-Run2015D-PromptReco-v4_RUNA_v08-f62a3527966d74334302f3a003049cf4/USER',
			'/JetHT/algomez-Run2015D-PromptReco-v4_RUNA_v08p1-01c9541dbd18d802f04a5e2e96c52a4d/USER',
			'/JetHT/algomez-Run2015D-05Oct2015-v1_RUNA_v08-ca239eceb4b414f3c0d6d2e09621d4e9/USER',
			]

	
	for dataset in Samples:
		#procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RUNA', '').split('-')[0]+'_'+version
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-','').replace('RUNA','TriggerEfficiency').replace('-0cc1d310cda5930bd3b3a68493077b41','')+'_'+version
		config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt'

		config.Data.inputDataset = dataset
		config.General.requestName = procName
		config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0' ]
		#crabCommand('submit', config = config)
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
