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
		'JetHT_Run2015B-PromptReco-v1',
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
options.register('AK4HT', 
		0.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"AK4HT cut"
		)
options.register('jetAK4Pt', 
		40.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"jetAK4Pt cut"
		)
options.register('HT', 
		700.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"HT cut"
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
options.register('DEta', 
		1.,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"DEta cut"
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
		'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15DR74_RUNA_Asympt25ns__v01/150703_162457/0000/RUNtuples_10.root'
	#	#'file:../../RUNtuples/test/RUNAEDMNtuple.root'
	    )
	)

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32 (options.maxEvents) )

if 'bj' in NAME: bjsample = True
else: bjsample = False

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNBoostedAnalysis_'+NAME+'.root' ) )
#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'anaPlots.root' ) )

process.AnalysisPlots = cms.EDAnalyzer('RUNBoostedAnalysis',
		#cutAK4HTvalue 		= cms.double( options.AK4HT ),
		#cutjetAK4Ptvalue 	= cms.double( options.jetAK4Pt ),
		#cutHTvalue 		= cms.double( options.HT ),
		cutjetPtvalue 		= cms.double( options.jetPt ),
		#cutTrimmedMassvalue	= cms.double( options.TMass ),
		cutAsymvalue 		= cms.double( options.Asym ),
		cutCosThetavalue 	= cms.double( options.CosTheta ),
		cutSubjetPtRatiovalue 	= cms.double( options.SubPt ),
		cutTau31value 		= cms.double( options.Tau31 ),
		cutTau21value 		= cms.double( options.Tau21 ),
		bjSample		= cms.bool( bjsample ),
		mkTree			= cms.bool( False  ),
)

process.test = process.AnalysisPlots.clone( mkTree = cms.bool( True ) )
process.AnalysisPlotsTrimmed = process.AnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8trimmedMass') )
process.AnalysisPlotsFiltered = process.AnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8filteredMass') )
process.AnalysisPlotsPruned = process.AnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8prunedMass') )


if options.debug:
	process.p = cms.Path( process.AnalysisPlotsPruned )
else:

	process.p = cms.Path( process.AnalysisPlots
		* process.AnalysisPlotsTrimmed
		* process.AnalysisPlotsPruned
		* process.AnalysisPlotsFiltered
		)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
