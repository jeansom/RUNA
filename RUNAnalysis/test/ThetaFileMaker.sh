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
	python ThetaFileMaker.py -c $chan -m CSVv2CBDMC -d 12417CSVv2CBDMC$chan/
    fi
elif [ $1 -lt 20 ]; 
then
    chan=$(($1%10))
    if [ $chan -lt 9 ];
    then
	python ThetaFileMaker.py -c $chan -m CSVv2BCDMC -d 12417CSVv2BCDMC$chan/
    fi
elif [ $1 -lt 30 ]; 
then
    chan=$(($1%10))
    if [ $chan -lt 9 ];
    then
	python ThetaFileMaker.py -c $chan -m CMVAv2CBDMC -d 12417CMVAv2CBDMC$chan/
    fi
elif [ $1 -lt 40 ]; 
then
    chan=$(($1%10))
    if [ $chan -lt 9 ];
    then
	python ThetaFileMaker.py -c $chan -m CMVAv2BCDMC -d 12417CMVAv2BCDMC$chan/
    fi
fi
    