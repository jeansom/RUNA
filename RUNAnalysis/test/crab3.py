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
config.JobType.psetName = 'RUNFullAnalysis_cfg.py'
#config.JobType.psetName = 'RUNBoostedResolutionCalc_cfg.py'
#config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.splitting = 'LumiBased'
config.Data.publication = False
#config.Data.ignoreLocality = True

#config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.storageSite = 'T3_US_Rutgers'
config.Data.outLFNDirBase = '/store/user/algomez/myArea/EOS/B2GAnaFW_80X_V2p1/'

def submit(config):
	try:
		crabCommand('submit', config = config)
		#crabCommand('submit', '--wait', config = config)
	except HTTPException, hte:
		print 'Cannot execute commend'
		print hte.headers



#######################################################################################
if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--sample', action='store', default='all', dest='sample', help='Sample to process. Example: QCD, RPV, TTJets.' )
	parser.add_argument('-v', '--version', action='store', default='v01p0', dest='version', help='Version: v01, v02.' )
	parser.add_argument('-b', '--btagCSVFile', action='store', default='CSVv2_ichep.csv', dest='btagCSVFile', help='BtagCSVFile: CSVv2_ichep.csv.' )

	try: args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	Samples = {}

	Samples[ 'JetHTB' ] = [ '/JetHT/algomez-Run2016B-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'JetHTC' ] = [ '/JetHT/algomez-Run2016C-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'JetHTD' ] = [ '/JetHT/algomez-Run2016D-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'JetHTE' ] = [ '/JetHT/algomez-Run2016E-PromptReco-v2_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8E' ]
	Samples[ 'JetHTF' ] = [ '/JetHT/algomez-Run2016F-PromptReco-v1_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8F' ]
	Samples[ 'JetHTG' ] = [ '/JetHT/algomez-Run2016G-PromptReco-v1_B2GAnaFW_80X_V2p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8p2' ]
	Samples[ 'JetHTH' ] = [ '/JetHT/algomez-Run2016H-PromptReco-v2_B2GAnaFW_80X_V2p01p1-3e507461fd667ac6961fa4af5b123b09/USER', 10, 'Spring16_25nsV8p2' ]

	Samples[ 'QCDHT300' ] = [ '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1_B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER', 30, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDHT500' ] = [ '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1_B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER', 30, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDHT700' ] = [ '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/grauco-B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDHT1000' ] = [ '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/grauco-B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDHT1500' ] = [ '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/grauco-B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDHT2000' ] = [ '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/grauco-B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER', 10, 'Spring16_25nsV8BCD' ]
	
	Samples[ 'QCDPt120' ] = [ '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDPt170' ] = [ '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDPt300' ] = [ '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDPt470' ] = [ '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDPt600' ] = [ '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDPt800' ] = [ '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDPt1000' ] = [ '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDPt1400' ] = [ '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDPt1800' ] = [ '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDPt2400' ] = [ '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'QCDPt3200' ] = [ '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]

	Samples[ 'QCDHerwig' ] = [ '/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/algomez-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1_B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER', 10, 'Spring16_25nsV8BCD' ]

	Samples[ 'TTJets' ] = [ '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/grauco-B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER', 100, 'Spring16_25nsV8BCD' ]
	Samples[ 'WJets' ] = [ '/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/eschmitz-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1_B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'ZJets' ] = [ '/ZJetsToQQ_HT600toInf_13TeV-madgraph/eschmitz-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'WWJets' ] = [ '/WWTo4Q_13TeV-powheg/algomez-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1_B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'ZZJets' ] = [ '/ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8/algomez-RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1_B2GAnaFW_80X_V2p1-edbed0685401a5848e7d61871b3a63d8/USER', 100, 'Spring16_25nsV8BCD' ]
	
	Samples[ 'RPV80' ] = [ '/RPVStopStopToJets_UDD312_M-80_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV90' ] = [ '/RPVStopStopToJets_UDD312_M-90_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV100' ] = [ '/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV110' ] = [ '/RPVStopStopToJets_UDD312_M-110_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV120' ] = [ '/RPVStopStopToJets_UDD312_M-120_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV140' ] = [ '/RPVStopStopToJets_UDD312_M-140_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV150' ] = [ '/RPVStopStopToJets_UDD312_M-150_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV170' ] = [ '/RPVStopStopToJets_UDD312_M-170_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV180' ] = [ '/RPVStopStopToJets_UDD312_M-180_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV190' ] = [ '/RPVStopStopToJets_UDD312_M-190_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV230' ] = [ '/RPVStopStopToJets_UDD312_M-230_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV240' ] = [ '/RPVStopStopToJets_UDD312_M-240_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV300' ] = [ '/RPVStopStopToJets_UDD312_M-300_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV350' ] = [ '/RPVStopStopToJets_UDD312_M-350_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV400' ] = [ '/RPVStopStopToJets_UDD312_M-400_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV450' ] = [ '/RPVStopStopToJets_UDD312_M-450_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV500' ] = [ '/RPVStopStopToJets_UDD312_M-500_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV550' ] = [ '/RPVStopStopToJets_UDD312_M-550_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV600' ] = [ '/RPVStopStopToJets_UDD312_M-600_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV650' ] = [ '/RPVStopStopToJets_UDD312_M-650_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV700' ] = [ '/RPVStopStopToJets_UDD312_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV750' ] = [ '/RPVStopStopToJets_UDD312_M-750_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV800' ] = [ '/RPVStopStopToJets_UDD312_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV900' ] = [ '/RPVStopStopToJets_UDD312_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV1100' ] = [ '/RPVStopStopToJets_UDD312_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV1200' ] = [ '/RPVStopStopToJets_UDD312_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]
	Samples[ 'RPV1300' ] = [ '/RPVStopStopToJets_UDD312_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1-3435c96292394b4f7f0ff1725e305a15/USER', 10, 'Spring16_25nsV8BCD' ]

	processingSamples = {}
	if 'all' in args.sample: 
		for sam in Samples: processingSamples[ sam ] = Samples[ sam ]
	else:
		for sam in Samples: 
			if sam.startswith( args.sample ): processingSamples[ sam ] = Samples[ sam ]

	if len(processingSamples)==0: print 'No sample found. \n Have a nice day :)'
		
	for sam in processingSamples:
		dataset = processingSamples[sam][0]
		jecVersion = processingSamples[sam][2]
		supportFiles = glob.glob('supportFiles/'+jecVersion+'*txt') + glob.glob('supportFiles/'+args.btagCSVFile )
		config.Data.inputDataset = dataset
		config.Data.unitsPerJob = processingSamples[sam][1]
		if 'JetHT' in dataset: 
			procName = dataset.split('/')[1]+dataset.split('/')[2].split('-')[1]+'_'+args.version
			config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'
			config.JobType.pyCfgParams = [ 'PROC='+procName, 'jecVersion='+jecVersion, 'CSVFile='+args.btagCSVFile ]

		else:
			pileUpFile = 'PileupData2016BCDEFGH_271036-283685_69200.root'
			supportFiles = supportFiles+glob.glob('supportFiles/'+pileUpFile)
			procName = dataset.split('/')[1].split('_TuneCUETP8M1')[0]+args.version
			config.JobType.pyCfgParams = ( [ 'PROC='+procName, 'systematics='+('0' if 'RPV' in sam else '0'), 'jecVersion='+jecVersion, 'namePUFile='+pileUpFile, 'CSVFile='+args.btagCSVFile ] )

		config.JobType.inputFiles =  supportFiles
		config.General.requestName = procName
		print config
		print '|--- Submmiting sample: ', procName
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
