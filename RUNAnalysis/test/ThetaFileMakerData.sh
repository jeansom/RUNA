#!/bin/bash


export SCRAM_ARCH=slc6_amd64_gcc491
export VO_CMS_SW_DIR=/cms/base/cmssoft
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`

if [ $1 -lt 10 ]; 
then
    chan=$(($1%10))
    if [ $chan -lt 9 ];
    then 
	python ThetaFileMakerQCD.py -c $chan -m CSVv2M_CBDMC -d /21217PtRewt/BeforeTheta/$chan -b 10
    fi
elif [ $1 -lt 20 ]; 
then
    chan=$(($1%10))
    if [ $chan -lt 9 ];
    then
	python ThetaFileMakerQCD.py -c $chan -m CSVv2M_BCDMC -d /21217PtRewt/BeforeTheta/$chan -b 10
    fi
elif [ $1 -lt 30 ]; 
then
    chan=$(($1%10))
    if [ $chan -lt 9 ];
    then
	python ThetaFileMakerQCD.py -c $chan -m CMVAv2M_CBDMC -d /21217PtRewt/BeforeTheta/$chan -b 10
    fi
elif [ $1 -lt 40 ]; 
then
    chan=$(($1%10))
    if [ $chan -lt 9 ];
    then
	python ThetaFileMakerQCD.py -c $chan -m CMVAv2M_BCDMC -d /21217PtRewt/BeforeTheta/$chan -b 10
    fi
#elif [ $1 -lt 50 ]; 
#then
#    chan=$(($1%10))
#    if [ $chan -lt 9 ];
#    then
#	python ThetaFileMakerQCD.py -c $chan -m CMVAv2TCBDMC -d /21217PtRewt/BeforeTheta/$chan
#    fi
#elif [ $1 -lt 60 ]; 
#then
#    chan=$(($1%10))
#    if [ $chan -lt 9 ];
#    then
#	python ThetaFileMakerQCD.py -c $chan -m CMVAv2TBCDMC -d /21217PtRewt/BeforeTheta/$chan
#    fi
fi
    