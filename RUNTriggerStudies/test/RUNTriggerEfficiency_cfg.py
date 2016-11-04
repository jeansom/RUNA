import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('PROC', 
		'JetHT_Run2015C',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"name"
		)
options.register('version', 
		'Full',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"Version of the analysis to run. (Full, Resolved, Boosted)"
		)

options.parseArguments()

process = cms.Process("TriggerEfficiency")
process.load("FWCore.MessageService.MessageLogger_cfi")
NAME = options.PROC

process.source = cms.Source("PoolSource",
		fileNames = cms.untracked.vstring(
			'/store/group/phys_b2g/B2GAnaFW_80X_V2p1/JetHT/Run2016C/JetHT/Run2016C-PromptReco-v2_B2GAnaFW_80X_V2p1/161013_132254/0000/B2GEDMNtuple_10.root',
			)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32 (options.maxEvents) )


if 'MET' in NAME: basedline = 'HLT_PFMET170_HBHECleaned'
elif 'SingleMu' in NAME: basedline =  'HLT_Mu50' #'HLT_IsoMu17_eta2p1_v'
#elif 'SingleElectron' in NAME: basedline =  'HLT_Mu50' #'HLT_IsoMu17_eta2p1_v'
else: basedline = 'HLT_PFHT475'

PFHTTrigger = ( 'HLT_PFHT900' if 'RUN2016H' in NAME else 'HLT_PFHT800' )


####################
#### Resolved 
process.ResolvedTriggerEfficiency = cms.EDAnalyzer('RUNResolvedTriggerEfficiency',
		#cutAK4jetPt	= cms.double( 50.0 ), 	# default 50.
		#cutAK4jet4Pt	= cms.double( 80.0 ), 	# default 80.
		#cutAK4HT	= cms.double( 800.0 ), 	# default 800.
		baseTrigger		= cms.string(basedline),
		triggerPass		= cms.vstring( [  PFHTTrigger, 'HLT_PFHT750_4Jet' ] ),

)
process.ResolvedTriggerEfficiencyPFHT7504Jet = process.ResolvedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ 'HLT_PFHT750_4JetPt' ] ) )
process.ResolvedTriggerEfficiencyPFHT800 = process.ResolvedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ PFHTTrigger ] ) )
############################################################



####################
#### Boosted
process.BoostedTriggerEfficiency = cms.EDAnalyzer('RUNBoostedTriggerEfficiency',
		#cutAK8jetPt	= cms.double( 150.0 ),		# default 150.
		#cutAK8HT	= cms.double( 900.0 ),		# default 900.
		#cutAK8jet1Pt	= cms.double( 500.0 ),		# default 500.
		#cutAK8jet2Pt	= cms.double( 450.0 ),		# default 450.
		#cutAK8jet1Mass	= cms.double( 60.0 ),		# default 60.
		baseTrigger		= cms.string(basedline),
		triggerPass		= cms.vstring( [ PFHTTrigger, 'HLT_AK8PFHT700_TrimR0p1PT0p03Mass50' ] ),
)

process.BoostedTriggerEfficiencyPFHT800 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ PFHTTrigger ] ) )

process.BoostedTriggerEfficiencyAK8PFHT700TrimMass50 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ 'HLT_AK8PFHT700_TrimR0p1PT0p03Mass50' ] ) )

process.BoostedTriggerEfficiencyAK8PFPt360TrimMass30 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ 'HLT_AK8PFJet360_TrimMass30' ] ) )

process.BoostedTriggerEfficiencyAK8PFHT7504Jet = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ 'HLT_PFHT750_4JetPt'] ) )

process.BoostedTriggerEfficiencyAK8DiPFJet280220TrimMass30Btagp20 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ 'HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20'] ) )

process.BoostedTriggerEfficiencyAK8DiPFJet280220TrimMass30 = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ 'HLT_AK8DiPFJet280_200_TrimMass30'] ) )

process.BoostedTriggerEfficiencySeveralTriggers = process.BoostedTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ PFHTTrigger, 
			'HLT_AK8PFHT700_TrimR0p1PT0p03Mass50',
			'HLT_AK8PFJet360_TrimMass30',
			'HLT_PFHT750_4JetPt',
			'HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20',
			'HLT_AK8DiPFJet280_200_TrimMass30'] ) )

process.BoostedTriggerEfficiencyPuppi = process.BoostedTriggerEfficiency.clone(
		jetPt = cms.InputTag("jetsAK8Puppi:jetAK8PuppiPt"),
		jetEta = cms.InputTag("jetsAK8Puppi:jetAK8PuppiEta"),
		jetPhi = cms.InputTag("jetsAK8Puppi:jetAK8PuppiPhi"),
		jetE = cms.InputTag("jetsAK8Puppi:jetAK8PuppiE"),
		jetTrimmedMass = cms.InputTag("jetsAK8Puppi:jetAK8PuppitrimmedMass"),
		jetPrunedMass = cms.InputTag("jetsAK8Puppi:jetAK8PuppiprunedMass"),
		jetSoftDropMass = cms.InputTag("jetsAK8Puppi:jetAK8PuppisoftDropMass"),
		jetCSVv2 = cms.InputTag("jetsAK8Puppi:jetAK8PuppiCSVv2"),
		jecFactor = cms.InputTag("jetsAK8Puppi:jetAK8PuppijecFactor0"),
		neutralHadronEnergyFrac = cms.InputTag("jetsAK8Puppi:jetAK8PuppineutralHadronEnergyFrac"),
		neutralEmEnergyFrac = cms.InputTag("jetsAK8Puppi:jetAK8PuppineutralEmEnergyFrac"),
		chargedEmEnergyFrac = cms.InputTag("jetsAK8Puppi:jetAK8PuppichargedEmEnergyFrac"),
		muonEnergy = cms.InputTag("jetsAK8Puppi:jetAK8PuppiMuonEnergy"),
		chargedHadronEnergyFrac = cms.InputTag("jetsAK8Puppi:jetAK8PuppichargedHadronEnergyFrac"),
		neutralMultiplicity = cms.InputTag("jetsAK8Puppi:jetAK8PuppineutralMultiplicity"),
		chargedMultiplicity = cms.InputTag("jetsAK8Puppi:jetAK8PuppichargedMultiplicity"),
		)

process.BoostedTriggerEfficiencyPuppiPFHT800 = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( [ PFHTTrigger ] ) )

process.BoostedTriggerEfficiencyPuppiAK8PFHT700TrimMass50 = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( [ 'HLT_AK8PFHT700_TrimR0p1PT0p03Mass50' ] ) )

process.BoostedTriggerEfficiencyPuppiAK8PFPt360TrimMass30 = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( [ 'HLT_AK8PFJet360_TrimMass30' ] ) )

process.BoostedTriggerEfficiencyPuppiAK8PFHT7504Jet = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( [ 'HLT_PFHT750_4JetPt'] ) )

process.BoostedTriggerEfficiencyPuppiAK8DiPFJet280220TrimMass30Btagp20 = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( [ 'HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20'] ) )

process.BoostedTriggerEfficiencyPuppiAK8DiPFJet280220TrimMass30 = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( [ 'HLT_AK8DiPFJet280_200_TrimMass30'] ) )

process.BoostedTriggerEfficiencyPuppiSeveralTriggers = process.BoostedTriggerEfficiencyPuppi.clone( 
		triggerPass = cms.vstring( [ PFHTTrigger, 
			'HLT_AK8PFHT700_TrimR0p1PT0p03Mass50',
			'HLT_AK8PFJet360_TrimMass30',
			'HLT_PFHT750_4JetPt',
			'HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20',
			'HLT_AK8DiPFJet280_200_TrimMass30'] ) )
############################################################



####################
#### Dijet 
process.DijetTriggerEfficiency = cms.EDAnalyzer('RUNDijetTriggerEfficiency', 	##### default puppi jets
		#cutAK8jetPt	= cms.double( 150.0 ),		# default 150.
		#cutAK8jet1Pt	= cms.double( 500.0 ),		# default 500.
		#cutAK8jet1Mass	= cms.double( 60.0 ),		# default 60.
		baseTrigger		= cms.string(basedline),
		triggerPass		= cms.vstring( [ PFHTTrigger, 'HLT_AK8PFHT700_TrimR0p1PT0p03Mass50', 'HLT_AK8PFJet360_TrimMass30' ] ),
)

process.DijetTriggerEfficiencyPFHT800 = process.DijetTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ PFHTTrigger ] ) )

process.DijetTriggerEfficiencyAK8PFHT700TrimMass50 = process.DijetTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ 'HLT_AK8PFHT700_TrimR0p1PT0p03Mass50' ] ) )

process.DijetTriggerEfficiencyAK8PFPt360TrimMass30 = process.DijetTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ 'HLT_AK8PFJet360_TrimMass30' ] ) )

process.DijetTriggerEfficiencyAK8PFHT7504Jet = process.DijetTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ 'HLT_PFHT750_4JetPt'] ) )

process.DijetTriggerEfficiencyAK8DiPFJet280220TrimMass30Btagp20 = process.DijetTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ 'HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20'] ) )

process.DijetTriggerEfficiencyAK8DiPFJet280220TrimMass30 = process.DijetTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ 'HLT_AK8DiPFJet280_200_TrimMass30'] ) )

process.DijetTriggerEfficiencySeveralTriggers = process.DijetTriggerEfficiency.clone( 
		triggerPass = cms.vstring( [ PFHTTrigger, 
			'HLT_AK8PFHT700_TrimR0p1PT0p03Mass50',
			'HLT_AK8PFJet360_TrimMass30',
			'HLT_PFHT750_4JetPt',
			'HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20',
			'HLT_AK8DiPFJet280_200_TrimMass30'] ) )
############################################################


process.p = cms.Path()
if 'Resolved' in options.version:
	outputNAME = 'Resolved'
	process.p += process.ResolvedTriggerEfficiency
	process.p += process.ResolvedTriggerEfficiencyPFHT7504Jet
	process.p += process.ResolvedTriggerEfficiencyPFHT800

elif 'Boosted' in options.version:
	outputNAME = 'Boosted'
	process.p += process.BoostedTriggerEfficiency
	process.p += process.BoostedTriggerEfficiencyPFHT800
	process.p += process.BoostedTriggerEfficiencyAK8PFHT700TrimMass50
	process.p += process.BoostedTriggerEfficiencyAK8PFPt360TrimMass30
	process.p += process.BoostedTriggerEfficiencyAK8PFHT7504Jet
	process.p += process.BoostedTriggerEfficiencyAK8DiPFJet280220TrimMass30Btagp20
	process.p += process.BoostedTriggerEfficiencyAK8DiPFJet280220TrimMass30
	process.p += process.BoostedTriggerEfficiencySeveralTriggers
	process.p += process.BoostedTriggerEfficiencyPuppi
	process.p += process.BoostedTriggerEfficiencyPuppiPFHT800
	process.p += process.BoostedTriggerEfficiencyPuppiAK8PFHT700TrimMass50
	process.p += process.BoostedTriggerEfficiencyPuppiAK8PFPt360TrimMass30
	process.p += process.BoostedTriggerEfficiencyPuppiAK8PFHT7504Jet
	process.p += process.BoostedTriggerEfficiencyPuppiAK8DiPFJet280220TrimMass30Btagp20
	process.p += process.BoostedTriggerEfficiencyPuppiAK8DiPFJet280220TrimMass30
	process.p += process.BoostedTriggerEfficiencyPuppiSeveralTriggers

elif 'Dijet' in options.version:
	outputNAME = 'Dijet'
	process.p += process.DijetTriggerEfficiency
	process.p += process.DijetTriggerEfficiencyPFHT800
	process.p += process.DijetTriggerEfficiencyAK8PFHT700TrimMass50
	process.p += process.DijetTriggerEfficiencyAK8PFPt360TrimMass30
	process.p += process.DijetTriggerEfficiencyAK8PFHT7504Jet
	process.p += process.DijetTriggerEfficiencyAK8DiPFJet280220TrimMass30Btagp20
	process.p += process.DijetTriggerEfficiencyAK8DiPFJet280220TrimMass30
	process.p += process.DijetTriggerEfficiencySeveralTriggers
else: 
	outputNAME = 'Full'
	process.p += process.ResolvedTriggerEfficiency
	process.p += process.ResolvedTriggerEfficiencyPFHT7504Jet
	process.p += process.ResolvedTriggerEfficiencyPFHT800
	process.p += process.BoostedTriggerEfficiency
	process.p += process.BoostedTriggerEfficiencyPFHT800
	process.p += process.BoostedTriggerEfficiencyAK8PFHT700TrimMass50
	process.p += process.BoostedTriggerEfficiencyAK8PFPt360TrimMass30
	process.p += process.BoostedTriggerEfficiencyAK8PFHT7504Jet
	process.p += process.BoostedTriggerEfficiencyAK8DiPFJet280220TrimMass30Btagp20
	process.p += process.BoostedTriggerEfficiencyAK8DiPFJet280220TrimMass30
	process.p += process.BoostedTriggerEfficiencySeveralTriggers
	process.p += process.BoostedTriggerEfficiencyPuppi
	process.p += process.BoostedTriggerEfficiencyPuppiPFHT800
	process.p += process.BoostedTriggerEfficiencyPuppiAK8PFHT700TrimMass50
	process.p += process.BoostedTriggerEfficiencyPuppiAK8PFPt360TrimMass30
	process.p += process.BoostedTriggerEfficiencyPuppiAK8PFHT7504Jet
	process.p += process.BoostedTriggerEfficiencyPuppiAK8DiPFJet280220TrimMass30Btagp20
	process.p += process.BoostedTriggerEfficiencyPuppiAK8DiPFJet280220TrimMass30
	process.p += process.BoostedTriggerEfficiencyPuppiSeveralTriggers
	process.p += process.DijetTriggerEfficiency
	process.p += process.DijetTriggerEfficiencyPFHT800
	process.p += process.DijetTriggerEfficiencyAK8PFHT700TrimMass50
	process.p += process.DijetTriggerEfficiencyAK8PFPt360TrimMass30
	process.p += process.DijetTriggerEfficiencyAK8PFHT7504Jet
	process.p += process.DijetTriggerEfficiencyAK8DiPFJet280220TrimMass30Btagp20
	process.p += process.DijetTriggerEfficiencyAK8DiPFJet280220TrimMass30
	process.p += process.DijetTriggerEfficiencySeveralTriggers

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUN'+outputNAME+'TriggerEfficiency_'+NAME+'.root' ) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
