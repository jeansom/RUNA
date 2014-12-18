import FWCore.ParameterSet.Config as cms
import sys

NAME = sys.argv[2]
#NAME = 'RPV'

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.load(NAME+'_RUNtuples_cfi')
#process.load('RPVSt100tojj_13TeV_pythia8_RUNtuples_cfi')

#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring(
#        '/store/user/algomez/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/EDMNtuple_710pre9_v1_QCD_Pt-800to1000_Tune4C_13TeV_pythia8_20bx25_EDM/bc7f0a20a856f8e1766683b51f85b3cf/myOutputFile_100_1_RUf.root'
#    )
#)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

Lumi = 1000
if 'QCD' in NAME:
	if '80to120'in NAME: SF = 3000114.3*0.8456 / 2153035.  
	elif '120to170'in NAME: SF = 493200. * 0.8355 / 2176333.
	elif '170to300'in NAME: SF = 120300 / 1142278.
	elif '300to470'in NAME: SF = 7475 / 1168604.
	elif '470to600'in NAME: SF = 587.1 / 1133901.
	elif '600to800'in NAME: SF = 167 / 1286492.
	elif '800to1000'in NAME: SF = 28.25 / 1114066.
else: 
	#SF = 559.757/98404.   ##PU20bx25
	SF = 559.757/80960.    ## PU40bx50  1 fb-1

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'anaPlots_'+NAME+'.root' ) )
#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'anaPlots.root' ) )
process.AnalysisPlots = cms.EDAnalyzer('RUNAna',
		scale = cms.double(SF*Lumi),
		jetPt = cms.InputTag('ak8jets:ak8jetPt'),
		jetEta = cms.InputTag('ak8jets:ak8jetEta'),
		jetPhi = cms.InputTag('ak8jets:ak8jetPhi'),
		jetE = cms.InputTag('ak8jets:ak8jetE'),
		jetMass = cms.InputTag('ak8jets:ak8jetMass'),
		jetTrimmedMass = cms.InputTag('ak8jets:ak8jetTrimmedMass'),
		jetPrunedMass = cms.InputTag('ak8jets:ak8jetPrunedMass'),
		jetFilteredMass = cms.InputTag('ak8jets:ak8jetFilteredMass'),
		jetTau1 = cms.InputTag('ak8jets:ak8jetTau1'),
		jetTau2 = cms.InputTag('ak8jets:ak8jetTau2'),
		jetTau3 = cms.InputTag('ak8jets:ak8jetTau3'),
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

process.p = cms.Path(process.AnalysisPlots)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
