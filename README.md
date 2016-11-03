# RU simulations, Ntuples and Analysis

This package contains scripts:

* RUNGeneration contains a simple script to set your madgraph environment. 
* RUNSimulations generates MC samples from lhe files.
* RUNTriggerStudies performs validation and efficiency studies for triggers.
* RUAnalysis includes an example of how to use your Ntuples in your Analysis.

## Instructions
```
cmsrel CMSSW_8_0_20
cd CMSSW_8_0_20/src/
cmsenv 
git cms-init
git clone git@github.com:RutgersHEX/RUNA.git -b v8020
scram b -j 18
cmsenv
```

## Technical details

* RUNGeneration does not need to be inside CMSSW.
* To run madgraph in the RU hexfarm, just download the script inside RUNGeneration and follow the instructions in the README file.
* RUNSimulations creates samples according to RunIISpring15DR74 campaing.
* RUNAnalysis uses [B2G ntuples](https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GAnalysisFwk).

> Disclaimer
> This is not an official CMS recipe. Use it with your own risk.
