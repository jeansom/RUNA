#!/usr/bin/env python

import sys,os,time, re
import csv
from math import *
from string import *
from array import array
import argparse
from ROOT import * 
from collections import OrderedDict
from multiprocessing import Process
import numpy as np
try: 
	from RUNA.RUNAnalysis.Plotting_Header import *
except ImportError: 
	sys.path.append('../python') 


gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
gStyle.SetOptStat(0)


#----------------------------------------------------------------------
### Main Optimization
###### BkgSamples: Background Samples
###### SigSamples: SigSamples
###### treename: Tree Name
###### varList: List of variables to optimize
###### mass: signal mass to optimize for
###### window: mass window (around signal mass)
###### BTAG: preselection
def makeTable( BkgSamples, SigSamples, treename, varList, mass, window, BTAG ):
    """docstring for makeTable"""
    cuts = {}
    cutlist = ()
    cutLengths = {}
    combinations = []

    # Make list of all combinations of variables
    for var in varList:
	    length = 0
	    cutVar = []
	    minVal = var[1]
	    maxVal = var[2]
	    step = var[4]
	    i = minVal
	    while i <= maxVal:
                    cutVar.append( i )
                    length+=1
		    i += step
	    cutLengths[ var[0] ] = length
	    cuts[ var[0] ] = cutVar
    possCombs( 0, varList, cuts, combinations, cutlist )

    outputTextFile = 'OptimizationFiles/RPVStopStopToJets_UDD323_Signal_Bkg.csv'
    output = open( outputTextFile, 'wt' )

    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    #-------------------------Event Loop-------------------------#

    #Signal
    SigTable = {}
    Sig = []
    SigTableScaled = {}
    SigScaled = []
    C=[]    

    # Loop through signal samples
    for sigSample in SigSamples:
	    for k in xrange( len(combinations) ):
		    Sig.append(0)		    
		    SigScaled.append(0)
		    
    
	    scale = "36600*1521.11/259991*puWeight" # Event weight
	    
	    cut = "prunedMassAve>("+str(mass)+"-"+str(window)+")&prunedMassAve<("+str(mass)+"+"+str(window)+")&"+BTAG

	    n = .1	    
	    for k in xrange( len(combinations) ):
		    if float(k)/float(len(combinations)) > n:
			    print str(n*100)+"%"
			    n = n + .1

		    cuts = cut
		    for j in xrange( len(combinations[k]) ):
			    cuts = cuts+"&"+varList[j][0]+"<"+str(combinations[k][j])
		    sigScaled = TH1D( "signalScaled"+str(k), "", 1000, 0, 1000 )
		    sig = TH1D( "signal"+str(k), "", 1000, 0, 1000 )
		    
		    quickplot( SigSamples[ sigSample ], treename, sigScaled, "prunedMassAve", "("+cuts+")", scale )
		    quickplot( SigSamples[ sigSample ], treename, sig, "prunedMassAve", "("+cuts+")", "1" )

		    Sig[ k ] = sig.Integral( 0,2000 )
		    SigScaled[ k ] = sigScaled.Integral( 0, 2000 )
	    SigTable[ sigSample ] = tuple( Sig )
	    SigTableScaled[ sigSample ] = tuple( SigScaled )

    #Bkg
    BkgTable = {}
    Bkg = []
    BkgTableScaled = {}
    BkgScaled = []

    # Loop through background samples
    for bkgSample in BkgSamples:
	    for k in xrange( len(combinations) ):
		    Bkg.append(0)		    
		    BkgScaled.append(0)
		    
    
	    scale = "36600*lumiWeight*puWeight"
	    
	    cut = "prunedMassAve>("+str(mass)+"-"+str(window)+")&prunedMassAve<("+str(mass)+"+"+str(window)+")&"+BTAG
	    
	    n = 0.1	    
	    for k in xrange( len(combinations) ):
		    if float(k)/float(len(combinations)) > n:
			    print str(n*100)+"%"
			    n = n + .1
		    cuts = cut
		    for j in xrange( len(combinations[k]) ):
			    cuts = cuts+"&"+varList[j][0]+"<"+str(combinations[k][j])

		    bkgScaled = TH1D( "bkgnalScaled"+str(k), "", 1000, 0, 1000 )
		    bkg = TH1D( "bkgnal"+str(k), "", 1000, 0, 1000 )

		    quickplot( BkgSamples[ bkgSample ][0], treename, bkgScaled, "prunedMassAve", cuts, scale )
		    quickplot( BkgSamples[ bkgSample ][0], treename, bkg, "prunedMassAve", cuts, "1" )
		    Bkg[ k ] = bkg.Integral( 0,2000 )
		    BkgScaled[ k ] = bkgScaled.Integral( 0, 2000 )
	    BkgTable[ bkgSample ] = tuple( Bkg )
	    BkgTableScaled[ bkgSample ] = tuple( BkgScaled )



    # Write out num signal events, num background events to csv file
    for k in xrange( len(combinations) ):
	    comb = ""
	    for j in xrange( len(combinations[k])):
		    comb += str(combinations[k][j])
		    comb += "  "
		    writer.writerow([ comb ] )
	    for sig in SigSamples:
		    writer.writerow( [str(sig), str(SigTableScaled[ sig ][k]), str(SigTable[ sig ][k])] )
	    for bkg in BkgSamples:
		    writer.writerow( [str(bkg), str(BkgTableScaled[ bkg ][k]), str(BkgTable[ bkg ][k])] )
    output.close()
				    
    totalBkgTable = []
    for k in xrange( len(combinations) ):
	    totalBkgTable.append(0)
    for bkgSample in BkgSamples:
	    for k in xrange( len(combinations) ):
		    totalBkgTable[k] += BkgTableScaled[ bkgSample ][k]

    Sig_SqrtB = []

    for sig in SigSamples:
	    for k in xrange( len(combinations) ):
		    if totalBkgTable[k] is not 0:
			    print str(SigTableScaled[ sig ][k]/sqrt( totalBkgTable[k] ) ) + "\t\t\t" + str( combinations[k] )
			    Sig_SqrtB.append( SigTableScaled[ sig ][k]/sqrt( totalBkgTable[k] ) )
    Sig_SqrtB.sort()
    
    # Make S/sqrt(B) histogram, save
    file = TFile( "OptimizationFiles/Optimized.root", "RECREATE" )
    file.cd()
    OptimizedCuts = TH1F( "OptimizedCuts", "Optimized Cuts", len(combinations)+2, 0, len(combinations)+1 )
    for k in xrange(len(Sig_SqrtB)):
	    OptimizedCuts.Fill(k+1,Sig_SqrtB[k])
    file.Write()
    file.Save()

# Finds all possible combinations of a set of variables/cuts
def possCombs(currentVarIndex, varList, cuts, combinations, cutlist = () ):
    tempCutList = []
    cutlist2 = list(cutlist)
    if  currentVarIndex is len(varList):
        combinations.append(cutlist)
    else:
	    tempCutList = cuts[ varList[ currentVarIndex ][0] ]
	    for i in xrange(len(tempCutList)):
		    cutlist2.append(tempCutList[i])
		    possCombs( currentVarIndex + 1, varList, cuts, combinations, tuple(cutlist2) )
		    del cutlist2[-1]
                
            
                
#----------------------------------------------------------------------

#################################################################################
if __name__ == '__main__':
	bkgSamples = OrderedDict()
	bkgSamples[ 'QCDHTAll' ] = [ 'v08/RUNAnalysis_QCDHTAll_80X_V2p4_v08.root', kBlue-4 ]

	sigSamples = {}
	sigSamples[ 'RPVSt100' ] = '80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-100_80X_V2p3_v06.root'

	treename = 'BoostedAnalysisPlots/RUNATree'

	var = [
                ##    0        1       2     3         4        7
		## Version,    Variable,  minX, maxX,  <? , step
		[ 'Boosted', "numJets", 0.45, 0.65, True, .15 ],
	]

        variables = [ x[1:] for x in var ]

	p0 = Process( target=makeTable, args=( bkgSamples, sigSamples, treename, variables, 100, 10, "1" ) )
        p0.start()
        p0.join()
