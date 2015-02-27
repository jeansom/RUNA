import FWCore.ParameterSet.Config as cms
import sys

#NAME = sys.argv[2]
NAME = 'B2G'
process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

#if 'QCD' in NAME:
#else: process.load(NAME+'_RUNtuples_cfi')
#process.load('RPVStop_'+NAME+'_cfi')
#process.load('QCD_Pt-300to470_'+NAME+'_cfi')
process.load('TTJets_13TeV_'+NAME+'_cfi')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'comparisonJTB_RPVStop_'+NAME+'.root' ) )
#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'comparisonJTB_QCD_Pt-300to470_'+NAME+'.root' ) )
process.TFileService=cms.Service("TFileService",fileName=cms.string( 'comparisonJTB_TTjets_'+NAME+'.root' ) )


process.ak8jets = cms.EDAnalyzer('comparisonJTB',
		jetPt = cms.InputTag('jetsAK8:jetAK8Pt'),
		jetEta = cms.InputTag('jetsAK8:jetAK8Eta'),
		jetPhi = cms.InputTag('jetsAK8:jetAK8Phi'),
		jetE = cms.InputTag('jetsAK8:jetAK8E'),
		jetMass = cms.InputTag('jetsAK8:jetAK8Mass'),
		jetTau1 = cms.InputTag('jetsAK8:jetAK8tau1'),
		jetTau2 = cms.InputTag('jetsAK8:jetAK8tau2'),
		jetTau3 = cms.InputTag('jetsAK8:jetAK8tau3'),
		jetTrimmedMass = cms.InputTag('jetsAK8:jetAK8trimmedMass'),
		jetPrunedMass = cms.InputTag('jetsAK8:jetAK8prunedMass'),
		jetFilteredMass = cms.InputTag('jetsAK8:jetAK8filteredMass'),
		jetNumberOfDaughters = cms.InputTag('jetsAK8:jetAK8numberOfDaughters'),
		jetSubjetIndex1 = cms.InputTag('jetsAK8:jetAK8subjetIndex1'),
		jetSubjetIndex0 = cms.InputTag('jetsAK8:jetAK8subjetIndex0'),
		subjetPt = cms.InputTag('subjetsAK8:subjetAK8Pt'),
		subjetEta = cms.InputTag('subjetsAK8:subjetAK8Eta'),
		subjetPhi = cms.InputTag('subjetsAK8:subjetAK8Phi'),
		subjetE = cms.InputTag('subjetsAK8:subjetAK8E'),
		subjetMass = cms.InputTag('subjetsAK8:subjetAK8Mass'),
)
process.cmsTopTagger = cms.EDAnalyzer('comparisonJTB',
		jetPt = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagPt'),
		jetEta = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagEta'),
		jetPhi = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagPhi'),
		jetE = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagE'),
		jetMass = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagMass'),
		jetTau1 = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagtau1'),
		jetTau2 = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagtau2'),
		jetTau3 = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagtau3'),
		jetTrimmedMass = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagtrimmedMass'),
		jetPrunedMass = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagprunedMass'),
		jetFilteredMass = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagfilteredMass'),
		jetNumberOfDaughters = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagnumberOfDaughters'),
		jetSubjetIndex1 = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagsubjetIndex1'),
		jetSubjetIndex0 = cms.InputTag('jetsCmsTopTag:jetsCmsTopTagsubjetIndex0'),
		subjetPt = cms.InputTag('subjetsCmsTopTag:subjetsCmsTopTagPt'),
		subjetEta = cms.InputTag('subjetsCmsTopTag:subjetsCmsTopTagEta'),
		subjetPhi = cms.InputTag('subjetsCmsTopTag:subjetsCmsTopTagPhi'),
		subjetE = cms.InputTag('subjetsCmsTopTag:subjetsCmsTopTagE'),
		subjetMass = cms.InputTag('subjetsCmsTopTag:subjetsCmsTopTagMass'),
)
#
#process.AnalysisPlotsTrimmed = process.AnalysisPlots.clone( jetMass = cms.InputTag('ak8jets:ak8jetTrimmedMass') )
#process.AnalysisPlotsFiltered = process.AnalysisPlots.clone( jetMass = cms.InputTag('ak8jets:ak8jetFilteredMass') )
#process.AnalysisPlotsPruned = process.AnalysisPlots.clone( jetMass = cms.InputTag('ak8jets:ak8jetPrunedMass') )

process.p = cms.Path(process.ak8jets
		* process.cmsTopTagger
		)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
