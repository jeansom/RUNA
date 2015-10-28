###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing('python')

options.register('outFilename',
    'bTaggingEfficiency.root',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    'output file name'
)
options.register('reportEvery',
    1000,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    'Report every N events (default is N=1000)'
)
options.register('wantSummary',
    False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Print out trigger and timing summary"
)
## 'maxEvents' is already registered by the Framework, changing default value
options.setDefault('maxEvents', -1)

options.parseArguments()

import FWCore.ParameterSet.Config as cms

process = cms.Process('USER')

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(options.wantSummary) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
    'file://eos/uscms/store/user/morris17/Sig_500SbtoWSt_100RPVSttojb_RUNA_v741p1/RunIISpring15DR74_MiniAOD/150616_165451/*/*.root'
    )
)

process.TFileService = cms.Service('TFileService',
   fileName = cms.string(options.outFilename)
)

process.bTaggingEffAnalyzerAK8PF = cms.EDAnalyzer('BTaggingEffAnalyzer',
    JetsTag            = cms.InputTag('slimmedJets'),
    DiscriminatorTag   = cms.string('combinedSecondaryVertexBJetTags'),
    DiscriminatorValue = cms.double(0.89),
    PtNBins            = cms.int32(100),
    PtMin              = cms.double(0.),
    PtMax              = cms.double(1000.),
    EtaNBins           = cms.int32(60),
    EtaMin             = cms.double(-3.),
    EtaMax             = cms.double(3.)
)

process.p = cms.Path(process.bTaggingEffAnalyzerAK8PF)
