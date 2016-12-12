version="v02"
ptBinList="120to170 170to300 300to470 470to600 600to800 800to1000 1000to1400 1400to1800 1800to2400 2400to3200 3200toInf"  
htBinList="300to500 500to700 700to1000 1000to1500 1500to2000 2000toInf"
RPVmass='80 90 100 110 1100 120 1200 140 170 180 190 230 240 300 350 400 450 500 550 600 650 700 750 800 900'

if [[ $1 == *"RPV"* ]]; then
	
	for mass in $RPVmass
	do 
		folder=$(ls -td ~/EOS/B2GAnaFW_80X_V2p1/RPV*M-${mass}_*/*${version}/* | head -1 )
		nohup hadd -f RUNAnalysis_RPVStopStopToJets_UDD312_M-${mass}_80X_V2p1_${version}.root $folder/00*/*root &> tmp${mass} &
		echo 'Hadding files from: '$folder 
	done
elif [[ $1 == *"QCD"* ]]; then

	if [[ $1 == *"Pt"* ]]; then
		for bin in $ptBinList
		do
			folder=$(ls -td ~/EOS/B2GAnaFW_80X_V2p1/QCD_Pt*${bin}*/*${version}/* | head -1 )
			nohup hadd -f RUNAnalysis_QCDPt${bin}_80X_V2p1_${version}.root $folder/00*/*root &> tmp${bin} &
			echo 'Hadding files from: '$folder 
		done
	else
		for bin in $htBinList
		do
			folder=$(ls -td ~/EOS/B2GAnaFW_80X_V2p1/QCD_HT*${bin}*/*${version}/* | head -1 )
			nohup hadd -f RUNAnalysis_QCDHT${bin}_80X_V2p1_${version}.root $folder/00*/*root &> tmp${bin} &
			echo 'Hadding files from: '$folder 
		done
	fi

elif [[ $1 == *"JetHT"* ]]; then

	folder=$(ls -td ~/EOS/B2GAnaFW_80X_V2p1/JetHT/*${2}*${version}/* | head -1 )
	nohup hadd -f RUNAnalysis_JetHT_Run2016${2}_V2p1_${version}.root $folder/00*/*root &> tmpJetHT${2} &
	echo 'Hadding files from: '$folder 

else
	folder=$(ls -td ~/EOS/B2GAnaFW_80X_V2p1/*${1}*/*${version}/* | head -1 )
	nohup hadd -f RUNAnalysis_${1}_80X_V2p1_${version}.root $folder/00*/*root &> tmp${1} &
	echo 'Hadding files from: '$folder 

fi
