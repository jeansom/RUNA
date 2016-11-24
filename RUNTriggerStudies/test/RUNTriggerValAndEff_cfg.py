import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('RUN', 
		'JetHT_Run2016C',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"name"
		)


options.parseArguments()

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

NAME = options.RUN

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
	   '/store/data/Run2016C/JetHT/MINIAOD/PromptReco-v2/000/275/657/00000/0ED91D8C-913B-E611-8C29-02163E0142F6.root',
	   '/store/data/Run2016C/JetHT/MINIAOD/PromptReco-v2/000/275/657/00000/2A1EB5E4-633B-E611-B444-02163E014607.root',
	   '/store/data/Run2016C/JetHT/MINIAOD/PromptReco-v2/000/275/657/00000/40CF17F5-603B-E611-AC93-02163E0119FB.root',
	   '/store/data/Run2016C/JetHT/MINIAOD/PromptReco-v2/000/275/657/00000/DAD5ADB7-6C3B-E611-9635-02163E0135FB.root',
	   '/store/data/Run2016C/JetHT/MINIAOD/PromptReco-v2/000/275/657/00000/F4AF8FFB-663B-E611-BA67-02163E0137AC.root',

    ),
   lumisToProcess = cms.untracked.VLuminosityBlockRange('275657:1-275657:max'),
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32( options.maxEvents ) )


process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNTriggerValAndEff_'+NAME+'.root' ) )

#process.RUNBoostedTriggerEfficiency = cms.EDAnalyzer('RUNTriggerValAndEff',
process.BoostedTriggerEfficiency = cms.EDAnalyzer('RUNBoostedMiniAODTriggerEfficiency',
		baseTrigger = cms.string("HLT_PFHT475"),
		triggerPass = cms.vstring([ "HLT_PFHT800","HLT_AK8PFHT700_TrimR0p1PT0p03Mass50" ]),
		recoJets = cms.InputTag("slimmedJetsAK8")
)

process.AK8PFHT650TrimMass50 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring(["HLT_AK8PFHT650_TrimR0p1PT0p03Mass50"]),
		)


process.p = cms.Path(
		process.BoostedTriggerEfficiency
		#* process.AK8PFHT650TrimMass50
		)

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
