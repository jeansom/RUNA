##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from httplib import HTTPException
config = config()

name = 'RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_'
version = 'v76x_v1p0'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.psetName = 'b2gedmntuples_cfg.py'
config.JobType.pyCfgParams = [ 'DataProcessing=Data25ns_76X' ]
config.JobType.inputFiles = [ 'Fall15_25nsV2_DATA.db' ]
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
			#'/JetHT/Run2015D-PromptReco-v4/MINIAOD',
			#'/JetHT/Run2015D-05Oct2015-v1/MINIAOD',
			'/JetHT/Run2015D-16Dec2015-v1/MINIAOD',
			#'/MET/Run2015B-PromptReco-v1/MINIAOD',
			##'/SingleMu/Run2015B-PromptReco-v1/MINIAOD',
			]
	
	from multiprocessing import Process
	for dataset in Samples:
		#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_Silver.txt' 
		config.Data.lumiMask = 'diff2.json' 
		config.Data.inputDataset = dataset
		procName = dataset.split('/')[1]+'_'+version
		config.General.requestName = procName+'v0p2'
		config.Data.outputDatasetTag = name+version
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
