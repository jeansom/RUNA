##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand
from httplib import HTTPException
from multiprocessing import Process

config = config()

name = 'RUNTriggerValidation'
version = 'v763'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNTriggerValidation_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 2
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
			'/QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIIFall15DR76-25nsFlat10to25TSG_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
			'/QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
			]
	
	for dataset in Samples:
		config.Data.inputDataset = dataset
		config.General.requestName = dataset.split('/')[1]+"_"+dataset.split('/')[2]+'_'+name+'_'+version
		if 'Run2015' in dataset: 
			config.JobType.pyCfgParams = [ 'RUN='+dataset.split('/')[1]+"_"+dataset.split('/')[2], 'local=0' ]
			config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-255031_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt'
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
