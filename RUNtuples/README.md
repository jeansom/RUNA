# RUNtuples 

EDMNtuples based on [B2GEDMNtuples](https://github.com/cmsb2g/B2GAnaFW/tree/master)

This is a modify version of the B2GEDMNtuples. The main change is that here, to make jet, I am using the jetToolbox. Initially the results must be the same.

To run this go to RUNtuples/test. There you have a file called `RUNtuples_cfg.py`. You should not change anything there unless you want to modify something specific for your analysis. To check if everything is working you can run a test job:

```
cmsRun RUNtuples_cfi.py
```

Remember to change the *GlobalTag* in RUNtuples_cfi according to your sample.

Then you have a `crab3.py` file to send your jobs to CRAB3. There you should only change the requestName, inputDataset, outLFN and publishDataName. Remember to set your CRAB3 environment before you send your crab job:

```
source /cvmfs/cms.cern.ch/crab3/crab.sh
```
