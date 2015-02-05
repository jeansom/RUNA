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
Once your job is done, you will have a new folder with the name of the output that you specified in the previous step. Then, you will have to modify some parameters in your recently created cards. Do not forget to change the value of the mass of the particles in the param_card.dat, in our example will be located here: `sSTOn3j_n3TOjjj/Cards/param_card.dat`. The other important card to change is `run_card.dat`.

After you modified this cards, you are ready to send your generation jobs to the cluster. In the main directory you have a file called `run_launch`.  This is a small script to run your generation in the cluster. Here: NAME_OF_PROCESS is the name of your lhe file, NAME_OF_DIRECTORY is the name of the directory created in the previous step. -f is to say yes to all questions while running. -c is to run in the cluster.
`run_launch` should look like:
```
launch -n 500sSTOn3j_100n3TOjjj sSTOn3j_n3TOjjj -f -c
```
And you can run it like:
```
nice nohup ./bin/mg5_aMC run_launch &
```
This will take a while depending on your process. At the end, you must have your lhe file inside the directory, (for example) `sSTOn3j_n3TOjjj/Events/500sSTOn3j_100n3TOjjj/`, and it is called `unweighted_events.lhe.gz`.

Enjoy it!
