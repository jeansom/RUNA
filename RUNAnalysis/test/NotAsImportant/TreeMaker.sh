#!/bin/bash


export SCRAM_ARCH=slc6_amd64_gcc491
export VO_CMS_SW_DIR=/cms/base/cmssoft
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`


if [ $1 -eq 0 ];
then
    python TreeMaker.py -o "80XRootFilesUpdated/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06.root" -n "80XRootFilesUpdated/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut4.root" -d "BoostedAnalysisPlots" -t "RUNATree"
elif [ $1 -eq 1 ];
then
    python TreeMaker.py -o "80XRootFiles/RUNAnalysis_JetHT_Run2016E_80X_V2p4_v05.root" -n "80XRootFiles/RUNAnalysis_JetHT_Run2016E_80X_V2p4_v05_cut.root" -d "BoostedAnalysisPlots" -t "RUNATree"
elif [ $1 -eq 2 ];
then
    python TreeMaker.py -o "80XRootFiles/RUNAnalysis_JetHT_Run2016F1_80X_V2p4_v05.root" -n "80XRootFiles/RUNAnalysis_JetHT_Run2016F1_80X_V2p4_v05_cut.root" -d "BoostedAnalysisPlots" -t "RUNATree"
elif [ $1 -eq 3 ];
then
    python TreeMaker.py -o "80XRootFiles/RUNAnalysis_JetHT_Run2016F2_80X_V2p4_v05.root" -n "80XRootFiles/RUNAnalysis_JetHT_Run2016F2_80X_V2p4_v05_cut.root" -d "BoostedAnalysisPlots" -t "RUNATree"
elif [ $1 -eq 4 ];
then
    python TreeMaker.py -o "80XRootFiles/RUNAnalysis_JetHT_Run2016F_80X_V2p4_v05.root" -n "80XRootFiles/RUNAnalysis_JetHT_Run2016F_80X_V2p4_v05_cut.root" -d "BoostedAnalysisPlots" -t "RUNATree"
elif [ $1 -eq 5 ];
then
    python TreeMaker.py -o "80XRootFiles/RUNAnalysis_JetHT_Run2016G_80X_V2p4_v05.root" -n "80XRootFiles/RUNAnalysis_JetHT_Run2016G_80X_V2p4_v05_cut.root" -d "BoostedAnalysisPlots" -t "RUNATree"
elif [ $1 -eq 6 ];
then
    python TreeMaker.py -o "80XRootFiles/RUNAnalysis_JetHT_Run2016H2_80X_V2p4_v05.root" -n "80XRootFiles/RUNAnalysis_JetHT_Run2016H2_80X_V2p4_v05_cut.root" -d "BoostedAnalysisPlots" -t "RUNATree"
elif [ $1 -eq 7 ];
then
    python TreeMaker.py -o "80XRootFiles/RUNAnalysis_JetHT_Run2016B_80X_V2p4_v05.root" -n "80XRootFiles/RUNAnalysis_JetHT_Run2016B_80X_V2p4_v05_cut.root" -d "BoostedAnalysisPlots" -t "RUNATree"
fi