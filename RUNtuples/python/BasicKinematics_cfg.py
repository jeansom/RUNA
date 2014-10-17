import FWCore.ParameterSet.Config as cms

kinematics = cms.EDProducer( "CandViewNtpProducer", 
    src = cms.InputTag("slimmedJets"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("AK4jets"),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("Mass"),
    quantity = cms.untracked.string("mass")
    ),
    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("Eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ), 
    cms.PSet(
    tag = cms.untracked.string("Energy"),
    quantity = cms.untracked.string("energy")
    ), 
    cms.PSet(
    tag = cms.untracked.string("Px"),
    quantity = cms.untracked.string("px")
    ), 
    cms.PSet(
    tag = cms.untracked.string("Py"),
    quantity = cms.untracked.string("py")
    ), 
    cms.PSet(
    tag = cms.untracked.string("Pz"),
    quantity = cms.untracked.string("pz")
    ), 
    cms.PSet(
    tag = cms.untracked.string("Charge"),
    quantity = cms.untracked.string("charge")
    ), 
  )  
 )
