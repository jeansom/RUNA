import FWCore.ParameterSet.Config as cms
import sys

NAME = sys.argv[1]   		#### Remember to change to 1 for CRAB3
#NAME = 'RPV'
process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

if 'QCD' in NAME:
	#process.load(NAME+'_RUNA_cfi')
	process.source = cms.Source("PoolSource",
	    fileNames = cms.untracked.vstring(
	#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/RPVSt100tojj_13TeV_pythia8_EDMNtuple_PU40bx50_v3/150105_175258/0000/EDMNtuples_344.root'
	'file:../../RUNtuples/test/RUNAEDMNtuple.root'
	    )
	)
else: process.load(NAME+'_RUNA_cfi')
#process.load('RPVSt100tojj_13TeV_pythia8_RUNtuples_cfi')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#if 'PU40bx50' in NAME: 
PU = 'PU40bx50'
Lumi = 1000

if 'QCD' in NAME:
	if '80to120'in NAME: SF = 3000114.3*0.8456 / 2497232. 
	elif '120to170'in NAME: SF = 493200. * 0.8355 / 2472588. 
	elif '170to300'in NAME: SF = 120300 / 1473894.
	elif '300to470'in NAME: SF = 7475 / 1494912.
	elif '470to600'in NAME: SF = 587.1 /  1496537.
	elif '600to800'in NAME: SF = 167 /  1455578.
	elif '800to1000'in NAME: SF = 28.25 / 1483569.
	else: SF = 1
else: 
	SF = 1521.11/ 98208.    ## PU40bx50  1 fb-1
'''
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
		SF = 1521.11/98404.   ##PU20bx25

else: SF = 1
'''

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNAnalysis_'+NAME+'.root' ) )
#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'anaPlots.root' ) )

process.AnalysisPlots = cms.EDAnalyzer('RUNAnalysis',
		scale = cms.double(SF*Lumi),
		jetPt = cms.InputTag('jetsAK8:jetAK8Pt'),
		jetEta = cms.InputTag('jetsAK8:jetAK8Eta'),
		jetPhi = cms.InputTag('jetsAK8:jetAK8Phi'),
		jetE = cms.InputTag('jetsAK8:jetAK8E'),
		jetMass = cms.InputTag('jetsAK8:jetAK8Mass'),
		jetTau1 = cms.InputTag('jetsAK8:jetAK8tau1'),
		jetTau2 = cms.InputTag('jetsAK8:jetAK8tau2'),
		jetTau3 = cms.InputTag('jetsAK8:jetAK8tau3'),
		jetNSubjets = cms.InputTag('jetsAK8:jetAK8nSubJets'),
		jetSubjetIndex0 = cms.InputTag('jetsAK8:jetAK8vSubjetIndex0'),
		jetSubjetIndex1 = cms.InputTag('jetsAK8:jetAK8vSubjetIndex1'),
		jetSubjetIndex2 = cms.InputTag('jetsAK8:jetAK8vSubjetIndex0'),
		jetSubjetIndex3 = cms.InputTag('jetsAK8:jetAK8vSubjetIndex1'),
		jetKeys = cms.InputTag('jetKeysAK8'),
		#### JetID
		jecFactor = cms.InputTag('jetsAK8:jetAK8jecFactor0'),
		neutralHadronEnergy = cms.InputTag('jetsAK8:jetAK8neutralHadronEnergy'),
		neutralEmEnergy = cms.InputTag('jetsAK8:jetAK8neutralEmEnergy'),
		chargeEmEnergy = cms.InputTag('jetsAK8:jetAK8chargedEmEnergy'),
		muonEnergy = cms.InputTag('jetsAK8:jetAK8MuonEnergy'),
		#### Subjets
		subjetPt = cms.InputTag('subjetsAK8:subjetAK8Pt'),
		subjetEta = cms.InputTag('subjetsAK8:subjetAK8Eta'),
		subjetPhi = cms.InputTag('subjetsAK8:subjetAK8Phi'),
		subjetE = cms.InputTag('subjetsAK8:subjetAK8E'),
		subjetMass = cms.InputTag('subjetsAK8:subjetAK8Mass'),

)

process.AnalysisPlotsTrimmed = process.AnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8trimmedMass') )
process.AnalysisPlotsFiltered = process.AnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8filteredMass') )
process.AnalysisPlotsPruned = process.AnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8prunedMass') )

process.p = cms.Path(process.AnalysisPlots
		* process.AnalysisPlotsTrimmed
		* process.AnalysisPlotsPruned
		* process.AnalysisPlotsFiltered
		)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
