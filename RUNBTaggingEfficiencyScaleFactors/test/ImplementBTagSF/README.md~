# Implementing B-Tagging Efficiency Scale Factors
This file gives a short overview of the steps necessary to implement b-tagging efficiency scale factors.

The code assumes CSVM, but this can be changed. 

The .csv files containing the scale factors can be found at: 
https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation76X#Boosted_event_topologies or in the 8TeV_SF or 13TeV_SF directory. 
Currently, the most up-to-date file is CSVv2.csv.

## 1) Instructions for producing scale factor corrected plots

   A) Run

   ./createCrabJobs.py -w CRAB_Jobs -d datasetList.txt -c ImplementBtaggingSF_cfg.py -t crab_template.py
      
   B) After the CRAB jobs have been created, enter the CRAB_Jobs/cfg_files directory. Open the CRAB cfg file, crabConfig.py, and edit it to fit your analysis 
      1. If you are running over an Ntuple:
            Open the file CMSSW_cfg.py and change the value of the variable isMiniAOD on line 28 to 1 

   C) Put your efficiency map file in the CRAB_Jobs directory. Make sure it is listed in your cfg file as an external file.
      Do the same with the CSVv2.csv file and the directory JECs
  
   D) From the CRAB_Jobs directory, run
      
      crab submit -c cfg_files/crabConfig.py
      
   E) Use crab status to check how the job is doing
   
   F) When the job is done, run
      crab getouput
      to get the output

   G) Go into the results directory in your crab directory and run
      
      hadd RESULTNAME.root result1.root result2.root ... 
      where RESULTNAME.root is whatever name you want for the final output and result1.root ... are the root files in the results folder


## 2) Instructions for adding errors to the bjet_pt_wt plot
##   (can be adapted for other plots)

   A) Open the file you made in Step 1, RESULTNAME.root, in root

   B) Go into the directory with the h_bjet_pt_wt plots and make sure that the plot h_bjet_pt_wt_errorsquared is there

   C) Run the command
      .x addErrors.cc

   The errors should be approximately sqrt(N)
   You need to rerun this every time you reopen the RESULTNAME.root file

          
