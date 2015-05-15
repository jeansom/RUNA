##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
config = config()

version = 'v09'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNFullAnalysis_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.outLFNDirBase = '/store/user/algomez/'
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
			#'/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/algomez-RUNA_PU40bx50_v01-e839e229a9e5d0ac5fa9b79d454f01f9/USER'
			#'/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-RUNA_PHYS14_PU40bx50_V03-f6b653bf81f18baefaea3aff0a94d1b3/USER',
			#'/RPVSt100tojj_13TeV_pythia8_GENSIM/algomez-RUNA_CSA14_PU40bx50_v03-513e0b55cd050b4b4b85e9ff437fb8b3/USER',
			#'/QCD_Pt-170to300_Tune4C_13TeV_pythia8/algomez-RUNA_CSA14_PU40bx50_v03-9a531a076c9753bf03a565049f526004/USER',
			#'/QCD_Pt-300to470_Tune4C_13TeV_pythia8/algomez-RUNA_CSA14_PU40bx50_v03-9a531a076c9753bf03a565049f526004/USER',
			#'/QCD_Pt-470to600_Tune4C_13TeV_pythia8/algomez-RUNA_CSA14_PU40bx50_v03-9a531a076c9753bf03a565049f526004/USER',
			#'/QCD_Pt-600to800_Tune4C_13TeV_pythia8/algomez-RUNA_CSA14_PU40bx50_v03-9a531a076c9753bf03a565049f526004/USER',
			#'/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/algomez-RUNA_CSA14_PU40bx50_v03-9a531a076c9753bf03a565049f526004/USER',
			#'/QCD_Pt-1000to1400_Tune4C_13TeV_pythia8/algomez-RUNA_CSA14_PU40bx50_v03-9a531a076c9753bf03a565049f526004/USER',
			#'/QCD_Pt-1400to1800_Tune4C_13TeV_pythia8/algomez-RUNA_CSA14_PU40bx50_v03-9a531a076c9753bf03a565049f526004/USER',

			### Phys14
			'/QCD_Pt-170to300_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU30BX50_v03-513e0b55cd050b4b4b85e9ff437fb8b3/USER',
			'/QCD_Pt-300to470_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU30BX50_v03-513e0b55cd050b4b4b85e9ff437fb8b3/USER',
			'/QCD_Pt-470to600_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU30BX50_v03-513e0b55cd050b4b4b85e9ff437fb8b3/USER',
			'/QCD_Pt-600to800_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU30BX50_v03-513e0b55cd050b4b4b85e9ff437fb8b3/USER',
			'/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU30BX50_v03-513e0b55cd050b4b4b85e9ff437fb8b3/USER',
			'/QCD_Pt-1000to1400_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU30BX50_v03-513e0b55cd050b4b4b85e9ff437fb8b3/USER',
			'/QCD_Pt-1400to1800_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU30BX50_v03-513e0b55cd050b4b4b85e9ff437fb8b3/USER',
			'/RPVSt100tojj_13TeV_pythia8/algomez-RUNA_CSA14_PU40bx50_v03-513e0b55cd050b4b4b85e9ff437fb8b3/USER',	## it is only the name.. it is PHYS14 PU30BX50
			'/RPVSt100tojj_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v03-3a44eabbfff85fd48f606f0490358b47/USER',
			#'/RPVSt100tobj_pythia8_13TeV/algomez-RUNA_PHYS14_PU20bx25_v03-170c2afdc214daaa597e50617fc92cfc/USER',
			'/RPVSt350tojj_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v03-3a44eabbfff85fd48f606f0490358b47/USER',
			#'/QCD_HT-500To1000_13TeV-madgraph/algomez-RUNA_PHYS14_PU20bx25_v03-3a44eabbfff85fd48f606f0490358b47/USER',
			#'/QCD_HT_1000ToInf_13TeV-madgraph/algomez-RUNA_PHYS14_PU20bx25_v03-3a44eabbfff85fd48f606f0490358b47/USER',
			'/QCD_Pt-170to300_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v03-170c2afdc214daaa597e50617fc92cfc/USER',
			'/QCD_Pt-300to470_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v03-170c2afdc214daaa597e50617fc92cfc/USER',
			'/QCD_Pt-470to600_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v03-170c2afdc214daaa597e50617fc92cfc/USER',
			'/QCD_Pt-600to800_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v03-170c2afdc214daaa597e50617fc92cfc/USER',
			'/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v03-170c2afdc214daaa597e50617fc92cfc/USER',
			'/QCD_Pt-1000to1400_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v03-170c2afdc214daaa597e50617fc92cfc/USER',
			'/QCD_Pt-1400to1800_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v03-170c2afdc214daaa597e50617fc92cfc/USER',
			]

	
	for dataset in Samples:
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RUNA', '').replace('CSA14_PU40bx50','PHYS14_PU30BX50').split('-')[0]+'_'+version
		#procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RUNA', '').split('-')[0]+'_'+version
		config.Data.inputDataset = dataset
		config.General.requestName = procName
		config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0' ]
		if 'QCD' in dataset: 
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 10
		else: 
			config.Data.splitting = 'FileBased'
			config.Data.unitsPerJob = 1
		crabCommand('submit', config = config)
