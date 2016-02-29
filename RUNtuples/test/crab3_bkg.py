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
config.JobType.inputFiles = [ 'Fall15_25nsV1_MC.db' ]
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 5
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
			#### RunIISpring15DR74 Asympt25ns
			#'/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
			#'/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
			#'/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
			#'/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
			#'/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
			#'/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
			#'/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
			#'/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
			#'/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
			#'/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
			#'/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
			
			#'/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
			#'/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
			#'/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
			'/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',
			#'/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/'+name+'mcRun2_asymptotic_v12-v1/MINIAODSIM',

			#'/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
			#'/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',

			]
	
	from multiprocessing import Process
	for dataset in Samples:
		config.Data.inputDataset = dataset
		procName = dataset.split('/')[1].replace('_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','')+'_'+name+'_'+version
		config.General.requestName = procName
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
