# RUNtuples 

EDMNtuples based on [B2GEDMNtuples](https://github.com/cmsb2g/B2GAnaFW/tree/master)

This is a modify version of the B2GEDMNtuples. The main change is that here, to make jet, I am using the jetToolbox. Initially the results must be the same.

First, if you didn't download the B2GEDMNtuples:

```
cd $CMSSW_BASE/src/
git clone https://github.com/cmsb2g/B2GAnaFW.git Analysis
scram b -j 18

```

To run this go to RUNtuples/test. There you have a file called `RUNtuples_cfg.py`. You should not change anything there unless you want to modify something specific for your analysis. To check if everything is working you can run a test job:

```
cmsRun RUNtuples_cfi.py
```

Then you have a `crab3.py` file to send your jobs to CRAB3. There you should only change the requestName, inputDataset, outLFN and publishDataName. Remember to set your CRAB3 environment before you send your crab job:

```
source /cvmfs/cms.cern.ch/crab3/crab.sh
```



