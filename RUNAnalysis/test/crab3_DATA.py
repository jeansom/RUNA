##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand
from multiprocessing import Process
config = config()

version = '_ts_v02'

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
			'/JetHT/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v01-89fb02accba11db128d1ea781dbd9ffe/USER',

			]

	
	for dataset in Samples:
		#procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RunIISpring15DR74_RUNA', '').split('-')[0]+'_'+version
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RunIISpring15DR74_RUNA_Asympt25ns', '_Asympt50ns').split('-')[0]+'_'+version
		#procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RUNA', '').split('-')[0]+'_'+version
		config.Data.inputDataset = dataset
		config.General.requestName = procName
		config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0' ]
		if 'RPV' in dataset: 
			config.Data.splitting = 'FileBased'
			config.Data.unitsPerJob = 1
		else: 
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 5
		#crabCommand('submit', config = config)
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
