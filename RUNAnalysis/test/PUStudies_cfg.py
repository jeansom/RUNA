import FWCore.ParameterSet.Config as cms
import sys

#NAME = sys.argv[2]
NAME = 'MiniAOD_JEC'
process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

#if 'QCD' in NAME:
#process.source = cms.Source("PoolSource",
#		fileNames = cms.untracked.vstring('file:jettoolbox.root'
#	'/store/user/algomez/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/EDMNtuple_710pre9_v1_QCD_Pt-800to1000_Tune4C_13TeV_pythia8_20bx25_EDM/bc7f0a20a856f8e1766683b51f85b3cf/myOutputFile_100_1_RUf.root'
	#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/RPVSt100tojj_13TeV_pythia8_EDMNtuple_PU40bx50_v3/150105_175258/0000/EDMNtuples_344.root'
 #   )
#)
#else: process.load(NAME+'_RUNtuples_cfi')
process.load('RPVStop_JTB_'+NAME+'_cfi')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'PUStudies_'+NAME+'.root' ) )

process.CA8Puppi = cms.EDAnalyzer('PUStudies', 
		jetLabel = cms.InputTag("patJetsCA8PFPuppi"),
		jetType = cms.string( "ca8" ),
		jetTYPE = cms.string( "CA8" ),
		PU = cms.string( "Puppi" ),
		)
process.CA8CS = process.CA8Puppi.clone( jetLabel = cms.InputTag("patJetsCA8PFCS"), PU = cms.string("CS") )
process.CA8CHS =process.CA8Puppi.clone( jetLabel = cms.InputTag("patJetsCA8PFCHS"), PU = cms.string("CHS") )
process.CA8SK = process.CA8Puppi.clone( jetLabel = cms.InputTag("patJetsCA8PFSK"), PU = cms.string("SK") )

process.AK8Puppi = process.CA8Puppi.clone( jetLabel = cms.InputTag("patJetsAK8PFPuppi"), jetType = "ak8", jetTYPE = 'AK8' )
process.AK8CS = process.AK8Puppi.clone( jetLabel = cms.InputTag("patJetsAK8PFCS"), PU = cms.string("CS") )
process.AK8CHS =process.AK8Puppi.clone( jetLabel = cms.InputTag("patJetsAK8PFCHS"), PU = cms.string("CHS") )
process.AK8SK = process.AK8Puppi.clone( jetLabel = cms.InputTag("patJetsAK8PFSK"), PU = cms.string("SK") )

process.CA12Puppi = process.CA8Puppi.clone( jetLabel = cms.InputTag("patJetsCA12PFPuppi"), jetType = "ca12", jetTYPE = 'CA12' )
process.CA12CS = process.CA12Puppi.clone( jetLabel = cms.InputTag("patJetsCA12PFCS"), PU = cms.string("CS") )
process.CA12CHS =process.CA12Puppi.clone( jetLabel = cms.InputTag("patJetsCA12PFCHS"), PU = cms.string("CHS") )
process.CA12SK = process.CA12Puppi.clone( jetLabel = cms.InputTag("patJetsCA12PFSK"), PU = cms.string("SK") )

process.AK8PrunedPuppi = process.CA8Puppi.clone( jetLabel = cms.InputTag("patJetsAK8PFPuppiPrunedPacked"), jetType = "ak8", jetTYPE = 'AK8' )
process.AK8PrunedCS = process.AK8PrunedPuppi.clone( jetLabel = cms.InputTag("patJetsAK8PFCSPrunedPacked"), PU = cms.string("CS") )
process.AK8PrunedCHS =process.AK8PrunedPuppi.clone( jetLabel = cms.InputTag("patJetsAK8PFCHSPrunedPacked"), PU = cms.string("CHS") )
process.AK8PrunedSK = process.AK8PrunedPuppi.clone( jetLabel = cms.InputTag("patJetsAK8PFSKPrunedPacked"), PU = cms.string("SK") )

process.AK8SoftDropPuppi = process.CA8Puppi.clone( jetLabel = cms.InputTag("patJetsAK8PFPuppiSoftDropPacked"), jetType = "ak8", jetTYPE = 'AK8' )
process.AK8SoftDropCS = process.AK8SoftDropPuppi.clone( jetLabel = cms.InputTag("patJetsAK8PFCSSoftDropPacked"), PU = cms.string("CS") )
process.AK8SoftDropCHS =process.AK8SoftDropPuppi.clone( jetLabel = cms.InputTag("patJetsAK8PFCHSSoftDropPacked"), PU = cms.string("CHS") )
process.AK8SoftDropSK = process.AK8SoftDropPuppi.clone( jetLabel = cms.InputTag("patJetsAK8PFSKSoftDropPacked"), PU = cms.string("SK") )

process.AK8CMSTopPuppi = process.CA8Puppi.clone( jetLabel = cms.InputTag("patJetsCMSTopTagPuppiPacked"), jetType = "ak8", jetTYPE = 'AK8' )
process.AK8CMSTopCS = process.AK8CMSTopPuppi.clone( jetLabel = cms.InputTag("patJetsCMSTopTagCSPacked"), PU = cms.string("CS") )
process.AK8CMSTopCHS =process.AK8CMSTopPuppi.clone( jetLabel = cms.InputTag("patJetsCMSTopTagCHSPacked"), PU = cms.string("CHS") )
process.AK8CMSTopSK = process.AK8CMSTopPuppi.clone( jetLabel = cms.InputTag("patJetsCMSTopTagSKPacked"), PU = cms.string("SK") )

process.p = cms.Path( process.CA8Puppi 
		* process.CA8CS 
		* process.CA8CHS
		* process.CA8SK
		* process.AK8Puppi
		* process.AK8CS 
		* process.AK8CHS
		* process.AK8SK
		* process.CA12Puppi
		* process.CA12CS 
		* process.CA12CHS
		* process.CA12SK
		* process.AK8PrunedPuppi
		* process.AK8PrunedCS 
		* process.AK8PrunedCHS
		* process.AK8PrunedSK
		* process.AK8SoftDropPuppi
		* process.AK8SoftDropCS 
		* process.AK8SoftDropCHS
		* process.AK8SoftDropSK
		* process.AK8CMSTopPuppi
		* process.AK8CMSTopCS 
		* process.AK8CMSTopCHS
		* process.AK8CMSTopSK
		)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
