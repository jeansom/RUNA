## Running the basic estimate
The code ThetaFileMakerQCD26MassSplit.py is the basic ABCD estimate. Run it using ThetaFileMakerDATA26Mass.sh.
To run it for preselection only:
```
chmod 777 ThetaFileMakerDATA26Mass.sh
./ThetaFileMakerDATA26Mass.sh 9
```
The argument defines which channel to run in and how to scale the resonant backgrounds. 
If the argument is x, the code will run channel number x%10 with scaling number (x - x%10)/10. 
For example, if the argument is 31, it will run channel 1, scaling 3

The channel numbers and scalings are defined (respectively) in ThetaFileMakerQCD26MassSplit.py L312-346, L196-226

In ThetaFileMakerDATA26Mass.sh:
* To run over data, make sure the argument -m has the word DATA in it instead of MC
* To run B*(C/D), make sure the argument -m has BCD in it instead of CBD
* To run over the HT binned QCD, make sure the argument -m has HT in it instead of Pt
* To add any cuts to the preselection, change the argument -j to include your cut
* To make log plots, change -l to True

### Code used when running the estimate (in the python directory)
* Converters.py: Defines the fit
* Distribution_Header.py: Sets up the distributions (QCD, TTJets, WJets, Data)
* Plotting.py: Actually runs the estimate and pretties up/saves the TF and est
* Plotting_Header.py: Contains basic functions for plotting
* Alphabet.py: Contains the code to calculate the bkg est
* Alphabet_Header.py: Calculates the TF
* CMS_lumi.py: Draws the CMS logo and that kind of stuff

## Running New Estimate 2.0
Use the code ABCDEF_Est.py. Just run 
```
python ABCDEF_Est.py
```
Make sure to change L52-59 to the cuts you want and to change L138-174 as needed.

### Code used when running New Estimate 2.0 (in the python directory)
* ABCDEF_Draw.py: Draws and saves the estimate
* ABCDEF_Ester.py: Calculates the new B/D values by fitting B/D in different deta bins
* ABCDEF_Functions.py: Contains basic methods to append arrays, calculate errors...
* Plotting_Header.py: Contains basic functions for plotting
* Distribution_Header.py: Sets up the distributions (QCD, TTJets, WJets, Data)
* CMS_lumi.py: Draws the CMS logo and that kind of stuff

> Disclaimer: This code has memory problems, I think, so sorry if it doesn't work all the time.

## Running the simultaneous optimization
Run using 
```
python RUNOptimizationTCuts.py
```

Change L198-210, L79, and L118 as appropriate for your purposes.
Change the variable names in the trees that are different in your trees.

## For debugging ThetaFileMakerQCD26MassSplit.py
The script SimpleBkgEst.py is a fairly straightforward way to run the background est and can be used to debug ThetaFileMakerQCD26MassSplit.py. It is relatively simple and self-explanatory.
Run using
```
python SimpleBkgEst.py
```
