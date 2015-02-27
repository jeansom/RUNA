

ptBins=( '80to120' '120to170' '170to300' '300to470' '470to600' '600to800' '800to1000' )
#ptBins=( '120to170' '170to300' '300to470' '470to600' '600to800' '800to1000' )
#fi


##############################################
##### Create the python file 
##############################################
for bin in ${ptBins[@]};
do
	#nameCRAB3File=crab3_QCD_Pt-${bin}_Tune4C_13TeV_pythia8_PU40bx50.py
	nameCRAB3File=crab3_QCD_Pt-${bin}_Tune4C_13TeV_pythia8_PU20bx25.py
	if [ -f $nameCRAB3File ]; then
		rm -rf $nameCRAB3File
	fi

	echo "from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'QCD_Pt-"${bin}"_Tune4C_13TeV_pythia8_RUNA_PU40bx50_v01'
#config.General.requestName = 'QCD_Pt-"${bin}"_Tune4C_13TeV_pythia8_RUNA_PU20bx25_v2'
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNtuples_cfg.py'
#config.JobType.pyCfgParams = [ 'outputLabel=RPVSt100tojj_13TeV_pythia8_RUNA_PU40bx50.root' ]
config.JobType.allowNonProductionCMSSW = True

config.Data.inputDataset = '/QCD_Pt-"${bin}"_Tune4C_13TeV_pythia8/Spring14miniaod-141029_PU40bx50_castor_PLS170_V6AN2-v1/MINIAODSIM'
#config.Data.inputDataset = '/QCD_Pt-"${bin}"_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 20
#config.Data.totalUnits = 1000
config.Data.outLFN = '/store/user/algomez/'
#config.Data.ignoreLocality = True
config.Data.publication = True
config.Data.ignoreLocality = True
config.Data.publishDataName = 'RUNA_PU40bx50_v01'
#config.Data.publishDataName = 'QCD_Pt-"${bin}"_Tune4C_13TeV_pythia8_RUNA_PU20bx25_v2'

config.Site.storageSite = 'T3_US_FNALLPC'
" >> ${nameCRAB3File}
	crab submit ${nameCRAB3File}

done
