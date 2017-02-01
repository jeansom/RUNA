import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

### General Options
options.register('PROC', 
		'RPVStopStopToJets_UDD312_M-120',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"name"
		)
options.register('local', 
		False,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.bool,
		"Run locally or crab"
		)
options.register('version', 
		'Boosted',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"Version of the analysis to run. (Full, Resolved, Boosted)"
		)
options.register('systematics', 
		False,		
		VarParsing.multiplicity.singleton,
		VarParsing.varType.bool,
		"Run systematics, default false."
		)
options.register('jecVersion', 
		'supportFiles/Spring16_25nsV8BCD',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"Version of the analysis to run. (Full, Resolved, Boosted)"
		)
options.register('namePUFile', 
		'supportFiles/PileupData2015D_JSON_latest.root',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"namePUFile"
		)



options.parseArguments()

process = cms.Process("RUNAnalysis")
process.load("FWCore.MessageService.MessageLogger_cfi")
NAME = options.PROC

if options.local:
	process.load(NAME+'_RUNA_cfi')
	#process.load('RPVSt100tojj_13TeV_pythia8_RUNtuples_cfi')
else:
	process.source = cms.Source("PoolSource",
		fileNames = cms.untracked.vstring(
			#'/store/user/grauco/B2GAnaFW/B2GAnaFW_80X_V2p1/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p1/161018_070036/0000/B2GEDMNtuple_1.root',
			#'/store/group/phys_b2g/B2GAnaFW_80X_V2p1/JetHT/Run2016C/JetHT/Run2016C-PromptReco-v2_B2GAnaFW_80X_V2p1/161013_132254/0000/B2GEDMNtuple_10.root',
			#'/store/user/jsomalwa/B2GAnaFW_80X_V2p4/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-Moriond17_MINIAODSIM-0b8c51c13c712fe6e73a79b549018f23_B2GAnaFW_80X_V2p4/161231_184903/0000/B2GEDMNtuple_984.root'
			#'/store/group/phys_b2g/B2GAnaFW_80X_V2p1/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1/161109_110436/0000/B2GEDMNtuple_1.root',
			#'/store/user/jsomalwa/B2GAnaFW_80X_V2p4/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-Moriond17_MINIAODSIM-0b8c51c13c712fe6e73a79b549018f23_B2GAnaFW_80X_V2p4/170104_225312/0000/B2GEDMNtuple_98.root'
			#'/store/user/jsomalwa/B2GAnaFW_80X_V2p4_1/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-Moriond17_MINIAODSIM-0b8c51c13c712fe6e73a79b549018f23_B2GAnaFW_80X_V2p4_1/170107_145208/0000/B2GEDMNtuple_977.root'
			'/store/group/phys_b2g/B2GAnaFW_80X_V2p4/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1_B2GAnaFW_80X_V2p4/161222_110143/0000/B2GEDMNtuple_210.root'
			#'/store/group/phys_b2g/B2GAnaFW_80X_V2p1/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1_B2GAnaFW_80X_V2p1/161018_200839/0000/B2GEDMNtuple_8.root'
			#'/store/user/grauco/B2GAnaFW/B2GAnaFW_80X_V2p1/TT_TuneCUETP8M1_13TeV-powheg-pythia8/B2GAnaFW_80X_V2p1/161021_085128/0003/B2GEDMNtuple_3465.root'
			#'/store/user/evah/B2GAnaFW_80X_V2p4/PhiToTwophi_BBAR_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8/evah/PhiToTwophi_BBAR_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8/evah-Moriond17_MINIAODSIM-28028af67189b3de7224b79195bd0e1d_B2GAnaFW_80X_V2p4/161226_035306/0000/B2GEDMNtuple_72.root'
			#'/store/user/algomez/RPVStopStopToJets_UDD323_M-180_TuneCUETP8M1_13TeV-madgraph-pythia8/algomez-Moriond17_MINIAODSIM-0b8c51c13c712fe6e73a79b549018f23_B2GAnaFW_80X_V2p4/170103_170441/0000/B2GEDMNtuple_982.root'
			#'/store/user/evah/B2GAnaFW_80X_V2p4/RPVStopStopToJets_UDD323_M-300_TuneCUETP8M1_13TeV-madgraph-pythia8/evah/RPVStopStopToJets_UDD323_M-300_TuneCUETP8M1_13TeV-madgraph-pythia8/evah-Moriond17_MINIAODSIM-0b8c51c13c712fe6e73a79b549018f23_B2GAnaFW_80X_V2p4/161228_165235/0000/B2GEDMNtuple_974.root'
	    )
	)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32 (options.maxEvents) )

from RUNA.RUNAnalysis.scaleFactors import scaleFactor

bjsample = True if 'bj' in NAME else False
if 'JetHT' in NAME: 
	SF = 1
	isData=True
	options.systematics = False
else:
	isData=False
	SF = scaleFactor(NAME)


##############################
#####   Resolved analysis

ResolvedTriggers = [  'HLT_PFHT800', 'HLT_PFHT900', 'HLT_PFHT750_4Jet', 'HLT_PFHT800_4Jet50', 'HLT_PFJet450' ]

process.ResolvedAnalysisPlots = cms.EDAnalyzer('RUNResolvedAnalysis',
		cutAK4jetPt 		= cms.double( 50.0 ),	# default 80.0
		#cutAK4HT 		= cms.double( 800.0 ),	# default 800.0
		#cutAK4MassAsym		= cms.double( 0.2 ),	# default 0.2
		cutDelta 		= cms.double( 200 ),	# default 180.0
		cutDeltaEtaDijetSyst	= cms.double( 1.0 ),	# default .75
		triggerPass 		= cms.vstring( ResolvedTriggers ),
		scale 			= cms.double( SF ),
		dataPUFile		= cms.string( options.namePUFile  ),
		jecVersion		= cms.string( options.jecVersion ),
		isData			= cms.bool( isData ),
		LHEcont			= cms.bool( True if 'QCD_Pt' in NAME else True ), ## logic is oposite
		massPairing		= cms.bool( False ),
		mkTree			= cms.bool( True ),
)

#process.ResolvedAnalysisPlotsScouting = process.ResolvedAnalysisPlots.clone( cutAK4jetPt = cms.double( 50.0 ), cutAK4HT = cms.double( 450 ), mkTree = cms.bool( True ) )
process.ResolvedAnalysisPlotsMassPairing = process.ResolvedAnalysisPlots.clone( massPairing = cms.bool( True ), mkTree = cms.bool( False ) )

process.ResolvedAnalysisPlotsJESUp = process.ResolvedAnalysisPlots.clone( systematics = cms.string( 'JESUp' ), mkTree = cms.bool( False ) )
process.ResolvedAnalysisPlotsJESDown = process.ResolvedAnalysisPlots.clone( systematics = cms.string( 'JESDown' ), mkTree = cms.bool( False ) )
process.ResolvedAnalysisPlotsJERUp = process.ResolvedAnalysisPlots.clone( systematics = cms.string( 'JERUp' ), mkTree = cms.bool( False ) )
process.ResolvedAnalysisPlotsJERDown = process.ResolvedAnalysisPlots.clone( systematics = cms.string( 'JERDown' ), mkTree = cms.bool( False ) )

############################################################


##############################
#####   Boosted analysis
BoostedTriggers =  [ 'HLT_PFHT800', 'HLT_PFHT900', 'HLT_AK8PFHT700_TrimR0p1PT0p03Mass50', 'HLT_AK8PFHT750_TrimMass50', 'HLT_PFJet450' ] 

process.BoostedAnalysisPlots = cms.EDAnalyzer('RUNBoostedAnalysis',
		#cutAK8jetPt 		= cms.double( 150.0 ),	# default 150.0
		#cutAK8HT 		= cms.double( 900.0 ),	# default 900.0
		#cutAK8MassAsym		= cms.double( 0.1 ),	# default 0.1
		#cutTau21 		= cms.double( 0.45 ),	# default 0.45
		#cutDeltaEtaDijet	= cms.double( 1.5 ),	# default 1.5
		triggerPass 		= cms.vstring( BoostedTriggers ),
		dataPUFile		= cms.string( options.namePUFile  ),
		jecVersion		= cms.string( options.jecVersion ),
		isData			= cms.bool( isData ),
		LHEcont			= cms.bool( True if 'QCD_Pt' in NAME else True ), ## logic is oposite
		scale 			= cms.double( SF ),
		mkTree			= cms.bool( True ),
)

#process.BoostedAnalysisPlotsSortInMass = process.BoostedAnalysisPlots.clone( sortInMass = cms.bool( True ), mkTree = cms.bool( False ) )
#process.BoostedAnalysisPlotsSortInTau21 = process.BoostedAnalysisPlots.clone( sortInTau21 = cms.bool( True ), mkTree = cms.bool( False ) )

process.BoostedAnalysisPlotsJESUp = process.BoostedAnalysisPlots.clone( systematics = cms.string( 'JESUp' ), mkTree = cms.bool( False ) )
process.BoostedAnalysisPlotsJESDown = process.BoostedAnalysisPlots.clone( systematics = cms.string( 'JESDown' ), mkTree = cms.bool( False ) )
process.BoostedAnalysisPlotsJERUp = process.BoostedAnalysisPlots.clone( systematics = cms.string( 'JERUp' ), mkTree = cms.bool( False ) )
process.BoostedAnalysisPlotsJERDown = process.BoostedAnalysisPlots.clone( systematics = cms.string( 'JERDown' ), mkTree = cms.bool( False ) )

process.BoostedAnalysisPlotsPuppi = process.BoostedAnalysisPlots.clone( 
		PUMethod		= cms.string('Puppi'),
		cutDeltaEtaDijet	= cms.double( 1. ),	# default 1.5
		jetPt 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiPt'),
		jetEta			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiEta'),
		jetPhi 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiPhi'),
		jetE 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiE'),
		jetTrimmedMass 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppitrimmedMass'),
		jetPrunedMass 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppisoftDropMass'),
		jetFilteredMass 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppifilteredMass'),
		jetSoftDropMass		= cms.InputTag('jetsAK8Puppi:jetAK8PuppiprunedMass'), 	#### Change name for puppi+softdrop
		jetTau1 		= cms.InputTag('jetsAK8Puppi:jetAK8Puppitau1'),
		jetTau2 		= cms.InputTag('jetsAK8Puppi:jetAK8Puppitau2'),
		jetTau3 		= cms.InputTag('jetsAK8Puppi:jetAK8Puppitau3'),
		jetNSubjets 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppinSubJets'),
		jetSubjetIndex0 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppivSubjetIndex0'),
		jetSubjetIndex1 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppivSubjetIndex1'),
		jetSubjetIndex2 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppivSubjetIndex0'),
		jetSubjetIndex3 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppivSubjetIndex1'),
		jetKeys 		= cms.InputTag('jetKeysAK8Puppi'),
		jetCSVv2 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppiCSVv2'),
		jetCMVAv2 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppiCMVAv2'),
		jetDoubleB	 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppiDoubleBAK8'),
		jetArea 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppijetArea'),
		jetGenPt 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppiGenJetPt'),
		jetGenEta		= cms.InputTag('jetsAK8Puppi:jetAK8PuppiGenJetEta'),
		jetGenPhi 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppiGenJetPhi'),
		jetGenE 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppiGenJetE'),
		jecFactor 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppijecFactor0'),
		neutralHadronEnergyFrac		= cms.InputTag('jetsAK8Puppi:jetAK8PuppineutralHadronEnergyFrac'),
		neutralEmEnergyFrac 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppineutralEmEnergyFrac'),
		chargedEmEnergyFrac 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppichargedEmEnergyFrac'),
		muonEnergyFrac 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiMuonEnergy'),
		chargedHadronEnergyFrac		= cms.InputTag('jetsAK8Puppi:jetAK8PuppichargedHadronEnergyFrac'),
		neutralMultiplicity 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppineutralMultiplicity'),
		chargedMultiplicity 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppichargedMultiplicity'),
		#### Subjets
		subjetPt 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiPt'),
		subjetEta 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiEta'),
		subjetPhi 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiPhi'),
		subjetE 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiE'),
		subjetMass 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiMass'),
		subjetCSVv2 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiCSVv2'),
		subjetCMVAv2 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiCMVAv2'),
		mkTree 			= cms.bool( True )
		)

process.BoostedAnalysisPlotsPuppiJESUp = process.BoostedAnalysisPlotsPuppi.clone( systematics = cms.string( 'JESUp' ) )
process.BoostedAnalysisPlotsPuppiJESDown = process.BoostedAnalysisPlotsPuppi.clone( systematics = cms.string( 'JESDown' ) )
process.BoostedAnalysisPlotsPuppiJERUp = process.BoostedAnalysisPlotsPuppi.clone( systematics = cms.string( 'JERUp' ) )
process.BoostedAnalysisPlotsPuppiJERDown = process.BoostedAnalysisPlotsPuppi.clone( systematics = cms.string( 'JERDown' ) )

############################################################


process.p = cms.Path()
if 'Resolved' in options.version:
	outputNAME = 'ResolvedAnalysis_'
	process.p += process.ResolvedAnalysisPlots
	process.p += process.ResolvedAnalysisPlotsMassPairing
	if options.systematics:
		process.p += process.ResolvedAnalysisPlotsJESUp
		process.p += process.ResolvedAnalysisPlotsJESDown
		process.p += process.ResolvedAnalysisPlotsJERUp
		process.p += process.ResolvedAnalysisPlotsJERDown

elif 'Boosted' in options.version:
	outputNAME = 'BoostedAnalysis_'
	process.p += process.BoostedAnalysisPlots
	process.p += process.BoostedAnalysisPlotsPuppi
	#process.p += process.BoostedAnalysisPlotsSortInMass
	#process.p += process.BoostedAnalysisPlotsSortInTau21
	if options.systematics:
		process.p += process.BoostedAnalysisPlotsJESUp
		process.p += process.BoostedAnalysisPlotsJESDown
		process.p += process.BoostedAnalysisPlotsJERUp
		process.p += process.BoostedAnalysisPlotsJERDown
		#process.p += process.BoostedAnalysisPlotsPuppiJESUp
		#process.p += process.BoostedAnalysisPlotsPuppiJESDown
else: 
	outputNAME = 'FullAnalysis_'
	process.p += process.ResolvedAnalysisPlots
	#process.p += process.ResolvedAnalysisPlotsScouting
	process.p += process.ResolvedAnalysisPlotsMassPairing
	process.p += process.BoostedAnalysisPlots
	#process.p += process.BoostedAnalysisPlotsSortInMass
	#process.p += process.BoostedAnalysisPlotsSortInTau21
	process.p += process.BoostedAnalysisPlotsPuppi

	if options.systematics:
		process.p += process.BoostedAnalysisPlotsJESUp
		process.p += process.BoostedAnalysisPlotsJESDown
		process.p += process.BoostedAnalysisPlotsJERUp
		process.p += process.BoostedAnalysisPlotsJERDown
		process.p += process.ResolvedAnalysisPlotsJESUp
		process.p += process.ResolvedAnalysisPlotsJESDown
		process.p += process.ResolvedAnalysisPlotsJERUp
		process.p += process.ResolvedAnalysisPlotsJERDown

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUN'+outputNAME+NAME+'.root' ) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
