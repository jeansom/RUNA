#!/bin/bash 

###########################################################################
###
###  Simple bash script to create python files for simulation.
###
###  Alejandro Gomez Espinosa
###  gomez@physics.rutgers.edu
###
###  How to run: 
###  source createJobs_CRAB.sh
###  (If it is an executable (chmod +x createJobs.sh):
###  ./createJobs_CRAB.sh 
###
###  You must change the PARAMETERS according with your needs. 
###  Initially is the only part that you should modify.
###
###########################################################################

######################################
### PARAMETERS
#####################################

stop1=200	## You can use this parameters later to make everything simpler. 
stop2=250	## You can use this parameters later to make everything simpler. Now I am not using them at all

totalNumberEvents=200000

#Name=RPVSt${stop1}tojj_13TeV_pythia8
Name=RPVStopStopToJets_UDD312_M-${stop1}-madgraph
LHEFile=/store/user/algomez/lhe/RPVStop${stop1}_UDD312_13TeV_200k.lhe					#### DONT USE the entire eos path!!!!!

PU=( 'Asympt25ns' ) # 'Asympt50ns' )									#### You can remove the PU scenario that you are not going to use.


#####################################################
#### Here is where the code starts.. 
#### Initially you shouldn't modify this part
#####################################################
echo " Creating directories..."
Main_Dir=$PWD 
####### Working directory
Working_Dir=${Main_Dir}/${Name}	
if [ -d $Working_Dir ]; then
	rm -rf $Working_Dir
	mkdir -p $Working_Dir
else
	mkdir -p $Working_Dir
fi

cd $Working_Dir/

user=`echo $USER`
sed -i 's/algomez/'"${user}"'/g' *

##############################################
##### Create the python file for Ntuples
##############################################

echo " Creating python file for GEN-SIM .. "
step0PythonFile="step0_${Name}_LHE_GEN_SIM.py"
cp ${Main_Dir}/step0_LHE_GEN_SIM.py  ${step0PythonFile}

sed -i 's,/store/user/algomez/lhe/RPVSt100tojj_ISR2j_13TeV.lhe,'"${LHEFile}"',' ${step0PythonFile}
sed -i 's/OUTPUT/'"${Name}"'_GEN/' ${step0PythonFile}

echo " Creating python file for RAWSIM (different PU scenarios).. "
step1PythonFile="step1_${Name}_DIGI_LI_DIGI2RAW_HLT_"
cp ${Main_Dir}/step1_DIGI_LI_DIGI2RAW_HLT.py  ${step1PythonFile}'Asympt50ns.py'
cp ${Main_Dir}/step1_DIGI_LI_DIGI2RAW_HLT.py  ${step1PythonFile}'Asympt25ns.py'
cp ${Main_Dir}/MinBias_TuneCUETP8M1_13TeV-pythia8_cfi.py  . 

sed -i 's/inputFile/'"${Name}"'_RAWSIM_Asympt50ns/' ${step1PythonFile}'Asympt50ns.py'
sed -i 's/inputFile/'"${Name}"'_RAWSIM_Asympt25ns/' ${step1PythonFile}'Asympt25ns.py'
sed -i 's/MCRUN2_74_V7A/MCRUN2_74_V9/' ${step1PythonFile}'Asympt25ns.py'
sed -i 's/mix_2015_50ns_Startup_PoissonOOTPU_cfi/mix_2015_25ns_Startup_PoissonOOTPU_cfi/' ${step1PythonFile}'Asympt25ns.py'
sed -i 's/HLT_50ns_5e33_v1_cff/HLT_25ns14e33_v1_cff/' ${step1PythonFile}'Asympt25ns.py'
sed -i 's/customisePostLS1_50ns/customisePostLS1/' ${step1PythonFile}'Asympt25ns.py'

echo " Creating python file for AODSIM (different PU scenarios).. "
step2PythonFile="step2_${Name}_RAW2DIGI_L1Reco_RECO_"
cp ${Main_Dir}/step2_RAW2DIGI_L1Reco_RECO.py  ${step2PythonFile}'Asympt50ns.py'
cp ${Main_Dir}/step2_RAW2DIGI_L1Reco_RECO.py  ${step2PythonFile}'Asympt25ns.py'
sed -i 's/inputFile/'"${Name}"'_AODSIM_Asympt50ns/' ${step2PythonFile}'Asympt50ns.py'
sed -i 's/inputFile/'"${Name}"'_AODSIM_Asympt25ns/' ${step2PythonFile}'Asympt25ns.py'
sed -i 's/MCRUN2_74_V9A/MCRUN2_74_V9/' ${step2PythonFile}'Asympt25ns.py'
sed -i 's/customisePostLS1_50ns/customisePostLS1/' ${step2PythonFile}'Asympt25ns.py'

echo " Creating python file for MiniAOD (different PU scenarios).. "
step3PythonFile="step3_${Name}_MiniAOD_"
cp ${Main_Dir}/step3_MiniAOD.py  ${step3PythonFile}'Asympt25ns.py'
cp ${Main_Dir}/step3_MiniAOD.py  ${step3PythonFile}'Asympt50ns.py'
sed -i 's/inputFile/'"${Name}"'_MiniAOD_Asympt25ns/' ${step3PythonFile}'Asympt25ns.py'
sed -i 's/inputFile/'"${Name}"'_MiniAOD_Asympt50ns/' ${step3PythonFile}'Asympt50ns.py'
sed -i 's/MCRUN2_74_V9A/MCRUN2_74_V9/' ${step3PythonFile}'Asympt25ns.py'
sed -i 's/customisePostLS1_50ns/customisePostLS1/' ${step3PythonFile}'Asympt25ns.py'

########################################################
######### Small file with the commands for condor
########################################################
echo " Creating crab files .... "
crabFileStep0=crab3_${Name}_GENSIM_step0.py
cp ${Main_Dir}/crab3.py  ${crabFileStep0}
sed -i 's/NAME/'"${Name}"'/' ${crabFileStep0}
sed -i 's/test/'"${step0PythonFile}"'/' ${crabFileStep0}

crabFileStep1=crab3_${Name}_RAWSIM_step1_
crabFileStep2=crab3_${Name}_AODSIM_step2_
crabFileStep3=crab3_${Name}_MiniAOD_step3_
for i in ${PU[@]}; do
	cp ${Main_Dir}/crab3_RAW.py  ${crabFileStep1}${i}'.py'
	cp ${Main_Dir}/crab3_RAW.py  ${crabFileStep1}${i}'.py'
	cp ${Main_Dir}/crab3_RAW.py  ${crabFileStep1}${i}'.py'
	sed -i 's/test/'"${step1PythonFile}${i}"'/' ${crabFileStep1}${i}'.py'
	sed -i 's/NAME/'"${Name}"'_RunIISpring15DR74_RAWSIM_'"${i}"'/' ${crabFileStep1}${i}'.py'
	sed -i 's/PROC/RunIISpring15DR74_RAWSIM_'${i}'/' ${crabFileStep1}${i}'.py'
	sed -i 's/None/ADD_YOUR_DATASET_HERE/' ${crabFileStep1}${i}'.py'

	cp ${Main_Dir}/crab3_RAW.py  ${crabFileStep2}${i}'.py'
	cp ${Main_Dir}/crab3_RAW.py  ${crabFileStep2}${i}'.py'
	cp ${Main_Dir}/crab3_RAW.py  ${crabFileStep2}${i}'.py'
	sed -i 's/test/'"${step2PythonFile}${i}"'/' ${crabFileStep2}${i}'.py'
	sed -i 's/NAME/'"${Name}"'_RunIISpring15DR74_AODSIM_'"${i}"'/' ${crabFileStep2}${i}'.py'
	sed -i 's/PROC/RunIISpring15DR74_AODSIM_'${i}'/' ${crabFileStep2}${i}'.py'
	sed -i 's/None/ADD_YOUR_DATASET_HERE/' ${crabFileStep2}${i}'.py'

	cp ${Main_Dir}/crab3_RAW.py  ${crabFileStep3}${i}'.py'
	cp ${Main_Dir}/crab3_RAW.py  ${crabFileStep3}${i}'.py'
	cp ${Main_Dir}/crab3_RAW.py  ${crabFileStep3}${i}'.py'
	sed -i 's/test/'"${step3PythonFile}${i}"'/' ${crabFileStep3}${i}'.py'
	sed -i 's/NAME/'"${Name}"'_RunIISpring15DR74_MiniAOD_'"${i}"'/' ${crabFileStep3}${i}'.py'
	sed -i 's/PROC/RunIISpring15DR74_MiniAOD_'${i}'/' ${crabFileStep3}${i}'.py'
	sed -i 's/None/ADD_YOUR_DATASET_HERE/' ${crabFileStep3}${i}'.py'

done

#################################
##### To make it run
#################################
echo 'To make it run: 
First load the libraries (only once per session):
source /cvmfs/cms.cern.ch/crab3/crab.sh

Create and submit your jobs (Example for step0):
cd '${Name}'
crab submit '${crabFileStep0}' 

To check the status:
crab status '${Name}'

Once you have the dataset from step0 or step1, for example:
sed -i "s/ADD_YOUR_DATASET_HERE/\/RPVSt100tojj_13TeV_pythia8_GENSIM\/algomez-RPVSt100tojj_13TeV_pythia8_GENSIM-62459d50bdc5c4568f334137235e3bfc\/USER/g" crab3*RAWSIM*
' >> README

echo 'This script creates CRAB3 config files by default. Crab3 instructions in the README file'
echo 'Have a nice day :D '

