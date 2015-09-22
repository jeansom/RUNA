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
		'RPVSt350tojj_pythia8_13TeV_PU20bx25',
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
options.register('HT', 
		0.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"HT cut"
		)
options.register('MassRes', 
		0.15,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"MassRes cut"
		)
options.register('Delta', 
		70.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Delta cut"
		)
options.register('EtaBand', 
		1.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"EtaBand cut"
		)
options.register('JetPt', 
		80.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"JetPt cut"
		)

options.register('boostedJetPt', 
		150.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"JetPt cut"
		)

options.register('boostedHT', 
		800.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"JetPt cut"
		)

options.register('Asym', 
		0.1,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Asymmetry cut"
		)
options.register('CosTheta', 
		0.4,
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
		0.5,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Tau21 cut"
		)
options.register('DEta', 
		1.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"DEta cut"
		)
options.register('btag', 
		#0.244,  ## CSVL
		0.679, ## CSVM
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Btag cut"
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
		   '/store/user/algomez/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74_RUNA_Asympt25ns_v03/150911_073406/0000/RUNtuples_102.root',
		#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15DR74_RUNA_Asympt25ns__v02/150719_102556/0000/RUNtuples_11.root'
		#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15DR74_RUNA_Asympt25ns__v02/150719_170508/0000/RUNtuples_101.root',
		#'file:RUNtuple_1.root'
	    )
	)

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32 (options.maxEvents) )

if 'bj' in NAME: bjsample = True
else: bjsample = False
Lumi = 15.47

from scaleFactors import scaleFactor
SF = scaleFactor(NAME)

if 'JetHT' in NAME:
	sf = 1
	HTtrigger = 'HLT_PFHT900'
else: 
	sf = SF*Lumi
	HTtrigger = 'HLT_PFHT800'

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNFullAnalysis_'+NAME+'.root' ) )

process.AnalysisPlots = cms.EDAnalyzer('RUNAnalysis',
		scale 			= cms.double( sf ),
		cutHT	 		= cms.double( options.HT ),
		cutMassRes 		= cms.double( options.MassRes ),
		cutDelta 		= cms.double( options.Delta ),
		cutEtaBand 		= cms.double( options.EtaBand ),
		cutJetPt 		= cms.double( options.JetPt ),
		bjSample		= cms.bool( bjsample ),
		jetPt 			= cms.InputTag('jetsAK4:jetAK4Pt'),
		jetEta			= cms.InputTag('jetsAK4:jetAK4Eta'),
		jetPhi 			= cms.InputTag('jetsAK4:jetAK4Phi'),
		jetE 			= cms.InputTag('jetsAK4:jetAK4E'),
		jetMass 		= cms.InputTag('jetsAK4:jetAK4Mass'),
		jetTau1 		= cms.InputTag('jetsAK8:jetAK8tau1'),
		jetTau2 		= cms.InputTag('jetsAK8:jetAK8tau2'),
		jetTau3 		= cms.InputTag('jetsAK8:jetAK8tau3'),
		jetKeys 		= cms.InputTag('jetKeysAK8'),
		jetCSV 			= cms.InputTag('jetsAK4:jetAK4CSV'),
		jetCSVV1 		= cms.InputTag('jetsAK4:jetAK4CSVV1'),
		NPV	 		= cms.InputTag('eventUserData:npv'),
		#### JetID
		jecFactor 		= cms.InputTag('jetsAK4:jetAK4jecFactor0'),
		neutralHadronEnergy 	= cms.InputTag('jetsAK4:jetAK4neutralHadronEnergy'),
		neutralEmEnergy 	= cms.InputTag('jetsAK4:jetAK4neutralEmEnergy'),
		chargeEmEnergy 		= cms.InputTag('jetsAK4:jetAK4chargedEmEnergy'),
		muonEnergy 		= cms.InputTag('jetsAK4:jetAK4MuonEnergy'),
)

process.AnalysisPlotsNOSCALE = process.AnalysisPlots.clone( scale = cms.double(1) )

process.BoostedAnalysisPlots = cms.EDAnalyzer('RUNBoostedAnalysis',
		scale 			= cms.double( sf ),
		cutjetPtvalue 		= cms.double( options.boostedJetPt ),
		cutHTvalue  		= cms.double( options.boostedHT ),
		cutAsymvalue 		= cms.double( options.Asym ),
		cutCosThetavalue 	= cms.double( options.CosTheta ),
		cutSubjetPtRatiovalue 	= cms.double( options.SubPt ),
		cutTau31value 		= cms.double( options.Tau31 ),
		cutTau21value 		= cms.double( options.Tau21 ),
		cutDEtavalue 		= cms.double( options.DEta ),
		cutBtagvalue 		= cms.double( options.btag ),
		bjSample		= cms.bool( bjsample ),
		mkTree			= cms.bool( False  ),
		Run			= cms.InputTag('eventInfo:evtInfoRunNumber'),
		Lumi			= cms.InputTag('eventInfo:evtInfoLumiBlock'),
		Event			= cms.InputTag('eventInfo:evtInfoEventNumber'),
		NPV	 		= cms.InputTag('eventUserData:npv'),
		jetAK4Pt 		= cms.InputTag('jetsAK4:jetAK4Pt'),
		jetAK4Eta		= cms.InputTag('jetsAK4:jetAK4Eta'),
		jetAK4Phi 		= cms.InputTag('jetsAK4:jetAK4Phi'),
		jetAK4E 		= cms.InputTag('jetsAK4:jetAK4E'),
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
		HLTtriggerOne		= cms.string('HLT_AK8PFHT700_TrimR0p1PT0p03Mass50'),
		HLTtriggerTwo		= cms.string('HLT_AK8PFHT650_TrimR0p1PT0p03Mass50'),
		#### JetID
		jecFactor 		= cms.InputTag('jetsAK8:jetAK8jecFactor0'),
		neutralHadronEnergy 	= cms.InputTag('jetsAK8:jetAK8neutralHadronEnergy'),
		neutralEmEnergy 	= cms.InputTag('jetsAK8:jetAK8neutralEmEnergy'),
		chargedHadronEnergy 	= cms.InputTag('jetsAK8:jetAK8chargedHadronEnergy'),
		chargedEmEnergy		= cms.InputTag('jetsAK8:jetAK8chargedEmEnergy'),
		chargedHadronMultiplicity 	= cms.InputTag('jetsAK8:jetAK8ChargedHadronMultiplicity'),
		neutralHadronMultiplicity 	= cms.InputTag('jetsAK8:jetAK8neutralHadronMultiplicity'),
		chargedMultiplicity 	= cms.InputTag('jetsAK8:jetAK8chargedMultiplicity'),
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

process.BoostedAnalysisPlotsTrimmed = process.BoostedAnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8trimmedMass') )
process.BoostedAnalysisPlotsFiltered = process.BoostedAnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8filteredMass') )
process.BoostedAnalysisPlotsPruned = process.BoostedAnalysisPlots.clone( 
		jetMass 		= cms.InputTag('jetsAK8:jetAK8prunedMass'),
		#### Subjets
		subjetPt 		= cms.InputTag('subjetsAK8Pruned:subjetAK8PrunedPt'),
		subjetEta 		= cms.InputTag('subjetsAK8Pruned:subjetAK8PrunedEta'),
		subjetPhi 		= cms.InputTag('subjetsAK8Pruned:subjetAK8PrunedPhi'),
		subjetE 		= cms.InputTag('subjetsAK8Pruned:subjetAK8PrunedE'),
		subjetMass 		= cms.InputTag('subjetsAK8Pruned:subjetAK8PrunedMass'),
		)
process.BoostedAnalysisPlotsSoftDrop = process.BoostedAnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8softDropMass') )
process.BoostedAnalysisPlotsPuppi = process.BoostedAnalysisPlots.clone( 
		jetPt 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiPt'),
		jetEta			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiEta'),
		jetPhi 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiPhi'),
		jetE 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiE'),
		jetMass 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppiMass'),
		jetTau1 		= cms.InputTag('jetsAK8Puppi:jetAK8Puppitau1'),
		jetTau2 		= cms.InputTag('jetsAK8Puppi:jetAK8Puppitau2'),
		jetTau3 		= cms.InputTag('jetsAK8Puppi:jetAK8Puppitau3'),
		jetNSubjets 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppinSubJets'),
		jetSubjetIndex0 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppivSubjetIndex0'),
		jetSubjetIndex1 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppivSubjetIndex1'),
		jetSubjetIndex2 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppivSubjetIndex0'),
		jetSubjetIndex3 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppivSubjetIndex1'),
		jetKeys 		= cms.InputTag('jetKeysAK8Puppi'),
		#### Subjets
		subjetPt 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiPt'),
		subjetEta 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiEta'),
		subjetPhi 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiPhi'),
		subjetE 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiE'),
		subjetMass 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiMass'),
		)

process.BoostedAnalysisPlotsNOSCALE = process.BoostedAnalysisPlots.clone( scale = cms.double(1) )
process.BoostedAnalysisPlotsPrunedNOSCALE = process.BoostedAnalysisPlotsPruned.clone( scale = cms.double(1) )
process.BoostedAnalysisPlotsSoftDropNOSCALE = process.BoostedAnalysisPlotsSoftDrop.clone( scale = cms.double(1) )

process.BoostedAnalysisPlotsPrunedNOTrigger = process.BoostedAnalysisPlotsPruned.clone( 
		HLTtriggerOne		= cms.string('NOTRIGGER'),
		)
process.BoostedAnalysisPlotsPrunedPFHT900 = process.BoostedAnalysisPlotsPruned.clone( 
		HLTtriggerOne		= cms.string(HTtrigger),
		HLTtriggerTwo		= cms.string(HTtrigger),
		)
process.BoostedAnalysisPlotsPrunedPFHT7504JetPt50 = process.BoostedAnalysisPlotsPruned.clone( 
		HLTtriggerOne		= cms.string('HLT_PFHT750_4JetPt50'),
		HLTtriggerTwo		= cms.string('HLT_PFHT750_4JetPt50'),
		)
process.BoostedAnalysisPlotsPrunedAK8PFHT700ANDPFHT7504Jet = process.BoostedAnalysisPlotsPruned.clone( 
		HLTtriggerOne		= cms.string('HLT_AK8PFHT700_TrimR0p1PT0p03Mass50'),
		HLTtriggerTwo		= cms.string('HLT_PFHT750_4JetPt50'),
		)
process.BoostedAnalysisPlotsSoftDropPFHT900 = process.BoostedAnalysisPlotsSoftDrop.clone( 
		HLTtrigger		= cms.string(HTtrigger),
		)

process.RUNATreeSoftDrop = process.BoostedAnalysisPlotsSoftDrop.clone( mkTree = cms.bool( True ) )
process.RUNATreePruned = process.BoostedAnalysisPlotsPruned.clone( mkTree = cms.bool( True ) )

if options.debug:
	process.p = cms.Path( process.AnalysisPlots
			* process.BoostedAnalysisPlots )
else:

	process.p = cms.Path( process.AnalysisPlots
		* process.AnalysisPlotsNOSCALE
		* process.BoostedAnalysisPlots
		* process.BoostedAnalysisPlotsTrimmed
		* process.BoostedAnalysisPlotsPruned
		* process.BoostedAnalysisPlotsSoftDrop
		* process.BoostedAnalysisPlotsPuppi
		* process.BoostedAnalysisPlotsFiltered
		#* process.BoostedAnalysisPlotsSoftDropNOSCALE
		* process.BoostedAnalysisPlotsPrunedNOSCALE
		#* process.BoostedAnalysisPlotsSoftDropPFHT900
		* process.BoostedAnalysisPlotsPrunedPFHT900
		* process.BoostedAnalysisPlotsPrunedPFHT7504JetPt50
		* process.BoostedAnalysisPlotsPrunedAK8PFHT700ANDPFHT7504Jet	
		* process.BoostedAnalysisPlotsPrunedNOTrigger
		* process.RUNATreeSoftDrop
		* process.RUNATreePruned
		)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
