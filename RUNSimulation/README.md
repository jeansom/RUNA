# Instructions to generate private Moriond17 samples 13TeV 

## Brief explanation

We are going to split the entire generation in 4 pieces. 

1. Step0: 
	First we are going to hadronize our madgraph generated file (from a gridpack or an lhe file), and simulate how particles interact with the detector (GENSIM).  This step *HAS* to be done in CMSSW_7_1_25_patch1 (use branch [[v7125patch1][https://github.com/RutgersHEX/RUNA/tree/v7125patch1/RUNSimulation]].
2. Step1: 
	We add pileup, simulate L1 and digitalize the signal (RAWSIM). This step saves the RAW data.  
3. Step2: 
	We reconstruct your objects and save them in the CMS format (AODSIM). 
4. Step3:
	We are going to take the AOD files an store only high level objets in a compress way, i.e. MiniAOD.
5. Step23:
	For simplicity I merge step2 and step3. If you are having problems you can run each job separated.


## To run the code

1. Step0 you need to be run in CMSSW_7_1_25_patch1, therefore:
```
cmsrel CMSSW_7_1_25_patch1
cd CMSSW_7_1_25_patch1/src/
cmsenv
git clone git@github.com:RutgersHEX/RUNA.git -b v7125patch1
scram b -j 18
cmsenv
cd RUNA/RUNSimulation/test/
```

Go to RUNA/RUNSimulation/test/
There you have a file called createJobs_CRAB.sh. You only need to modify the first part, PARAMETERS.
To run: 
```
./createJobs_CRAB.sh (total number of events) (RPV stop mass)
```

You will create a folder with the name of the process that you wrote in createJobs_CRAB.sh script.
There you will have python files and crab files almost ready to run. (You shouldn't change anything there)

First run Step0: you just need to submit the crab job. (If you don't know how to submit them, after you run createJobs_CRAB.sh you will have some instructions in the README file.) THIS STEP YOU WILL HAVE TO DO IT ONCE. Search in the output of the publishing step for the name of the dataset. It looks like:

```
datasetpath = /RPVSt200tojj_13TeV_GENSIM/algomez-RPVSt200tojj_13TeV_GENSIM-62459d50bdc5c4568f334137235e3bfc/USER
```

You will need to recall the name of the dataset that you create. This information must be shown in the publishing process. If not you can go here: 

https://cmsweb.cern.ch/das/

and search: `dataset=/*/YOURUSERNAME*/USER` (the last user is NOT your username, is the word USER). 

For Step1: go to crab_*_RAWIM_step1_*.cfg and add the dataset from step0. This step is different for each PU scenario, but the procedure is the same as step0. To simplify this step, once you run createJobs_CRAB.sh, you will have 3 different python config files (each one for each different PU scenario). You will have to submit your crab jobs as in step0. 

For Step2 and Step3: do should do the same as step1 but now your crab file is called crab_*_AODSIM_step2_*.cfg. 

##### For a quick test
You can use the python script called analyzerMiniAOD.py on your MiniAOD files. It will print some quantities in your screen.  

Enjoy it!. 


**DISCLAIMER**
This instructions are, by NO MEANS, any official 
prescription to generate events in CMS. 
Use it at your own risk!
