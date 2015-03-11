from CRABClient.UserUtilities import config
config = config()


config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNtuples_cfg.py'
config.JobType.allowNonProductionCMSSW = True

config.Data.inputDataset = ''
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFN = '/store/user/algomez/'
config.Data.publication = True
config.Data.ignoreLocality = True
config.Data.publishDataName = 'RUNA_PHYS14_PU20bx25_v01'

config.Site.storageSite = 'T3_US_FNALLPC'

if __name__ == '__main__':

	from CRABAPI.RawCommand import crabCommand

	QCDHT = [ '/QCD_HT-100To250_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
			'/QCD_HT_250To500_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
			'/QCD_HT-500To1000_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
			'/QCD_HT-500To1000_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1_ext1-v1/MINIAODSIM',
			'/QCD_HT_1000ToInf_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
			'/QCD_HT_1000ToInf_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1_ext1-v1/MINIAODSIM'
			]

	### CSA14 samples
	QCDPt = [ '/QCD_Pt-80to120_Tune4C_13TeV_pythia8/Spring14miniaod-141029_PU40bx50_castor_PLS170_V6AN2-v1/MINIAODSIM',
			'/QCD_Pt-120to170_Tune4C_13TeV_pythia8/Spring14miniaod-141029_PU40bx50_castor_PLS170_V6AN2-v1/MINIAODSIM',
			'/QCD_Pt-170to300_Tune4C_13TeV_pythia8/Spring14miniaod-141029_PU40bx50_castor_PLS170_V6AN2-v1/MINIAODSIM',
			'/QCD_Pt-300to470_Tune4C_13TeV_pythia8/Spring14miniaod-141029_PU40bx50_castor_PLS170_V6AN2-v1/MINIAODSIM',
			'/QCD_Pt-470to600_Tune4C_13TeV_pythia8/Spring14miniaod-141029_PU40bx50_castor_PLS170_V6AN2-v1/MINIAODSIM',
			'/QCD_Pt-600to800_Tune4C_13TeV_pythia8/Spring14miniaod-141029_PU40bx50_castor_PLS170_V6AN2-v1/MINIAODSIM',
			'/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/Spring14miniaod-141029_PU40bx50_castor_PLS170_V6AN2-v1/MINIAODSIM',
			]
	
	for dataset in QCDHT:
		config.Data.inputDataset = dataset
		config.General.requestName = dataset.replace('/','_')+'_RUNtuples_v01'
		crabCommand('submit', config = config)
