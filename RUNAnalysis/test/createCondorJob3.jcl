universe = vanilla
initialdir = /cms/jeans/Analysis/80XCode/CMSSW_8_0_20/src/RUNA/RUNAnalysis/test/
error = /cms/jeans/Analysis/80XCode/CMSSW_8_0_20/src/RUNA/RUNAnalysis/test/outputs/condor/TreeMaker$(Process).error
log =  /cms/jeans/Analysis/80XCode/CMSSW_8_0_20/src/RUNA/RUNAnalysis/test/outputs/condor/TreeMaker$(Process).log
output =  /cms/jeans/Analysis/80XCode/CMSSW_8_0_20/src/RUNA/RUNAnalysis/test/outputs/condor/TreeMaker$(Process).out
executable = TreeMaker.sh
arguments = $(Process)
queue 8