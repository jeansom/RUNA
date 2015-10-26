from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.requestName = 'Name'
config.section_('JobType')
config.JobType.psetName = 'cfg_files/CMSSW_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.pyCfgParams = []
config.JobType.inputFiles = [ 'EfficiencyMapsAK4.root','EfficiencyMapsAK8.root','CSV.csv']
config.section_('Data')

#config.Data.inputDataset = 'DATASET'
#config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/DBS_INSTANCE/DBSReader/'
config.Data.primaryDataset = '/Sig_500SbtoWSt_100RPVSttojb_RUNA_v741p1/sftoolplot/MINRVSECMINR'
config.Data.userInputFiles = open('/eos/uscms/store/user/morris17/MiniAODfiles.txt').readlines()
config.Data.publication = False
config.Data.unitsPerJob = 50
config.Data.splitting = 'FileBased'
config.Data.publishDataName = 'PUBLICATION_NAME'
config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'
