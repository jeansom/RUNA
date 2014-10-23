import FWCore.ParameterSet.Config as cms

substructure = cms.EDProducer( "CandViewNtpProducer", 
    src = cms.InputTag("patJetsAK8PFCHS"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("AK8jets"),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("Tau1"),
    quantity = cms.untracked.string("userFloat('NjetinessAK8:tau1')")
    ),
    cms.PSet(
    tag = cms.untracked.string("Tau2"),
    quantity = cms.untracked.string("userFloat('NjetinessAK8:tau2')")
    ),
    cms.PSet(
    tag = cms.untracked.string("Tau3"),
    quantity = cms.untracked.string("userFloat('NjetinessAK8:tau3')")
    ),
    cms.PSet(
    tag = cms.untracked.string("Tau4"),
    quantity = cms.untracked.string("userFloat('NjetinessAK8:tau4')")
    ),
    cms.PSet(
    tag = cms.untracked.string("Tau5"),
    quantity = cms.untracked.string("userFloat('NjetinessAK8:tau5')")
    ),
    cms.PSet(
    tag = cms.untracked.string("QjetsVolatility"),
    quantity = cms.untracked.string("userFloat('QJetsAdderAK8:QjetsVolatility')")
    ), 
    cms.PSet(
    tag = cms.untracked.string("PrunedMass"),
    quantity = cms.untracked.string("userFloat('ak8PFJetsCHSPrunedLinks')")
    ), 
    cms.PSet(
    tag = cms.untracked.string("TrimmedMass"),
    quantity = cms.untracked.string("userFloat('ak8PFJetsCHSTrimmedLinks')")
    ), 
    cms.PSet(
    tag = cms.untracked.string("FilteredMass"),
    quantity = cms.untracked.string("userFloat('ak8PFJetsCHSFilteredLinks')")
    ), 
    cms.PSet(
    tag = cms.untracked.string("CmsTopTag"),
    quantity = cms.untracked.string("userFloat('cmsTopTagPFJetsCHSLinksAK8')")
    ), 
  )  
 )
