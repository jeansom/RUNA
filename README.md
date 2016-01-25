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
cmsrel CMSSW_7_6_3
cd CMSSW_7_6_3/src/
cmsenv 
git cms-addpkg CommonTools/PileupAlgos
git clone https://github.com/cmsb2g/B2GAnaFW.git Analysis/B2GAnaFW -b v7.4.x_v8.4
git clone https://github.com/cms-jet/JetToolbox JMEAnalysis/JetToolbox -b jetToolbox_763
git clone git@github.com:alefisico/RUNA.git -b v763
scram b -j 18
cmsenv
```

## Technical details

* RUNGeneration does not need to be inside CMSSW.
* To run madgraph in the RU hexfarm, just download the script inside RUNGeneration and follow the instructions in the README file.
* RUNSimulations creates samples according to RunIISpring15DR74 campaing.
* RUNtuples is a modified version of the [B2GNtuple](https://github.com/cmsb2g/B2GAnaFW/tree/master), using the 74X version of the jetToolbox.
* RUNAnalysis uses the ntuples created with this version of the RUNtuples. 

> Disclaimer
> This is not an official CMS recipe. Use it with your own risk.
