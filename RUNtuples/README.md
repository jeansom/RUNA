# RUNtuples 

EDMNtuples based on [B2GEDMNtuples](https://github.com/cmsb2g/B2GAnaFW/tree/master)

This is a modify version of the B2GEDMNtuples. The main change is that here, to make jet, I am using the jetToolbox. Initially the results must be the same.

Before you set your enviroment as described in the main README of these package, go to RUNtuples/test. There you have a file called `RUNtuples_cfg.py`. You should not change anything there unless you want to modify something specific for your analysis. To check if everything is working you can run a test job:

## Usage:
The globalTag is automatically chosen according to the input 'DataProcessing' value. 
However it can be explictily specified to override the default option.
Remember that the value of 'DataProcessing' is not set by default. The user has the choice of MC50ns, MC25ns, Data50ns, Data25ns. 
For DATA, it is important to add the option 'DataReco' to differentiate between PromptReco and 05Oct2015 versions of MiniAODv2. 

* Running on 25 ns data (Run2015 A, B, and C):
```
cmsRun RUNtuples_cfg.py maxEvents=1000 DataProcessing='Data25ns'
```
* Running on 25 ns data (Run2015 D and MiniAODv2):
```
cmsRun RUNtuples_cfg.py maxEvents=1000 DataProcessing='Data25nsv2' (for any MC MiniAODv2)
cmsRun RUNtuples_cfg.py maxEvents=1000 DataProcessing='Data25nsv2' DataReco='PromptReco' (for Run2015D-PromptReco-v4)
cmsRun RUNtuples_cfg.py maxEvents=1000 DataProcessing='Data25nsv2' DataReco='05Oct2015' (for Run2015D-05Oct2015-v1)
```
* Running on 50 ns MC:
```
cmsRun RUNtuples_cfg.py maxEvents=1000 DataProcessing='MC50ns'
```
* Running on 50 ns data:
```
cmsRun RUNtuples_cfg.py maxEvents=1000 DataProcessing='Data50ns'
```

There are 3 crab3 files for signal, backgrounds and data. They are very straightforward, just change with what you need. To run those python script:

```
python crab3.py
```

Remember to set your CRAB3 environment before you send your crab job:

```
source /cvmfs/cms.cern.ch/crab3/crab.sh
```
