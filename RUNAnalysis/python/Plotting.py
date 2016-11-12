#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

import RUNA.RUNAnalysis.Alphabet_Header
from RUNA.RUNAnalysis.Alphabet_Header import *
import RUNA.RUNAnalysis.Plotting_Header
from RUNA.RUNAnalysis.Plotting_Header import *
import RUNA.RUNAnalysis.Converters
from RUNA.RUNAnalysis.Converters import *
import RUNA.RUNAnalysis.Distribution_Header
from RUNA.RUNAnalysis.Distribution_Header import *
import RUNA.RUNAnalysis.Alphabet
from RUNA.RUNAnalysis.Alphabet import *

# Makes B, D vs var1 plot and B/D ratio + fit plot and saves both
#### Est: The instance of Alphabet used for the background estimate
#### F: The form of the fit function
#### bins: The bins to find the ratio B/D for
#### var1: The name of the variable to fit as a function of (for the axis label)
#### var2: The name of the variable used to define B vs D (for the axis label)
#### presel: Preselection cuts
#### antitag: The inverse of the tag used to define A vs B
#### cut: the cut to determine B vs D, in the form [ variableName, "<" or ">" ]
#### center: Where to center the 2D plot, can be 0
def MakeFitPlots( Est, F, bins, var1, var2, var_array, presel, antitag, cut, center, Est2, F2, blinded=True ):

    Est.SetRegions( var_array, presel+"&"+antitag ) # Makes the 2D plot
    Est.TwoDPlot.SetStats(0)

    C1 = TCanvas( "C1", "", 800, 600 )
    C1.cd()

    # Make the 2D plot prettier, save    
    Est.TwoDPlot.Draw( "COLZ" )
    Est.TwoDPlot.GetXaxis().SetTitle( var1 )
    Est.TwoDPlot.GetYaxis().SetTitle( var2 )
    C1.SaveAs( "outputs/"+var1+"_2D.png" )

    # Find the ratio B/D in the bins and fit to F
    Est.GetRates( cut, bins, center, F )
    
    if blinded and "DATA" in Est.name:
        Est2.SetRegions( var_array, presel+"&"+antitag ) # Makes the 2D plot
        Est2.GetRates( cut, bins, center, F )
    
    # Create legend for plot
    leg = TLegend( 0.11, 0.6, 0.4, 0.8 )
    leg.SetLineColor(0)
    leg.SetFillColor(4001)
    leg.SetTextSize(0.03)
    leg.AddEntry( Est.G, "events used in fit", "PLE" )
    leg.AddEntry( Est.Fit.fit, "fit", "L" )
    leg.AddEntry( Est.Fit.ErrDn, "fit errors", "L" )


    # Pretty up G, Fit, and save
    C2 = TCanvas( "C2", "", 600, 800 )
    C2.cd()
    Est.G.SetTitle("")
    Est.G.Draw("AP")
    Est.G.GetXaxis().SetTitle( var1 )
    Est.G.GetYaxis().SetTitle( "R_{p/f}" )
    Est.G.GetYaxis().SetTitleOffset( 1.3 )

    gStyle.SetOptFit()

    Est.Fit.fit.Draw("same")
    Est.Fit.ErrUp.SetLineStyle(2)
    Est.Fit.ErrUp.Draw("same")
    Est.Fit.ErrDn.SetLineStyle(2)
    Est.Fit.ErrDn.Draw("same")
    
    leg.Draw()
    
    C2.SaveAs("outputs/"+var1+"Est_Fit.png")

# Makes the final background estimation plots and saves them.
# Draws the estimate with errors, and the actual signal region.
# Also draws ( Actual - Estimate )/Sigma_Actual plot
#### Est: The instance of Alphabet used for the background estimate
#### variable: The variable to plot the estimate as a function of
#### varTitle: Title of variable (for axis label)
#### binBoundaries: bins to plot background estimate in
#### antitag: Cut to define C region
#### tag: Cut to deine A region
#### var1: Variable fit is binned in
#### Est2: ONLY IF RUNNING ON BLINDED DATA: The MC instance of alphabet to plot the signal region (see blinded)
#### blinded: If running on data, should keep signal region blinded; If true, will plot the estimate on top of the MC signal region 
def MakeEstPlots( Est, variable, varTitle, binBoundaries, antitag, tag, var1, Est2, blinded=True ):

    Est.MakeEst( variable, binBoundaries, antitag, tag ) # Makes actual estimate

    FILE = TFile( "outputs/"+var1+"Est.root", "RECREATE" ) # Creates a root file to store plots in
    FILE.cd()
    
    V = TH1F( "data_obs", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Histogram for actual signal region plot
    VStack = THStack( "data_obs", "" ) # Stacked histogram for signal region plot

    # If the data is blinded, look at the MC signal region instead of the data
    if blinded and "DATA" in Est.name:
        Est2.MakeEstVariable( variable, binBoundaries, antitag, tag )
        for i in Est2.hists_MSR:
            i.Suw2()
            i.SetStats(0)
            V.Add(i)
            VStack.Add(i)
    # Otherwise:
    else:
        for i in Est.hists_MSR:
            i.Sumw2()
            i.SetStats(0)
            V.Add(i)
            VStack.Add(i)
        

    # The estimate is the sum of the histograms in self.hists_EST and self.hists_MSR_SUB
    N = TH1F( "EST", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Nominal estimate histogram
    for i in Est.hists_EST:
        N.Add( i, 1. )
    for i in Est.hists_MSR_SUB:
        N.Add( i, 1. )
    
    # We can do the same thing for the Up and Down shapes:
    NU = TH1F( "EST_Up", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Up estimate histogram
    for i in Est.hists_EST_UP:
        NU.Add( i, 1. )
    for i in Est.hists_MSR_SUB:
        NU.Add( i, 1. )

    ND = TH1F( "EST_Down", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Down estimate histogram
    for i in Est.hists_EST_DN:
        ND.Add( i, 1. )
    for i in Est.hists_MSR_SUB:
        ND.Add( i, 1. )
    
    # Anti-tag region (C) Plot
    A = TH1F( "EST_Antitag", "", len(binBoundaries)-1, array('d',binBoundaries)) # anti-tag region (C) histogram
    for i in Est.hists_ATAG:
        A.Add( i, 1. )

    ##################################################
    #### SKIPPED SETTING BIN CONTENT FOR OVERFLOW ####
    ##################################################

    FILE.Write()
    FILE.Save() 

    # Pretty up plots for saving
    NU.SetLineColor( kBlack )
    ND.SetLineColor( kBlack )
    NU.SetLineStyle(2)
    ND.SetLineStyle(2)
    N.SetLineColor( kBlack )
    N.SetFillColor( kPink+3 )

    V.SetStats(0)
    V.Sumw2()
    V.SetLineColor(1)
    V.SetMarkerColor(1)
    V.SetMarkerStyle(20)

    N.GetYaxis().SetTitle("events")
    N.GetXaxis().SetTitle( varTitle )

    FindAndSetMax( [ V, N, NU, ND ] ) # Set maximum and minimum of all the plots
    
    Pull = V.Clone( "Pull" ) # Ratio (actual - est)/sigma_actual plot
    Pull.Add( N, -1 )
    
    ################################################
    ### DON'T UNDERSTAND ERRORS ON PLOTS, VERIFY ###
    ################################################

    for i in range(1, N.GetNbinsX()+1):
        
        # Filling Pull Plot
        P = Pull.GetBinContent(i)
        Ve = V.GetBinError(i)
        if Ve > 1.:
            Pull.SetBinContent(i, P/Ve)
        Pull.SetBinError(i, 1.) #????????????????????

    # Pretty up pull plot
    Pull.GetXaxis().SetTitle("")
    Pull.SetStats(0)
    Pull.SetLineColor(1)
    Pull.SetFillColor(0)
    Pull.SetMarkerColor(1)
    Pull.SetMarkerStyle(20)
    Pull.GetXaxis().SetNdivisions(0)
    Pull.GetYaxis().SetNdivisions(4)
    Pull.GetYaxis().SetTitle("#frac{MC - Data Est}{#sigma_{MC}}")
    Pull.GetYaxis().SetLabelSize(85/15*Pull.GetYaxis().GetLabelSize())
    Pull.GetYaxis().SetTitleSize(4.2*Pull.GetYaxis().GetTitleSize())
    Pull.GetYaxis().SetTitleOffset(0.175)
    Pull.GetYaxis().SetRangeUser(-3.,3.)

    leg2 = TLegend(0.6,0.6,0.89,0.89)
    leg2.SetLineColor(0)
    leg2.SetFillColor(0)
    leg2.AddEntry(V, "MC Backgrounds", "PL")
    leg2.AddEntry(N, "Data background prediction", "F")

    # A line at -2, -1, 0, 1, 2 for pull plot
    T0 = TLine(800,0.,4509,0.)
    T0.SetLineColor(kBlue)
    T2 = TLine(800,2.,4509,2.)
    T2.SetLineColor(kBlue)
    T2.SetLineStyle(2)
    Tm2 = TLine(800,-2.,4509,-2.)
    Tm2.SetLineColor(kBlue)
    Tm2.SetLineStyle(2)

    T1 = TLine(800,1.,4509,1.)
    T1.SetLineColor(kBlue)
    T1.SetLineStyle(3)
    Tm1 = TLine(800,-1.,4509,-1.)
    Tm1.SetLineColor(kBlue)
    Tm1.SetLineStyle(3)

    C4 = TCanvas("C4", "", 800, 800)

    # Draw all plots and save
    plot = TPad("pad1", "The pad 80% of the height",0,0.15,1,1)
    pull = TPad("pad2", "The pad 20% of the height",0,0,1.0,0.15)
    plot.Draw()
    pull.Draw()
    plot.cd()

    N.Draw("Hist")
    V.Draw("same E0")
    plot.SetLogy()
    leg2.Draw()

    pull.cd()
    Pull.Draw("")

    T0.Draw("same")
    T2.Draw("same")
    Tm2.Draw("same")
    T1.Draw("same")
    Tm1.Draw("same")

    Pull.Draw("same")

    C4.SaveAs("outputs/"+var1+"Est_Plot.png")

    print str(N.Integral())
    print str(V.Integral())

