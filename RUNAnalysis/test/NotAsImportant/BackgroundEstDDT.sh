#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc491
export VO_CMS_SW_DIR=/cms/base/cmssoft
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`

if [ $1 -eq 0 ];
then
    python BackgroundEstDDT.py -c "b0t0"
elif [ $1 -eq 1 ];
then
    python BackgroundEstDDT.py -c "b1t0"
elif [ $1 -eq 2 ];
then
    python BackgroundEstDDT.py -c "b2t0"
elif [ $1 -eq 3 ];
then
    python BackgroundEstDDT.py -c "b0t1"
elif [ $1 -eq 4 ];
then
    python BackgroundEstDDT.py -c "b1t1"
elif [ $1 -eq 5 ];
then
    python BackgroundEstDDT.py -c "b2t1"
elif [ $1 -eq 6 ];
then
    python BackgroundEstDDT.py -c "b0t2"
elif [ $1 -eq 7 ];
then
    python BackgroundEstDDT.py -c "b1t2"
elif [ $1 -eq 8 ];
then
    python BackgroundEstDDT.py -c "b2t2"
elif [ $1 -eq 9 ];
then
    python BackgroundEstDDT.py -c "pres"
fi