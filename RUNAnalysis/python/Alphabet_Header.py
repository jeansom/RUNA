#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy
import numpy as numpy
from RUNA.RUNAnalysis.Converters import *

###################################################################
### Provides the methods needed to make a B/D graph and fit it. ###
###################################################################

# Takes a 2D plot and measures the Pass/Fail ratios in given bins
#### plot: 2D plot to perform the measurement on
#### bins: list of bins to measure the P/F ratio in (each will yield a B/D point)
#### cut: value to differentiate pass from fail. Should be on the y-axis of the plot
#### which: ">" or "<" to tell which way the cut goes
#### center: the x-var is recentered about the middle of the blinded region. This tells where to recenter to. Can be left as 0.
def AlphabetSlicer( plot, bins, cut, which, center ):
    x = [] # X values for each bin
    y = [] # Y values (pass/fail ratios) for each bin
    exl = [] # error below x values
    eyl = [] # error below y values
    exh = [] # error above x values
    eyh = [] # error above y values

    for b in bins: # Loop through the bins (along x axis, should contain gap for signal region)
        passed = 0 # Number of events which passed cut in bin b
        failed = 0 # Number of events which failed cut in bin b
        for i in range( plot.GetNbinsX()+1 ):
            for j in range( plot.GetNbinsY()+1 ): # Loops through all the bins in the 2D plot
                if plot.GetXaxis().GetBinCenter(i) < b[1] and plot.GetXaxis().GetBinCenter(i) > b[0]: # If the bin (i,j) is in bin b

                    # Add num entries in b to failed if they fail cut
                    # Add num entries in b to passed if they pass cut
                    if which == ">":
                        if plot.GetYaxis().GetBinCenter(j) < cut:
                            failed = failed + plot.GetBinContent(i,j)
                        else:
                            passed = passed + plot.GetBinContent(i,j)
                    if which == "<":
                        if plot.GetYaxis().GetBinCenter(j) > cut:
                            failed = failed + plot.GetBinContent(i,j)
                        else:
                            passed = passed + plot.GetBinContent(i,j)
        # Corrects for negative passed or failed values
        if passed < 0:
            passed = 0
        if failed < 0:
            failed = 0

        ep = math.sqrt( passed ) # Error on passed
        ef = math.sqrt( failed ) # Error on failed
        
        if passed == 0 and failed == 0:
#            print "bin not filled: passed = 0 and failed = 0"
            continue
        elif failed == 0:
#            print "bin not filled: failed = 0"
            continue
        elif passed == 0:
#            print "bin not filled: passed = 0"
            continue

        err = (passed/(failed))*(ep/passed+ef/failed) # Error on ratio

        x.append( (float( (b[0]+b[1])/2. - center ) ) ) # X value = bin center - center
        exl.append( float( (b[1]-b[0])/2. ) ) # X low error = bin width
        exh.append( float( (b[1]-b[0])/2. ) ) # X high error = bin width
        
        y.append( float(passed/failed) ) # Y value = pass/fail
        eyh.append( float(err) ) # See error calculation above

        # Lower error on ratio
        if (passed/failed) - err > 0.: # If err is not greater than the ratio
            eyl.append(float(err)) # The lower error is also err
        else: # Otherwise
            eyl.append( float(passed/failed) ) # The lower error is just the ratio --> brings it to 0, not below
        
    # Creates TGraphAsymmErrors with x values, y values, and errors
    if len(x) > 0:
        G = TGraphAsymmErrors( len(x), scipy.array(x), scipy.array(y), scipy.array(exl), scipy.array(exh), scipy.array(eyl), scipy.array(eyh) )
    else:
        G = TGraphAsymmErrors()

    return [G, x, y, exl, exh, eyl, eyh]
        
# Fits a TGAE, G, to a function, using the form F. Uses a ROOT function to calculate the errors on the fit, and saves them as TGraphs
#### G: A TGraphAsymmErrors, see method AlphabetSlicer
#### F: A Converter, see Converters.py
def AlphabetFitter( G, F, fitter, bins, truthbins ):
    # Fits G to F
    if G.GetN() > 0:
        fitResult = TFitResultPtr(G.Fit( F.fit, F.Opt )) # Fits G to a function of form F
        fitter = gMinuit.fStatus
    else:
        F.Fit = TF1("emptyFit", "0", F.rm, F.rp )
    fitter2 = TVirtualFitter.GetFitter()

    # Calculates errors on each point of F and saves
    if G.GetN() > 0:
        F.ConvFact = F.fit
        fitErrors = []
        listBinCenter = []
        fitValues = []
        bins2 = truthbins+bins
        for i in xrange(0,len(bins2)):
            binCenter = (bins2[i][0]+bins2[i][1])/2
            listBinCenter.append(float(binCenter))
            err = array( 'd', [0] )
            fitResult.GetConfidenceIntervals( 1, 1, 1, array('d',[binCenter]), err, 0.683, False )
            fitErrors.append(float(err[0]))
            fitValues.append(float(F.fit.Eval(binCenter)))
        F.ConvFactUp = TGraph( len(fitValues), array('d', listBinCenter ), numpy.add( fitValues, fitErrors ) )
	F.ConvFactDn = TGraph( len(fitValues), array('d', listBinCenter ), numpy.subtract( fitValues, fitErrors ) )
        F.ErrUp = F.ConvFactUp.Clone()
        F.ErrDn = F.ConvFactDn.Clone()
        return fitValues, fitErrors
