universe = vanilla
initialdir = /cms/jeans/Analysis/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/
error = /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/122016Git/test/outputs/condor/ThetaFile$(Process).error
log =  /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/122016Git/test/outputs/condor/ThetaFile$(Process).log
output =  /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/122016Git/test/outputs/condor/ThetaFile$(Process).out
executable = ThetaFileMaker.sh
arguments = $(Process)
queue 9