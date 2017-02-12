universe = vanilla
initialdir = /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/
error = /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/outputsBin/condor/ThetaFile$(Process).error
log =  /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/outputsBin/condor/ThetaFile$(Process).log
output =  /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/outputsBin/condor/ThetaFile$(Process).out
executable = ThetaFileMakerBin.sh
arguments = $(Process)
queue 9