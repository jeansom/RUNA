#! /bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: source haddFromEOS.sh option1 option2"
	echo " |---> option1 : NAME OF FOLDER IN EOS"
	echo " |---> option2 : name_of_rootfile.root"
	echo "For example: source haddFromEOS.sh RPVStopStopToJets_UDD312_M-100-madgraph/crab_RPVStopStopToJets_UDD312_M-100-madgraph_v02jetIdL/151213_185004/ test.root"

else
	eosFolder=$1
	haddFile=$2
	myEOSLS() { eosls -l /store/user/"$USER"/$1; }
	numDir=($(myEOSLS ${eosFolder} | awk '{print $9}'))
	arrayOfAllFiles=()
	for i in "${numDir[@]}"
	do
		arrayOfFiles=()
		eachFile=($(myEOSLS ${eosFolder}/$i | awk '{ print $9 }'))
		for j in "${eachFile[@]}"
		do 
			if [[ "${j}" != "failed" ]] 
			then 
				echo ${eosFolder}/${i}/${j}
				if [ "${#eachFile[@]}" -gt 1 ]; then
					arrayOfFiles+="root://cmseos.fnal.gov//store/user/${USER}/${eosFolder}/${i}/${j} "
				else
					arrayOfAllFiles+="root://cmseos.fnal.gov//store/user/${USER}/${eosFolder}/${i}/${j} "
				fi
			fi
		done
		if [ "${#eachFile[@]}" -gt 1 ]; then
			echo "Making tmp"${i}${haddFile}" file"
			hadd -f tmp${i}${haddFile} $arrayOfFiles
		fi
	done
	if [ "${#arrayOfAllFiles[@]}" -gt 0 ]; then
		hadd -f $haddFile $arrayOfAllFiles
		echo "test"
	else
		hadd -f $haddFile tmp*${haddFile}
		rm tmp*${haddFile}
	fi

fi
