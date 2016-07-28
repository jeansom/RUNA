# Converting AK4 B-Tagging Efficiency Scale Factors to AK8 B-Tag Eff SF

This file gives a short overview of the steps necessary to convert AK4 B-Tagging Efficiency Scale Factors to AK8 B-Tagging Efficiency Scale Factors

The code assumes CSVM, but this can be changed. 

The code implements JECs for ONLY AK8 Jets in MiniAODs. 

The .csv files containing the scale factors can be found at: 
https://twiki.cern.ch/twiki/bin/view/CMS/BTagCalibration or in the 8TeV_SF or 13TeV_SF directory. 
Currently, the most up-to-date file is CSVv2.csv. The scale factor cuts for this file can be found at:
https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation80X

## Instructions for converting the scale factors

### Step 1: Finding the appropriate Delta R cut for your sample

1. Run

	./createCrabJobs.py -w CRAB_Jobs -d datasetList.txt -c bTaggingSFConverter_cfg.py -t crab_template.py      
	to create the CRAB jobs
	
      After the CRAB jobs have been created, copy the directory JECs into CRAB_Jobs

      Enter the CRAB_Jobs/cfg_files directory.
      Open the CRAB cfg file and make any changes needed to fit your analysis
      If you are running over an Ntuple:
      	 Open CMSSW_cfg.py and change the value of the variable isMiniAOD on line 25 to 1
	
 
2.  From the ConvertAK4BTaggingSFtoAK8BTaggingSF directory, run

    ./checkCrabJobs.py -w CRAB_Jobs -s
    to submit the jobs

    Use crab status to check how the job is doing
   
3. When the job is done, run

      crab getoutput

      to get the output

      Go into the results directory in your crab directory and run
      hadd RESULTNAME.root result1.root result2.root ... where RESULTNAME.root is whatever name you want for the final output and result1.root ... are the root files in the results folder

## To calculate AK8 BTag SF

1. Copy MakePlots.cc into your results folder (use the cp command)

2. Open the root file output.root
   	root -l output.root

3. Enter the "demo" directory
   	 _file0->cd("demo")

4. Run
   .x MakePlots.cc
   To make pdfs of the plots

5. Open the pdf "h_delta_r_2nd_min.pdf". Look at the bins close to delta R = 0 that have no entries. Find the maximum of these (should be around delta R = .3). This will be your delta R cut.

6. Enter the directory CMSSW_7_6_3_patch2/src/RUNA/RUNBTaggingEfficiencyScaleFactors/plugins and open the file ConvertBtaggingSF.cc

7. Change the number on line 462 from .3 to whatever delta R cut you found in step 5

8. Run
   
   cd $CMSSW_BASE/src/

   scram b -j 18

   cd CMSSW_7_6_3_patch2/src/RUNA/RUNBTaggingEfficiencyScaleFactors/test/

   cmsenv

9. Rerun steps 1, 2, and 3 under the category step 1

10. Rerun steps 1, 2, 3, 4 under the category "To calculate AK8 BTag SF"

11. Open the file h_ratio_AK4eff_AK8eff_bin_with_AK8pt_fit.pdf

12. Find 1 - p0 for the fit. 

13. When you are implementing the scale factors for AK8 jets, use the AK4 scale factor and add 1 - p0 in quadrature with the regular systematics for the scale factor