export X509_USER_PROXY=/afs/cern.ch/user/a/algomez/x509up_u15148
cd /afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_6_3_patch2/src/
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/
#cmsRun simpleMatching.py
#python RUNMiniAnalyzer.py -s QCDPt
python RUNMiniBoostedAnalyzer.py -m 110 -s DATA -r low -g pruned 
python RUNMiniBoostedAnalyzer.py -m 190 -s DATA -r high -g pruned 
python RUNMiniBoostedAnalyzer.py -m 110 -s DATA -r low -g softDropPuppi
python RUNMiniBoostedAnalyzer.py -m 190 -s DATA -r high -g softDropPuppi
python RUNMiniBoostedAnalyzer.py -m 110 -s DATA -r low -g softDrop
python RUNMiniBoostedAnalyzer.py -m 110 -s DATA -r low -g prunedPuppi
python RUNMiniBoostedAnalyzer.py -m 190 -s DATA -r high -g softDrop
python RUNMiniBoostedAnalyzer.py -m 190 -s DATA -r high -g prunedPuppi

#python RUNBkgEstimation.py -m 110 -p DATA -r low -g pruned 
#python RUNBkgEstimation.py -m 110 -p DATA -r low -g softDrop
#python RUNBkgEstimation.py -m 110 -p DATA -r low -g softDropPuppi
#python RUNBkgEstimation.py -m 110 -p DATA -r low -g prunedPuppi
#python RUNBkgEstimation.py -m 190 -p DATA -r high -g softDrop
#python RUNBkgEstimation.py -m 190 -p DATA -r high -g pruned 
#python RUNBkgEstimation.py -m 190 -p DATA -r high -g softDropPuppi
#python RUNBkgEstimation.py -m 190 -p DATA -r high -g prunedPuppi
