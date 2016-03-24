FOLDER=/eos/uscms/store/user/algomez/
#FILES=RPVSt100tojj_13TeV_pythia8/RunIISpring15DR74_AODSIM_Asympt25ns/*/*/*root
#FILES=RPVSt200tobj_13TeV_pythia8/RunIISpring15DR74_RAWSIM_Asympt25ns_v4/*/*/*root
#FILES=RPVSt350tobj_13TeV_pythia8/RunIISpring15DR74_AODSIM_Asympt25ns/*/*/*root
FILES=RPVSt100tobj_13TeV_pythia8/RunIISpring15DR74_AODSIM_Asympt25ns/*/*/*root

for f in $FOLDER$FILES
do
	echo "Processing $f file..."
	srmcp -debug=true -2 -streams_num=10 file:///$f srm://ruhex-osgce.rutgers.edu:8443/srm/v2/server\?SFN=/cms/data24/algomez/EOS/${f//$FOLDER/}
	#srmcp -debug=true -2 -streams_num=10 file:///$f srm://ruhex-osgce.rutgers.edu:8443/srm/v2/server\?SFN=/cms/gomez/EOS/${f//$FOLDER/}
done

