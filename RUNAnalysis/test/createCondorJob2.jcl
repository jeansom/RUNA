universe = vanilla
initialdir = /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/
error = /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/outputs2/condor/PullPlot$(Process).error
log =  /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/outputs2/condor/PullPlot$(Process).log
output =  /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/outputs2/condor/PullPlot$(Process).out
executable = PullPlotCondor.sh
arguments = $(Process)
queue 40