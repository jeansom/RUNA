# Implementing B-Tagging Efficiency Scale Factors

This file gives a short overview of the steps necessary to implement b-tagging efficiency scale factors.

The code assumes CSVM, but this can be changed. 

The .csv files containing the scale factors can be found at: 
https://twiki.cern.ch/twiki/bin/view/CMS/BTagCalibration or in the 8TeV_SF or 13TeV_SF directory. 
Currently, the most up-to-date file is CSVv2.csv. The scale factor cuts for this file can be found at:
https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation74X50ns

## Instructions for producing scale factor corrected plots

1. Run
      ./createCrabJobs.py -w CRAB_Jobs -c MiniAOD_cfg.py -t crab_template.py
      
      After the CRAB jobs have been created, enter the CRAB_Jobs/cfg_files directory.
      Open the CRAB cfg file, crabConfig.py, and edit it to fit your analysis (Put it in the dataset name...)

      Put your efficiency map file in the CRAB_Jobs directory. Make sure it is listed in your cfg file as an external file.
      Do the same with the CSV.csv file
  
2.  From the CRAB_Jobs directory, run
    crab submit -c cfg_files/crabConfig.py
    Use crab status to check how the job is doing
   
3. When the job is done, run
      crab getouput
      to get the output

      Go into the results directory in your crab directory and run
      hadd RESULTNAME.root result1.root result2.root ... where RESULTNAME.root is whatever name you want for the final output and result1.root ... are the root files in the results folder

## Instructions for adding errors to the bjet_pt_wt plot
   (can be adapted for other plots)

1. Open the file you made in Step 1, RESULTNAME.root, in root

2. Go into the directory with the h_bjet_pt_wt plots and make sure that the plot h_bjet_pt_wt_errorsquared is there

3. Run the command
      .x addErrors.cc

      The errors should be approximately sqrt(N)
      You need to rerun this every time you reopen the RESULTNAME.root file

          
