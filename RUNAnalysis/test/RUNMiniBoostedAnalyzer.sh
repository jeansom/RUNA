#!/bin/bash


export SCRAM_ARCH=slc6_amd64_gcc491
export VO_CMS_SW_DIR=/cms/base/cmssoft
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`

if [ $1 -eq 8 ]; then
    python RUNBkgEstimationUDD323.py -m 100 -d UDD323 -v v05
fi
if [ $1 -eq 1 ]; then
    python RUNMiniBkgEstimationUDD323.py -m 100 -d UDD323 -p single -s QCDPtAll -g pruned -r low -v v05
fi
if [ $1 -eq 2 ]; then
    python RUNMiniBkgEstimationUDD323.py -m 100 -d UDD323 -p single -s TTJets -g pruned -r low -v v05
fi
if [ $1 -eq 3 ]; then
    python RUNMiniBkgEstimationUDD323.py -m 100 -d UDD323 -p single -s WJetsToQQ -g pruned -r low -v v05
fi
if [ $1 -eq 4 ]; then
    python RUNMiniBkgEstimationUDD323.py -m 100 -d UDD323 -p single -s WWTo4Q -g pruned -r low -v v05
fi
if [ $1 -eq 5 ]; then
    python RUNMiniBkgEstimationUDD323.py -m 100 -d UDD323 -p single -s WZ -g pruned -r low -v v05
fi 
if [ $1 -eq 6 ]; then
    python RUNMiniBkgEstimationUDD323.py -m 100 -d UDD323 -p single -s ZJetsToQQ -g pruned -r low -v v05
fi
if [ $1 -eq 7 ]; then
    python RUNMiniBkgEstimationUDD323.py -m 100 -d UDD323 -p single -s ZZTo4Q -g pruned -r low -v v05
fi
if [ $1 -eq 0 ]; then
    python RUNMiniBkgEstimationUDD323.py -m 100 -d UDD323 -p single -s DATA -g pruned -r low -v v05
fi