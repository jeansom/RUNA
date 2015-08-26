##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand
from multiprocessing import Process
config = config()

version = 'v06'

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

config.Site.storageSite = 'T3_US_FNALLPC'

def submit(config):
	try:
		crabCommand('submit', config = config)
	except HTTPException, hte:
		print 'Cannot execute commend'
		print hte.headers

if __name__ == '__main__':


	Samples = [ 


			#### RunIISpring15DR74
			#'/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			#'/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v01-1886d118546a0d39f46d888ed262e31b/USER',
			#'/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			#'/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			#'/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v01-1886d118546a0d39f46d888ed262e31b/USER',
			#'/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			#'/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			#'/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns__v01-5fc672f84cef33a66015627a5c47070b/USER',
			#'/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/mmorris-crab_RUNA_TTJets_v745p1-1886d118546a0d39f46d888ed262e31b/USER',
			#'/ZJetsToQQ_HT600toInf_13TeV-madgraph/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v01p2-1886d118546a0d39f46d888ed262e31b/USER',
			#'/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v01p2-1886d118546a0d39f46d888ed262e31b/USER',
			#'/JetHT/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v01p2-59a8f6968d1faf0a39f7c4c693699d7c/USER',

			#'/RPVSt100tojj_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v02p2-1886d118546a0d39f46d888ed262e31b/USER',
			#'/RPVSt100tobj_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v02p3-1886d118546a0d39f46d888ed262e31b/USER',
			'/RPVSt200tobj_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v02p3-1886d118546a0d39f46d888ed262e31b/USER',
			'/RPVSt350tobj_13TeV_pythia8/algomez-RunIISpring15DR74_RUNA_Asympt25ns_v02p3-1886d118546a0d39f46d888ed262e31b/USER',

			]

	
	for dataset in Samples:
		procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RunIISpring15DR74_RUNA','').replace('mmorris-crab_RUNA_TTJets_v745p1','v01').split('-')[0]+'_'+version
		#procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RUNA', '').split('-')[0]+'_'+version
		config.Data.inputDataset = dataset
		config.General.requestName = procName
		if 'RPV' in dataset: 
			config.Data.splitting = 'FileBased'
			config.Data.unitsPerJob = 1
		elif 'JetHT' in dataset: 
			procName = dataset.split('/')[1]+dataset.split('/')[2].replace('algomez-RunIISpring15DR74_RUNA_Asympt25ns', '_Asympt50ns').split('-')[0]+'_'+version
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 5
			config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_v2.txt'
		else: 
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 10 if 'QCD' in dataset else 100
		config.JobType.pyCfgParams = [ 'PROC='+procName, 'local=0' ]
		#crabCommand('submit', config = config)
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
