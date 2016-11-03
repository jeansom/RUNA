##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from httplib import HTTPException
import glob

config = config()

version = 'v00'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNFullAnalysis_cfg.py'
#config.JobType.psetName = 'RUNBoostedResolutionCalc_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.publication = False
config.Data.ignoreLocality = True
supportFiles = glob.glob('supportFiles/*')
config.JobType.inputFiles = supportFiles

#config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.storageSite = 'T3_US_Rutgers'
config.Data.outLFNDirBase = '/store/user/algomez/myArea/EOS/B2GAnaFW_80X_V2p1/'

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
			#'/JetHT/algomez-Run2016C-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER',

			#'/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/grauco-B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER',
			#'/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/grauco-B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER',
			#'/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/grauco-B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER',
			#'/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/grauco-B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER',

			'/TT_TuneCUETP8M1_13TeV-powheg-pythia8/grauco-B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER',

			#'/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER',
			#'/RPVStopStopToJets_UDD312_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER',

			]

	
	for dataset in Samples:
		config.Data.inputDataset = dataset
		if 'JetHT' in dataset: 
			procName = dataset.split('/')[1]+dataset.split('/')[2].split('-')[1]+'_'+version
			config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-283685_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'
			config.JobType.pyCfgParams = [ 'PROC='+procName, 'jecVersion=Spring16_25nsV7BCD' ]
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 10

		elif 'RPV' in dataset: 
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 10
			procName = dataset.split('/')[1].split('_TuneCUETP8M1')[0]+version
			config.JobType.pyCfgParams = [ 'PROC='+procName, 'systematics=0', 'jecVersion=Spring16_25nsV7BCD', 'namePUFile=PileupData2016C_69200.root' ]
		else: 
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = ( 100 if 'TT' in dataset else 10 )
			procName = dataset.split('/')[1].split('_TuneCUETP8M1')[0]+version
			config.JobType.pyCfgParams = [ 'PROC='+procName, 'jecVersion=Spring16_25nsV7BCD', 'namePUFile=PileupData2016B_69200.root' ]
		config.General.requestName = procName
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
