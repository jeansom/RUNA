##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from httplib import HTTPException

config = config()

version = '_v01'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNFullAnalysis_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.publication = False
config.Data.ignoreLocality = True
config.JobType.inputFiles = [ 'supportFiles/PileupData2015D_JSON_11-19-2015.root',
		'supportFiles/Fall15_25nsV2_DATA_L1FastJet_AK4PFchs.txt',
		'supportFiles/Fall15_25nsV2_DATA_L1FastJet_AK8PFchs.txt',
		'supportFiles/Fall15_25nsV2_DATA_L2L3Residual_AK4PFchs.txt',
		'supportFiles/Fall15_25nsV2_DATA_L2L3Residual_AK8PFchs.txt',
		'supportFiles/Fall15_25nsV2_DATA_L2Relative_AK4PFchs.txt',
		'supportFiles/Fall15_25nsV2_DATA_L2Relative_AK8PFchs.txt',
		'supportFiles/Fall15_25nsV2_DATA_L3Absolute_AK4PFchs.txt',
		'supportFiles/Fall15_25nsV2_DATA_L3Absolute_AK8PFchs.txt',
		'supportFiles/Fall15_25nsV2_DATA_Uncertainty_AK4PFchs.txt',
		'supportFiles/Fall15_25nsV2_DATA_Uncertainty_AK8PFchs.txt',
		'supportFiles/Fall15_25nsV2_MC_L1FastJet_AK4PFchs.txt',
		'supportFiles/Fall15_25nsV2_MC_L1FastJet_AK8PFchs.txt',
		'supportFiles/Fall15_25nsV2_MC_L2Relative_AK4PFchs.txt',
		'supportFiles/Fall15_25nsV2_MC_L2Relative_AK8PFchs.txt',
		'supportFiles/Fall15_25nsV2_MC_L3Absolute_AK4PFchs.txt',
		'supportFiles/Fall15_25nsV2_MC_L3Absolute_AK8PFchs.txt',
		'supportFiles/Fall15_25nsV2_MC_Uncertainty_AK4PFchs.txt',
		'supportFiles/Fall15_25nsV2_MC_Uncertainty_AK8PFchs.txt',
		]

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
			#'/JetHT/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-f22ee4b431887aefaa4bd1ff29f8ab62/USER',
			#'/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/alkahn-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/mmorris-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/TT_TuneCUETP8M1_13TeV-powheg-pythia8/vorobiev-B2GAnaFW_RunIIFall15MiniAODv2_25ns_v76x_v1_0-a5b607ee9aade77691e6d24b0736dda8/USER',



			######## Centrally produced
			#'/RPVStopStopToJets_UDD312_M-110_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-120_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			'/RPVStopStopToJets_UDD312_M-130_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-140_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-190_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-210_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-240_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',


			######## Privately produced
#			#'/RPVSt100tojj_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09-6cd9a37acb7fba8686d9247b86713620/USER',
#			#'/RPVSt350tojj_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09-6cd9a37acb7fba8686d9247b86713620/USER',
#			'/RPVStopStopToJets_UDD312_M-100-madgraph/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09p1-6cd9a37acb7fba8686d9247b86713620/USER',
#			'/RPVStopStopToJets_UDD312_M-200-madgraph/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09p1-6cd9a37acb7fba8686d9247b86713620/USER',
#			'/RPVStopStopToJets_UDD312_M-350-madgraph/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09p1-6cd9a37acb7fba8686d9247b86713620/USER',
#			'/RPVStopStopToJets_UDD312_M-800-madgraph/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09-6cd9a37acb7fba8686d9247b86713620/USER',

			]

	
	from multiprocessing import Process
	for dataset in Samples:
		config.Data.inputDataset = dataset
		if 'JetHT' in dataset: 
			procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-','').replace('RUNA','')+'_'+version
			config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_Silver.txt'
			config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0', 'jecVersion=Fall15_25nsV2' ]
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 10

		elif 'RPV' in dataset: 
			config.Data.splitting = 'FileBased'
			config.Data.unitsPerJob = 1
			procName = dataset.split('/')[1].replace('_TuneCUETP8M1_13TeV-madgraph-pythia8','')+dataset.split('/')[2].replace( dataset.split('/')[2].split('-')[0] , '').split('-')[1]+'_'+dataset.split('/')[2].replace(dataset.split('/')[2].split('-')[0], '').split('-')[2]+version
			config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0', 'systematics=1', 'jecVersion=Fall15_25nsV2', 'namePUFile=PileupData2015D_JSON_11-19-2015.root' ]
		else: 
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 10
			procName = dataset.split('/')[1].replace('_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','')+dataset.split('/')[2].replace('algomez', '').split('-')[1]+'_'+dataset.split('/')[2].replace('algomez', '').split('-')[2]+version
			config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0', 'jecVersion=Fall15_25nsV2', 'namePUFile=PileupData2015D_JSON_11-19-2015.root' ]
		config.General.requestName = procName
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
