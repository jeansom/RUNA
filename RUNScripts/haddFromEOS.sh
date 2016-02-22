#! /bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: source haddFromEOS.sh option1 option2"
	echo " |---> option1 : NAME OF FOLDER IN EOS"
	echo " |---> option2 : name_of_rootfile.root"
	echo "For example: source haddFromEOS.sh RPVStopStopToJets_UDD312_M-100-madgraph/crab_RPVStopStopToJets_UDD312_M-100-madgraph_v02jetIdL/151213_185004/ test.root"

else
	eosFolder=$1
	haddFile=$2
	arrayOfFiles=()
	myEOSLS() { eosls -l /store/user/"$USER"/$1; }
	numDir=($(myEOSLS ${eosFolder} | awk '{print $9}'))
	for i in "${numDir[@]}"
	do
		eachFile=($(myEOSLS ${eosFolder}/$i | awk '{ print $9 }'))
		for j in "${eachFile[@]}"
		do 
			echo ${eosFolder}/${i}/${j}
			arrayOfFiles+="root://cmseos.fnal.gov//store/user/${USER}/${eosFolder}/${i}/${j} "
		done
	done
	hadd -f $haddFile $arrayOfFiles

fi


