import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

#options.register('NAME', False,
#		    VarParsing.multiplicity.singleton,
#		        VarParsing.varType.bool,
#			    "Run this on real data"
#			    )
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
options.setDefault('maxEvents', 100)

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

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

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
	Lumi = 1000

	if 'QCD' in NAME:
		if 'QCD_HT' in NAME:
			if '500To1000' in NAME: SF = 26740. / 4063345.
			elif '1000ToInf' in NAME: SF =  769.7 / 1130720.
		else:
			if '170to300'in NAME: SF = 120300 / 2794554.
			elif '300to470'in NAME: SF = 7475 / 2705941.
			elif '470to600'in NAME: SF = 587.1 /  2926313.
			elif '600to800'in NAME: SF = 167 / 2857014.
			elif '800to1000'in NAME: SF = 28.25 / 2916394.
			elif '1000to1400'in NAME: SF = 8.195 / 2884228.
			elif '1400to1800'in NAME: SF = 0.7346 / 2931706.
	else: 
		if bjsample: SF = 1521.11/ 91100. 
		else: SF = 1521.11/ 98300.    

else: SF = 1

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNAnalysis_'+NAME+'.root' ) )
#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'anaPlots.root' ) )

process.AnalysisPlots = cms.EDAnalyzer('RUNAnalysis',
		scale 			= cms.double(SF*Lumi),
		cutHTvalue 		= cms.double( 700. ),
		cutAsymvalue 		= cms.double( 0.1 ),
		cutCosThetavalue 	= cms.double( 0.3 ),
		cutSubjetPtRatiovalue 	= cms.double( 0.3 ),
		cutTau31value 		= cms.double( 0.5 ),
		cutTau21value 		= cms.double( 0.6 ),
		bjSample		= cms.bool( bjsample ),
		jetPt 			= cms.InputTag('jetsAK8:jetAK8Pt'),
		jetEta			= cms.InputTag('jetsAK8:jetAK8Eta'),
		jetPhi 			= cms.InputTag('jetsAK8:jetAK8Phi'),
		jetE 			= cms.InputTag('jetsAK8:jetAK8E'),
		jetMass 		= cms.InputTag('jetsAK8:jetAK8Mass'),
		jetTau1 		= cms.InputTag('jetsAK8:jetAK8tau1'),
		jetTau2 		= cms.InputTag('jetsAK8:jetAK8tau2'),
		jetTau3 		= cms.InputTag('jetsAK8:jetAK8tau3'),
		jetNSubjets 		= cms.InputTag('jetsAK8:jetAK8nSubJets'),
		jetSubjetIndex0 	= cms.InputTag('jetsAK8:jetAK8vSubjetIndex0'),
		jetSubjetIndex1 	= cms.InputTag('jetsAK8:jetAK8vSubjetIndex1'),
		jetSubjetIndex2 	= cms.InputTag('jetsAK8:jetAK8vSubjetIndex0'),
		jetSubjetIndex3 	= cms.InputTag('jetsAK8:jetAK8vSubjetIndex1'),
		jetKeys 		= cms.InputTag('jetKeysAK8'),
		jetCSV 			= cms.InputTag('jetsAK8:jetAK8CSV'),
		jetCSVV1 		= cms.InputTag('jetsAK8:jetAK8CSVV1'),
		NPV	 		= cms.InputTag('eventUserData:npv'),
		#### JetID
		jecFactor 		= cms.InputTag('jetsAK8:jetAK8jecFactor0'),
		neutralHadronEnergy 	= cms.InputTag('jetsAK8:jetAK8neutralHadronEnergy'),
		neutralEmEnergy 	= cms.InputTag('jetsAK8:jetAK8neutralEmEnergy'),
		chargeEmEnergy 		= cms.InputTag('jetsAK8:jetAK8chargedEmEnergy'),
		muonEnergy 		= cms.InputTag('jetsAK8:jetAK8MuonEnergy'),
		#### Subjets
		subjetPt 		= cms.InputTag('subjetsAK8:subjetAK8Pt'),
		subjetEta 		= cms.InputTag('subjetsAK8:subjetAK8Eta'),
		subjetPhi 		= cms.InputTag('subjetsAK8:subjetAK8Phi'),
		subjetE 		= cms.InputTag('subjetsAK8:subjetAK8E'),
		subjetMass 		= cms.InputTag('subjetsAK8:subjetAK8Mass'),
		##### Trigger
		jetTrimmedMass 		= cms.InputTag('jetsAK8:jetAK8trimmedMass'),

)

process.AnalysisPlotsTrimmed = process.AnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8trimmedMass') )
process.AnalysisPlotsFiltered = process.AnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8filteredMass') )
process.AnalysisPlotsPruned = process.AnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8prunedMass') )

process.AnalysisPlotsNOSCALE = process.AnalysisPlots.clone( scale = cms.double(1) )
process.AnalysisPlotsTrimmedNOSCALE = process.AnalysisPlotsTrimmed.clone( scale = cms.double(1) )
process.AnalysisPlotsPrunedNOSCALE = process.AnalysisPlotsPruned.clone( scale = cms.double(1) )
process.AnalysisPlotsFilteredNOSCALE = process.AnalysisPlotsFiltered.clone( scale = cms.double(1) )

process.p = cms.Path(process.AnalysisPlots
		* process.AnalysisPlotsTrimmed
		* process.AnalysisPlotsPruned
		* process.AnalysisPlotsFiltered
		* process.AnalysisPlotsNOSCALE
		* process.AnalysisPlotsTrimmedNOSCALE
		* process.AnalysisPlotsPrunedNOSCALE
		* process.AnalysisPlotsFilteredNOSCALE
		)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
