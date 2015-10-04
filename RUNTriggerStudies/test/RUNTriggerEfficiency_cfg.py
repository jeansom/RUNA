import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('PROC', 
		'JetHT_Run2015C',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"name"
		)

options.register('local', 
		True,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.bool,
		"Run locally or crab"
		)
options.register('debug', 
		False,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.bool,
		"Run just pruned"
		)
options.register('jetPt', 
		150.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"jetPt cut"
		)
options.register('Asym', 
		0.1,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Asymmetry cut"
		)
options.register('CosTheta', 
		0.3,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"CosThetaStar cut"
		)
options.register('SubPt', 
		0.3,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Subjet Pt Ratio cut"
		)
options.register('Tau31', 
		0.5,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Tau31 cut"
		)
options.register('Tau21', 
		0.3,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Tau21 cut"
		)

options.parseArguments()

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

NAME = options.PROC

if options.local:
	process.load(NAME+'_RUNA_cfi')
	#process.load('RPVSt100tojj_13TeV_pythia8_RUNtuples_cfi')
else:
	process.source = cms.Source("PoolSource",
	   fileNames = cms.untracked.vstring(
		   '/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_1.root',
		   '/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_10.root',
		   '/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_100.root',
		   '/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_101.root',
		   '/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_102.root',
		   '/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_103.root',
		   '/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_104.root',
		   '/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_105.root',
		   '/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_106.root',
		   '/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_107.root',
	    )
	)

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32 (options.maxEvents) )

if 'bj' in NAME: bjsample = True
else: bjsample = False


if 'MET' in NAME: basedline = 'HLT_PFMET170_NoiseCleaned'
elif 'SingleMu' in NAME: basedline = 'HLT_IsoMu17_eta2p1_v'
else: basedline = 'HLT_PFHT475'

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNTriggerEfficiency_'+NAME+'.root' ) )

process.TriggerEfficiency = cms.EDAnalyzer('RUNTriggerEfficiency',
		cutjetPtvalue 		= cms.double( options.jetPt ),
		cutAsymvalue 		= cms.double( options.Asym ),
		cutCosThetavalue 	= cms.double( options.CosTheta ),
		#cutSubjetPtRatiovalue 	= cms.double( options.SubPt ),
		cutTau31value 		= cms.double( options.Tau31 ),
		cutTau21value 		= cms.double( options.Tau21 ),
		bjSample		= cms.bool( bjsample ),
		HLTtriggerOne		= cms.string(basedline),
		HLTtriggerTwo		= cms.string('HLT_AK8PFHT700_TrimR0p1PT0p03Mass50'),

)

process.TriggerEfficiencyPFHT800 = process.TriggerEfficiency.clone( HLTtriggerTwo = cms.string('HLT_PFHT800') )
process.TriggerEfficiencyAK8PFHT650 = process.TriggerEfficiency.clone( HLTtriggerTwo = cms.string('HLT_AK8PFHT650_TrimR0p1PT0p03Mass50') )
process.TriggerEfficiencyAK8PFHT650AndPFHT800 = process.TriggerEfficiencyAK8PFHT650.clone( HLTtriggerOne = cms.string('HLT_PFHT800') )

if options.debug:
	process.p = cms.Path( process.TriggerEfficiencyPruned )
else:

	process.p = cms.Path( process.TriggerEfficiency
		* process.TriggerEfficiencyPFHT800
		)
	if 'RPV' in NAME:
		process.p += process.TriggerEfficiencyAK8PFHT650
		process.p += process.TriggerEfficiencyAK8PFHT650AndPFHT800

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
