
MG=MG5_aMC_v2.2.2.tar.gz
MGSOURCE=https://cms-project-generators.web.cern.ch/cms-project-generators/$MG


wget --no-check-certificate ${MGSOURCE}
tar xzf ${MG}
rm $MG

wget https://feynrules.irmp.ucl.ac.be/raw-attachment/wiki/RPVMSSM/af1_ufo.tgz --no-check-certificate
tar xzf af1_ufo.tgz -C MG5_aMC_v2_2_2/models/
rm af1_ufo.tgz
