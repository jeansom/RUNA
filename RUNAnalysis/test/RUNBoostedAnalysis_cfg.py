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
options.register('TMass', 
		50.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Trimmed Mass (trigger) cut"
		)
options.register('HT', 
		700.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"HT cut"
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
		'/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/B2g_PU40bx50_v0/150219_165100/0000/B2GEDMNtuple_1.root',
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

if 'PU40bx50' in NAME: PU = 'PU40bx50'
elif 'PU30BX50' in NAME: PU = 'PU30BX50'
elif 'PU20bx25' in NAME: PU = 'PU20bx25'
else: PU = 'NOPU'

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNBoostedAnalysis_'+NAME+'.root' ) )
#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'anaPlots.root' ) )

process.AnalysisPlots = cms.EDAnalyzer('RUNBoostedAnalysis',
		scale 			= cms.double(SF*Lumi),
		cutHTvalue 		= cms.double( options.HT ),
		cutTrimmedMassvalue	= cms.double( options.TMass ),
		cutAsymvalue 		= cms.double( options.Asym ),
		cutCosThetavalue 	= cms.double( options.CosTheta ),
		cutSubjetPtRatiovalue 	= cms.double( options.SubPt ),
		cutTau31value 		= cms.double( options.Tau31 ),
		cutTau21value 		= cms.double( options.Tau21 ),
		bjSample		= cms.bool( bjsample ),
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
		NPV	 		= cms.InputTag('eventUserData:npv'),
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

process.AnalysisPlotsTrimmed = process.AnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8trimmedMass') )
process.AnalysisPlotsFiltered = process.AnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8filteredMass') )
process.AnalysisPlotsPruned = process.AnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8prunedMass') )

process.AnalysisPlotsNOSCALE = process.AnalysisPlots.clone( scale = cms.double(1) )
process.AnalysisPlotsTrimmedNOSCALE = process.AnalysisPlotsTrimmed.clone( scale = cms.double(1) )
process.AnalysisPlotsPrunedNOSCALE = process.AnalysisPlotsPruned.clone( scale = cms.double(1) )
process.AnalysisPlotsFilteredNOSCALE = process.AnalysisPlotsFiltered.clone( scale = cms.double(1) )

if options.debug:
	process.p = cms.Path( process.AnalysisPlotsPruned )
else:

	process.p = cms.Path( process.AnalysisPlots
		* process.AnalysisPlotsTrimmed
		* process.AnalysisPlotsPruned
		* process.AnalysisPlotsFiltered
		* process.AnalysisPlotsNOSCALE
		* process.AnalysisPlotsTrimmedNOSCALE
		* process.AnalysisPlotsPrunedNOSCALE
		* process.AnalysisPlotsFilteredNOSCALE
		)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
