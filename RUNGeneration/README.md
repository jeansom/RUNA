# Generation of LHE files using Madgraph

Here the only script that you need to run is called `setGeneration.sh`.

It is a simple script to download the latest version of madgraph, change the condor setup for the Rutgers hexfarm and download the RPV model.
If you are going to run in the hexfarm, please change the variable `HEXFARM` to true in `setGeneration.sh`, default is false.

In my experience, it is better to run this part in the hexfarm because your priority is rapidly going down in the cmslpc. 

Once you run:
```
./setGeneration.sh
```
you have an example proc card called: `proc_example_card.dat` that is for a simple case. But you can do something more interesting, like:
```
import model RPVMSSM_UFO
define sq = b1 b1~
define neu = n3 n4
generate p p > sq sq, ( sq > j neu, neu > j j j ) @0
add process p p > sq sq j, ( sq > j neu, neu > j j j ) @1
add process p p > sq sq j j, ( sq > j neu, neu > j j j ) @2
output sSTOn3j_n3TOjjj
```
Notice that thie example process above is extremely time consuming, it is just to show you another more complicated proc_card.

In MG5_aMC, an easy way to create a folder with the needed process is by running:
```
./bin/mg5_aMC proc_card_mg5.dat 
```
Or in batch mode:
```
nice nohup ./bin/mg5_aMC proc_card_mg5.dat -f &
```

