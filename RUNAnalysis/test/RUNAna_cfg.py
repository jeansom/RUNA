import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('PROC', 
		'RPVSt100tojj_pythia8_13TeV_PU20bx25',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"name"
		)

options.register('local', 
		True,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.bool,
		"Run locally or crab"
		)
## 'maxEvents' is already registered by the Framework, changing default value
#options.setDefault('maxEvents', 100)

options.parseArguments()

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

NAME = options.PROC

if options.local:
	process.load(NAME+'_RUNA_cfi')
	#process.load('RPVSt100tojj_13TeV_pythia8_RUNtuples_cfi')
else:
	process.source = cms.Source("PoolSource",
	   fileNames = cms.untracked.vstring(
		'/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/B2g_PU40bx50_v0/150219_165100/0000/B2GEDMNtuple_1.root',
	#	#'file:../../RUNtuples/test/RUNAEDMNtuple.root'
	    )
	)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

if 'bj' in NAME: bjsample = True
else: bjsample = False

if 'PU40bx50' in NAME:
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
		if bjsample: SF = 1521.11/ 49500. 
		else: SF = 1521.11/ 98208.    ## PU40bx50  1 fb-1

elif 'PU20bx25' in NAME: 
	PU = 'PU20bx25'
	Lumi = 4000

	if 'QCD' in NAME:
		if '500To1000' in NAME: SF = 26740. / 4063345.
		elif '1000ToInf' in NAME: SF =  769.7 / 1130720.
	else: 
		if bjsample: SF = 1521.11/ 49500. 
		else: SF = 1521.11/ 98300.    

else: SF = 1

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNAna_'+NAME+'.root' ) )

process.AnalysisPlots = cms.EDAnalyzer('RUNAna',
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
		jetCSV = cms.InputTag('jetsAK8:jetAK8CSV'),
		jetCSVV1 = cms.InputTag('jetsAK8:jetAK8CSVV1'),
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
