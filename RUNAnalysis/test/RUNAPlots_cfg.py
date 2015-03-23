import FWCore.ParameterSet.Config as cms
import sys

NAME = sys.argv[2]
#NAME = 'RPV'
process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

if 'QCD' in NAME:
	process.source = cms.Source("PoolSource",
	    fileNames = cms.untracked.vstring(
		'/store/user/algomez/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/EDMNtuple_710pre9_v1_QCD_Pt-800to1000_Tune4C_13TeV_pythia8_20bx25_EDM/bc7f0a20a856f8e1766683b51f85b3cf/myOutputFile_100_1_RUf.root'
		#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/RPVSt100tojj_13TeV_pythia8_EDMNtuple_PU40bx50_v3/150105_175258/0000/EDMNtuples_344.root'
	    )
	)
else: process.load(NAME+'_RUNtuples_cfi')
#process.load('RPVSt100tojj_13TeV_pythia8_RUNtuples_cfi')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

if 'PU40bx50' in NAME: 
	PU = 'PU40bx50'
	Lumi = 1000

	if 'QCD' in NAME:
		if '80to120'in NAME: SF = 3000114.3*0.8456 / 2405333.  
		elif '120to170'in NAME: SF = 493200. * 0.8355 / 2319812.
		elif '170to300'in NAME: SF = 120300 / 1249192.
		elif '300to470'in NAME: SF = 7475 / 1410272.
		elif '470to600'in NAME: SF = 587.1 / 1425097.
		elif '600to800'in NAME: SF = 167 / 1403209.
		elif '800to1000'in NAME: SF = 28.25 / 1423109.
		else: SF = 1
	else: 
		SF = 559.757/ 98404.    ## PU40bx50  1 fb-1

elif 'PU20bx25' in NAME: 
	PU = 'PU20bx25'
	Lumi = 1000

	if 'QCD' in NAME:
		if '80to120'in NAME: SF = 3000114.3*0.8456 / 2405333.  
		elif '120to170'in NAME: SF = 493200. * 0.8355 / 2319812.
		elif '170to300'in NAME: SF = 120300 / 1249192.
		elif '300to470'in NAME: SF = 7475 / 1410272.
		elif '470to600'in NAME: SF = 587.1 / 1425097.
		elif '600to800'in NAME: SF = 167 / 1403209.
		elif '800to1000'in NAME: SF = 28.25 / 1423109.
	else: 
		SF = 559.757/98404.   ##PU20bx25

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'anaPlots_'+NAME+'.root' ) )
#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'anaPlots.root' ) )

process.AnalysisPlots = cms.EDAnalyzer('RUNAna',
		scale = cms.double(SF*Lumi),
		jetPt = cms.InputTag('ak8jets:ak8jetPt'),
		jetEta = cms.InputTag('ak8jets:ak8jetEta'),
		jetPhi = cms.InputTag('ak8jets:ak8jetPhi'),
		jetE = cms.InputTag('ak8jets:ak8jetE'),
		jetMass = cms.InputTag('ak8jets:ak8jetMass'),
		jetTau1 = cms.InputTag('ak8jets:ak8jetTau1'),
		jetTau2 = cms.InputTag('ak8jets:ak8jetTau2'),
		jetTau3 = cms.InputTag('ak8jets:ak8jetTau3'),
		jet1Subjets = cms.InputTag('ak8JetSubsSubjets:p4Subjet1'),
		jet2Subjets = cms.InputTag('ak8JetSubsSubjets:p4Subjet2'),
		jet3Subjets = cms.InputTag('ak8JetSubsSubjets:p4Subjet3'),
		jet4Subjets = cms.InputTag('ak8JetSubsSubjets:p4Subjet4'),
		#### JetID
		neutralHadronEnergyFraction = cms.InputTag('ak8jets:ak8jetneutralHadronEnergyFraction'),
		HFHadronEnergyFraction = cms.InputTag('ak8jets:ak8jetHFHadronEnergyFraction'),
		photonEnergy = cms.InputTag('ak8jets:ak8jetPhotonEnergy'),
		chargedHadronMultiplicity = cms.InputTag('ak8jets:ak8jetChargedHadronMultiplicity'),
		neutralHadronMultiplicity = cms.InputTag('ak8jets:ak8jetneutralHadronMultiplicity'),
		muonEnergy = cms.InputTag('ak8jets:ak8jetMuonEnergy'),
		electronEnergy = cms.InputTag('ak8jets:ak8jetElectronEnergy'),
		chargedHadronEnergyFraction = cms.InputTag('ak8jets:ak8jetChargedHadronEnergyFraction'),
		jecFactor = cms.InputTag('ak8jets:ak8jetjecFactor'),

)

process.AnalysisPlotsTrimmed = process.AnalysisPlots.clone( jetMass = cms.InputTag('ak8jets:ak8jetTrimmedMass') )
process.AnalysisPlotsFiltered = process.AnalysisPlots.clone( jetMass = cms.InputTag('ak8jets:ak8jetFilteredMass') )
process.AnalysisPlotsPruned = process.AnalysisPlots.clone( jetMass = cms.InputTag('ak8jets:ak8jetPrunedMass') )

process.p = cms.Path(process.AnalysisPlots
		* process.AnalysisPlotsTrimmed
		* process.AnalysisPlotsPruned
		* process.AnalysisPlotsFiltered
		)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
