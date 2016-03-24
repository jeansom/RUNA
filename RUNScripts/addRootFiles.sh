version="v03_v01p3"
#PUList="PU30BX50 PU20bx25"
ptBinList="Pt_170to300 Pt_300to470 Pt_470to600 Pt_600to800 Pt_800to1000 Pt_1000to1400 Pt_1400to1800 Pt_1800to2400"  
#htBinList="HT-500To1000 HT_1000ToInf"
campaignList="CSA14 PHYS14"
PU=$2
camp="RunIISpring15DR74" #$3

#for PU in $PUList
#do
#	for camp in $campaignList
#	do
if [[ $1 == *"QCD"* ]]; then

	if [[ $1 == *"Pt"* ]]; then
		for bin in $ptBinList
		do
			hadd -f RUNAnalysis_QCD_${bin}_${camp}_${PU}_${version}.root /eos/uscms/store/user/algomez/QCD_${bin}_TuneCUETP8M1_13TeV_pythia8/crab_QCD_${bin}_TuneCUETP8M1_13TeV_pythia8_${PU}*${version}/*/*/*root
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
	#rm -rf RUNAnalysis_RPVSt100tojj_${camp}_${PU}_${version}.root 
	#hadd RUNAnalysis_RPVSt100tojj_GENSIM_${camp}_${PU}_${version}.root /eos/uscms/store/user/algomez/RPVSt100tojj_13TeV_pythia8_GENSIM/crab_RPVSt100tojj_13TeV_pythia8_*${version}/*/*/*root
	hadd -f RUNAnalysis_RPVSt100tojj_${camp}_${PU}_${version}.root /eos/uscms/store/user/algomez/RPVSt100tojj_13TeV_pythia8/crab_RPVSt100tojj_13TeV_pythia8_${camp}_${PU}_${version}/*/*/*root
	#hadd -f RUNAnalysis_RPVSt100tobj_${camp}_${PU}_${version}.root /eos/uscms/store/user/algomez/RPVSt100tobj_pythia8_13TeV/crab_RPVSt100tobj_pythia8_13TeV_${camp}_${PU}_${version}/*/*/*root
	#hadd -f RUNAnalysis_RPVSt350tojj_${camp}_${PU}_${version}.root /eos/uscms/store/user/algomez/RPVSt350tojj_13TeV_pythia8/crab_RPVSt350tojj_13TeV_pythia8_${camp}_${PU}_${version}/*/*/*root
fi
#done 
