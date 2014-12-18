import FWCore.ParameterSet.Config as cms
import copy

leptonssize = cms.untracked.int32(5)
jetssize = cms.untracked.int32(20)

DMTreesDumper = cms.EDAnalyzer(
    'DMTreeMaker',
    physicsObjects = cms.VPSet(
        cms.PSet(
            label = cms.string("electrons"),
            maxInstances = leptonssize,
            variablesF = cms.VInputTag(
                cms.InputTag("electrons","elE"),
                cms.InputTag("electrons","elPt"),
                cms.InputTag("electrons","elMass"),
                cms.InputTag("electrons","elEta"),
                cms.InputTag("electrons","elPhi"),
                cms.InputTag("electrons","elCharge"),
                cms.InputTag("electrons","elD0"),
                cms.InputTag("electrons","elDz"),
                cms.InputTag("electrons","elEta"),
                cms.InputTag("electrons","elHoE"),
                cms.InputTag("electrons","elIso03"),
                cms.InputTag("electrons","elY"),
                cms.InputTag("electrons","eldEtaIn"),
                cms.InputTag("electrons","eldPhiIn"),
                cms.InputTag("electrons","elexpectedMissInHits"),
                cms.InputTag("electrons","elfull5x5siee"),
                cms.InputTag("electrons","elooEmooP"),
                cms.InputTag("electrons","elpssConVeto"),

                                       ),
            variablesI = cms.VInputTag(),
            singleI = cms.VInputTag(),
            singleF = cms.VInputTag(),
            ),
        cms.PSet(
            label = cms.string("muons"),
            maxInstances = leptonssize,
            variablesF = cms.VInputTag(
                cms.InputTag("muons","muE"),
                cms.InputTag("muons","muPt"),
                cms.InputTag("muons","muMass"),
                cms.InputTag("muons","muEta"),
                cms.InputTag("muons","muPhi"),
                cms.InputTag("muons","muCharge"),
                cms.InputTag("muons","muIsLooseMuon"),
                cms.InputTag("muons","muIsSoftMuon"),
                cms.InputTag("muons","muIsTightMuon"),
                cms.InputTag("muons","muD0"),
                cms.InputTag("muons","muD0err"),
                cms.InputTag("muons","muDz"),
                cms.InputTag("muons","muDzerr"),
                cms.InputTag("muons","muGenMuonCharge"),
                cms.InputTag("muons","muGenMuonEta"),
                cms.InputTag("muons","muGenMuonPt"),
                cms.InputTag("muons","muGenMuonE"),
                cms.InputTag("muons","muGenMuonPhi"),
                cms.InputTag("muons","muGenMuonY"),
                cms.InputTag("muons","muGlbTrkNormChi2"),
                cms.InputTag("muons","muHLTmuonDeltaR"),
                cms.InputTag("muons","muHLTmuonE"),
                cms.InputTag("muons","muHLTmuonEta"),
                cms.InputTag("muons","muHLTmuonPt"),
                cms.InputTag("muons","muHLTmuonPhi"),
                cms.InputTag("muons","muInTrkNormChi2"),
                cms.InputTag("muons","muIsGlobalMuon"),
                cms.InputTag("muons","muIsPFMuon"),
                cms.InputTag("muons","muIsTrackerMuon"),
                cms.InputTag("muons","muIso03"),
                cms.InputTag("muons","muNumberMatchedStations"),
                cms.InputTag("muons","muNumberOfPixelLayers"),
                cms.InputTag("muons","muNumberOfValidTrackerHits"),
                cms.InputTag("muons","muNumberTrackerLayers"),
                cms.InputTag("muons","muNumberValidMuonHits"),
                cms.InputTag("muons","muNumberValidPixelHits"),
                cms.InputTag("muons","muSumChargedHadronPt"),
                cms.InputTag("muons","muSumNeutralHadronPt"),
                cms.InputTag("muons","muSumPUPt"),
                cms.InputTag("muons","muSumPhotonPt"),
                cms.InputTag("muons","muY"),

),
            variablesI = cms.VInputTag(),
            singleI = cms.VInputTag(),
            singleF = cms.VInputTag(),
            ),
        cms.PSet(
            label = cms.string("jets"),
            maxInstances = jetssize,
            variablesF = cms.VInputTag(
                cms.InputTag("jets","jetE"),
                cms.InputTag("jets","jetPt"),
                cms.InputTag("jets","jetMass"),
                cms.InputTag("jets","jetEta"),
                cms.InputTag("jets","jetPhi"),
                cms.InputTag("jets","jetPartonFlavour"),
                cms.InputTag("jets","jetPhi"),
                cms.InputTag("jets","jetCSV"),
                cms.InputTag("jets","jetCSVV1"),
                cms.InputTag("jets","jetCharge"),
                cms.InputTag("jets","jetChargeMuEnergy"),
                cms.InputTag("jets","jetChargedHadronMultiplicity"),
                cms.InputTag("jets","jetElectronEnergy"),
                cms.InputTag("jets","jetGenJetCharge"),
                cms.InputTag("jets","jetGenJetE"),
                cms.InputTag("jets","jetGenJetEta"),
                cms.InputTag("jets","jetGenJetPhi"),
                cms.InputTag("jets","jetGenJetPt"),
                cms.InputTag("jets","jetGenJetY"),
                cms.InputTag("jets","jetGenPartonCharge"),
                cms.InputTag("jets","jetGenPartonE"),
                cms.InputTag("jets","jetGenPartonEta"),
                cms.InputTag("jets","jetGenPartonPhi"),
                cms.InputTag("jets","jetGenPartonPt"),
                cms.InputTag("jets","jetGenPartonY"),
                cms.InputTag("jets","jetHFEMEnergy"),
                cms.InputTag("jets","jetHFEMMultiplicity"),
                cms.InputTag("jets","jetHFHadronEnergy"),
                cms.InputTag("jets","jetHFHadronMultiplicity"),
                cms.InputTag("jets","jetHLTjetDeltaR"),
                cms.InputTag("jets","jetHLTjetE"),
                cms.InputTag("jets","jetHLTjetEta"),
                cms.InputTag("jets","jetHLTjetPt"),
                cms.InputTag("jets","jetHLTjetPhi"),
                cms.InputTag("jets","jetHadronFlavour"),
                cms.InputTag("jets","jetIsCSVL"),
                cms.InputTag("jets","jetIsCSVM"),
                cms.InputTag("jets","jetIsCSVT"),
                cms.InputTag("jets","jetSmearedE"),
                cms.InputTag("jets","jetSmearedPt"),
                cms.InputTag("jets","jetSmearedPEta"),
                cms.InputTag("jets","jetSmearedPhi"),
                cms.InputTag("jets","jetY"),
                cms.InputTag("jets","jetelectronMultiplicity"),
                cms.InputTag("jets","jetmuonMultiplicity"),
                cms.InputTag("jets","jetneutralHadronMultiplicity"),
                cms.InputTag("jets","jetneutralMultiplicity"),
                cms.InputTag("jets","jetphotonMultiplicity"),
                                       ),
            variablesI = cms.VInputTag(),
            singleI = cms.VInputTag(),
            singleF = cms.VInputTag(),
            ),

        )
    )

