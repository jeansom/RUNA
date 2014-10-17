import FWCore.ParameterSet.Config as cms
import sys

NAME = sys.argv[1]

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

#process.load(NAME+'_RUNA_cfi')

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/user/algomez/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/EDMNtuple_710pre9_v1_QCD_Pt-800to1000_Tune4C_13TeV_pythia8_20bx25_EDM/bc7f0a20a856f8e1766683b51f85b3cf/myOutputFile_100_1_RUf.root'
    )
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

Lumi = 10000
if 'QCD' in NAME:
	if '80to120'in NAME: SF = 3000114.3*0.8456 / 99796  
	elif '120to170'in NAME: SF = 493200. * 0.8355 / 99388
	elif '170to300'in NAME: SF = 120300 / 99796
	elif '300to470'in NAME: SF = 7475 / 98980
	elif '470to600'in NAME: SF = 587.1 / 99592
	elif '600to800'in NAME: SF = 167 / 99592
	elif '800to1000'in NAME: SF = 28.25 / 86944
else: 
	SF = 559.757/98404

#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'anaPlots_'+NAME+'.root' ) )
process.TFileService=cms.Service("TFileService",fileName=cms.string( 'anaPlots.root' ) )
process.AnalysisPlots = cms.EDAnalyzer('RUNAna',
		scale = cms.double(SF*Lumi),
		jetPt = cms.InputTag('AK8jetKinematics:AK8jetPt'),
		jetEta = cms.InputTag('AK8jetKinematics:AK8jetEta'),
		jetPhi = cms.InputTag('AK8jetKinematics:AK8jetPhi'),
		jetE = cms.InputTag('AK8jetKinematics:AK8jetEnergy'),
		jetMass = cms.InputTag('AK8jetKinematics:AK8jetMass'),
		jetTrimmedMass = cms.InputTag('AK8jetSubstructure:AK8jetsTrimmedMass'),
		jetPrunedMass = cms.InputTag('AK8jetSubstructure:AK8jetsPrunedMass'),
		jetFilteredMass = cms.InputTag('AK8jetSubstructure:AK8jetsFilteredMass'),
		jetTau1 = cms.InputTag('AK8jetSubstructure:AK8jetTau1'),
		jetTau2 = cms.InputTag('AK8jetSubstructure:AK8jetTau2'),
		jetTau3 = cms.InputTag('AK8jetSubstructure:AK8jetTau3'),
)

process.p = cms.Path(process.AnalysisPlots)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
