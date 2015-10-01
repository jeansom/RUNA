##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from httplib import HTTPException

config = config()

version = 'v00p2'

config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNFullAnalysis_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False
config.Data.ignoreLocality = True

config.Site.storageSite = 'T3_US_FNALLPC'

def submit(config):
	try:
		crabCommand('submit', config = config)
	except HTTPException, hte:
		print 'Cannot execute commend'
		print hte.headers

if __name__ == '__main__':

	from CRABAPI.RawCommand import crabCommand

	Samples = [ 


			#### RunIISpring15DR74
#			'/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v06-b4868673ff475f0715ff7cbd0e4e7e14/USER',
			'/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v06-b4868673ff475f0715ff7cbd0e4e7e14/USER',
#			'/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v06-b4868673ff475f0715ff7cbd0e4e7e14/USER',
#			'/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v06-b4868673ff475f0715ff7cbd0e4e7e14/USER',
#			'/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v06-b4868673ff475f0715ff7cbd0e4e7e14/USER',
#			'/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v06-b4868673ff475f0715ff7cbd0e4e7e14/USER',
#			'/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v06-b4868673ff475f0715ff7cbd0e4e7e14/USER',
#			'/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v06-b4868673ff475f0715ff7cbd0e4e7e14/USER',
#			'/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v06-b4868673ff475f0715ff7cbd0e4e7e14/USER',
#			'/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v06-b4868673ff475f0715ff7cbd0e4e7e14/USER',
#
#			'/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt50ns_v06-1c38a9eb9711f82aabe7a19f984a8f27/USER',
#			'/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt50ns_v06-1c38a9eb9711f82aabe7a19f984a8f27/USER',
#			'/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt50ns_v06-1c38a9eb9711f82aabe7a19f984a8f27/USER',
#			'/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt50ns_v06-1c38a9eb9711f82aabe7a19f984a8f27/USER',
#			'/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt50ns_v06-1c38a9eb9711f82aabe7a19f984a8f27/USER',
#			'/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt50ns_v06-1c38a9eb9711f82aabe7a19f984a8f27/USER',
#			'/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt50ns_v06-1c38a9eb9711f82aabe7a19f984a8f27/USER',
#			'/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt50ns_v06-1c38a9eb9711f82aabe7a19f984a8f27/USER',
#			'/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt50ns_v06-1c38a9eb9711f82aabe7a19f984a8f27/USER',
#
#			'/JetHT/algomez-Run2015B-PromptReco-v1_RUNA_v06-0cc1d310cda5930bd3b3a68493077b41/USER',			
#			'/JetHT/algomez-Run2015C-PromptReco-v1_RUNA_v06-0cc1d310cda5930bd3b3a68493077b41/USER',			
#			'/JetHT/algomez-Run2015D-PromptReco-v3_RUNA_v06-0cc1d310cda5930bd3b3a68493077b41/USER',			

#			'/RPVSt100tojj_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v03-b4868673ff475f0715ff7cbd0e4e7e14/USER',
			#'/RPVSt100tobj_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v03-b4868673ff475f0715ff7cbd0e4e7e14/USER',
#			'/RPVSt200tobj_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v03-b4868673ff475f0715ff7cbd0e4e7e14/USER',
#			'/RPVSt350tobj_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v03-b4868673ff475f0715ff7cbd0e4e7e14/USER',


			]

	
	from multiprocessing import Process
	for dataset in Samples:
		config.Data.inputDataset = dataset
		if 'JetHT' in dataset: 
			procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-','').replace('RUNA','').replace('-0cc1d310cda5930bd3b3a68493077b41','')+'_'+version
			if 'Run2015B' in dataset:
				config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-255031_13TeV_PromptReco_Collisions15_50ns_JSON.txt'
			else:
				config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-256869_13TeV_PromptReco_Collisions15_25ns_JSON.txt'

		else: procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RunIISpring15DR74_RUNA','').split('-')[0]+'_'+version
		config.General.requestName = procName
		config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0' ]
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
