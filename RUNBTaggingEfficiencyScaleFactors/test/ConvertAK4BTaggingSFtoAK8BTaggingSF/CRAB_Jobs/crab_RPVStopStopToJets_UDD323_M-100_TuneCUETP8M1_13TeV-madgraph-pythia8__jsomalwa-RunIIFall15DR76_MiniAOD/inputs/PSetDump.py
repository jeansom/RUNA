import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://cmseos.fnal.gov//store/user/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15DR76_MiniAOD_Asympt25ns/160202_114630/0000/RPVStopStopToJets_UDD323_M-100-madgraph_MiniAOD_Asympt25ns_986.root')
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

process.demo = cms.EDAnalyzer("ConvertBtaggingSF",
    ak8jets = cms.InputTag("slimmedJetsAK8"),
    electronPt = cms.InputTag(""),
    electrons = cms.InputTag("slimmedElectrons"),
    isMiniAOD = cms.int32(0),
    jetAK8Area = cms.InputTag(""),
    jetAK8CSV = cms.InputTag(""),
    jetAK8CSVV1 = cms.InputTag(""),
    jetAK8E = cms.InputTag(""),
    jetAK8Eta = cms.InputTag(""),
    jetAK8Mass = cms.InputTag(""),
    jetAK8PartonFlavour = cms.InputTag(""),
    jetAK8Phi = cms.InputTag(""),
    jetAK8Pt = cms.InputTag(""),
    jetArea = cms.InputTag(""),
    jetCSV = cms.InputTag(""),
    jetCSVV1 = cms.InputTag(""),
    jetE = cms.InputTag(""),
    jetEta = cms.InputTag(""),
    jetMass = cms.InputTag(""),
    jetPartonFlavour = cms.InputTag(""),
    jetPhi = cms.InputTag(""),
    jetPt = cms.InputTag(""),
    jets = cms.InputTag("slimmedJets"),
    mets = cms.InputTag("slimmedMETs"),
    muonPt = cms.InputTag(""),
    muons = cms.InputTag("slimmedMuons"),
    npv = cms.InputTag(""),
    photons = cms.InputTag("slimmedPhotons"),
    puppijets = cms.InputTag("slimmedJetsPuppi"),
    rho = cms.InputTag("fixedGridRhoFastjetCentralNeutral"),
    taus = cms.InputTag("slimmedTaus"),
    vertices = cms.InputTag("offlineSlimmedPrimaryVertices")
)


process.p = cms.Path(process.demo)


process.MessageLogger = cms.Service("MessageLogger",
    FrameworkJobReport = cms.untracked.PSet(
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            optionalPSet = cms.untracked.bool(True)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        optionalPSet = cms.untracked.bool(True)
    ),
    categories = cms.untracked.vstring('FwkJob', 
        'FwkReport', 
        'FwkSummary', 
        'Root_NoDictionary'),
    cerr = cms.untracked.PSet(
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            optionalPSet = cms.untracked.bool(True)
        ),
        FwkReport = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            optionalPSet = cms.untracked.bool(True),
            reportEvery = cms.untracked.int32(1)
        ),
        FwkSummary = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            optionalPSet = cms.untracked.bool(True),
            reportEvery = cms.untracked.int32(1)
        ),
        INFO = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        Root_NoDictionary = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            optionalPSet = cms.untracked.bool(True)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000)
        ),
        noTimeStamps = cms.untracked.bool(False),
        optionalPSet = cms.untracked.bool(True),
        threshold = cms.untracked.string('INFO')
    ),
    cerr_stats = cms.untracked.PSet(
        optionalPSet = cms.untracked.bool(True),
        output = cms.untracked.string('cerr'),
        threshold = cms.untracked.string('WARNING')
    ),
    cout = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    debugModules = cms.untracked.vstring(),
    debugs = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    default = cms.untracked.PSet(

    ),
    destinations = cms.untracked.vstring('warnings', 
        'errors', 
        'infos', 
        'debugs', 
        'cout', 
        'cerr'),
    errors = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    fwkJobReports = cms.untracked.vstring('FrameworkJobReport'),
    infos = cms.untracked.PSet(
        Root_NoDictionary = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            optionalPSet = cms.untracked.bool(True)
        ),
        optionalPSet = cms.untracked.bool(True),
        placeholder = cms.untracked.bool(True)
    ),
    statistics = cms.untracked.vstring('cerr_stats'),
    suppressDebug = cms.untracked.vstring(),
    suppressInfo = cms.untracked.vstring(),
    suppressWarning = cms.untracked.vstring(),
    warnings = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    )
)


process.TFileService = cms.Service("TFileService",
    fileName = cms.string('output_someEvents.root')
)


