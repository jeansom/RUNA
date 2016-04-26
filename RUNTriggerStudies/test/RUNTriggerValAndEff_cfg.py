import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('RUN', 
		'QCD_Pt-15to3000', #'JetHT_Run2015C',
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
		   '/store/mc/RunIIFall15MiniAODv1/RPVStopStopToJets_UDD312_M-110_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/60000/0EB8FA1A-C5DB-E511-B188-0CC47A4DEDA2.root',
		   ##### 76X samples
		   #'/store/mc/RunIISpring15DR74/QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8/MINIAODSIM/HFscaleFlat10to30Asympt25ns_MCRUN2_74_V9-v1/10000/00060131-045F-E511-949D-0CC47A6B5B20.root',
		   #'/store/mc/RunIISpring15DR74/QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8/MINIAODSIM/HFscaleFlat10to30Asympt25ns_MCRUN2_74_V9-v1/10000/0082C690-035F-E511-952B-002618943886.root',
		   #'/store/mc/RunIISpring15DR74/QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8/MINIAODSIM/HFscaleFlat10to30Asympt25ns_MCRUN2_74_V9-v1/10000/0296CA5C-045F-E511-BDCC-003048FFD730.root',
		   ##### miniAODv2 samples with 76X
		   #'/store/mc/RunIIFall15MiniAODv2/QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/70000/0002078C-B0B9-E511-8907-0025905C431C.root',
		   #'/store/mc/RunIIFall15MiniAODv2/QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/70000/0004527F-6BB9-E511-A522-001E67504255.root',
	    )
	)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNTriggerValAndEff_'+NAME+'.root' ) )

process.AK8PFHT700TrimMass50 = cms.EDAnalyzer('RUNTriggerValAndEff',
		baseTrigger = cms.string("HLT_PFHT475"),
		triggerPass = cms.vstring([ "HLT_AK8PFHT700_TrimR0p1PT0p03Mass50" ]),
		recoJets = cms.InputTag("slimmedJetsAK8")
)

process.AK8PFHT650TrimMass50 = process.AK8PFHT700TrimMass50.clone( 
		triggerPass = cms.vstring(["HLT_AK8PFHT650_TrimR0p1PT0p03Mass50"]),
		)


process.p = cms.Path(
		process.AK8PFHT700TrimMass50
		* process.AK8PFHT650TrimMass50
		)

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
