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
	Lumi = 4000

	if 'QCD' in NAME:
		if '500To1000' in NAME: SF = 26740. / 4063345.
		elif '1000ToInf' in NAME: SF =  769.7 / 1130720.
	else: 
		if bjsample: SF = 1521.11/ 49500. 
		else: SF = 1521.11/ 98300.    

else: SF = 1

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNMCAnalysis_'+NAME+'.root' ) )
#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'anaPlots.root' ) )

process.AnalysisPlots = cms.EDAnalyzer('RUNMCAnalysis',
		scale = cms.double(SF*Lumi),
		bjSample = cms.bool( bjsample ),
		genPt = cms.InputTag('genPart:genPartPt'),
		genEta = cms.InputTag('genPart:genPartEta'),
		genPhi = cms.InputTag('genPart:genPartPhi'),
		genE = cms.InputTag('genPart:genPartE'),
		genMass = cms.InputTag('genPart:genPartMass'),
		genID = cms.InputTag('genPart:genPartID'),
		genMomID = cms.InputTag('genPart:genPartMomID'),
		genStatus = cms.InputTag('genPart:genPartStatus'),
		genCharge = cms.InputTag('genPart:genPartCharge'),

)


process.p = cms.Path(process.AnalysisPlots )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
