import FWCore.ParameterSet.Config as cms
import sys

#PU = sys.argv[3]
#NAME = sys.argv[2]

process = cms.Process("Ana")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'PLS170_V7AN1::All')
#############   Set the number of events #############

#############   Define the source file ###############
#process.load('RPVStop100_AOD_cfi')
#process.TFileService=cms.Service("TFileService", fileName=cms.string('simpleMatching_RPVStop.root'))
#process.load('SqTOjn0_n0TOjjj_AOD_cfi')
#process.TFileService=cms.Service("TFileService", fileName=cms.string('simpleMatching_SqTOJn0.root'))
#process.load('goTOtbs_alan_AOD_cfi')
#process.TFileService=cms.Service("TFileService", fileName=cms.string('simpleMatching_goTOtbs.root'))
process.load('RSGraviton_AOD_cfi')
process.TFileService=cms.Service("TFileService", fileName=cms.string('simpleMatching_RSGraviton.root'))
process.maxEvents.input = cms.untracked.int32(-1)
    


#############   User analyzer (PF jets) ##
process.histos = cms.EDAnalyzer("Matching",
		jets = cms.InputTag( "ak8PFJetsCHS" ),
		genParticles = cms.InputTag( 'genParticles' ),
		#### stop
		#particle1 = cms.int32( 1000002 ),
		#particle2 = cms.int32( 0 ),
		#particle3 = cms.int32( 0 ),
		#### squark
		#particle1 = cms.int32( 1000005 ),
		#particle2 = cms.int32( 1000035 ),
		#particle3 = cms.int32( 1000025 ),
		### gluino
		#particle1 = cms.int32( 1000021 ),
		#particle2 = cms.int32( 6 ),
		#particle3 = cms.int32( 24 ),
		#### RSGraviton
		particle1 = cms.int32( 24 ),
		particle2 = cms.int32( 0 ),
		particle3 = cms.int32( 0 ),
		)

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleListDrawer",
		maxEventsToPrint = cms.untracked.int32(1),
		printVertex = cms.untracked.bool(False),
		src = cms.InputTag("genParticles")
		)


#############   Path       ###########################
process.p = cms.Path(
	process.histos
	* process.printTree
)
#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 100

