import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

### General Options
options.register('PROC', 
		'RPVStopStopToJets_UDD312_M-100',
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
		'supportFiles/Summer15_25nsV6',
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
options.register('Asym', 
		0.1,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Asymmetry cut"
		)
options.register('CosTheta', 
		0.2,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"CosThetaStar cut"
		)
options.register('SubPt', 
		0.3,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Subjet Pt Ratio cut"
		)
options.register('Tau31', 
		0.4,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Tau31 cut"
		)
options.register('Tau21', 
		0.6,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Tau21 cut"
		)
options.register('DEta', 
		1.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"DEta cut"
		)
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
			'/store/user/algomez/JetHT/Run2015D-PromptReco-v4_RUNA_v09/151117_100001/0000/RUNtuple_1.root',
			#'/store/user/algomez/JetHT/Run2015D-PromptReco-v4_RUNA_v09/151117_100001/0000/RUNtuple_10.root',
			#'/store/user/algomez/JetHT/Run2015D-PromptReco-v4_RUNA_v09/151117_100001/0000/RUNtuple_100.root',
			#'/store/user/algomez/JetHT/Run2015D-PromptReco-v4_RUNA_v09/151117_100001/0000/RUNtuple_101.root',
			#'/store/user/algomez/JetHT/Run2015D-PromptReco-v4_RUNA_v09/151117_100001/0000/RUNtuple_102.root',
			#'/store/user/algomez/JetHT/Run2015D-PromptReco-v4_RUNA_v09/151117_100001/0000/RUNtuple_103.root',
			#'/store/user/algomez/JetHT/Run2015D-PromptReco-v4_RUNA_v09/151117_100001/0000/RUNtuple_104.root',
			#'/store/user/algomez/JetHT/Run2015D-PromptReco-v4_RUNA_v09/151117_100001/0000/RUNtuple_105.root',
			#'/store/user/algomez/JetHT/Run2015D-PromptReco-v4_RUNA_v09/151117_100001/0000/RUNtuple_106.root',
			#'/store/user/algomez/JetHT/Run2015D-PromptReco-v4_RUNA_v09/151117_100001/0000/RUNtuple_107.root'
			#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09/151116_131102/0000/RUNtuple_1.root',
			#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09/151116_131102/0000/RUNtuple_10.root',
			#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09/151116_131102/0000/RUNtuple_100.root',
			#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09/151116_131102/0000/RUNtuple_101.root',
			#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09/151116_131102/0000/RUNtuple_102.root',
			#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09/151116_131102/0000/RUNtuple_103.root',
			#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09/151116_131102/0000/RUNtuple_104.root',
			#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09/151116_131102/0000/RUNtuple_105.root',
			#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09/151116_131102/0000/RUNtuple_106.root',
			#'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v09/151116_131102/0000/RUNtuple_107.root'
	    )
	)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32 (options.maxEvents) )

from RUNA.RUNAnalysis.scaleFactors import scaleFactor

bjsample = True if 'bj' in NAME else False
if 'Run2015' in NAME: 
	isData=True
	SF = 1 
	HTtrigger = 'HLT_PFHT800'
	options.systematics = False
else:
	isData=False
	SF = scaleFactor(NAME) 
	HTtrigger = 'HLT_PFHT900'


process.ResolvedAnalysisPlots = cms.EDAnalyzer('RUNAnalysis',
		cutMassAsym 		= cms.double( options.MassRes ),
		cutDelta 		= cms.double( options.Delta ),
		cutDeltaR 		= cms.double( options.DeltaR ),
		cutCosThetaStar 	= cms.double( options.ResolvedCosThetaStar ),
		cutDEta    		= cms.double( options.EtaBand ),
		triggerPass 		= cms.vstring( [ HTtrigger, 'HLT_PFHT750_4JetPt' ] ),
		scale 			= cms.double( SF ),
		bjSample		= cms.bool( bjsample ),
		dataPUFile		= cms.string( options.namePUFile  ),
		jecVersion		= cms.string( options.jecVersion ),
		isData			= cms.bool( isData ),
)
process.RUNATree = process.ResolvedAnalysisPlots.clone( mkTree = cms.bool( True ) )
process.ResolvedAnalysisPlotsJESUp = process.ResolvedAnalysisPlots.clone( systematics = cms.string( 'JESUp' ) )
process.ResolvedAnalysisPlotsJESDown = process.ResolvedAnalysisPlots.clone( systematics = cms.string( 'JESDown' ) )


process.BoostedAnalysisPlots = cms.EDAnalyzer('RUNBoostedAnalysis',
		cutAsymvalue 		= cms.double( options.Asym ),
		cutCosThetavalue 	= cms.double( options.CosTheta ),
		cutSubjetPtRatiovalue 	= cms.double( options.SubPt ),
		cutTau31value 		= cms.double( options.Tau31 ),
		cutTau21value 		= cms.double( options.Tau21 ),
		cutDEtavalue 		= cms.double( options.DEta ),
		cutBtagvalue 		= cms.double( options.btag ),
		triggerPass 		= cms.vstring( [ 'HLT_AK8PFHT700_TrimR0p1PT0p03Mass50', HTtrigger ] ),
		scale 			= cms.double( SF ),
		bjSample		= cms.bool( bjsample ),
		dataPUFile		= cms.string( options.namePUFile  ),
		jecVersion		= cms.string( options.jecVersion ),
		isData			= cms.bool( isData ),
)

process.BoostedAnalysisPlotsTrimmed = process.BoostedAnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8trimmedMass') )
process.BoostedAnalysisPlotsFiltered = process.BoostedAnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8filteredMass') )
process.BoostedAnalysisPlotsPruned = process.BoostedAnalysisPlots.clone( 
		jetMass 		= cms.InputTag('jetsAK8:jetAK8prunedMass'),
		#### Subjets
		#subjetPt 		= cms.InputTag('subjetsAK8Pruned:subjetAK8PrunedPt'),
		#subjetEta 		= cms.InputTag('subjetsAK8Pruned:subjetAK8PrunedEta'),
		#subjetPhi 		= cms.InputTag('subjetsAK8Pruned:subjetAK8PrunedPhi'),
		#subjetE 		= cms.InputTag('subjetsAK8Pruned:subjetAK8PrunedE'),
		#subjetMass 		= cms.InputTag('subjetsAK8Pruned:subjetAK8PrunedMass'),
		)
process.BoostedAnalysisPlotsPrunedJESUp = process.BoostedAnalysisPlotsPruned.clone( systematics = cms.string( 'JESUp' ) )
process.BoostedAnalysisPlotsPrunedJESDown = process.BoostedAnalysisPlotsPruned.clone( systematics = cms.string( 'JESDown' ) )

process.BoostedAnalysisPlotsSoftDrop = process.BoostedAnalysisPlots.clone( jetMass = cms.InputTag('jetsAK8:jetAK8softDropMass') )
process.BoostedAnalysisPlotsPuppi = process.BoostedAnalysisPlots.clone( 
		jetPt 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiPt'),
		jetEta			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiEta'),
		jetPhi 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiPhi'),
		jetE 			= cms.InputTag('jetsAK8Puppi:jetAK8PuppiE'),
		jetMass 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppiMass'),
		jetTau1 		= cms.InputTag('jetsAK8Puppi:jetAK8Puppitau1'),
		jetTau2 		= cms.InputTag('jetsAK8Puppi:jetAK8Puppitau2'),
		jetTau3 		= cms.InputTag('jetsAK8Puppi:jetAK8Puppitau3'),
		jetNSubjets 		= cms.InputTag('jetsAK8Puppi:jetAK8PuppinSubJets'),
		jetSubjetIndex0 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppivSubjetIndex0'),
		jetSubjetIndex1 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppivSubjetIndex1'),
		jetSubjetIndex2 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppivSubjetIndex0'),
		jetSubjetIndex3 	= cms.InputTag('jetsAK8Puppi:jetAK8PuppivSubjetIndex1'),
		jetKeys 		= cms.InputTag('jetKeysAK8Puppi'),
		#### Subjets
		subjetPt 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiPt'),
		subjetEta 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiEta'),
		subjetPhi 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiPhi'),
		subjetE 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiE'),
		subjetMass 		= cms.InputTag('subjetsAK8Puppi:subjetAK8PuppiMass'),
		)


process.RUNATreeSoftDrop = process.BoostedAnalysisPlotsSoftDrop.clone( mkTree = cms.bool( True ) )
process.RUNATreePruned = process.BoostedAnalysisPlotsPruned.clone( mkTree = cms.bool( True ) )

if 'Resolved' in options.version:
	outputNAME = 'ResolvedAnalysis_'
	process.p = cms.Path( process.ResolvedAnalysisPlots
		* process.RUNATree
		)
	if options.systematics:
		process.p += process.ResolvedAnalysisPlotsJESUp
		process.p += process.ResolvedAnalysisPlotsJESDown
elif 'Boosted' in options.version:
	outputNAME = 'BoostedAnalysis_'
	process.p = cms.Path( #* process.BoostedAnalysisPlots
		#* process.BoostedAnalysisPlotsTrimmed
		process.BoostedAnalysisPlotsPruned
		#* process.BoostedAnalysisPlotsSoftDrop
		#* process.BoostedAnalysisPlotsPuppi
		#* process.BoostedAnalysisPlotsFiltered
		#* process.RUNATreeSoftDrop
		* process.RUNATreePruned
		)
	if options.systematics:
		process.p += process.BoostedAnalysisPlotsPrunedJESUp
		process.p += process.BoostedAnalysisPlotsPrunedJESDown
else: 
	outputNAME = 'FullAnalysis_'
	process.p = cms.Path( process.ResolvedAnalysisPlots
		* process.RUNATree
		#* process.BoostedAnalysisPlots
		#* process.BoostedAnalysisPlotsTrimmed
		* process.BoostedAnalysisPlotsPruned
		#* process.BoostedAnalysisPlotsSoftDrop
		#* process.BoostedAnalysisPlotsPuppi
		#* process.BoostedAnalysisPlotsFiltered
		#* process.RUNATreeSoftDrop
		* process.RUNATreePruned
		)
	if options.systematics:
		process.p += process.BoostedAnalysisPlotsPrunedJESUp
		process.p += process.BoostedAnalysisPlotsPrunedJESDown
		process.p += process.ResolvedAnalysisPlotsJESUp
		process.p += process.ResolvedAnalysisPlotsJESDown

process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUN'+outputNAME+NAME+'.root' ) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
