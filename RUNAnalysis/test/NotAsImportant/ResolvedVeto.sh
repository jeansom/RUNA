#!/bin/bash
#python ResolvedVeto.py -r "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-180_80X_V2p3_v06.root" -i "ResolvedAnalysisPlots" -a "RUNATree", -o "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-180_80X_V2p3_v06.root" -n "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-180_80X_V2p3_v06_ResVeto.root" -d "BoostedAnalysisPlots" -t "RUNATree"

#python ResolvedVeto.py -r "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-200_80X_V2p3_v06.root" -i "ResolvedAnalysisPlots" -a "RUNATree", -o "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-200_80X_V2p3_v06.root" -n "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-200_80X_V2p3_v06_ResVeto.root" -d "BoostedAnalysisPlots" -t "RUNATree"

#python ResolvedVeto.py -r "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-220_80X_V2p3_v06.root" -i "ResolvedAnalysisPlots" -a "RUNATree", -o "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-220_80X_V2p3_v06.root" -n "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-220_80X_V2p3_v06_ResVeto.root" -d "BoostedAnalysisPlots" -t "RUNATree"

#python ResolvedVeto.py -r "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-300_80X_V2p3_v06.root" -i "ResolvedAnalysisPlots" -a "RUNATree", -o "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-300_80X_V2p3_v06.root" -n "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-300_80X_V2p3_v06_ResVeto.root" -d "BoostedAnalysisPlots" -t "RUNATree"

for ifile in `ls -1 80XRootFilesUpdated/RUNAnalysis_RPV*`
do
    if [[ $ifile == *"${1}"* ]]
    then
	echo python ../ResolvedVeto.py -r $ifile -i "ResolvedAnalysisPlots" -a "RUNATree", -o $ifile -n $ifile -d "BoostedAnalysisPlots" -t "RUNATree"
    fi
done