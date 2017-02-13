universe = vanilla
initialdir = /cms/jeans/Analysis/80XCode/CMSSW_8_0_20/src/RUNA/RUNAnalysis/test/
error = /cms/jeans/Analysis/80XCode/CMSSW_8_0_20/src/RUNA/RUNAnalysis/test/outputs/condor/PullPlot$(Process).error
log =  /cms/jeans/Analysis/80XCode/CMSSW_8_0_20/src/RUNA/RUNAnalysis/test/outputs/condor/PullPlot$(Process).log
output =  /cms/jeans/Analysis/80XCode/CMSSW_8_0_20/src/RUNA/RUNAnalysis/test/outputs/condor/PullPlot$(Process).out
executable = PullPlotCondor.sh
arguments = $(Process)
queue 80