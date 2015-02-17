import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
                            # replace 'myfile.root' with the source file you want to use
                            #fileNames = cms.untracked.vstring('file:jettoolbox.root')
                            #fileNames = cms.untracked.vstring('/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/JTB_MiniAOD_JEC_PU40bx50_v0/150212_230230/0000/jettoolbox_10.root')
			    fileNames = cms.untracked.vstring('root://cmsxrootd-site.fnal.gov//store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/JTB_MiniAOD_JEC_PU40bx50_v0/150212_230230/0000/jettoolbox_102.root')
                            )

process.demo = cms.EDAnalyzer('jetAnalyzer',
                              #src=cms.InputTag("patJetsAK4PFCHS")
                              #src=cms.InputTag("patJetsCA8PFCHS")
                              src=cms.InputTag("patJetsCA8PFCHS")
                              )
process.demo2 = cms.EDAnalyzer('jetAnalyzer',
                              #src=cms.InputTag("patJetsAK4PFCHS")
                              src=cms.InputTag("patJetsCA8PFCHS")
                              #src=cms.InputTag("selectedPatJetsAK8PFCHS")
                              #src=cms.InputTag("patJetsAK8PFCHS")
                              )
process.demo21 = process.demo2.clone( src=cms.InputTag("patJetsCA8PFCS") )
process.demo22 = process.demo2.clone( src=cms.InputTag("patJetsCA8PFSK") )


#process.demo1 = cms.EDAnalyzer('subjetTest',
process.demo1 = cms.EDAnalyzer('jetAnalyzer',
                              #src=cms.InputTag("patJetsAK4PFCHS")
                              #jets=cms.InputTag("subjetAK8",'withSubjets')
                              src=cms.InputTag('patJetsCA8withSubjets')
                              #jets=cms.InputTag("patJetsCA8Subjets")
                              #src=cms.InputTag("patJetsAK8PFCHS")
                              )


process.p = cms.Path( process.demo ) #* process.demo21 * process.demo22 )
