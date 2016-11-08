# RUNA Analysis 


This part contains an example of how to use the Ntuples in an Analysis. The important scripts are:


* plugins/RUNAna.cc: C++ code for your analysis.
* test/RUNAna_cfi.py: python file to run your analysis.
* test/***_RUNtuples_cfi.py: python input file for your analysis.
* test/crab3.py: to send jobs for several datasets at ones.

The rest of files are for my private use only. Please do not pay attention to them. 
Remember that this is only an example. Some parts of the RUNAna.cc may be wrong. 

## To use crab3

In general for crab3, you must run this source code *first*:
```
source /cvmfs/cms.cern.ch/crab3/crab.sh
```
For more info about crab3, please visit: [CRAB3 Tutorial](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial)

In particular, to run the crab3.py file in this package, because it is mimic multicrab capabilities to run several jobs for different datasets at once, you will have to run it like:
```
python crab3.py
``` 


> Disclaimer
> This is not an official CMS recipe. Use it with your own risk.
