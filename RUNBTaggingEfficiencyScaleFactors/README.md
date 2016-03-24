# Converting AK4 B-Tagging Efficiency Scale Factors to AK8 B-Tag Eff SF

This file gives a short overview of the steps necessary to use b-tagging efficiency scale factors

All the code assumes CSVM, but this can be changed. 

The .csv files containing the scale factors can be found at: 
https://twiki.cern.ch/twiki/bin/view/CMS/BTagCalibration or in the 8TeV_SF or 13TeV_SF directory. 
Currently, the most up-to-date file is CSVv2.csv. The scale factor cuts for this file can be found at:
https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation74X50ns

They are also available in the directory 13TeV_SF

## Implementing the SFb

1. Enter the directory test/MakeBTaggingEfficiencyMaps

2. Follow the instructions in the README file there

3. Enter the directory test/ImplementBTagSF

4. Follow the instructions in the README file

## Converting the AK4 SFb to AK8 SFb

1. Enter the directory test/ConvertAK4BTaggingSFtoAK8BTaggingSF

2. Follow the instructions in the README file there