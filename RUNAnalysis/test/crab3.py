##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
config = config()


version = 'v02'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNAnalysis_cfg.py'
config.JobType.allowNonProductionCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.outLFN = '/store/user/algomez/'
config.Data.publication = False
config.Data.ignoreLocality = True
#config.Data.publishDataName = 'RUNA_PHYS14_PU20bx25_'+version

config.Site.storageSite = 'T3_US_FNALLPC'

if __name__ == '__main__':

	from CRABAPI.RawCommand import crabCommand

	Samples = [ 
			### CSA14
			#'/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-RUNA_PU40bx50_v01-e839e229a9e5d0ac5fa9b79d454f01f9/USER',
			#'/QCD_Pt-80to120_Tune4C_13TeV_pythia8/algomez-RUNA_PU40bx50_v01-e839e229a9e5d0ac5fa9b79d454f01f9/USER',
			#'/QCD_Pt-120to170_Tune4C_13TeV_pythia8/algomez-RUNA_PU40bx50_v01-e839e229a9e5d0ac5fa9b79d454f01f9/USER',
			#'/QCD_Pt-170to300_Tune4C_13TeV_pythia8/algomez-RUNA_PU40bx50_v01-e839e229a9e5d0ac5fa9b79d454f01f9/USER',
			#'/QCD_Pt-300to470_Tune4C_13TeV_pythia8/algomez-RUNA_PU40bx50_v01-e839e229a9e5d0ac5fa9b79d454f01f9/USER',
			#'/QCD_Pt-470to600_Tune4C_13TeV_pythia8/algomez-RUNA_PU40bx50_v01-e839e229a9e5d0ac5fa9b79d454f01f9/USER',
			#'/QCD_Pt-600to800_Tune4C_13TeV_pythia8/algomez-RUNA_PU40bx50_v01-e839e229a9e5d0ac5fa9b79d454f01f9/USER',
			'/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/algomez-RUNA_PU40bx50_v01-e839e229a9e5d0ac5fa9b79d454f01f9/USER'
			### Phys14
			#'/RPVSt100tojj_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v03-3a44eabbfff85fd48f606f0490358b47/USER',
			#'/RPVSt100tobj_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v03-3a44eabbfff85fd48f606f0490358b47/USER',
			#'/QCD_HT-500To1000_13TeV-madgraph/algomez-RUNA_PHYS14_PU20bx25_v03-3a44eabbfff85fd48f606f0490358b47/USER',
			#'/QCD_HT_1000ToInf_13TeV-madgraph/algomez-RUNA_PHYS14_PU20bx25_v03-3a44eabbfff85fd48f606f0490358b47/USER' 
			]

	
	for dataset in Samples:
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RUNA', '').split('-')[0]+version
		config.Data.inputDataset = dataset
		config.General.requestName = procName
		config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0' ]
		if 'QCD' in dataset: 
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 20
		else: 
			config.Data.splitting = 'FileBased'
			config.Data.unitsPerJob = 1
		crabCommand('submit', config = config)
