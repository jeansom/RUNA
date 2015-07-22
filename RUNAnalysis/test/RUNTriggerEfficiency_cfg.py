import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

#options.register('NAME', False,
#		    VarParsing.multiplicity.singleton,
#		        VarParsing.varType.bool,
#			    "Run this on real data"
#			    )
options.register('PROC', 
		'RPVSt100tojj_pythia8_13TeV_PU20bx25',
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
		#'/store/user/algomez/JetHT/RunIISpring15DR74_RUNA_Asympt25ns_v01/150714_152253/0000/RUNtuples_101.root'
	#	#'file:../../RUNtuples/test/RUNAEDMNtuple.root'
	    )
	)

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32 (options.maxEvents) )

if 'bj' in NAME: bjsample = True
else: bjsample = False
Lumi = 1000

from scaleFactors import scaleFactor
SF = scaleFactor(NAME)

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNTriggerEfficiency_'+NAME+'.root' ) )

process.TriggerEfficiencyPFHT475 = cms.EDAnalyzer('RUNTriggerEfficiency',
		scale 			= cms.double( 1 if SF == 1 else SF*Lumi ),
		cutjetPtvalue 		= cms.double( options.jetPt ),
		cutAsymvalue 		= cms.double( options.Asym ),
		cutCosThetavalue 	= cms.double( options.CosTheta ),
		cutSubjetPtRatiovalue 	= cms.double( options.SubPt ),
		cutTau31value 		= cms.double( options.Tau31 ),
		cutTau21value 		= cms.double( options.Tau21 ),
		bjSample		= cms.bool( bjsample ),
		Run			= cms.InputTag('eventInfo:evtInfoRunNumber'),
		Lumi			= cms.InputTag('eventInfo:evtInfoLumiBlock'),
		Event			= cms.InputTag('eventInfo:evtInfoEventNumber'),
		NPV	 		= cms.InputTag('eventUserData:npv'),
		ak4jetPt 		= cms.InputTag('jetsAK4:jetAK4Pt'),
		jetPt 			= cms.InputTag('jetsAK8:jetAK8Pt'),
		jetEta			= cms.InputTag('jetsAK8:jetAK8Eta'),
		jetPhi 			= cms.InputTag('jetsAK8:jetAK8Phi'),
		jetE 			= cms.InputTag('jetsAK8:jetAK8E'),
		jetMass 		= cms.InputTag('jetsAK8:jetAK8Mass'),
		jetTau1 		= cms.InputTag('jetsAK8:jetAK8tau1'),
		jetTau2 		= cms.InputTag('jetsAK8:jetAK8tau2'),
		jetTau3 		= cms.InputTag('jetsAK8:jetAK8tau3'),
		jetNSubjets 		= cms.InputTag('jetsAK8:jetAK8nSubJets'),
		jetSubjetIndex0 	= cms.InputTag('jetsAK8:jetAK8vSubjetIndex0'),
		jetSubjetIndex1 	= cms.InputTag('jetsAK8:jetAK8vSubjetIndex1'),
		jetSubjetIndex2 	= cms.InputTag('jetsAK8:jetAK8vSubjetIndex0'),
		jetSubjetIndex3 	= cms.InputTag('jetsAK8:jetAK8vSubjetIndex1'),
		jetKeys 		= cms.InputTag('jetKeysAK8'),
		jetCSV 			= cms.InputTag('jetsAK8:jetAK8CSV'),
		jetCSVV1 		= cms.InputTag('jetsAK8:jetAK8CSVV1'),
		#### Trigger
		triggerBit		= cms.InputTag('TriggerUserData:triggerBitTree'),
		triggerName		= cms.InputTag('TriggerUserData:triggerNameTree'),
		HLTtriggerOne		= cms.string('HLT_PFHT475'),
		HLTtriggerTwo		= cms.string('HLT_AK8PFHT700_TrimR0p1PT0p03Mass50'),
		#### JetID
		jecFactor 		= cms.InputTag('jetsAK8:jetAK8jecFactor0'),
		neutralHadronEnergy 	= cms.InputTag('jetsAK8:jetAK8neutralHadronEnergy'),
		neutralEmEnergy 	= cms.InputTag('jetsAK8:jetAK8neutralEmEnergy'),
		chargeEmEnergy 		= cms.InputTag('jetsAK8:jetAK8chargedEmEnergy'),
		muonEnergy 		= cms.InputTag('jetsAK8:jetAK8MuonEnergy'),
		#### Subjets
		subjetPt 		= cms.InputTag('subjetsAK8:subjetAK8Pt'),
		subjetEta 		= cms.InputTag('subjetsAK8:subjetAK8Eta'),
		subjetPhi 		= cms.InputTag('subjetsAK8:subjetAK8Phi'),
		subjetE 		= cms.InputTag('subjetsAK8:subjetAK8E'),
		subjetMass 		= cms.InputTag('subjetsAK8:subjetAK8Mass'),
		##### Trigger
		jetTrimmedMass 		= cms.InputTag('jetsAK8:jetAK8trimmedMass'),

)

process.TriggerEfficiencyPFMET170 = process.TriggerEfficiencyPFHT475.clone( HLTtriggerOne = cms.string('HLT_PFMET170_NoiseCleaned') )
process.TriggerEfficiencyIsoMu17 = process.TriggerEfficiencyPFHT475.clone( HLTtriggerOne = cms.string('HLT_IsoMu17_eta2p1_v') )
process.TriggerEfficiencyPFHT475PFHT800 = process.TriggerEfficiencyPFHT475.clone( HLTtriggerTwo = cms.string('HLT_PFHT800') )
process.TriggerEfficiencyPFMET170PFHT800 = process.TriggerEfficiencyPFHT475PFHT800.clone( HLTtriggerOne = cms.string('HLT_PFMET170_NoiseCleaned') )
process.TriggerEfficiencyIsoMu17PFHT800 = process.TriggerEfficiencyPFHT475PFHT800.clone( HLTtriggerOne = cms.string('HLT_IsoMu17_eta2p1_v') )
process.TriggerEfficiencyPFHT475AKPFHT650 = process.TriggerEfficiencyPFHT475.clone( HLTtriggerTwo = cms.string('HLT_AK8PFHT650_TrimR0p1PT0p03Mass50') )
process.TriggerEfficiencyPFHT475AKPFHT600 = process.TriggerEfficiencyPFHT475.clone( HLTtriggerTwo = cms.string('HLT_AK8PFHT600_TrimR0p1PT0p03Mass50') )
process.TriggerEfficiencyPFHT475AKPFHT550 = process.TriggerEfficiencyPFHT475.clone( HLTtriggerTwo = cms.string('HLT_AK8PFHT550_TrimR0p1PT0p03Mass50') )
process.TriggerEfficiencyPFHT475AKPFHT500 = process.TriggerEfficiencyPFHT475.clone( HLTtriggerTwo = cms.string('HLT_AK8PFHT500_TrimR0p1PT0p03Mass50') )

if options.debug:
	process.p = cms.Path( process.TriggerEfficiencyPruned )
else:

	process.p = cms.Path( process.TriggerEfficiencyPFHT475
		* process.TriggerEfficiencyPFMET170
		* process.TriggerEfficiencyIsoMu17
		* process.TriggerEfficiencyPFHT475PFHT800
		* process.TriggerEfficiencyPFMET170PFHT800
		* process.TriggerEfficiencyIsoMu17PFHT800
		)
	if 'RPV' in NAME:
		process.p += process.TriggerEfficiencyPFHT475AKPFHT650
		process.p += process.TriggerEfficiencyPFHT475AKPFHT600
		process.p += process.TriggerEfficiencyPFHT475AKPFHT500
		process.p += process.TriggerEfficiencyPFHT475AKPFHT550

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
