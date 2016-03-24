
HEXFARM=true


MG=MG5_aMC_v2.2.2.tar.gz
MGDir=MG5_aMC_v2_2_2
MGSOURCE=https://cms-project-generators.web.cern.ch/cms-project-generators/$MG

#### Downloading Madgraph
echo "########### DOWNLOADING MADGRAPH "
wget --no-check-certificate ${MGSOURCE}
echo "########### UNTAR MADGRAPH "
tar xzf ${MG}
#rm $MG

#### For hexfarm: change condor preferences
echo "--- cluster.original.py	2015-02-05 09:52:49.003699000 -0600
+++ cluster.py	2015-02-05 09:54:41.134744000 -0600
@@ -839,8 +839,8 @@
                   error = %(stderr)s
                   log = %(log)s
                   %(argument)s
-                  should_transfer_files = YES
-                  when_to_transfer_output = ON_EXIT
+                  should_transfer_files = NO
+                  # when_to_transfer_output = ON_EXIT
                   transfer_input_files = %(input_files)s
                   %(output_files)s
                   Universe = vanilla
" > cluster.patch 
 

if $HEXFARM; then
	patch ${MGDir}/madgraph/various/cluster.py < cluster.patch
fi

#### Changing default parameters
echo "--- mg5_configuration.original.txt	2015-02-05 09:27:11.926101000 -0600
+++ mg5_configuration.txt	2015-02-05 09:27:30.249762000 -0600
@@ -81,16 +81,16 @@
 
 #! Allow/Forbid the automatic opening of the web browser  (on the status page)
 #!  when launching MadEvent [True/False]
-# automatic_html_opening = True
+automatic_html_opening = False
 
 #! Default Running mode 
 #!  0: single machine/ 1: cluster / 2: multicore
-# run_mode = 2
+run_mode = 1
 
 #! Cluster Type [pbs|sge|condor|lsf|ge|slurm|htcaas|htcaas2] Use for cluster run only
 #!  And cluster queue (or partition for slurm)
-# cluster_type = condor
-# cluster_queue = madgraph
+cluster_type = condor
+cluster_queue = madgraph
 
 #! Path to a node directory to avoid direct writting on the central disk
 #!  Note that condor cluster avoid direct writting by default (therefore this
" > mg5_configuration.patch

patch ${MGDir}/input/mg5_configuration.txt < mg5_configuration.patch
rm *patch

#### Move example card
echo "#************************************************************
#*                     MadGraph5_aMC@NLO                    *
#*                                                          *
#*                *                       *                 *
#*                  *        * *        *                   *
#*                    * * * * 5 * * * *                     *
#*                  *        * *        *                   *
#*                *                       *                 *
#*                                                          *
#*                                                          *
#*         VERSION 2.2.2                 2014-11-06         *
#*                                                          *
#*    The MadGraph5_aMC@NLO Development Team - Find us at   *
#*    https://server06.fynu.ucl.ac.be/projects/madgraph     *
#*                                                          *
#************************************************************
#*                                                          *
#*               Command File for MadGraph5_aMC@NLO         *
#*                                                          *
#*     run as ./bin/mg5_aMC  filename                       *
#*                                                          *
#************************************************************
set group_subprocesses Auto
set ignore_six_quark_processes False
set loop_optimized_output True
set complex_mass_scheme False
import model sm
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~
define l+ = e+ mu+
define l- = e- mu-
define vl = ve vm vt
define vl~ = ve~ vm~ vt~
#### add your process below
import model RPVMSSM_UFO
generate p p > ul ul~, ul > d~ s~, ul~ > d s
output RPVSttojj" >> proc_example_card.dat
mv proc_example_card.dat ${MGDir}/  

##### Charging RPVMSSM_UFO model
echo "############# DOWNLOADING RPVMSSM MODEL"
wget https://feynrules.irmp.ucl.ac.be/raw-attachment/wiki/RPVMSSM/af1_ufo.tgz --no-check-certificate
tar xzf af1_ufo.tgz -C ${MGDir}/models/
rm af1_ufo.tgz

##### Adding file to run 
echo "## This is a small script to run your generation in the cluster, after you run ./bin/mg5_aMC proc_card.dat
## NAME_OF_PROCESS is the name of your lhe file, NAME_OF_DIRECTORY is the name of the directory created in the previous step. -f is to say yes to all questions while running. -c is to run in the cluster.
## Example: launch -n 500sSTOn3j_100n3TOjjj sSTOn3j_n3TOjjj -f -c
launch -n NAME_OF_PROCESS NAME_OF_DIRECTORY -f -c
" >> ${MGDir}/run_launch 

echo "############## DONE
Have a nice day! :)"
