# RU Simulations and Ntuples  


This package contains scripts:

* RUNGeneration contains a simple script to set your madgraph environment. 
* RUNSimulations generates MC samples from lhe files.
* RUNtuples creates Ntuples out of MiniAOD files, generated in RUNSimulations
* RUAnalysis includes an example of how to use your Ntuples in your Analysis.


### Instructions
```
cmsrel CMSSW_7_2_0
cd CMSSW_7_2_0/src/
cmsenv
git cms-addpkg RecoJets/JetProducers
git cms-merge-topic -u alefisico:jetToolbox_72X
git clone https://github.com/alefisico/RUNA.git
scram b -j 18
cmsen
```

### Technical details

* RUNGeneration does not need to be inside CMSSW, but madgraph *needs* the python version that is loaded with CMSSW. 
* To run madgraph in the RU hexfarm, just download the script inside RUNGeneration and follow the instructions in the README file.
* RUNSimulations creates GENSIM files according to Spring13 campaign. RAWSIM, AODSIM and MiniAOD files are based on the PHYS14 campaign.
* RUNtuples is a modified version of the first version of the [B2GNtuple](https://github.com/cmsb2g/B2GAnaFW/tree/master), using the 72X version of the jetToolbox. Use it as a test.
* RUNAnalysis uses the ntuples created with this version of the RUNtuples. 

> Disclaimer
> This is not an official CMS recipe. Use it with your own risk.
