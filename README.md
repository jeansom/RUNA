# RU Simulations and Ntuples  


This package contains scripts:

* RUNGeneration contains a simple script to set your madgraph environment. 
* RUNSimulations generates MC samples from lhe files.
* RUNtuples creates Ntuples out of MiniAOD files, generated in RUNSimulations
* RUAnalysis includes an example of how to use your Ntuples in your Analysis.


## Instructions
```
cmsrel CMSSW_7_4_1_patch1
cd CMSSW_7_4_1_patch1/src/
cmsenv
git clone https://github.com/cms-jet/JetToolbox JMEAnalysis/JetToolbox -b jetToolbox_74X
git clone https://github.com/cmsb2g/B2GAnaFW.git Analysis/B2GAnaFW/
git clone https://github.com/alefisico/RUNA.git 
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
