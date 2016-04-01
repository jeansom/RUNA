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


### Resolved Analysis Options
options.register('MassRes', 
		0.20,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"MassRes cut"
		)
options.register('Delta', 
		180.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Delta cut"
		)
options.register('DeltaR', 
		1.5,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"DeltaR cut"
		)
options.register('EtaBand', 
		0.75,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"EtaBand cut"
		)
options.register('ResolvedCosThetaStar', 
		0.6,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Resolved CosThetaStar cut"
		)

### Boosted Analysis Options
options.register('btag', 
		#0.244,  ## CSVL
		0.679, ## CSVM
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Btag cut"
		)
options.register('namePUFile', 
		'supportFiles/PileupData2015D_JSON_10-28-2015.root',
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
			'/store/user/algomez/RPVStopStopToJets_UDD312_M-150_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v2p0/160331_081614/0000/B2GEDMNtuple_1.root',
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


process.ResolvedAnalysisPlots = cms.EDAnalyzer('RUNAnalysis',
		cutMassAsym 		= cms.double( options.MassRes ),
		cutDelta 		= cms.double( options.Delta ),
		cutDeltaR 		= cms.double( options.DeltaR ),
		cutCosThetaStar 	= cms.double( options.ResolvedCosThetaStar ),
		cutDEta    		= cms.double( options.EtaBand ),
		triggerPass 		= cms.vstring( [ 'HLT_PFHT800', 'HLT_PFHT750_4JetPt' ] ),
		bjSample		= cms.bool( bjsample ),
		scale 			= cms.double( SF ),
		dataPUFile		= cms.string( options.namePUFile  ),
		jecVersion		= cms.string( options.jecVersion ),
		isData			= cms.bool( isData ),
)
process.ResolvedAnalysisPlotsJESUp = process.ResolvedAnalysisPlots.clone( systematics = cms.string( 'JESUp' ) )
process.ResolvedAnalysisPlotsJESDown = process.ResolvedAnalysisPlots.clone( systematics = cms.string( 'JESDown' ) )


process.BoostedAnalysisPlots = cms.EDAnalyzer('RUNBoostedAnalysis',
		triggerPass 		= cms.vstring( [ 'HLT_AK8PFHT650_TrimR0p1PT0p03Mass50', 'HLT_PFHT800'] ),
		bjSample		= cms.bool( bjsample ),
		dataPUFile		= cms.string( options.namePUFile  ),
		jecVersion		= cms.string( options.jecVersion ),
		isData			= cms.bool( isData ),
		scale 			= cms.double( SF ),
)

process.BoostedAnalysisPlotsJESUp = process.BoostedAnalysisPlots.clone( systematics = cms.string( 'JESUp' ) )
process.BoostedAnalysisPlotsJESDown = process.BoostedAnalysisPlots.clone( systematics = cms.string( 'JESDown' ) )

process.BoostedAnalysisPlotsPuppi = process.BoostedAnalysisPlots.clone( 
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
		jetCSV	 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppiCSVv2'),
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
		)

process.BoostedAnalysisPlotsPuppiJESUp = process.BoostedAnalysisPlotsPuppi.clone( systematics = cms.string( 'JESUp' ) )
process.BoostedAnalysisPlotsPuppiJESDown = process.BoostedAnalysisPlotsPuppi.clone( systematics = cms.string( 'JESDown' ) )



process.p = cms.Path()
if 'Resolved' in options.version:
	outputNAME = 'ResolvedAnalysis_'
	process.p += process.ResolvedAnalysisPlots
	if options.systematics:
		process.p += process.ResolvedAnalysisPlotsJESUp
		process.p += process.ResolvedAnalysisPlotsJESDown
elif 'Boosted' in options.version:
	outputNAME = 'BoostedAnalysis_'
	process.p += process.BoostedAnalysisPlots
	process.p += process.BoostedAnalysisPlotsPuppi
	if options.systematics:
		process.p += process.BoostedAnalysisPlotsJESUp
		process.p += process.BoostedAnalysisPlotsJESDown
		#process.p += process.BoostedAnalysisPlotsPuppiJESUp
		#process.p += process.BoostedAnalysisPlotsPuppiJESDown
else: 
	outputNAME = 'FullAnalysis_'
	process.p += process.ResolvedAnalysisPlots
	process.p += process.BoostedAnalysisPlots
	process.p += process.BoostedAnalysisPlotsPuppi
	if options.systematics:
		process.p += process.BoostedAnalysisPlotsJESUp
		process.p += process.BoostedAnalysisPlotsJESDown
		process.p += process.ResolvedAnalysisPlotsJESUp
		process.p += process.ResolvedAnalysisPlotsJESDown

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUN'+outputNAME+NAME+'.root' ) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
