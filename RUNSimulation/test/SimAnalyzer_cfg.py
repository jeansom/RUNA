import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
#process.load("RPVSt100tojj_13TeV_pythia8_GENSIM_TESTHT500_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
	    #'/store/user/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15DR76_RAW_AODSIM_Asympt25ns/160131_123741/0000/RPVStopStopToJets_UDD323_M-100-madgraph_AODSIM_Asympt25ns_1.root',
	    #'/store/user/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15DR76_RAW_AODSIM_Asympt25ns/160131_123741/0000/RPVStopStopToJets_UDD323_M-100-madgraph_AODSIM_Asympt25ns_10.root',
	    #'/store/user/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15DR76_RAW_AODSIM_Asympt25ns/160131_123741/0000/RPVStopStopToJets_UDD323_M-100-madgraph_AODSIM_Asympt25ns_100.root',
	    #'/store/user/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15DR76_RAW_AODSIM_Asympt25ns/160131_123741/0000/RPVStopStopToJets_UDD323_M-100-madgraph_AODSIM_Asympt25ns_101.root',
	    '/store/user/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15DR76_MiniAOD_Asympt25ns/160202_114630/0000/RPVStopStopToJets_UDD323_M-100-madgraph_MiniAOD_Asympt25ns_1.root',
	    '/store/user/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15DR76_MiniAOD_Asympt25ns/160202_114630/0000/RPVStopStopToJets_UDD323_M-100-madgraph_MiniAOD_Asympt25ns_10.root',
	    '/store/user/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15DR76_MiniAOD_Asympt25ns/160202_114630/0000/RPVStopStopToJets_UDD323_M-100-madgraph_MiniAOD_Asympt25ns_100.root',
	    '/store/user/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15DR76_MiniAOD_Asympt25ns/160202_114630/0000/RPVStopStopToJets_UDD323_M-100-madgraph_MiniAOD_Asympt25ns_101.root',
	    '/store/user/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15DR76_MiniAOD_Asympt25ns/160202_114630/0000/RPVStopStopToJets_UDD323_M-100-madgraph_MiniAOD_Asympt25ns_102.root',
    )
)

process.TFileService = cms.Service("TFileService",
		fileName = cms.string('SimAnalyzer.root')
)

process.AK8Jets = cms.EDAnalyzer('SimAnalyzerMiniAOD',  ### CHANGE IT TO SimAnalyzerAOD to run on AOD
		genJets		= cms.InputTag('slimmedGenJetsAK8'), 	#miniAOD
		recoJets	= cms.InputTag('slimmedJetsAK8'), 	#miniAOD
		#recoJets	= cms.InputTag('ak8PFJetsCHS'), 	#AOD
		#genJets	= cms.InputTag('ak8GenJetsNoNu'), 	#AOD
		genParticles	= cms.InputTag('prunedGenParticles'),
		momPdgId 	= cms.double( 1000002 ),
		dau1PdgId	= cms.double( 3 ),
		dau2PdgId 	= cms.double( 5 ),
		minPt 		= cms.double( 100 ),
		dauDeltaR 	= cms.double( 0.7 ),
)

process.AK4Jets = process.AK8Jets.clone( 
		#genJets	= cms.InputTag('ak4GenJetsNoNu'), 	#AOD
		#recoJets	= cms.InputTag('ak4PFJetsCHS'), 	#AOD
		genJets		= cms.InputTag('slimmedGenJets'), 	#miniAOD
		recoJets	= cms.InputTag('slimmedJets'), 		#miniAOD
		dauDeltaR 	= cms.double( 0.3 ),
		minPt 		= cms.double( 50 ),
		)

process.p = cms.Path(
		process.AK8Jets
		* process.AK4Jets
		)
process.MessageLogger.cerr.FwkReport.reportEvery = 100
