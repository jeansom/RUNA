#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc491
export VO_CMS_SW_DIR=/cms/base/cmssoft
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`

# Runs over all combinations of channel and scale

if [ $1 -lt 10 ]; 
then
    chan=$(($1%10))
    scale=$(($(($1-$chan))/10))
    if [ $chan -ne 10 ];
    then
	python ThetaFileMakerQCD26MassSplit.py -c $chan -s $scale -m CBDPtMC -d /52617/80/$chan\_$scale -b 10 -l False -j "1."
    fi
elif [ $1 -lt 20 ]; 
then
    chan=$(($1%10))
    scale=$(($(($1-$chan))/10))
    if [ $chan -ne 10 ];
    then
	python ThetaFileMakerQCD26MassSplit.py -c $chan -s $scale -m CBDPtMC -d /52617/80/$chan\_$scale -b 10 -l False -j "1."
    fi
elif [ $1 -lt 30 ]; 
then
    chan=$(($1%10))
    scale=$(($(($1-$chan))/10))
    if [ $chan -ne 10 ];
    then
	python ThetaFileMakerQCD26MassSplit.py -c $chan -s $scale -m CBDPtMC -d /52617/80/$chan\_$scale -b 10 -l False -j "1."
    fi
elif [ $1 -lt 40 ]; 
then
    chan=$(($1%10))
    scale=$(($(($1-$chan))/10))
    if [ $chan -ne 10 ];
    then
	python ThetaFileMakerQCD26MassSplit.py -c $chan -s $scale -m CBDPtMC -d /52617/80/$chan\_$scale -b 10 -l False -j "1."
    fi
elif [ $1 -lt 50 ]; 
then
    chan=$(($1%10))
    scale=$(($(($1-$chan))/10))
    if [ $chan -ne 10 ];
    then
	python ThetaFileMakerQCD26MassSplit.py -c $chan -s $scale -m CBDPtMC -d /52617/80/$chan\_$scale -b 10 -l False -j "1."
    fi
elif [ $1 -lt 60 ]; 
then
    chan=$(($1%10))
    scale=$(($(($1-$chan))/10))
    if [ $chan -ne 10 ];
    then
	python ThetaFileMakerQCD26MassSplit.py -c $chan -s $scale -m CBDPtMC -d /52617/80/$chan\_$scale -b 10 -l False -j "1."
    fi
elif [ $1 -lt 70 ]; 
then
    chan=$(($1%10))
    scale=$(($(($1-$chan))/10))
    if [ $chan -ne 10 ];
    then
	python ThetaFileMakerQCD26MassSplit.py -c $chan -s $scale -m CBDPtMC -d /52617/80/$chan\_$scale -b 10 -l False -j "1."
    fi
elif [ $1 -lt 80 ]; 
then
    chan=$(($1%10))
    scale=$(($(($1-$chan))/10))
    if [ $chan -ne 10 ];
    then
	python ThetaFileMakerQCD26MassSplit.py -c $chan -s $scale -m CBDPtMC -d /52617/80/$chan\_$scale -b 10 -l False -j "1."
    fi
elif [ $1 -lt 90 ]; 
then
    chan=$(($1%10))
    scale=$(($(($1-$chan))/10))
    if [ $chan -ne 10 ];
    then
	python ThetaFileMakerQCD26MassSplit.py -c $chan -s $scale -m CBDPtMC -d /52617/80/$chan\_$scale -b 10 -l False -j "1."
    fi
elif [ $1 -lt 100 ]; 
then
    chan=$(($1%10))
    scale=$(($(($1-$chan))/10))
    if [ $chan -ne 10 ];
    then
	python ThetaFileMakerQCD26MassSplit.py -c $chan -s $scale -m CBDPtMC -d /52617/80/$chan\_$scale -b 10 -l False -j "1."
    fi
fi