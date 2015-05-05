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
		#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/B2g_PU40bx50_v0/150219_165100/0000/B2GEDMNtuple_1.root',
		'file:RUNtuple_1.root'
	    )
	)

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32 (options.maxEvents) )

if 'bj' in NAME: bjsample = True
else: bjsample = False
Lumi = 1000

from scaleFactors import scaleFactor
SF = 1 #scaleFactor(NAME)

if 'PU40bx50' in NAME: PU = 'PU40bx50'
elif 'PU30BX50' in NAME: PU = 'PU30BX50'
elif 'PU20bx25' in NAME: PU = 'PU20bx25'
else: PU = 'NOPU'

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNAnalysis_'+NAME+'.root' ) )
#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'anaPlots.root' ) )

process.AnalysisPlots = cms.EDAnalyzer('RUNAnalysis',
		scale 			= cms.double(SF*Lumi),
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

if options.debug:
	process.p = cms.Path( process.AnalysisPlots )
else:

	process.p = cms.Path( process.AnalysisPlots
		* process.AnalysisPlotsNOSCALE
		)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
