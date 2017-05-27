#!/bin/bash


export SCRAM_ARCH=slc6_amd64_gcc491
export VO_CMS_SW_DIR=/cms/base/cmssoft
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`

if [ $1 -lt 11 ]; 
then
    chan=$(($1%11))
    python ThetaFileMakerResVeto26.py -c $chan -m CSVv2M_Before_CBDMC -d /31017/MC2666ResVeto26/BeforeTheta/$chan -b 10 #-j "900<HT&HT<1400"
elif [ $1 -lt 22 ]; 
then
    chan=$(($1%11))
    python ThetaFileMakerResVeto26.py -c $chan -m CSVv2M_Before_BCDDMC -d /31017/MC2666ResVeto/BeforeTheta/$chan -b 10 #-j "900<HT&HT<1400"
elif [ $1 -lt 33 ]; 
then
    chan=$(($1%11))
    python ThetaFileMakerResVeto26.py -c $chan -m CMVAv2M_Before_CBDMC -d /31017/MC2666ResVeto/BeforeTheta/$chan -b 10 #-j "900<HT&HT<1400"
elif [ $1 -lt 44 ]; 
then
    chan=$(($1%11))
    python ThetaFileMakerResVeto26.py -c $chan -m CMVAv2M_Before_BCDMC -d /31017/MC2666ResVeto/BeforeTheta/$chan -b 10 #-j "900<HT&HT<1400"
fi
#elif [ $1 -lt 55 ]; 
#then
#    chan=$(($1%11))
#    python ThetaFileMakerResVeto26.py -c $chan -m CSVv2M_Before_CBDMC_HT2 -d /31017/MC2666ResVeto/BeforeTheta/$chan -b 10 #-j "1400<HT&HT<1900"
#elif [ $1 -lt 66 ]; 
#then
#    chan=$(($1%11))
#    python ThetaFileMakerResVeto26.py -c $chan -m CSVv2M_Before_BCDDMC_HT2 -d /31017/MC2666ResVeto/BeforeTheta/$chan -b 10 #-j "1400<HT&HT<1900"
#elif [ $1 -lt 77 ]; 
#then
#    chan=$(($1%11))
#    python ThetaFileMakerResVeto26.py -c $chan -m CMVAv2M_Before_CBDMC_HT2 -d /31017/MC2666ResVeto/BeforeTheta/$chan -b 10 #-j "1400<HT&HT<1900"
#elif [ $1 -lt 88 ]; 
#then
#    chan=$(($1%11))
#    python ThetaFileMakerResVeto26.py -c $chan -m CMVAv2M_Before_BCDMC_HT2 -d /31017/MC2666ResVeto/BeforeTheta/$chan -b 10 #-j "1400<HT&HT<1900"
#elif [ $1 -lt 99 ]; 
#then
#    chan=$(($1%11))
#    python ThetaFileMakerResVeto26.py -c $chan -m CSVv2M_Before_CBDMC_HT3 -d /31017/MC2666ResVeto/BeforeTheta/$chan -b 10 #-j "1900<HT"
#elif [ $1 -lt 110 ]; 
#then
#    chan=$(($1%11))
#    python ThetaFileMakerResVeto26.py -c $chan -m CSVv2M_Before_BCDDMC_HT3 -d /31017/MC2666ResVeto/BeforeTheta/$chan -b 10 #-j "1900<HT"
#elif [ $1 -lt 121 ]; 
#then
#    chan=$(($1%11))
#    python ThetaFileMakerResVeto26.py -c $chan -m CMVAv2M_Before_CBDMC_HT3 -d /31017/MC2666ResVeto/BeforeTheta/$chan -b 10 #-j "1900<HT"
#elif [ $1 -lt 132 ]; 
#then
#    chan=$(($1%11))
#    python ThetaFileMakerResVeto26.py -c $chan -m CMVAv2M_Before_BCDMC_HT3 -d /31017/MC2666ResVeto/BeforeTheta/$chan -b 10 #-j "1900<HT"
#fi