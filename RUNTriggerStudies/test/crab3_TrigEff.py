##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand
from multiprocessing import Process
from httplib import HTTPException

config = config()

version = 'v02p1'

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
config.Data.splitting = 'LumiBased'
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
			'/JetHT/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-f22ee4b431887aefaa4bd1ff29f8ab62/USER',
			]

	
	for dataset in Samples:
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-', '').split('-')[0]+'_'+version
		#procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-','').replace('RUNA','TriggerEfficiency').replace('-0cc1d310cda5930bd3b3a68493077b41','')+'_'+version
		#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_Silver.txt'
		config.Data.lumiMask = 'testLumi.json'

		config.Data.inputDataset = dataset
		config.General.requestName = procName
		config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0' ]
		#crabCommand('submit', config = config)
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
