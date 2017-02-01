import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('PROC', 
		'RPVSt100tojj_pythia8_13TeV_PU20bx25',
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
## 'maxEvents' is already registered by the Framework, changing default value
#options.setDefault('maxEvents', 100)

options.parseArguments()

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

NAME = options.PROC

if options.local:
	process.load(NAME+'_cfi')
	#process.load('RPVSt100tojj_13TeV_pythia8_RUNtuples_cfi')
else:
	process.source = cms.Source("PoolSource",
	   fileNames = cms.untracked.vstring(
		   '/store/user/alkahn/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165125/0000/B2GEDMNtuple_1.root',
		   '/store/user/alkahn/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165125/0000/B2GEDMNtuple_10.root',
		   '/store/user/alkahn/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165125/0000/B2GEDMNtuple_100.root',
		   '/store/user/alkahn/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165125/0000/B2GEDMNtuple_101.root',
		   '/store/user/alkahn/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165125/0000/B2GEDMNtuple_102.root',
		   '/store/user/alkahn/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165125/0000/B2GEDMNtuple_103.root',
		   '/store/user/alkahn/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165125/0000/B2GEDMNtuple_104.root',
		   '/store/user/alkahn/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165125/0000/B2GEDMNtuple_105.root',
		   '/store/user/alkahn/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165125/0000/B2GEDMNtuple_106.root',
		   '/store/user/alkahn/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165125/0000/B2GEDMNtuple_107.root',
	    )
	)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#process.TFileService=cms.Service("TFileService",fileName=cms.string( 'RUNAna_'+NAME+'.root' ) )

process.RUNWeightSum = cms.EDAnalyzer('RUNWeightSum',
		generator = cms.InputTag("generator")

)


process.p = cms.Path(process.RUNWeightSum
		)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
