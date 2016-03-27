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
			'file:///eos/uscms/store/user/dgsheffi/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09/151116_211916/0000/RUNtuple_504.root', 
			#'file:///eos/uscms/store/user/morris17/RunIISpring15DR74_MiniAOD/150616_165451/0000/Sig_500SbtoWSt_100RPVSttojb_RUNA_v741p1_MiniAOD_Asympt25ns_210.root',	    
			 )
				    )

if 'ttbar' in events : process.load("Test.MiniAnalyzer.ttbar_cfi")

isMiniAOD = 1 #0 is true, 1 is false (nTuple)

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'output_'+events+'Events.root' ) )

if isMiniAOD == 0:  
	process.demo = cms.EDAnalyzer("ImplementBtaggingSF",
				      vertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
				      muons = cms.InputTag("slimmedMuons"),
				      electrons = cms.InputTag("slimmedElectrons"),
				      taus = cms.InputTag("slimmedTaus"),
				      photons = cms.InputTag("slimmedPhotons"),
				      jets = cms.InputTag("slimmedJets"),
				      puppijets = cms.InputTag("slimmedJetsPuppi"),
				      mets = cms.InputTag("slimmedMETs"),

				      jetPt = cms.InputTag(""),
				      jetEta = cms.InputTag(""),
				      jetPhi = cms.InputTag(""),
				      jetE = cms.InputTag(""),
				      jetCSV = cms.InputTag(""),
				      jetCSVV1 = cms.InputTag(""),
				      jetPartonFlavour = cms.InputTag(""),
				      jetMass = cms.InputTag(""),
				      jetArea = cms.InputTag(""),
				      npv = cms.InputTag(""),
				      rho = cms.InputTag("fixedRhoFastjetCentralNeutral"),
				      isMiniAOD =  cms.int32(isMiniAOD)
				      )
	
if isMiniAOD == 1:
	process.demo = cms.EDAnalyzer("ImplementBtaggingSF",
				      vertices = cms.InputTag(""),
				      muons = cms.InputTag(""),
				      electrons = cms.InputTag(""),
				      taus = cms.InputTag(""),
				      photons = cms.InputTag(""),
				      jets = cms.InputTag(""),
				      puppijets = cms.InputTag(""),
				      mets = cms.InputTag(""),


				      jetPt = cms.InputTag("jetsAK4:jetAK4Pt"),
				      jetEta = cms.InputTag("jetsAK4:jetAK4Eta"),
				      jetPhi = cms.InputTag("jetsAK4:jetAK4Phi"),
				      jetE = cms.InputTag("jetsAK4:jetAK4E"),
				      jetCSV = cms.InputTag("jetsAK4:jetAK4CSV"),
				      jetCSVV1 = cms.InputTag("jetsAK4:jetAK4CSVV1"),
				      jetPartonFlavour = cms.InputTag("jetsAK4:jetAK4PartonFlavour"),
				      jetMass = cms.InputTag("jetsAK4:jetAK4Mass"),
				      jetArea = cms.InputTag("jetsAK4:jetAK4jetArea"),
				      npv = cms.InputTag("eventUserData:npv"),
				      rho = cms.InputTag(""),
				      isMiniAOD =  cms.int32(isMiniAOD)
				      )
	

process.p = cms.Path(process.demo)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
