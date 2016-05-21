import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
#process.load("RPVSt100tojj_13TeV_pythia8_GENSIM_TESTHT500_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
	    '/store/mc/RunIIFall15MiniAODv2/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/40000/0E23CAB7-CCF7-E511-B774-008CFA166000.root',
	    '/store/mc/RunIIFall15MiniAODv2/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/40000/365E2FB1-DDF7-E511-9B95-008CFA0A59C0.root',
#	    '/store/mc/RunIIFall15MiniAODv2/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/40000/3EB87929-13F8-E511-AEE2-001517FB2458.root',
#	    '/store/mc/RunIIFall15MiniAODv2/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/40000/6A7AD8ED-F7F7-E511-A873-001E67DDD0AA.root',
#	    '/store/mc/RunIIFall15MiniAODv2/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/40000/90DB15EB-CCF7-E511-9241-008CFA5807F0.root',

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
		dau2PdgId 	= cms.double( 1 ),
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
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
