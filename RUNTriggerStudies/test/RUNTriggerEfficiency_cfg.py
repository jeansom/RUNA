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
options.register('ak4Jet4Pt', 
		80.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"jetPt cut"
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
#options.register('SubPt', 
#		0.3,
#		VarParsing.multiplicity.singleton,
#		VarParsing.varType.float,
#		"Subjet Pt Ratio cut"
#		)
options.register('Tau31', 
		0.3,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Tau31 cut"
		)
options.register('Tau21', 
		0.4,
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
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_1.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_10.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_100.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_101.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_102.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_103.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_104.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_105.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_106.root',
		   '/store/user/algomez/JetHT/Run2015D-PromptReco-v3_RUNA_v06/150930_081518/0000/RUNtuples_107.root',

		   #'/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_1.root',
		   #'/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_10.root',
		   #'/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_100.root',
		   #'/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_101.root',
		   #'/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_102.root',
		   #'/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_103.root',
		   #'/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_104.root',
		   #'/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_105.root',
		   #'/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_106.root',
		   #'/store/user/algomez/JetHT/Run2015B-PromptReco-v1_RUNA_v06/150930_081418/0000/RUNtuples_107.root',
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

process.ResolvedTriggerEfficiency = cms.EDAnalyzer('RUNResolvedTriggerEfficiency',
		cutjetPtvalue 		= cms.double( options.ak4Jet4Pt ),
		bjSample		= cms.bool( bjsample ),
		baseTrigger		= cms.string(basedline),
		triggerPass		= cms.vstring( ['HLT_PFHT800'] ),

)
process.ResolvedTriggerEfficiencyPFHT7504Jet = process.ResolvedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_PFHT750_4JetPt'] ) )
process.ResolvedTriggerEfficiencyPFHT800PFHT7504Jet = process.ResolvedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_PFHT800', 'HLT_PFHT750_4JetPt'] ) )

process.BoostedTriggerEfficiency = cms.EDAnalyzer('RUNBoostedTriggerEfficiency',
		cutjetPtvalue 		= cms.double( options.jetPt ),
		cutAsymvalue 		= cms.double( options.Asym ),
		cutCosThetavalue 	= cms.double( options.CosTheta ),
		cutTau31value 		= cms.double( options.Tau31 ),
		cutTau21value 		= cms.double( options.Tau21 ),
		bjSample		= cms.bool( bjsample ),
		baseTrigger		= cms.string(basedline),
		triggerPass		= cms.vstring( ['HLT_AK8PFHT700_TrimR0p1PT0p03Mass50'] ),

)

process.BoostedTriggerEfficiencyPFHT800 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencyAK8PFHT700PFHT800 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT700_TrimR0p1PT0p03Mass50', 'HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencyAK8PFHT700Pt360 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT700_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30'] ) )

process.BoostedTriggerEfficiencyAK8PFHT700PFHT7504Jets = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT700_TrimR0p1PT0p03Mass50', 'HLT_PFHT750_4JetPt'] ) )

process.BoostedTriggerEfficiencyAK8PFHT700Pt360PFHT800 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT700_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30', 'HLT_PFHT800'] ) )

process.BoostedTriggerEfficiencyAK8PFHT700Pt360PFHT7504Jets = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT700_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30', 'HLT_PFHT750_4JetPt'] ) )

process.BoostedTriggerEfficiencyAK8PFHT700Pt360PFHT7504JetsPFHT800 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( ['HLT_AK8PFHT700_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30', 'HLT_PFHT750_4JetPt', 'PFHT800'] ) )


if options.debug:
	process.p = cms.Path( process.BoostedTriggerEfficiency )
else:

	process.p = cms.Path( process.BoostedTriggerEfficiency
		* process.BoostedTriggerEfficiencyPFHT800 
		* process.BoostedTriggerEfficiencyAK8PFHT700PFHT800 
		* process.BoostedTriggerEfficiencyAK8PFHT700PFHT800
		* process.BoostedTriggerEfficiencyAK8PFHT700Pt360
		* process.BoostedTriggerEfficiencyAK8PFHT700PFHT7504Jets
		* process.BoostedTriggerEfficiencyAK8PFHT700Pt360PFHT800
		* process.BoostedTriggerEfficiencyAK8PFHT700Pt360PFHT7504Jets
		* process.BoostedTriggerEfficiencyAK8PFHT700Pt360PFHT7504JetsPFHT800
		* process.ResolvedTriggerEfficiency
		* process.ResolvedTriggerEfficiencyPFHT7504Jet
		* process.ResolvedTriggerEfficiencyPFHT800PFHT7504Jet
		)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
