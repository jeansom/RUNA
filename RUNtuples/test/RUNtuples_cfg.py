### *****************************************************************************************
### Usage:
###
### cmsRun RUNtuples_cfg.py maxEvts=N 
###
### Default values for the options are set:
### maxEvts     = -1
### *****************************************************************************************
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as opts

options = opts.VarParsing ('analysis')

options.register('maxEvts',
                 100,# default value: process all events
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.int,
                 'Number of events to process')

options.register('sample',
                 '/store/mc/RunIISpring15DR74/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/Asympt25nsRecodebug_MCRUN2_74_V9-v1/70000/12B18945-2E03-E511-800A-B083FED73FEC.root',
		 #'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15DR74_MiniAOD_v2/150613_105255/0000/RPVSt100tojj_13TeV_pythia8_MiniAOD_Asympt25ns_100.root',
		 #'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15DR74_MiniAOD_v2/150613_105255/0002/RPVSt100tojj_13TeV_pythia8_MiniAOD_Asympt25ns_2164.root',
		 #'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/162/00000/0A926801-4627-E511-99E6-02163E0144D6.root',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Sample to analyze')

options.register('lheLabel',
                 'source',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'LHE module label')

options.register('outputLabel',
                 'RUNtuples.root',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Output label')

options.register('globalTag',
                 #'MCRUN2_74_V9A',    ### For 50ns
                 '74X_mcRun2_asymptotic_v2', #'MCRUN2_74_V9',    ### For 25ns
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Global Tag')

options.register('isData',
                 False,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Is data?')

options.register('LHE',
                 False,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Keep LHEProducts')

options.parseArguments()

if(options.isData):options.LHE = False

    
###inputTag labels
muLabel  = 'slimmedMuons'
elLabel  = 'slimmedElectrons'
jLabel = 'slimmedJets'
jLabelAK8 = 'slimmedJetsAK8'

pvLabel  = 'offlineSlimmedPrimaryVertices'
convLabel = 'reducedEgamma:reducedConversions'
particleFlowLabel = 'packedPFCandidates'    
metLabel = 'slimmedMETs'
rhoLabel = 'fixedGridRhoFastjetAll'

triggerResultsLabel = "TriggerResults"
triggerSummaryLabel = "hltTriggerSummaryAOD"
hltMuonFilterLabel       = "hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f40QL3crIsoRhoFiltered0p15"
hltPathLabel             = "HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL"
hltElectronFilterLabel  = "hltL1sL1Mu3p5EG12ORL1MuOpenEG12L3Filtered8"
lheLabel = "source"

process = cms.Process("RUNtuples")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append('HLTrigReport')
process.MessageLogger.cerr.FwkReport.reportEvery = 100
### Output Report
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
### Number of maximum events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvts) )
### Source file
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
        options.sample
        )
)

process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = options.globalTag 


from JMEAnalysis.JetToolbox.jetToolbox_cff import jetToolbox
from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets

if ( options.isData ):
	jetToolbox( process, 'ak8', 'analysisPath', 'edmNtuplesOut', runOnMC=False, PUMethod='Puppi', addSoftDropSubjets=True, addPrunedSubjets=True, addTrimming=True, addPruning=True, addFiltering=True, addSoftDrop=True, addNsub=True )
	jetToolbox( process, 'ak8', 'analysisPath', 'edmNtuplesOut', runOnMC=False, PUMethod='SK', addSoftDropSubjets=True, addPrunedSubjets=True, addTrimming=True, addPruning=True, addFiltering=True, addSoftDrop=True, addNsub=True )
	jetToolbox( process, 'ak8', 'analysisPath', 'edmNtuplesOut', runOnMC=False, addSoftDropSubjets=True, addPrunedSubjets=True, addTrimming=True, addPruning=True, addFiltering=True, addSoftDrop=True, addNsub=True )
	jetToolbox( process, 'ca8', 'analysisPath', 'edmNtuplesOut', runOnMC=False, addCMSTopTagger=True )
else:
	jetToolbox( process, 'ak8', 'analysisPath', 'edmNtuplesOut', PUMethod='Puppi', addSoftDropSubjets=True, addPrunedSubjets=True, addTrimming=True, addPruning=True, addFiltering=True, addSoftDrop=True, addNsub=True )
	jetToolbox( process, 'ak8', 'analysisPath', 'edmNtuplesOut', PUMethod='SK', addSoftDropSubjets=True, addPrunedSubjets=True, addTrimming=True, addPruning=True, addFiltering=True, addSoftDrop=True, addNsub=True )
	jetToolbox( process, 'ak8', 'analysisPath', 'edmNtuplesOut', addSoftDropSubjets=True, addPrunedSubjets=True, addTrimming=True, addPruning=True, addFiltering=True, addSoftDrop=True, addNsub=True )
	jetToolbox( process, 'ca8', 'analysisPath', 'edmNtuplesOut', addCMSTopTagger=True )
jLabelAK8 = 'selectedPatJetsAK8PFCHS'

### Selected leptons and jets
process.skimmedPatMuons = cms.EDFilter(
    "PATMuonSelector",
    src = cms.InputTag(muLabel),
    cut = cms.string("pt > 10 && abs(eta) < 2.4")
    )

process.skimmedPatElectrons = cms.EDFilter(
    "PATElectronSelector",
    src = cms.InputTag(elLabel),
    cut = cms.string("pt > 10 && abs(eta) < 2.5")
    )

process.skimmedPatMET = cms.EDFilter(
    "PATMETSelector",
    src = cms.InputTag(metLabel),
    cut = cms.string("")
    )


process.skimmedPatJets = cms.EDFilter(
    "PATJetSelector",
    src = cms.InputTag(jLabel),
    cut = cms.string(" pt > 25 && abs(eta) < 5.")
    )

process.skimmedPatJetsAK8 = cms.EDFilter(
    "CandViewSelector",
    src = cms.InputTag(jLabelAK8),
    cut = cms.string("pt > 100 && abs(eta) < 5.")    
    )

process.skimmedPatJetsAK8Puppi = cms.EDFilter(
    "CandViewSelector",
    #src = cms.InputTag(jLabelAK8.replace('CHS', 'Puppi')),
    src = cms.InputTag('selectedPatJetsAK8PFPuppi'),
    cut = cms.string("pt > 100 && abs(eta) < 5.")    
    )

process.skimmedPatJetsAK8SK = cms.EDFilter(
    "CandViewSelector",
    src = cms.InputTag('selectedPatJetsAK8PFSK'),
    cut = cms.string("pt > 100 && abs(eta) < 5.")    
    )


process.eventUserData = cms.EDProducer(
    'EventUserData',
    pileup = cms.InputTag("addPileupInfo"),
    pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices")
)

process.muonUserData = cms.EDProducer(
    'MuonUserData',
    muonLabel = cms.InputTag("skimmedPatMuons"),
    pv        = cms.InputTag(pvLabel),
    ### TTRIGGER ###
    triggerResults = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltMuonFilter  = cms.InputTag(hltMuonFilterLabel),
    hltPath            = cms.string("HLT_IsoMu40_eta2p1_v11"),
    hlt2reco_deltaRmax = cms.double(0.1),
    # mainROOTFILEdir    = cms.string("../data/")
    )

process.jetUserData = cms.EDProducer(
    'JetUserData',
    jetLabel  = cms.InputTag(jLabel),
    ### TTRIGGER ###
    triggerResults = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltJetFilter       = cms.InputTag("hltPFHT900"),
    hltPath            = cms.string("HLT_PFHT900_v1"),
    hlt2reco_deltaRmax = cms.double(0.2),
    )


process.jetUserDataAK8 = cms.EDProducer(
    'JetUserData',
    jetLabel  = cms.InputTag(jLabelAK8),
    pv        = cms.InputTag(pvLabel),
    ### TTRIGGER ###
    triggerResults = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltJetFilter       = cms.InputTag("hltAK8PFJetsTrimR0p1PR0p03Mass50"),
    hltPath            = cms.string("HLT_AK8PFHT700_TrimR0p1PT0p03Mass50_v1"),
    hlt2reco_deltaRmax = cms.double(0.2)
)
process.boostedJetUserDataAK8 = cms.EDProducer(
    'BoostedJetToolboxUserData',
    jetLabel  = cms.InputTag('jetUserDataAK8'),
    topjetLabel = cms.InputTag('patJetsCMSTopTagCHSPacked'),
    vjetLabel = cms.InputTag('selectedPatJetsAK8PFCHSSoftDropPacked'),
    distMax = cms.double(0.8)
)
process.boostedJetUserDataAK8Pruned = cms.EDProducer(
    'BoostedJetToolboxUserData',
    jetLabel  = cms.InputTag('jetUserDataAK8'),
    topjetLabel = cms.InputTag('patJetsCMSTopTagCHSPacked'),
    vjetLabel = cms.InputTag('selectedPatJetsAK8PFCHSPrunedPacked'),
    distMax = cms.double(0.8)
)


process.jetUserDataAK8Puppi = cms.EDProducer(
    'JetUserData',
    jetLabel  = cms.InputTag( 'selectedPatJetsAK8PFPuppi' ),
    pv        = cms.InputTag(pvLabel),
    ### TTRIGGER ###
    triggerResults = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltJetFilter       = cms.InputTag("hltSixCenJet20L1FastJet"),
    hltPath            = cms.string("HLT_QuadJet60_DiJet20_v6"),
    hlt2reco_deltaRmax = cms.double(0.2)
)

process.boostedJetUserDataAK8Puppi = cms.EDProducer(
    'BoostedJetToolboxUserData',
    jetLabel  = cms.InputTag('jetUserDataAK8Puppi'),
    topjetLabel = cms.InputTag('selectedPatJetsAK8PFPuppiSoftDropPacked'),
    vjetLabel = cms.InputTag('selectedPatJetsAK8PFPuppiSoftDropPacked'),
    distMax = cms.double(0.8)
)

process.boostedJetUserDataAK8PuppiPruned = cms.EDProducer(
    'BoostedJetToolboxUserData',
    jetLabel  = cms.InputTag('jetUserDataAK8Puppi'),
    topjetLabel = cms.InputTag('selectedPatJetsAK8PFPuppiPrunedPacked'),
    vjetLabel = cms.InputTag('selectedPatJetsAK8PFPuppiPrunedPacked'),
    distMax = cms.double(0.8)
)

process.jetUserDataAK8SK = cms.EDProducer(
    'JetUserData',
    jetLabel  = cms.InputTag( 'selectedPatJetsAK8PFSK' ),
    pv        = cms.InputTag(pvLabel),
    ### TTRIGGER ###
    triggerResults = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltJetFilter       = cms.InputTag("hltSixCenJet20L1FastJet"),
    hltPath            = cms.string("HLT_QuadJet60_DiJet20_v6"),
    hlt2reco_deltaRmax = cms.double(0.2)
)

process.boostedJetUserDataAK8SK = cms.EDProducer(
    'BoostedJetToolboxUserData',
    jetLabel  = cms.InputTag('jetUserDataAK8SK'),
    topjetLabel = cms.InputTag('selectedPatJetsAK8PFSKSoftDropPacked'),
    vjetLabel = cms.InputTag('selectedPatJetsAK8PFSKSoftDropPacked'),
    distMax = cms.double(0.8)
)

process.boostedJetUserDataAK8SKPruned = cms.EDProducer(
    'BoostedJetToolboxUserData',
    jetLabel  = cms.InputTag('jetUserDataAK8SK'),
    topjetLabel = cms.InputTag('selectedPatJetsAK8PFSKPrunedPacked'),
    vjetLabel = cms.InputTag('selectedPatJetsAK8PFSKPrunedPacked'),
    distMax = cms.double(0.8)
)



process.electronUserData = cms.EDProducer(
    'ElectronUserData',
    eleLabel = cms.InputTag("skimmedPatElectrons"),
    pv        = cms.InputTag(pvLabel),
    conversion        = cms.InputTag(convLabel),
    rho        = cms.InputTag(rhoLabel),
    triggerResults = cms.InputTag(triggerResultsLabel),
    triggerSummary = cms.InputTag(triggerSummaryLabel),
    hltElectronFilter  = cms.InputTag(hltElectronFilterLabel),  ##trigger matching code to be fixed!
    hltPath             = cms.string("HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL"),
    #electronVetoIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V0-miniAOD-standalone-veto"),
    #electronTightIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V0-miniAOD-standalone-tight"),
    )


from PhysicsTools.PatAlgos.tools.pfTools import *
## Adapt primary vertex collection
adaptPVs(process, pvCollection=cms.InputTag('offlineSlimmedPrimaryVertices'))

#################################################


from PhysicsTools.CandAlgos.EventShapeVars_cff import *
process.eventShapePFVars = pfEventShapeVars.clone()
process.eventShapePFVars.src = cms.InputTag(particleFlowLabel)

process.eventShapePFJetVars = pfEventShapeVars.clone()
process.eventShapePFJetVars.src = cms.InputTag("skimmedPatJets")

process.centrality = cms.EDProducer("CentralityUserData",
    src = cms.InputTag("skimmedPatJets")
    )                                    

process.TriggerUserData = cms.EDProducer(
    'TriggerUserData',
    bits = cms.InputTag("TriggerResults","","HLT"),
    prescales = cms.InputTag("patTrigger"),
    storePrescales = cms.untracked.bool(True), 
    hltProcName = cms.untracked.string("HLT"), 
    objects = cms.InputTag("selectedPatTrigger")
    )                                 
#process.TriggerUserDataMYHLT = cms.EDProducer(
#    'TriggerUserData',
#    bits = cms.InputTag("TriggerResults","","MYHLT"),
#    prescales = cms.InputTag("patTrigger"),
#    storePrescales = cms.untracked.bool(False), 
#    hltProcName = cms.untracked.string("MYHLT"), 
#    objects = cms.InputTag("selectedPatTrigger")
#    )                                 

### Including ntuplizer 
process.load("RUNA.RUNtuples.RUNtuples_cff")
from RUNA.RUNtuples.RUNtuples_cff import basic, jetVars, jetAK8Vars, jetToolboxAK8Vars, jetToolboxAK8PuppiVars, jetToolboxAK8SKVars
process.subjetKeysAK8.jetLabel = cms.InputTag("selectedPatJetsAK8PFCHSSoftDropPacked", "SubJets")
process.subjetsAK8.src = cms.InputTag("selectedPatJetsAK8PFCHSSoftDropPacked", "SubJets")
process.subjetsCmsTopTag.src = cms.InputTag("patJetsCMSTopTagCHSPacked", "SubJets")
process.subjetsCmsTopTagKeys.jetLabel = cms.InputTag("patJetsCMSTopTagCHSPacked", "SubJets")
process.jetsAK8.src = 'boostedJetUserDataAK8'
process.jetsAK8.variables += jetToolboxAK8Vars

process.subjetsAK8Pruned = process.subjetsAK8.clone( prefix = 'subjetAK8Pruned', src = cms.InputTag('selectedPatJetsAK8PFCHSPrunedPacked', "SubJets") )
process.edmNtuplesOut.outputCommands+=('keep *_subjetsAK8Pruned_*_*',)

### Puppi
process.jetsAK8Puppi = copy.deepcopy(basic)
process.jetsAK8Puppi.variables += jetVars
process.jetsAK8Puppi.variables += jetToolboxAK8PuppiVars 
process.jetsAK8Puppi.prefix = 'jetAK8Puppi'
process.jetsAK8Puppi.src = cms.InputTag( 'boostedJetUserDataAK8Puppi' )
process.subjetsAK8Puppi = process.subjetsAK8.clone( prefix = 'subjetAK8Puppi', src = cms.InputTag('selectedPatJetsAK8PFPuppiSoftDropPacked', "SubJets") )
process.subjetsAK8PuppiPruned = process.subjetsAK8.clone( prefix = 'subjetAK8PuppiPruned', src = cms.InputTag('selectedPatJetsAK8PFPuppiPrunedPacked', "SubJets") )
process.jetKeysAK8Puppi = process.jetKeysAK8.clone( jetLabel = 'jetUserDataAK8Puppi' )
process.edmNtuplesOut.outputCommands+=('keep *_jetsAK8Puppi_*_*',)
process.edmNtuplesOut.outputCommands+=('keep *_jetKeysAK8Puppi_*_*',)
process.edmNtuplesOut.outputCommands+=('keep *_subjetsAK8Puppi_*_*',)
process.edmNtuplesOut.outputCommands+=('keep *_subjetsAK8PuppiPruned_*_*',)

### SK
process.jetsAK8SK = copy.deepcopy(basic)
process.jetsAK8SK.variables += jetVars
process.jetsAK8SK.variables += jetToolboxAK8SKVars 
process.jetsAK8SK.prefix = 'jetAK8SK'
process.jetsAK8SK.src = cms.InputTag( 'boostedJetUserDataAK8SK' )
process.subjetsAK8SK = process.subjetsAK8.clone( prefix = 'subjetAK8SK', src = cms.InputTag('selectedPatJetsAK8PFSKSoftDropPacked', "SubJets") )
process.subjetsAK8SKPruned = process.subjetsAK8.clone( prefix = 'subjetAK8SKPruned', src = cms.InputTag('selectedPatJetsAK8PFSKPrunedPacked', "SubJets") )
process.jetKeysAK8SK = process.jetKeysAK8.clone( jetLabel = 'jetUserDataAK8SK' )
process.edmNtuplesOut.outputCommands+=('keep *_jetsAK8SK_*_*',)
process.edmNtuplesOut.outputCommands+=('keep *_jetKeysAK8SK_*_*',)
process.edmNtuplesOut.outputCommands+=('keep *_subjetsAK8SK_*_*',)
process.edmNtuplesOut.outputCommands+=('keep *_subjetsAK8SKPruned_*_*',)



process.options.allowUnscheduled = cms.untracked.bool(True)


### keep info from LHEProducts if they are stored in PatTuples
if(options.LHE):
  process.LHEUserData = cms.EDProducer("LHEUserData",
  lheLabel = cms.InputTag(options.lheLabel)
  )
  #process.analysisPath+=process.LHEUserData
  process.edmNtuplesOut.outputCommands+=('keep *_*LHE*_*_*',)
  process.edmNtuplesOut.outputCommands+=('keep LHEEventProduct_*_*_*',)
### end LHE products     

process.edmNtuplesOut.outputCommands+=('keep *_generator_*_*',)
process.edmNtuplesOut.fileName=options.outputLabel

if ( options.isData ): process.edmNtuplesOut.outputCommands+=('drop *_*gen*_*_*',)

#process.edmNtuplesOut.SelectEvents = cms.untracked.PSet(
#    SelectEvents = cms.vstring('filterPath')
#    )


#process.fullPath = cms.Schedule(
#    process.analysisPath
#    )

process.endPath = cms.EndPath(process.edmNtuplesOut)


#open('B2GEntupleFileDump.py','w').write(process.dumpPython())
