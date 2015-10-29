import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

### General Options
options.register('PROC', 
		'RPVSt350tojj_pythia8_13TeV_PU20bx25',
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
options.register('debug', 
		False,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.bool,
		"Run just pruned"
		)
options.register('version', 
		'Both',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"Version of the analysis to run. (Both, Resolved, Boosted)"
		)

### Resolved Analysis Options
options.register('HT', 
		800.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"HT cut"
		)
options.register('MassRes', 
		0.30,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"MassRes cut"
		)
options.register('Delta', 
		300.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Delta cut"
		)
options.register('EtaBand', 
		1.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"EtaBand cut"
		)
options.register('JetPt', 
		0.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"JetPt cut"
		)

### Boosted Analysis Options
options.register('boostedJetPt', 
		150.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"JetPt cut"
		)

options.register('boostedHT', 
		800.0,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"JetPt cut"
		)

options.register('Asym', 
		0.1,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Asymmetry cut"
		)
options.register('CosTheta', 
		0.3,
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
		0.3,
		VarParsing.multiplicity.singleton,
		VarParsing.varType.float,
		"Tau31 cut"
		)
options.register('Tau21', 
		0.4,
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
		'PileupData2015D_JSON_10-23-2015.root',
		VarParsing.multiplicity.singleton,
		VarParsing.varType.string,
		"namePUFile"
		)


options.parseArguments()

process = cms.Process("RUNAnalysis")
process.load("FWCore.MessageService.MessageLogger_cfi")
NAME = options.PROC
if 'Run2015' in NAME: isData=True
else: isData=False

if options.local:
	process.load(NAME+'_RUNA_cfi')
	#process.load('RPVSt100tojj_13TeV_pythia8_RUNtuples_cfi')
else:
	process.source = cms.Source("PoolSource",
			fileNames = cms.untracked.vstring(
				'/store/user/algomez/RPVSt100tojj_13TeV_pythia8/RunIISpring15MiniAODv2-74X_RUNA_Asympt25ns_v08/151023_030853/0000/RUNtuple_101.root',
	    )
	)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32 (options.maxEvents) )
process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNFullAnalysis_'+NAME+'.root' ) )

if 'bj' in NAME: bjsample = True
else: bjsample = False

if 'JetHT' in NAME: HTtrigger = 'HLT_PFHT800'
else: HTtrigger = 'HLT_PFHT900'


process.ResolvedAnalysisPlots = cms.EDAnalyzer('RUNAnalysis',
		cutHT	 		= cms.double( options.HT ),
		cutMassRes 		= cms.double( options.MassRes ),
		cutDelta 		= cms.double( options.Delta ),
		cutEtaBand 		= cms.double( options.EtaBand ),
		cutJetPt 		= cms.double( options.JetPt ),
		bjSample		= cms.bool( bjsample ),
		triggerPass 		= cms.vstring( [ HTtrigger, 'HLT_PFHT750_4JetPt' ] ),
		dataPUFile		= cms.string( '../data/'+options.namePUFile  ),
		isData			= cms.bool( isData ),
)
process.RUNATree = process.ResolvedAnalysisPlots.clone( mkTree = cms.bool( True ) )


process.BoostedAnalysisPlots = cms.EDAnalyzer('RUNBoostedAnalysis',
		cutjetPtvalue 		= cms.double( options.boostedJetPt ),
		cutHTvalue  		= cms.double( options.boostedHT ),
		cutAsymvalue 		= cms.double( options.Asym ),
		cutCosThetavalue 	= cms.double( options.CosTheta ),
		cutSubjetPtRatiovalue 	= cms.double( options.SubPt ),
		cutTau31value 		= cms.double( options.Tau31 ),
		cutTau21value 		= cms.double( options.Tau21 ),
		cutDEtavalue 		= cms.double( options.DEta ),
		cutBtagvalue 		= cms.double( options.btag ),
		bjSample		= cms.bool( bjsample ),
		mkTree			= cms.bool( False  ),
		triggerPass 		= cms.vstring( [ 'HLT_AK8PFHT700_TrimR0p1PT0p03Mass50', HTtrigger ] ),
		dataPUFile		= cms.string( '../data/'+options.namePUFile  ),
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

if options.debug:
	process.p = cms.Path( process.ResolvedAnalysisPlots
			* process.BoostedAnalysisPlots )
else:

	process.p = cms.Path( process.ResolvedAnalysisPlots
		* process.RUNATree
		* process.BoostedAnalysisPlots
		* process.BoostedAnalysisPlotsTrimmed
		* process.BoostedAnalysisPlotsPruned
		* process.BoostedAnalysisPlotsSoftDrop
		#* process.BoostedAnalysisPlotsPuppi
		* process.BoostedAnalysisPlotsFiltered
		* process.RUNATreeSoftDrop
		* process.RUNATreePruned
		)


process.MessageLogger.cerr.FwkReport.reportEvery = 1000
