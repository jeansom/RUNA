universe = vanilla
initialdir = /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/
error = /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/outputs/condor/ThetaFileData$(Process).error
log =  /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/outputs/condor/ThetaFileData$(Process).log
output =  /cms/jeans/Analysis/122016Git/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/outputs/condor/ThetaFileData$(Process).out
executable = ThetaFileMakerData.sh
arguments = $(Process)
queue 40