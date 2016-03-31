# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: ste31 --filein dbs:/HSCPgluino_M-1800_TuneCUETP8M1_13TeV-pythia8/RunIIFall15DR76-PU25nsData2015v1_HSCP_customise_76X_mcRun2_asymptotic_v12-v1/AODSIM --fileout file:EXO-RunIIFall15MiniAODv1-01658.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 76X_mcRun2_asymptotic_v12 --step PAT --era Run2_25ns --python_filename step3_MiniAOD_v763.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 1920
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('PAT',eras.Run2_25ns)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1920)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/mc/RunIIFall15DR76/HSCPgluino_M-1800_TuneCUETP8M1_13TeV-pythia8/AODSIM/PU25nsData2015v1_HSCP_customise_76X_mcRun2_asymptotic_v12-v1/10000/14777FDA-D2BA-E511-AF3F-141877410316.root', 
        '/store/mc/RunIIFall15DR76/HSCPgluino_M-1800_TuneCUETP8M1_13TeV-pythia8/AODSIM/PU25nsData2015v1_HSCP_customise_76X_mcRun2_asymptotic_v12-v1/10000/5235A78B-D5BA-E511-B7E2-002590A3C95E.root', 
        '/store/mc/RunIIFall15DR76/HSCPgluino_M-1800_TuneCUETP8M1_13TeV-pythia8/AODSIM/PU25nsData2015v1_HSCP_customise_76X_mcRun2_asymptotic_v12-v1/10000/5A2FE875-D5BA-E511-BDFC-0025905C9742.root', 
        '/store/mc/RunIIFall15DR76/HSCPgluino_M-1800_TuneCUETP8M1_13TeV-pythia8/AODSIM/PU25nsData2015v1_HSCP_customise_76X_mcRun2_asymptotic_v12-v1/10000/76CD8462-B0BA-E511-BC90-141877410E71.root', 
        '/store/mc/RunIIFall15DR76/HSCPgluino_M-1800_TuneCUETP8M1_13TeV-pythia8/AODSIM/PU25nsData2015v1_HSCP_customise_76X_mcRun2_asymptotic_v12-v1/10000/829C1379-D5BA-E511-960C-B083FED3EE25.root', 
        '/store/mc/RunIIFall15DR76/HSCPgluino_M-1800_TuneCUETP8M1_13TeV-pythia8/AODSIM/PU25nsData2015v1_HSCP_customise_76X_mcRun2_asymptotic_v12-v1/10000/9012D69F-9ABA-E511-8844-B083FED4263D.root', 
        '/store/mc/RunIIFall15DR76/HSCPgluino_M-1800_TuneCUETP8M1_13TeV-pythia8/AODSIM/PU25nsData2015v1_HSCP_customise_76X_mcRun2_asymptotic_v12-v1/10000/A2985106-94BA-E511-8470-001EC94BE81B.root', 
        '/store/mc/RunIIFall15DR76/HSCPgluino_M-1800_TuneCUETP8M1_13TeV-pythia8/AODSIM/PU25nsData2015v1_HSCP_customise_76X_mcRun2_asymptotic_v12-v1/10000/BAF48A7F-A9BA-E511-8AAF-90B11C0BE662.root', 
        '/store/mc/RunIIFall15DR76/HSCPgluino_M-1800_TuneCUETP8M1_13TeV-pythia8/AODSIM/PU25nsData2015v1_HSCP_customise_76X_mcRun2_asymptotic_v12-v1/10000/C815F53B-A9BA-E511-9DF6-00266CF94A84.root', 
        '/store/mc/RunIIFall15DR76/HSCPgluino_M-1800_TuneCUETP8M1_13TeV-pythia8/AODSIM/PU25nsData2015v1_HSCP_customise_76X_mcRun2_asymptotic_v12-v1/10000/CE3108E8-A9BA-E511-B14A-14187733AD81.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('ste31 nevts:1920'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('MINIAODSIM'),
        filterName = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('file:inputFile.root'),
    outputCommands = process.MINIAODSIMEventContent.outputCommands,
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '76X_mcRun2_asymptotic_v12', '')

# Path and EndPath definitions
process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.primaryVertexFilter)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_chargedHadronTrackResolutionFilter = cms.Path(process.chargedHadronTrackResolutionFilter)
process.Flag_CSCTightHaloTrkMuUnvetoFilter = cms.Path(process.CSCTightHaloTrkMuUnvetoFilter)
process.Flag_HBHENoiseIsoFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseIsoFilter)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseFilter)
process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_EcalDeadCellBoundaryEnergyFilter = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
process.Flag_HcalStripHaloFilter = cms.Path(process.HcalStripHaloFilter)
process.Flag_muonBadTrackFilter = cms.Path(process.muonBadTrackFilter)
process.Flag_CSCTightHalo2015Filter = cms.Path(process.CSCTightHalo2015Filter)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.Flag_HBHENoiseFilter,process.Flag_HBHENoiseIsoFilter,process.Flag_CSCTightHaloFilter,process.Flag_CSCTightHaloTrkMuUnvetoFilter,process.Flag_CSCTightHalo2015Filter,process.Flag_HcalStripHaloFilter,process.Flag_hcalLaserEventFilter,process.Flag_EcalDeadCellTriggerPrimitiveFilter,process.Flag_EcalDeadCellBoundaryEnergyFilter,process.Flag_goodVertices,process.Flag_eeBadScFilter,process.Flag_ecalLaserCorrFilter,process.Flag_trkPOGFilters,process.Flag_chargedHadronTrackResolutionFilter,process.Flag_muonBadTrackFilter,process.Flag_trkPOG_manystripclus53X,process.Flag_trkPOG_toomanystripclus53X,process.Flag_trkPOG_logErrorTooManyClusters,process.Flag_METFilters,process.endjob_step,process.MINIAODSIMoutput_step)

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions
#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)
process.load('Configuration.StandardSequences.PATMC_cff')
from FWCore.ParameterSet.Utilities import cleanUnscheduled
process=cleanUnscheduled(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 

#call to customisation function miniAOD_customizeAllMC imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllMC(process)

# End of customisation functions
