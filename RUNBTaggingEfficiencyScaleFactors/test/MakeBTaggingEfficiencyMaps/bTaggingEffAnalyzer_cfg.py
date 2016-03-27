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

## Set isMiniAOD = 0 if running on a MiniAOD, set isMiniAOD = 1 if running on a Ntuple
isMiniAOD = 0;

process = cms.Process('USER')

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(options.wantSummary) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
    #'file:///eos/uscms/store/user/dgsheffi/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09/151116_211916/0000/RUNtuple_549.root',
     'file:///eos/uscms/store/user/morris17/RunIISpring15DR74_MiniAOD/150616_165451/0000/Sig_500SbtoWSt_100RPVSttojb_RUNA_v741p1_MiniAOD_Asympt25ns_992.root',
    )
)

process.TFileService = cms.Service('TFileService',
   fileName = cms.string(options.outFilename)
)
if( isMiniAOD == 0 ):
    process.bTaggingEffAnalyzerAK8PF = cms.EDAnalyzer('BTaggingEffAnalyzer',
        JetsTag            = cms.InputTag('slimmedJets'),
        JetPtTag           = cms.InputTag(''),
        JetEtaTag          = cms.InputTag(''),
        JetPartonFlavorTag = cms.InputTag(''),
        JetCSVTag          = cms.InputTag(''),                              
        DiscriminatorTag   = cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
        DiscriminatorValue = cms.double(0.8),
        PtNBins            = cms.int32(100),
        PtMin              = cms.double(0.),
        PtMax              = cms.double(1000.),
        EtaNBins           = cms.int32(60),
        EtaMin             = cms.double(-3.),
        EtaMax             = cms.double(3.),
        isMiniAOD          = cms.int32(isMiniAOD)
        )
if( isMiniAOD == 1 ):
    process.bTaggingEffAnalyzerAK8PF = cms.EDAnalyzer('BTaggingEffAnalyzer',
        JetsTag            = cms.InputTag(''),
        JetPtTag           = cms.InputTag('jetsAK4:jetAK4Pt'),
        JetEtaTag          = cms.InputTag('jetsAK4:jetAK4Eta'),
        JetPartonFlavorTag = cms.InputTag('jetsAK4:jetAK4PartonFlavour'),
        JetCSVTag          = cms.InputTag('jetsAK4:jetAK4CSV'),            
        DiscriminatorTag   = cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
        DiscriminatorValue = cms.double(0.89),
        PtNBins            = cms.int32(100),
        PtMin              = cms.double(0.),
        PtMax              = cms.double(1000.),
        EtaNBins           = cms.int32(60),
        EtaMin             = cms.double(-3.),
        EtaMax             = cms.double(3.),
        isMiniAOD          = cms.int32(isMiniAOD)
        )
process.p = cms.Path(process.bTaggingEffAnalyzerAK8PF)
