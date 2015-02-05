

ptBins=( '80to120' '120to170' '170to300' '300to470' '470to600' '600to800' '800to1000' )
#ptBins=( '120to170' '170to300' '300to470' '470to600' '600to800' '800to1000' )
#fi


##############################################
##### Create the python file 
##############################################
for bin in ${ptBins[@]};
do
	nameCRAB3File=crab3_QCD_Pt-${bin}_Tune4C_13TeV_pythia8_PU40bx50.py
	if [ -f $nameCRAB3File ]; then
		rm -rf $nameCRAB3File
	fi

	echo "from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.requestName = 'QCD_Pt-"${bin}"_Tune4C_13TeV_pythia8_RUNPlots_PU40bx50_v0'
#config.General.workArea = 'crab_projects'

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'RUNAPlots_cfg.py'
config.JobType.pyCfgParams = [ 'QCD_Pt-"${bin}"_Tune4C_13TeV_pythia8_PU40bx50' ]
config.JobType.allowNonProductionCMSSW = True

config.section_('Data')
config.Data.inputDataset = '/QCD_Pt-"${bin}"_Tune4C_13TeV_pythia8/algomez-QCD_Pt-"${bin}"_Tune4C_13TeV_pythia8_EDMNtuple_PU40bx50_v3-12973f35cd7b5b825f439eacc298d434/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 20
#config.Data.totalUnits = 1000
config.Data.outLFN = '/store/user/algomez/'
#config.Data.ignoreLocality = True
config.Data.publication = False
config.Data.ignoreLocality = True

config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'
" >> ${nameCRAB3File}
	crab submit ${nameCRAB3File}

done
