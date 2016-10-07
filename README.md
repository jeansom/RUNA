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
cmsrel CMSSW_7_6_3_patch2
cd CMSSW_7_6_3_patch2/src/
cmsenv 
git cms-init
```
Temporary fix (only for 763 releases):
```
git remote add btv-cmssw https://github.com/cms-btv-pog/cmssw.git
git fetch --tags btv-cmssw
git cms-merge-topic cms-btv-pog:fixTMVAEvaluatorMemoryProblem-from-CMSSW_7_6_3 
```
```
git clone git@github.com:cmsb2g/B2GAnaFW.git Analysis/B2GAnaFW -b v7.6.x_v1.2
git clone git@github.com:cms-jet/JetToolbox.git JMEAnalysis/JetToolbox -b jetToolbox_763
git clone git@github.com:RutgersHEX/RUNA.git -b v763_V1
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
