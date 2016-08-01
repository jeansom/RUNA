from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')

### To use a specific name of UI directory where CRAB will create job to submit (with full path).
### the default directory will be "crab_0_data_time"
config.General.requestName = 'RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8__jsomalwa-RunIIFall15DR76_MiniAOD'

### OUTPUT files INTO A SE
config.General.transferOutputs = True


config.section_('JobType')

### The ParameterSet you want to use
config.JobType.psetName = '/uscms_data/d3/jsomalwa/SFb80X/test8116/CMSSW_8_0_12/src/RUNA/RUNBTaggingEfficiencyScaleFactors/test/MakeBTaggingEfficiencyMaps/CRAB_Jobs/cfg_files/CMSSW_cfg.py'

config.JobType.pluginName = 'Analysis'

### Parameters to be passed to the python config file
config.JobType.pyCfgParams = ['wantSummary=True']

### Input Files
config.JobType.inputFiles = [ 'JECs' ]

### The output files (comma separated list)
#config.JobType.outputFiles = 'OUTPUT_FILES'


config.section_('Data')

### The data you want to access (to be found on DBS)
config.Data.inputDataset = '/RPVStopStopToJets_UDD323_M-100_TuneCUETP8M1_13TeV-madgraph-pythia8/jsomalwa-RunIIFall15DR76_MiniAOD_Asympt25ns-928d46295c808b28c2560dd199b08897/USER'

### To select a single (list of) run within a single processed dataset define run number (list)
### Selection can be a comma-separated list of run numbers and run number ranges: 1,2,3-4
#config.Data.runRange = 'RUN_SELECTION'

### A JSON file that describes which runs and lumis to process. CRAB will skip luminosity blocks not
### listed in the file. When using this setting, you must also use lumi-based splitting rather than
### event based splitting as shown below.
#config.Data.lumiMask = 'LUMI_MASK'

### To publish produced output in a local istance of DBS set publish_data = 1
config.Data.publication = False

config.Data.unitsPerJob = 50 #DEFAULT

config.Data.splitting = 'FileBased' #DEFAULT


### Specify the dataset name. The full path will be <primarydataset>/<publish_data_name>/USER
config.Data.outputDatasetTag = 'PUBLICATION_NAME'

### Specify the URL of DBS istance where CRAB has to publish the output files
config.Data.publishDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSWriter/'

### Specify the URL of DBS istance where CRAB has to get the dataset from
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader/'

config.section_('User')
config.section_('Site')

### FNAL SE
config.Site.storageSite = 'T3_US_FNALLPC'

