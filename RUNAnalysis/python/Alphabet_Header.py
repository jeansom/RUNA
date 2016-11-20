#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

from RUNA.RUNAnalysis.Converters import *

###################################################################
### Provides the methods needed to make a B/D graph and fit it. ###
###################################################################

# Takes a 2D plot and measures the Pass/Fail ratios in given bins
#### plot: 2D plot to perform the measurement on
#### bins: list of bins to measure the P/F ratio in (each will yield a B/D point)
#### cut: valeu to differentiate pass from fail. Should be on the y-axis of the plot
#### which: ">" or "<" to tell which way the cut goes
#### center: the x-var is recentered about the middle of the blinded region. This tells where to recenter to. Can be left as 0.
def AlphabetSlicer( plot, bins, cut, which, center ):
    x = [] # X values for each bin
    y = [] # Y values (pass/fail ratios) for each bin
    exl = [] # error below x values
    eyl = [] # error below y values
    exh = [] # error above x values
    eyh = [] # error above y values

#    print str( bins )
    for b in bins: # Loop through the bins (along x axis, should contain gap for signal region)
        print str(b)
        passed = 0 # Number of events which passed cut in bin b
        failed = 0 # Number of events which failed cut in bin b
        for i in range( plot.GetNbinsX() ):
            for j in range( plot.GetNbinsY() ): # Loops through all the bins in the 2D plot
                if plot.GetXaxis().GetBinCenter(i) < b[1] and plot.GetXaxis().GetBinCenter(i) > b[0]: # If the bin (i,j) is in bin b
                    print "here"

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
                            print plot.GetBinContent(i,j)
                        else:
                            passed = passed + plot.GetBinContent(i,j)
                            print plot.GetBinContent(i,j)
                    
        # Corrects for negative passed or failed values
        ######################
        ####### VERIFY #######
        ######################
        print str(passed) + " " + str(failed)
        if passed < 0:
            passed = 0
        if failed < 0:
            failed = 0

        print str(passed) + " pass"
        print str(failed) + " fail"
        
        ep = math.sqrt( passed ) # Error on passed
        ef = math.sqrt( failed ) # Error on failed
        
        ##################################
        ####### SKIPPED CONDITIONS #######
        ##################################

        if passed == 0 and failed == 0:
            print "bin not filled: passed = 0 and failed = 0"
            continue
        elif failed == 0:
            print "bin not filled: failed = 0"
            continue
        elif passed == 0:
            print "bin not filled: passed = 0"
            continue
        ###########################
        ###### VERIFY ERROR #######
        ###########################

        errl = (passed/failed) * TMath.Sqrt( TMath.Power((ep/passed),2) + TMath.Power((ef/failed),2) ) # Error on passed/failed
        errh = (passed/failed) * TMath.Sqrt( TMath.Power((ep/passed),2) + TMath.Power((ef/failed),2) ) # Error on passed/failed
#        errl = TMath.Sqrt( TMath.Power( ((passed/(failed-ef))-passed/failed),2) + TMath.Power( ((passed+ep)/failed) - passed/failed,2) ) # Error on passed/failed
#        errh = TMath.Sqrt( TMath.Power( ((passed/(failed+ef))-passed/failed),2) + TMath.Power( ((passed-ep)/failed) - passed/failed ,2 ) )  # Error on passed/failed

        x.append( (float( (b[0]+b[1])/2. - center ) ) ) # X value = bin center - center
        exl.append( float( (b[1]-b[0])/2. ) ) # X low error = bin width
        exh.append( float( (b[1]-b[0])/2. ) ) # X high error = bin width
        
        y.append( passed/failed ) # Y value = pass/fail
        eyh.append( errh ) # See error calculation above
        eyl.append( errl )
        # Low y error
        ######################
        ####### VERIFY #######
        #####################
#        if (passed/failed) - err > 0.:
#            eyl.append(err)
#        else:
#            eyl.append( passed/failed )
        
    # Creates TGraphAsymmErrors with x values, y values, and errors
    if len(x) > 0:
        G = TGraphAsymmErrors( len(x), scipy.array(x), scipy.array(y), scipy.array(exl), scipy.array(exh), scipy.array(eyl), scipy.array(eyh) )
    else:
        G = TGraphAsymmErrors()

    return G

def AlphabetDivide( BPlot, DPlot, bins ):

    rebin = BPlot.GetNbinsX()
    rebin = rebin/(len(bins))
    print rebin
    if rebin != 1: 
        print "Rebinning"
        BPlot.Rebin( rebin )
        DPlot.Rebin( rebin )

    BPlot.Sumw2()
    DPlot.Sumw2()
    RatioPlot = BPlot.Clone()
    RatioPlot.Sumw2()
    RatioPlot.Divide( DPlot )
    
    x = [] # X values for each bin
    y = [] # Y values (pass/fail ratios) for each bin
    exl = [] # error below x values
    eyl = [] # error below y values
    exh = [] # error above x values
    eyh = [] # error above y values

    for b in bins:
        print RatioPlot.GetBinContent( RatioPlot.FindBin( (b[0]+b[1])/2 ) )
        x.append( float( (b[0]+b[1])/2 ) )
        exl.append( float( (b[1]-b[0])/2 ) )
        exh.append( float( (b[1]-b[0])/2 ) )
        y.append( float( RatioPlot.GetBinContent( RatioPlot.FindBin( (b[0]+b[1])/2 ) ) ) )
        eyl.append( float ( RatioPlot.GetBinError( RatioPlot.FindBin( (b[0]+b[1])/2 ) ) ) )
        eyh.append( float( RatioPlot.GetBinError( RatioPlot.FindBin( (b[0]+b[1])/2 ) ) ) )

    if len(x) > 0:
        G = TGraphAsymmErrors( len(x), scipy.array(x), scipy.array(y), scipy.array(exl), scipy.array(exh), scipy.array(eyl), scipy.array(eyh) )
    else:
        G = TGraphAsymmErrors()
    return G

        
# Fits a TGAE, G, to a function, using the form F
#### G: A TGraphAsymmErrors, see method AlphabetSlicer
#### F: A Converter, see Converters.py
def AlphabetFitter( G, F ):
    G.Fit( F.fit, F.Opt ) # Fits G to a function of form F
    fitter = TVirtualFitter.GetFitter()
    F.Converter(fitter) # Gets fit errors and saves as F.ErrUp and F.ErrDn