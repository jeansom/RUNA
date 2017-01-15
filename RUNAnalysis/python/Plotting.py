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
def MakeFitPlots( Est, F, bins, var1, var2, var_array, presel, antitag, tagB, tagD, cut, center, Est2, F2, folder, blinded=True ):

    Est.SetRegions( var_array, presel+"&"+antitag, tagB, tagD ) # Makes the 2D plot
    Est.TwoDPlot.SetStats(0)
    EstProf = Est.TwoDPlot.ProfileX("EstProfX")

    C1 = TCanvas( "C1", "", 800, 600 )
    C1.cd()

    # Make the 2D plot prettier, save    
    Est.TwoDPlot.Draw( "COLZ" )
    Est.TwoDPlot.GetXaxis().SetTitle( var1 )
    Est.TwoDPlot.GetYaxis().SetTitle( var2 )
    C1.SaveAs( folder+var1+"_2D.png" )

    # Find the ratio B/D in the bins and fit to F
    Est.GetRates( cut, bins, center, F )
    
    if blinded:
        print "Staying blinded"
        Est2.SetRegions( var_array, presel+"&"+antitag, tagB, tagD ) # Makes the 2D plot
        Est2.GetRates( cut, bins, center, F2 )
    
    # Create legend for plot
    leg = TLegend( 0.11, 0.68, 0.4, 0.85 )
    leg.SetLineColor(0)
    leg.SetFillColor(4001)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.03)
    leg.AddEntry( Est.G, "events used in fit", "PLE" )
    leg.AddEntry( Est.Fit.fit, "fit", "L" )

    # Pretty up G, Fit, and save
    C2 = TCanvas( "C2", "", 10, 10, 750, 500 )
    C2.cd()
    C2.SetGrid( 4 )
    Est.G.SetTitle("")
    Est.G.GetYaxis().SetRangeUser(0,0.87)
    Est.G.Draw("AP")
    Est.G.GetXaxis().SetTitle( var1 )
    Est.G.GetYaxis().SetTitle( "R_{p/f}" )
    Est.G.GetYaxis().SetTitleOffset( 1.3 )
    Est.G.GetYaxis().SetNdivisions( 28 )
    gStyle.SetOptFit()

    Est.Fit.fit.Draw("same")
    if Est.G.GetN() > 0:
        leg.AddEntry( Est.Fit.ErrDn, "fit errors", "L" )
        Est.Fit.ErrUp.SetLineStyle(2)
        Est.Fit.ErrUp.Draw("same")
        Est.Fit.ErrDn.SetLineStyle(2)
        Est.Fit.ErrDn.Draw("same")
    
    leg.Draw()
    
    C2.SaveAs(folder+var1+"Est_Fit.png")

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
def MakeEstPlots( Est, variable, varTitle, binBoundaries, antitag, tag, var1, Est2, folder, blinded=True, Pull=TH1D()  ):

    Est.MakeEst( variable, binBoundaries, antitag, tag ) # Makes actual estimate

    FILE = TFile( folder+var1+"Est.root", "RECREATE" ) # Creates a root file to store plots in
    FILE.cd()
    
    V = TH1F( "data_obs", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Histogram for actual signal region plot
    VStack = THStack( "data_obs", "" ) # Stacked histogram for signal region plot

    # If the data is blinded, look at the MC signal region instead of the data
    if blinded:
        print "Staying blinded"
        Est2.MakeEst( variable, binBoundaries, antitag, tag )
        for i in Est2.hists_MSR:
            i.Sumw2()
            i.SetStats(0)
            V.Add(i)
            VStack.Add(i)
    # Otherwise:
    else:
        for i in Est.hists_MSR:
            print "here"
            i.Sumw2()
            i.SetStats(0)
            V.Add(i)
            VStack.Add(i)
        

    # The estimate is the sum of the histograms in self.hists_EST and self.hists_MSR_SUB
    N = TH1F( "EST", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Nominal estimate histogram
    N1 = TH1F( "EST1", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Nominal estimate histogram
    NStack = THStack( "EST", "" )
    for i in Est.hists_EST:
        N.Add( i, 1. )
        N1.Add( i, 1. )
        i.SetLineColor(kBlack)
    if len(Est.hists_MSR_SUB) == 6:
        Est.hists_MSR_SUB[0].SetFillColor(6)
        Est.hists_MSR_SUB[1].SetFillColor(6)
        Est.hists_MSR_SUB[2].SetFillColor(6)
        Est.hists_MSR_SUB[3].SetFillColor(5)
        Est.hists_MSR_SUB[4].SetFillColor(8)
        Est.hists_MSR_SUB[5].SetFillColor(2)
    elif len(Est.hists_MSR_SUB) == 2:
        Est.hists_MSR_SUB[0].SetFillColor(8)
        Est.hists_MSR_SUB[1].SetFillColor(2)        
    else:
        n = 7
        for hist in Est.hists_MSR_SUB:
            hist.SetFillColor(n)
            n += 1
    for i in Est.hists_MSR_SUB:
        N.Add( i, 1. )
        NStack.Add(i)
        i.SetLineColor(kBlack)
    NStack.Add(N1)
    
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
    N1.SetLineColor( kBlack )
    N1.SetFillColor( kBlue )
    N.SetLineColor( kBlack )
    N.SetFillColor( kBlue )

    V.SetStats(0)
    V.Sumw2()
    V.SetLineColor(kBlack)
    V.SetMarkerColor(1)
    V.SetMarkerStyle(20)

    N1.GetYaxis().SetTitle("events")
    N1.GetXaxis().SetTitle( varTitle )

    FindAndSetMax( [ N, NU, ND ], False ) # Set maximum and minimum of all the plots
    Pull = V.Clone( "Pull" ) # Ratio (actual - est)/sigma_actual plot
    Pull.Add( N, -1 )
    
    ################################################
    ### DON'T UNDERSTAND ERRORS ON PLOTS, VERIFY ###
    ################################################

    Boxes = []
    sBoxes = []
    pBoxes = []
    maxy = 0.
    for i in range(1, N.GetNbinsX()+1):
        P = Pull.GetBinContent(i)
        Ve = V.GetBinError(i)
        if Ve > 1.:
            Pull.SetBinContent(i, P/Ve)
        Pull.SetBinError(i, 1.)
        if A.GetBinContent(i)==0:
            a = 0
        else:
            a = A.GetBinError(i)*N.GetBinContent(i)/A.GetBinContent(i)
        u = NU.GetBinContent(i) - N.GetBinContent(i)
        d = N.GetBinContent(i) - ND.GetBinContent(i)
        x1 = Pull.GetBinCenter(i) - (0.5*Pull.GetBinWidth(i))
        y1 = N.GetBinContent(i) - math.sqrt((d*d) + (a*a))
        s1 = N.GetBinContent(i) - a
        if y1 < 0.:
            y1 = 0
        if s1 < 0:
            s1 = 0
        x2 = Pull.GetBinCenter(i) + (0.5*Pull.GetBinWidth(i))
        y2 = N.GetBinContent(i) + math.sqrt((u*u) + (a*a))
        s2 = N.GetBinContent(i) + a
        if maxy < y2:
            maxy = y2
        if Ve > 1.:
            yP1 = -math.sqrt((d*d) + (a*a))/Ve
            yP2 = math.sqrt((u*u) + (a*a))/Ve
        else:
            yP1 = -math.sqrt((d*d) + (a*a))
            yP2 = math.sqrt((u*u) + (a*a))
        tempbox = TBox(x1,y1,x2,y2)
        temppbox = TBox(x1,yP1,x2,yP2)
        tempsbox = TBox(x1,s1,x2,s2)
        Boxes.append(tempbox)
        sBoxes.append(tempsbox)
        pBoxes.append(temppbox)

    pullInt = Pull.Integral()

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
#    Pull.GetYaxis().SetTitle(""))
    print pullInt
    Pull.GetYaxis().SetLabelSize(85/15*Pull.GetYaxis().GetLabelSize())
    Pull.GetYaxis().SetTitleSize(4.2*Pull.GetYaxis().GetTitleSize())
    Pull.GetYaxis().SetTitleOffset(0.175)
    Pull.GetYaxis().SetRangeUser(-3.,3.)

    for i in Boxes:
        i.SetFillColor(12)
        i.SetFillStyle(3244)
    for i in pBoxes:
        i.SetFillColor(12)
        i.SetFillStyle(3144)
    for i in sBoxes:
        i.SetFillColor(38)
        i.SetFillStyle(3002)

    leg2 = TLegend(0.4,0.73,0.89,0.89)
    leg2.SetLineColor(0)
    leg2.SetFillColor(0)
    leg2.SetFillStyle(0)
    leg2.AddEntry(V, "Data", "PL")
    leg2.AddEntry( N1, "Data background prediction", "F")
    leg2.AddEntry( Est.hists_MSR_SUB[0], "W Jets", "F")
    leg2.AddEntry( Est.hists_MSR_SUB[1], "TT Jets", "F")
#    leg2.AddEntry( 0, str(pullInt), "" )
    leg2.AddEntry(Boxes[0], "total uncertainty", "F")
    leg2.AddEntry(sBoxes[0], "background statistical component", "F")
    leg2.AddEntry( 0, "Number of predicted events: " + str(N.Integral()), "" )
    leg2.AddEntry( 0, "Actual number of events: " + str(V.Integral()), "" )
    # A line at -2, -1, 0, 1, 2 for pull plot
    T0 = TLine(50,0.,350,0.)
    T0.SetLineColor(kBlue)
    T2 = TLine(50,2.,350,2.)
    T2.SetLineColor(kBlue)
    T2.SetLineStyle(2)
    Tm2 = TLine(50,-2.,350,-2.)
    Tm2.SetLineColor(kBlue)
    Tm2.SetLineStyle(2)

    T1 = TLine(50,1.,350,1.)
    T1.SetLineColor(kBlue)
    T1.SetLineStyle(3)
    Tm1 = TLine(50,-1.,350,-1.)
    Tm1.SetLineColor(kBlue)
    Tm1.SetLineStyle(3)

    C4 = TCanvas("C4", "", 800, 800)

    # Draw all plots and save
    plot = TPad("pad1", "The pad 80% of the height",0,0.10,1,1)
    pull = TPad("pad2", "The pad 20% of the height",0,0,1.0,0.12)
    plot.Draw()
    pull.Draw()
    plot.cd()

    NStack.Draw("Hist")
    NStack.GetYaxis().SetRangeUser( .5, 5000 )
    NStack.SetMaximum( 5000 )
    NStack.SetMinimum( .5 )
    NStack.Draw("Hist")
    V.SetLineWidth(2)
    V.GetYaxis().SetRangeUser( .5, 5000 )
    V.Draw("same E0")
    plot.SetLogy()
    for i in Boxes:
        i.Draw("same")
    for i in sBoxes:
        i.Draw("same")
    leg2.Draw()
    pull.cd()
    Pull.Draw("")
    for i in pBoxes:
        i.Draw("same")
    T0.Draw("same")
    T2.Draw("same")
    Tm2.Draw("same")
    T1.Draw("same")
    Tm1.Draw("same")

    Pull.Draw("same")

    C4.SaveAs(folder+var1+"Est_Plot.png")

    print str(N.Integral())
    print str(V.Integral())

    print(Pull)
    return pBoxes

