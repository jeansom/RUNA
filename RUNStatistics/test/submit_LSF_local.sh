export X509_USER_PROXY=/afs/cern.ch/user/a/algomez/x509up_u15148
cd /afs/cern.ch/work/a/algomez/RPVStops/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/a/algomez/RPVStops/CMSSW_8_0_20/src/RUNA/RUNStatistics/test/
source runCombine.sh all fullCLs
