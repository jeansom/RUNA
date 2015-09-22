export X509_USER_PROXY=/afs/cern.ch/user/a/algomez/x509up_u15148
cd /afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_4_5_patch1/src/
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/a/algomez/Substructure/CMSSW_7_4_5_patch1/src/RUNA/RUNAnalysis/test/
#cmsRun simpleMatching.py
#source setup.sh
#python myplot.py 
python RUNMiniAnalyzer.py -s QCDPt
