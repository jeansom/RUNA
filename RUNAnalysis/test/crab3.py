##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from httplib import HTTPException

config = config()

version = 'v01'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNFullAnalysis_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False
config.Data.ignoreLocality = True
config.JobType.inputFiles = [ '/afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_4_14/src/RUNA/RUNAnalysis/data/PileupData2015D_JSON_10-23-2015.root' ]

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
			#'/JetHT/algomez-Run2015D-PromptReco-v4_RUNA_v08p1-01c9541dbd18d802f04a5e2e96c52a4d/USER',
			'/JetHT/algomez-Run2015D-05Oct2015-v1_RUNA_v08-ca239eceb4b414f3c0d6d2e09621d4e9/USER',

			#'/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',
			#'/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',
			#'/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',
			#'/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',
			#'/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',
			#'/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',
			#'/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',
			#'/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',
			#'/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',
			#'/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',
			'/RPVSt100tojj_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',
			'/RPVSt200tobj_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',
			'/RPVSt350tobj_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08-4a60e85fe45fa92e3d679925522bbd7b/USER',

			]

	
	from multiprocessing import Process
	for dataset in Samples:
		config.Data.inputDataset = dataset
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-','').replace('RUNA','')+'_'+version
		if 'JetHT' in dataset: 
			config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt'
		config.General.requestName = procName
		config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0' ]
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
