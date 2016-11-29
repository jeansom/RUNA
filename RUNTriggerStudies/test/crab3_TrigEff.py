##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
import argparse, sys
from httplib import HTTPException
from CRABAPI.RawCommand import crabCommand
from multiprocessing import Process
import glob


config = config()

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNTriggerEfficiency_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.outLFNDirBase = '/store/user/algomez/'
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 10

#config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.storageSite = 'T3_US_Rutgers'
config.Data.outLFNDirBase = '/store/user/algomez/myArea/EOS/TriggerEfficiency/'


def submit(config):
	try:
		crabCommand('submit', config = config)
	except HTTPException, hte:
		print 'Cannot execute commend'
		print hte.headers

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--sample', action='store', default='all', dest='sample', help='Sample to process. Example: QCD, RPV, TTJets.' )
	parser.add_argument('-v', '--version', action='store', default='v01p0', dest='version', help='Version: v01, v02.' )

	try: args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	Samples = {}

	Samples[ 'B2GJetHTB' ] = [ '/JetHT/algomez-Run2016B-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'B2GJetHTC' ] = [ '/JetHT/algomez-Run2016C-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'B2GJetHTD' ] = [ '/JetHT/algomez-Run2016D-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'B2GJetHTE' ] = [ '/JetHT/algomez-Run2016E-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8E' ]
	Samples[ 'B2GJetHTF' ] = [ '/JetHT/algomez-Run2016F-PromptReco-v1_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8F' ]
	Samples[ 'B2GJetHTG' ] = [ '/JetHT/algomez-Run2016G-PromptReco-v1_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8p2' ]
	Samples[ 'miniAODJetHTB' ] = [ '/JetHT/Run2016B-PromptReco-v2/MINIAOD', 10 ]
	Samples[ 'miniAODJetHTC' ] = [ '/JetHT/Run2016C-PromptReco-v2/MINIAOD', 10 ]
	Samples[ 'miniAODJetHTD' ] = [ '/JetHT/Run2016D-PromptReco-v2/MINIAOD', 10 ]
	Samples[ 'miniAODJetHTE' ] = [ '/JetHT/Run2016E-PromptReco-v2/MINIAOD', 10 ]
	Samples[ 'miniAODJetHTF' ] = [ '/JetHT/Run2016F-PromptReco-v1/MINIAOD', 10 ]
	Samples[ 'miniAODJetHTG' ] = [ '/JetHT/Run2016G-PromptReco-v1/MINIAOD', 10 ]
	Samples[ 'miniAODJetHTH' ] = [ '/JetHT/Run2016H-PromptReco-v2/MINIAOD', 10 ]

	Samples[ 'B2GSingleMuonB' ] = [ '/SingleMuon/algomez-Run2016B-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'B2GSingleMuonC' ] = [ '/SingleMuon/algomez-Run2016C-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'B2GSingleMuonD' ] = [ '/SingleMuon/algomez-Run2016D-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'B2GSingleMuonE' ] = [ '/SingleMuon/algomez-Run2016E-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8E' ]
	Samples[ 'B2GSingleMuonF' ] = [ '/SingleMuon/algomez-Run2016F-PromptReco-v1_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8F' ]
	Samples[ 'B2GSingleMuonG' ] = [ '/SingleMuon/algomez-Run2016G-PromptReco-v1_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8p2' ]
	Samples[ 'B2GSingleMuonH' ] = [ '/SingleMuon/algomez-Run2016H-PromptReco-v2_B2GAnaFW_80X_V2p01p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8p2' ]
	Samples[ 'miniAODSingleMuonB' ] = [ '/SingleMuon/Run2016B-PromptReco-v2/MINIAOD', 10 ]
	Samples[ 'miniAODSingleMuonC' ] = [ '/SingleMuon/Run2016C-PromptReco-v2/MINIAOD', 10 ]
	Samples[ 'miniAODSingleMuonD' ] = [ '/SingleMuon/Run2016D-PromptReco-v2/MINIAOD', 10 ]
	Samples[ 'miniAODSingleMuonE' ] = [ '/SingleMuon/Run2016E-PromptReco-v2/MINIAOD', 10 ]
	Samples[ 'miniAODSingleMuonF' ] = [ '/SingleMuon/Run2016F-PromptReco-v1/MINIAOD', 10 ]
	Samples[ 'miniAODSingleMuonG' ] = [ '/SingleMuon/Run2016G-PromptReco-v1/MINIAOD', 10 ]
	Samples[ 'miniAODSingleMuonH' ] = [ '/SingleMuon/Run2016H-PromptReco-v2/MINIAOD', 10 ]

	processingSamples = {}
	if 'all' in args.sample: 
		for sam in Samples: processingSamples[ sam ] = Samples[ sam ]
	else:
		for sam in Samples: 
			if sam.startswith( args.sample ): processingSamples[ sam ] = Samples[ sam ]

	if len(processingSamples)==0: print 'No sample found. \n Have a nice day :)'
		
	for sam in processingSamples:
		dataset = processingSamples[sam][0]
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-', '').split('-')[0]+'_'+args.version
		config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'

		config.Data.inputDataset = dataset
		config.General.requestName = procName
		if 'B2G' in args.sample:
			config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
			supportFiles = glob.glob('../../RUNAnalysis/test/supportFiles/'+processingSamples[sam][2]+'*txt')
			config.JobType.inputFiles = supportFiles

		config.JobType.pyCfgParams = [ 'PROC='+procName, ( 'miniAOD=True' if 'miniAOD' in args.sample else 'jecVersion='+processingSamples[sam][2]) ]
		#crabCommand('submit', config = config)
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
