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
		True,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.bool,
		"Run locally or crab"
		)
options.register('version', 
		'Full',
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
		'supportFiles/Fall15_25nsV2',
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



### Boosted Analysis Options
options.register('cutTau21', 
		0.5, 
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Tau21 cut"
		)

options.register('cutTau31', 
		0.3, 
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Tau31 cut"
		)
options.register('cutMassAsym', 
		0.2, 
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"MassAsym cut"
		)
options.register('cutDeltaEtaDijet', 
		0.5, 
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"DeltaEtaDijet cut"
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
			'/store/user/algomez/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0/160405_143224/0000/B2GEDMNtuple_10.root',
			'/store/user/algomez/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0/160405_143224/0000/B2GEDMNtuple_11.root',
			'/store/user/algomez/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0/160405_143224/0000/B2GEDMNtuple_12.root',
			'/store/user/algomez/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0/160405_143224/0000/B2GEDMNtuple_13.root',
			'/store/user/algomez/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0/160405_143224/0000/B2GEDMNtuple_14.root',
			'/store/user/algomez/RPVStopStopToJets_UDD312_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0/160405_143224/0000/B2GEDMNtuple_15.root',
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


process.BoostedAnalysisPlots = cms.EDAnalyzer('RUNBoostedResolutionCalc',
		#triggerPass 		= cms.vstring( [ 'HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_PFHT800'] ),
		bjSample		= cms.bool( bjsample ),
		dataPUFile		= cms.string( options.namePUFile  ),
		jecVersion		= cms.string( options.jecVersion ),
		isData			= cms.bool( isData ),
		scale 			= cms.double( SF ),
		cutTau21		= cms.double( options.cutTau21 ),
		cutTau31		= cms.double( options.cutTau31 ),
		cutMassAsym		= cms.double( options.cutMassAsym ),
		cutDeltaEtaDijet	= cms.double( options.cutDeltaEtaDijet ),
)


process.BoostedAnalysisPlotsPuppi = process.BoostedAnalysisPlots.clone( 
		PUMethod		= cms.string('Puppi'),
		jetPt 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiPt'),
		jetEta			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiEta'),
		jetPhi 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiPhi'),
		jetE 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiE'),
		jetMass 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppiMass'),
		jetTrimmedMass 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppitrimmedMass'),
		jetPrunedMass 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppiprunedMass'),
		jetFilteredMass 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppifilteredMass'),
		jetSoftDropMass		= cms.InputTag('jetsAK8Puppi:jetAK8PuppisoftDropMass'),
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
		neutralHadronEnergy 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppineutralHadronEnergy'),
		neutralEmEnergy 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppineutralEmEnergy'),
		chargedEmEnergy 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppichargedEmEnergy'),
		muonEnergy 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiMuonEnergy'),
		chargedHadronEnergy 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppichargedHadronEnergy'),
		chargedHadronMultiplicity 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppiChargedHadronMultiplicity'),
		neutralHadronMultiplicity 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppineutralHadronMultiplicity'),
		chargedMultiplicity 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppichargedMultiplicity'),
		#### Subjets
		subjetPt 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiPt'),
		subjetEta 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiEta'),
		subjetPhi 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiPhi'),
		subjetE 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiE'),
		subjetMass 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiMass'),
		subjetCSVv2 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiCSVv2'),
		subjetCMVAv2 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiCMVAv2'),
		)




process.p = cms.Path()
outputNAME = 'BoostedResolutionCalc_'
process.p += process.BoostedAnalysisPlots
#process.p += process.BoostedAnalysisPlotsPuppi

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUN'+outputNAME+NAME+'.root' ) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
