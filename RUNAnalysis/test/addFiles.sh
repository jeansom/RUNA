version="v03_v06"
PUList="PU40bx50 PU20bx25"
ptBinList="Pt-170to300 Pt-300to470 Pt-470to600 Pt-600to800 Pt-800to1000 Pt-1000to1400 Pt-1400to1800"  
htBinList="HT-500To1000 HT_1000ToInf"
campaignList="CSA14 PHYS14"
PU=$2
camp=$3

#for PU in $PUList
#do
#	for camp in $campaignList
#	do
if [[ $1 == *"QCD"* ]]; then

	if [[ $1 == *"Pt"* ]]; then
		for bin in $ptBinList
		do
			hadd -f RUNAnalysis_QCD_${bin}_${camp}_${PU}_${version}.root /eos/uscms/store/user/algomez/QCD_${bin}_Tune4C_13TeV_pythia8/crab_QCD_${bin}_Tune4C_13TeV_pythia8_${camp}_${PU}_${version}/*/*/*root
		done
		hadd -f RUNAnalysis_QCDPtAll_${camp}_${PU}_${version}.root RUNAnalysis_QCD_Pt*_${camp}_${PU}_${version}.root
	else
		for bin in $htBinList
		do
			hadd -f RUNAnalysis_QCD_${bin}_${camp}_${PU}_${version}.root /eos/uscms/store/user/algomez/QCD_${bin}_13TeV-madgraph/crab_QCD_${bin}_13TeV-madgraph_${camp}_${PU}_${version}/*/*/*root
		done
		hadd -f RUNAnalysis_QCDHTAll_${camp}_${PU}_${version}.root RUNAnalysis_QCD_HT*_${camp}_${PU}_${version}.root
	fi

else
	#hadd -f RUNAnalysis_RPVSt100tojj_GENSIM_${camp}_${PU}_${version}.root /eos/uscms/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/crab_RPVSt100tojj_13TeV_pythia8_*${version}/*/*/*root
	hadd -f RUNAnalysis_RPVSt100tojj_${camp}_${PU}_${version}.root /eos/uscms/store/user/algomez/RPVSt100tojj_13TeV_pythia8/crab_RPVSt100tojj_13TeV_pythia8_*${version}/*/*/*root
fi
#	done
#done 
