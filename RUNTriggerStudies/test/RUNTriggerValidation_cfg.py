import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('RUN', 
		'JetHT_Run2015C',
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

options.parseArguments()

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

NAME = options.RUN

if options.local:
	process.load(NAME+'_cfi')
else:
	process.source = cms.Source("PoolSource",
	   fileNames = cms.untracked.vstring(
		#'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/809/00000/FED49B77-7440-E511-ACA4-02163E015603.root',
		'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/620/00000/D4BD3FF3-1D40-E511-8375-02163E0142EE.root',
		'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/808/00000/3E6025B5-7340-E511-A8B7-02163E01440E.root',
		'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/809/00000/FED49B77-7440-E511-ACA4-02163E015603.root',
		'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/888/00000/823ED736-0941-E511-B9BA-02163E0145D8.root',
		'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/890/00000/BE9881D7-2741-E511-B9E9-02163E015539.root',
		'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/901/00000/FC888C66-2841-E511-820F-02163E014531.root',
		'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/943/00000/362CA705-3741-E511-ACD6-02163E0144DB.root',
		'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/944/00000/E020E2B8-5941-E511-9975-02163E013414.root',
		'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/948/00000/B2E1FF3E-4141-E511-B07E-02163E014260.root',
		'/store/data/Run2015C/JetHT/MINIAOD/PromptReco-v1/000/253/950/00000/7E834373-4241-E511-9A88-02163E015661.root',
	#	#'file:../../RUNtuples/test/RUNAEDMNtuple.root'
	    )
	)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNTriggerValidation_'+NAME+'.root' ) )

process.AK8PFHT700TrimMass50 = cms.EDAnalyzer('RUNTriggerValidation',
		bits = cms.InputTag("TriggerResults","","HLT"),
		prescales = cms.InputTag("patTrigger"),
		objects = cms.InputTag("selectedPatTrigger"),
		hltPath = cms.string("HLT_AK8PFHT700_TrimR0p1PT0p03Mass50"),
		hltTrigger = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
		recoJets = cms.InputTag("slimmedJetsAK8")
)

process.AK8PFHT650TrimMass50 = process.AK8PFHT700TrimMass50.clone( 
		hltPath = cms.string("HLT_AK8PFHT650_TrimR0p1PT0p03Mass50"),
		)


process.p = cms.Path(
		process.AK8PFHT700TrimMass50
		* process.AK8PFHT650TrimMass50
		)

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
