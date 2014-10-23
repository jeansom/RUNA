from RUNA.RUNtuples.initializer_cfg import *


#process.ak8PFJetsCHSTrimmedMod = process.ak5PFJetsTrimmed.clone( src = 'chs', rParam = 0.8, rFilt = 0.1 )
#process.ak8PFJetsCHSTrimmedModLinks = process.ak8PFJetsCHSTrimmedLinks.clone( matched = 'ak8PFJetsCHSTrimmedMod')
#process.patJetsAK8PFCHS.userData.userFloats.src += ['ak8PFJetsCHSTrimmedModLinks'] 



#process.selectedPatJetsAK8PFCHS = cms.EDProducer("CandSelector", 
#		src = cms.InputTag("patJetsAK8PFCHS"),
#		cut = cms.string("pt > 10 & abs( eta ) < 2"))

process.load('RUNA.RUNtuples.BasicKinematics_cfg')

process.muonKinematics = process.kinematics.clone( src = 'slimmedMuons', prefix = 'mu' )
process.electronKinematics = process.kinematics.clone( src = 'slimmedElectrons', prefix = 'el' )
process.tauKinematics = process.kinematics.clone( src = 'slimmedTaus', prefix = 'tau' )
process.photonKinematics = process.kinematics.clone( src = 'slimmedPhotons', prefix = 'pho' )
process.AK4jetKinematics = process.kinematics.clone( src = 'slimmedJets', prefix = 'AK4jet' )
process.AK8jetKinematics = process.kinematics.clone( src = 'patJetsAK8PFCHS', prefix = 'AK8jet' )
process.CA8jetKinematics = process.kinematics.clone( src = 'patJetsCA8PFCHS', prefix = 'CA8jet' )


process.load('RUNA.RUNtuples.JetsSubstructure_cfg')
process.AK8jetSubstructure = process.substructure.clone( )
process.CA8jetSubstructure = process.substructure.clone( src = 'patJetsCA8PFCHS', prefix = 'CA8jet' )

### Gen Info
process.genInfo = cms.EDProducer('GenInfo', src = cms.InputTag('prunedGenParticles'))

#process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
#process.printTree = cms.EDAnalyzer("ParticleListDrawer",
#		  maxEventsToPrint = cms.untracked.int32(1),
#		    printVertex = cms.untracked.bool(False),
#		      src = cms.InputTag("prunedGenParticles")
#		      )

process.p = cms.Path(
		#process.printTree *
		process.genInfo *
		process.muonKinematics *
		process.electronKinematics *
		process.tauKinematics *
		process.photonKinematics *
		process.AK4jetKinematics *
		process.AK8jetKinematics *
		process.CA8jetKinematics *
		process.AK8jetSubstructure *
		process.CA8jetSubstructure 
		)


process.maxEvents.input = cms.untracked.int32(10) 
process.MessageLogger.cerr.FwkReport.reportEvery = 10

process.out = cms.OutputModule('PoolOutputModule',
		fileName = cms.untracked.string('outputFile_RUNtuple.root'),
		outputCommands = cms.untracked.vstring([
			"keep *_*genInfo*_*_*",
			"keep *_*Kinematics*_*_*",
			"keep *_*Substructure*_*_*",
			])
		)
process.endpath = cms.EndPath(process.out)

process.source = cms.Source("PoolSource",
		fileNames = cms.untracked.vstring(
#			'file:miniAOD-prod_PAT_1_1_Ir2.root'
		#	'/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/RPVSt100tojj_13TeV_pythia8_MiniAOD_v706_PU20bx25/b71e879835d2f0083a0e044b05216236/miniAOD-prod_PAT_1000_1_rnU.root',
		#	'/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/RPVSt100tojj_13TeV_pythia8_MiniAOD_v706_PU20bx25/b71e879835d2f0083a0e044b05216236/miniAOD-prod_PAT_1001_1_99p.root'
			'/store/user/mmorris/Sig_500SbtoWSt_100RPVSttojj_13TeV_100K_GENSIM/Sig_500SbtoWSt_100RPVSttojj_13TeV_100K_MiniAOD_v706_PU20bx25/b71e879835d2f0083a0e044b05216236/Sig_500SbtoWSt_100RPVSttojj_13TeV_100K_MiniAOD_PU20bx25_1000_1_OkP.root'
		)
)
