#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc491
export VO_CMS_SW_DIR=/cms/base/cmssoft
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`

#if [ $1 -lt 10 ]; 
#then
#    chan=$(($1%10))
#    scale=$(($(($1-$chan))/10))
#    if [ $chan -ne 10 ];
#    then
#	python ThetaFileMakerQCD26MassSplit.py -c $chan -s $scale -m CBDMC -d /42917/MASSTFBTAGNJetsG1/$chan\_$scale -b 10 -l False -j "numJets>1"
#    fi
if [ $1 -lt 10 ]; 
then
    chan=$(($1%10))
    scale=$(($(($1-$chan))/10))
    if [ $chan -ne 10 ];
    then
	python ThetaFileMakerQCD26MassEta.py -c $chan -s $scale -m CBDMC -d /5217/MCETAEST/$chan\_$scale -b 5 -l False -j "numJets==2"
    fi
#elif [ $1 -lt 30 ]; 
#then
#    chan=$(($1%10))
#    scale=$(($(($1-$chan))/10))
#    if [ $chan -ne 10 ];
#    then
#	python ThetaFileMakerQCD26MassSplit.py -c $chan -s $scale -m CBDMC -d /42917/MASSTFBTAGNJetsG2/$chan\_$scale -b 10 -l False -j "numJets>2"
#    fi
fi