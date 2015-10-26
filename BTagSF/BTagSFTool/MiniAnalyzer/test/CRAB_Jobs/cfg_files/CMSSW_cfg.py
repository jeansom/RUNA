import FWCore.ParameterSet.Config as cms
import sys

print len(sys.argv)
if (len(sys.argv) > 2) : events = str(sys.argv[2])
else :
	#events = 'all'
	events = 'some'

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

if 'all' in events : process.load("Test.MiniAnalyzer.CfiFile_cfi")

if 'some' in events:

	process.source = cms.Source("PoolSource",
	    fileNames = cms.untracked.vstring(
		    'file:///eos/uscms/store/user/morris17/Sig_500SbtoWSt_100RPVSttojb_RUNA_v741p1/RunIISpring15DR74_MiniAOD/150616_165451/0001/Sig_500SbtoWSt_100RPVSttojb_RUNA_v741p1_MiniAOD_Asympt25ns_1000.root',
	    )
	)

if 'ttbar' in events : process.load("Test.MiniAnalyzer.ttbar_cfi")



process.TFileService=cms.Service("TFileService",fileName=cms.string( 'output_'+events+'Events.root' ) )

process.demo = cms.EDAnalyzer("QCDAnalyzer",
    vertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    muons = cms.InputTag("slimmedMuons"),
    electrons = cms.InputTag("slimmedElectrons"),
    taus = cms.InputTag("slimmedTaus"),
    photons = cms.InputTag("slimmedPhotons"),
    jets = cms.InputTag("slimmedJets"),
    ak8jets = cms.InputTag("slimmedJetsAK8"),
    puppijets = cms.InputTag("slimmedJetsPuppi"),
    mets = cms.InputTag("slimmedMETs"),
)

process.p = cms.Path(process.demo)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
