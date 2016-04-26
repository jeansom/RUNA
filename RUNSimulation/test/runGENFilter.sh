#!/bin/bash
initialFolder=${PWD}
for mass in 80 90 100 110 120 130 140 150 160 170 180 190 200 210 220 230 240 250 300 350 400 450 500 550 600 650 700 750 800 850 900 950 1000 1100 1200 1300 1400 1500
do
	NAME=RPVStopStopToJets_UDD323_M-${mass}
	workingDir=${initialFolder}/calcFilterEff/${NAME}
	echo "Creating Folder and Files "$workingDir 
	if [ ! -d $workingDir ]; then
		mkdir -p $workingDir
	fi
	cp ${initialFolder}/step0_LHE_cfg.py ${workingDir}/step00_${NAME}_LHE_cfg.py
	cp ${initialFolder}/step0_GEN_SIM_v763.py ${workingDir}/step01_${NAME}_GENSIM_cfg.py
	sed -i 's/HadRPVStop100_UDD312_13TeV_LHE.root/'"${NAME}"'_LHE.root/' ${workingDir}/step00_${NAME}_LHE_cfg.py 
	sed -i 's/HadRPVStop100_UDD323_13TeV_tarball.tar.xz/HadRPVStop'"${mass}"'_UDD323_13TeV_tarball.tar.xz/' ${workingDir}/step00_${NAME}_LHE_cfg.py 
	sed -i 's/HadRPVStop100_UDD312_13TeV_LHE.root/'"${NAME}"'_LHE.root/' ${workingDir}/step01_${NAME}_GENSIM_cfg.py 
	sed -i 's/HadRPVStop100_UDD312_13TeV_GENSIM.root/'"${NAME}"'_GENSIM.root/' ${workingDir}/step01_${NAME}_GENSIM_cfg.py 
	if [ ${mass} -gt 250 ]; then
		sed -i 's/process.ProductionFilterSequence = cms.Sequence(process.generator+process.htFilter)/process.ProductionFilterSequence = cms.Sequence(process.generator)/' ${workingDir}/step01_${NAME}_GENSIM_cfg.py
	fi
	cd ${workingDir}
	echo "Running LHE"
	cmsRun step00_${NAME}_LHE_cfg.py &> lhe.log; cmsRun step01_${NAME}_GENSIM_cfg.py &> gen.log; 
	cd ${initialFolder}
done
