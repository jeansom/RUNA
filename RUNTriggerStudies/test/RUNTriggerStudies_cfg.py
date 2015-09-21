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

process.load('JetHT_Run2015C_cfi')
#if options.local:
#	process.load(NAME+'_RUNA_cfi')
#	#process.load('RPVSt100tojj_13TeV_pythia8_RUNtuples_cfi')
#else:
#process.source = cms.Source("PoolSource",
#   fileNames = cms.untracked.vstring(
#	#'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/809/00000/FED49B77-7440-E511-ACA4-02163E015603.root',
#	'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/620/00000/D4BD3FF3-1D40-E511-8375-02163E0142EE.root',
#	'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/808/00000/3E6025B5-7340-E511-A8B7-02163E01440E.root',
#	'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/809/00000/FED49B77-7440-E511-ACA4-02163E015603.root',
#	'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/888/00000/823ED736-0941-E511-B9BA-02163E0145D8.root',
#	'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/890/00000/BE9881D7-2741-E511-B9E9-02163E015539.root',
#	'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/901/00000/FC888C66-2841-E511-820F-02163E014531.root',
#	'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/943/00000/362CA705-3741-E511-ACD6-02163E0144DB.root',
#	'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/944/00000/E020E2B8-5941-E511-9975-02163E013414.root',
#	'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/948/00000/B2E1FF3E-4141-E511-B07E-02163E014260.root',
#	'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/950/00000/7E834373-4241-E511-9A88-02163E015661.root',
##	#'file:../../RUNtuples/test/RUNAEDMNtuple.root'
#    )
#)

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

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNTriggerStudies_'+NAME+'.root' ) )

process.TriggerPlots = cms.EDAnalyzer('RUNTriggerStudies',
		bits = cms.InputTag("TriggerResults","","HLT"),
		prescales = cms.InputTag("patTrigger"),
		objects = cms.InputTag("selectedPatTrigger"),
		hltPath = cms.string("HLT_AK8PFHT"),
		hltTrigger = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
		recoJets = cms.InputTag("slimmedJetsAK8")
)


process.p = cms.Path(process.TriggerPlots
		)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
