# RU simulations, Ntuples and Analysis


This package contains scripts:

* RUNGeneration contains a simple script to set your madgraph environment. 
* RUNSimulations generates MC samples from lhe files.
* RUNTriggerStudies performs validation and efficiency studies for triggers.
* RUNtuples creates Ntuples out of MiniAOD files, generated in RUNSimulations.
* RUAnalysis includes an example of how to use your Ntuples in your Analysis.
* RUNBTagScaleFactors and RUNMakeEfficiecyMaps contain scripts to calculate btag scale factors. 


## Instructions
```
setenv SCRAM_ARCH slc6_amd64_gcc530 (or in bash: export SCRAM_ARCH=slc6_amd64_gcc530)
cmsrel CMSSW_8_0_8_patch2
cd CMSSW_8_0_8_patch2/src
cmsenv
```
```
git clone git@github.com:cmsb2g/B2GAnaFW.git Analysis/B2GAnaFW -b CMSSW_8_0_X_V2
git clone git@github.com:cms-jet/JetToolbox.git JMEAnalysis/JetToolbox -b jetToolbox_763
git clone git@github.com:jeansom/RUNA.git -b v808
scram b -j 18
cmsenv
```

## Technical details

* RUNGeneration does not need to be inside CMSSW.
* To run madgraph in the RU hexfarm, just download the script inside RUNGeneration and follow the instructions in the README file.
* RUNSimulations creates samples according to RunIISpring15DR74 campaing.
* RUNtuples is a modified version of the [B2GNtuple](https://github.com/cmsb2g/B2GAnaFW/tree/master), using the 763 version of the jetToolbox.
* RUNAnalysis uses the ntuples created with this version of the RUNtuples. 

> Disclaimer
> This is not an official CMS recipe. Use it with your own risk.
