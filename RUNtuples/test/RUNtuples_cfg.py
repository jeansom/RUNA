#Prepare all the toolbox inputs
from RecoJets.JetProducers.jettoolboxMiniHelper_cff import *

#Load the toolbox
process.load('RecoJets.JetProducers.jettoolbox_cff')

process.GlobalTag.globaltag = 'PLS170_V7AN1::All'
#if miniAODInput: 
    #QGTagger.srcVertexCollection = 'unpackedTracksAndVertices'
#    pass

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#Deswizzle valueMaps and attach to PAT::Jets as userFloats

#process.patJetsAK4PFCHS.userData.userFloats.src += ['pileupJetIdEvaluator:fullDiscriminant','QGTagger:qgLikelihood']
#process.patJetsAK4PFCHS.userData.userInts.src   += ['pileupJetIdEvaluator:cutbasedId','pileupJetIdEvaluator:fullId']

#process.ak8PFJetsCHSTrimmedMod = process.ak5PFJetsTrimmed.clone( src = 'chs', rParam = 0.8, rFilt = 0.1 )
#process.ak8PFJetsCHSTrimmedModLinks = process.ak8PFJetsCHSTrimmedLinks.clone( matched = 'ak8PFJetsCHSTrimmedMod')

process.patJetsCA8PFCHS.userData.userFloats.src += ['NjettinessCA8:tau1','NjettinessCA8:tau2','NjettinessCA8:tau3',
                                                    'QJetsAdderCA8:QjetsVolatility',
                                                    'ca8PFJetsCHSPrunedLinks','ca8PFJetsCHSTrimmedLinks','ca8PFJetsCHSFilteredLinks',
                                                    'cmsTopTagPFJetsCHSLinksCA8']

process.patJetsAK8PFCHS.userData.userFloats.src += ['NjettinessAK8:tau1','NjettinessAK8:tau2','NjettinessAK8:tau3',
                                                    'QJetsAdderAK8:QjetsVolatility',
                                                    'ak8PFJetsCHSPrunedLinks','ak8PFJetsCHSTrimmedLinks','ak8PFJetsCHSFilteredLinks',#'ak8PFJetsCHSTrimmedModLinks',
                                                    'cmsTopTagPFJetsCHSLinksAK8']

process.load('Ntuples.Ntuples.BasicKinematics_cfg')

process.muonKinematics = process.kinematics.clone( src = 'slimmedMuons', prefix = 'mu' )
process.electronKinematics = process.kinematics.clone( src = 'slimmedElectrons', prefix = 'el' )
process.tauKinematics = process.kinematics.clone( src = 'slimmedTaus', prefix = 'tau' )
process.photonKinematics = process.kinematics.clone( src = 'slimmedPhotons', prefix = 'pho' )
process.AK4jetKinematics = process.kinematics.clone( src = 'slimmedJets', prefix = 'AK4jet' )
process.AK8jetKinematics = process.kinematics.clone( src = 'patJetsAK8PFCHS', prefix = 'AK8jet' )
process.CA8jetKinematics = process.kinematics.clone( src = 'patJetsCA8PFCHS', prefix = 'CA8jet' )

process.load('Ntuples.Ntuples.JetsSubstructure_cfg')

process.AK8jetSubstructure = process.substructure.clone( )
process.CA8jetSubstructure = process.substructure.clone( src = 'patJetsCA8PFCHS', prefix = 'CA8jet' )

process.p = cms.Path(
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

process.source.fileNames = cms.untracked.vstring(
		'/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/RPVSt100tojj_13TeV_pythia8_MiniAOD_v706_PU20bx25/b71e879835d2f0083a0e044b05216236/miniAOD-prod_PAT_1000_1_rnU.root',
		'/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/RPVSt100tojj_13TeV_pythia8_MiniAOD_v706_PU20bx25/b71e879835d2f0083a0e044b05216236/miniAOD-prod_PAT_1001_1_99p.root'
		)
#process.load('RPVStop100_MiniAOD_cfi')
process.maxEvents.input = cms.untracked.int32(10) 
process.out.fileName = cms.untracked.string('myOutputFile.root')
process.out.outputCommands = cms.untracked.vstring('drop *', 
		"keep *_*Kinematics*_*_*",
		"keep *_*Substructure*_*_*",
#		"keep *_MyAna2_*_*"
)
#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'Ntuple.root' ) )
#process.endpath.remove( process.out )
