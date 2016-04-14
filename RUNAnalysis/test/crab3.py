##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from httplib import HTTPException
import glob

config = config()

version = '_v03'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNFullAnalysis_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.publication = False
config.Data.ignoreLocality = True
supportFiles = glob.glob('supportFiles/*')
config.JobType.inputFiles = supportFiles
#config.JobType.inputFiles = [ 'supportFiles/PileupData2015D_JSON_latest.root',
#		'supportFiles/Fall15_25nsV2_DATA_L1FastJet_AK4PFchs.txt',
#		'supportFiles/Fall15_25nsV2_DATA_L1FastJet_AK8PFchs.txt',
#		'supportFiles/Fall15_25nsV2_DATA_L2L3Residual_AK4PFchs.txt',
#		'supportFiles/Fall15_25nsV2_DATA_L2L3Residual_AK8PFchs.txt',
#		'supportFiles/Fall15_25nsV2_DATA_L2Relative_AK4PFchs.txt',
#		'supportFiles/Fall15_25nsV2_DATA_L2Relative_AK8PFchs.txt',
#		'supportFiles/Fall15_25nsV2_DATA_L3Absolute_AK4PFchs.txt',
#		'supportFiles/Fall15_25nsV2_DATA_L3Absolute_AK8PFchs.txt',
#		'supportFiles/Fall15_25nsV2_DATA_Uncertainty_AK4PFchs.txt',
#		'supportFiles/Fall15_25nsV2_DATA_Uncertainty_AK8PFchs.txt',
#		'supportFiles/Fall15_25nsV2_MC_L1FastJet_AK4PFchs.txt',
#		'supportFiles/Fall15_25nsV2_MC_L1FastJet_AK8PFchs.txt',
#		'supportFiles/Fall15_25nsV2_MC_L2Relative_AK4PFchs.txt',
#		'supportFiles/Fall15_25nsV2_MC_L2Relative_AK8PFchs.txt',
#		'supportFiles/Fall15_25nsV2_MC_L3Absolute_AK4PFchs.txt',
#		'supportFiles/Fall15_25nsV2_MC_L3Absolute_AK8PFchs.txt',
#		'supportFiles/Fall15_25nsV2_MC_Uncertainty_AK4PFchs.txt',
#		'supportFiles/Fall15_25nsV2_MC_Uncertainty_AK8PFchs.txt',
#		]

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
			#'/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			
			#'/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/alkahn-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/alkahn-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/alkahn-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/alkahn-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p00-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',

			#'/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/alkahn-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p1-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/WWTo4Q_13TeV-powheg/alkahn-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p1-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/WZ_TuneCUETP8M1_13TeV-pythia8/mmorris-RunIIFall15MiniAODv2-PU25nsData2015v1_76X__b2ganafw763_v01-134aae24c3b7e602a70b1ddad6b4dd6c/USER',
			#'/ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',



			######## Centrally produced
			#'/RPVStopStopToJets_UDD312_M-90_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			#'/RPVStopStopToJets_UDD312_M-110_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			#'/RPVStopStopToJets_UDD312_M-120_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-130_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/RPVStopStopToJets_UDD312_M-140_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-150_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0-6ff2d2372798a32b31bae3809d51b58e/USER',
			#'/RPVStopStopToJets_UDD312_M-170_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-180_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-190_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-210_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-220_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-230_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',
			#'/RPVStopStopToJets_UDD312_M-240_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',


			#'/RPVStopStopToJets_UDD312_M-450_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',


			######## UDD323
			#'/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-088cec57f5d5229e192abf7cc5daa816/USER',


			######## Privately produced
#			#'/RPVSt100tojj_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09-6cd9a37acb7fba8686d9247b86713620/USER',
#			#'/RPVSt350tojj_13TeV_pythia8/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09-6cd9a37acb7fba8686d9247b86713620/USER',
#			'/RPVStopStopToJets_UDD312_M-100-madgraph/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09p1-6cd9a37acb7fba8686d9247b86713620/USER',
#			'/RPVStopStopToJets_UDD312_M-200-madgraph/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09p1-6cd9a37acb7fba8686d9247b86713620/USER',
#			'/RPVStopStopToJets_UDD312_M-350-madgraph/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09p1-6cd9a37acb7fba8686d9247b86713620/USER',
#			'/RPVStopStopToJets_UDD312_M-800-madgraph/algomez-RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09-6cd9a37acb7fba8686d9247b86713620/USER',

			#'/RPVStopStopToJets_UDD312_M-450_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/RPVStopStopToJets_UDD312_M-500_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/RPVStopStopToJets_UDD312_M-550_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/RPVStopStopToJets_UDD312_M-600_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/RPVStopStopToJets_UDD312_M-650_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/RPVStopStopToJets_UDD312_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/RPVStopStopToJets_UDD312_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/RPVStopStopToJets_UDD312_M-950_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/RPVStopStopToJets_UDD312_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/RPVStopStopToJets_UDD312_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
			#'/RPVStopStopToJets_UDD312_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER',
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
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 5
			procName = dataset.split('/')[1].replace('_TuneCUETP8M1_13TeV-madgraph-pythia8','')+dataset.split('/')[2].replace( dataset.split('/')[2].split('-')[0] , '').split('-')[1]+'_'+dataset.split('/')[2].replace(dataset.split('/')[2].split('-')[0], '').split('-')[2]+version
			config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0', 'systematics=1', 'jecVersion=Fall15_25nsV2', 'namePUFile=PileupData2015D_JSON_latest.root' ]
		else: 
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 1
			#procName = dataset.split('/')[1].replace('_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','').replace('_TuneCUETP8M1_13TeV_pythia8','').replace('13TeV_amcatnloFXFX_madspin_pythia8','')+dataset.split('/')[2].replace('jkarancs', '').split('-')[1]+'_'+dataset.split('/')[2].replace('jkarancs', '').split('-')[2]+version
			procName = dataset.split('/')[1].replace('_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','').replace('_TuneCUETP8M1_13TeV_pythia8','').replace('13TeV_amcatnloFXFX_madspin_pythia8','')+version+'p1'
			config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0', 'jecVersion=Fall15_25nsV2', 'namePUFile=PileupData2015D_JSON_latest.root' ]
			config.Data.lumiMask = 'crab_projects/crab_QCD_HT500to700_v03/results/notFinishedLumis.json'
		config.General.requestName = procName
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
