##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from httplib import HTTPException
config = config()

name = 'RunIIFall15MiniAODv2-PU25nsData2015v1_76X_'
version = 'b2ganafw763_v01'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNtuples_cfg.py'
config.JobType.pyCfgParams = [ 'DataProcessing=MC25ns_MiniAOD_76X', 'useNoHFMET=0' ]
config.JobType.inputFiles = [ 'Summer15_25nsV7_MC.db' ]
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
#config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = True
#config.Data.ignoreLocality = True
config.Data.outputDatasetTag = name+'_'+version

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

	Samples = [ 
			'/RPVStopStopToJets_UDD312_M-120_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-130_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-140_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-210_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-240_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-300_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-350_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-400_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-450_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-500_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-550_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-600_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-750_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-950_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
#			'/RPVStopStopToJets_UDD312_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',

			##### privately produced
			#'/RPVStopStopToJets_UDD312_M-100-madgraph/algomez-RunIISpring15DR74_MiniAOD_Asympt25ns-612faf0bd9dc3ce1d1b2e0252700e0a7/USER',
			#'/RPVStopStopToJets_UDD312_M-200-madgraph/algomez-RunIISpring15DR74_MiniAOD_Asympt25ns-612faf0bd9dc3ce1d1b2e0252700e0a7/USER',
			#'/RPVStopStopToJets_UDD312_M-350-madgraph/algomez-RunIISpring15DR74_MiniAOD_Asympt25ns-612faf0bd9dc3ce1d1b2e0252700e0a7/USER',
			#'/RPVStopStopToJets_UDD312_M-800-madgraph/algomez-RunIISpring15DR74_MiniAOD_Asympt25ns-612faf0bd9dc3ce1d1b2e0252700e0a7/USER',
			]
	
	for dataset in Samples:
		config.Data.inputDataset = dataset
		procName = dataset.split('/')[1].replace('_TuneCUETP8M1_13TeV-madgraph-pythia8','')+'_'+name+'_'+version
		config.General.requestName = procName
		#crabCommand('submit', config = config)
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
