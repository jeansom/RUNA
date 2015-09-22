# RU simulations, Ntuples and Analysis


This package contains scripts:

* RUNGeneration contains a simple script to set your madgraph environment. 
* RUNSimulations generates MC samples from lhe files.
* RUNTriggerStudies performs validation and efficiency studies for triggers.
* RUNtuples creates Ntuples out of MiniAOD files, generated in RUNSimulations.
* RUAnalysis includes an example of how to use your Ntuples in your Analysis.


## Instructions
```
cmsrel CMSSW_7_4_5_patch1
cd CMSSW_7_4_5_patch1/src/
cmsenv
git cms-addpkg CommonTools/PileupAlgos
git cms-merge-topic nhanvtran:puppi-etadep-742p1-v6
git clone https://github.com/cms-jet/JetToolbox JMEAnalysis/JetToolbox -b jetToolbox_74X_PuppiWithGroomers
git clone https://github.com/cmsb2g/B2GAnaFW.git Analysis/B2GAnaFW -b CMSSW_7_4_X_V2
git clone https://github.com/alefisico/RUNA.git -b v745patch1 
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
