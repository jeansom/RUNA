##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
config = config()

version = 'v01'

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

def submit(config):
	try:
		crabCommand('submit', config = config)
	except HTTPException, hte:
		print 'Cannot execute commend'
		print hte.headers

if __name__ == '__main__':

	from CRABAPI.RawCommand import crabCommand
	from multiprocessing import Process

	Samples = [ 

			### Phys14
#			'/RPVSt100tojj_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_V04-4ec6b714e09c1d3232adb8ad471fe07b/USER',
#			'/RPVSt100tobj_pythia8_13TeV/algomez-RUNA_PHYS14_PU20bx25_v04-4ec6b714e09c1d3232adb8ad471fe07b/USER',
#			'/RPVSt350tojj_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v04-4ec6b714e09c1d3232adb8ad471fe07b/USER',
#			'/QCD_Pt-170to300_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_V04-4ec6b714e09c1d3232adb8ad471fe07b/USER',
#			'/QCD_Pt-300to470_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v04-4ec6b714e09c1d3232adb8ad471fe07b/USER',
#			'/QCD_Pt-470to600_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v04-4ec6b714e09c1d3232adb8ad471fe07b/USER',
#			'/QCD_Pt-600to800_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v04-4ec6b714e09c1d3232adb8ad471fe07b/USER',
#			'/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v04-4ec6b714e09c1d3232adb8ad471fe07b/USER',
#			'/QCD_Pt-1000to1400_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v04-4ec6b714e09c1d3232adb8ad471fe07b/USER',
#			'/QCD_Pt-1400to1800_Tune4C_13TeV_pythia8/algomez-RUNA_PHYS14_PU20bx25_v04-4ec6b714e09c1d3232adb8ad471fe07b/USER',

			#### RunIISpring15DR74
			'/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			'/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			'/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			#'/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v01-5fc672f84cef33a66015627a5c47070b/USER',
			'/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			'/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			'/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',

			'/RPVSt100tojj_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			'/RPVSt200tojj_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			'/RPVSt350tojj_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',

			]

	
	for dataset in Samples:
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RUNA', '').split('-')[0]+'_'+version
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
		#crabCommand('submit', config = config)
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
