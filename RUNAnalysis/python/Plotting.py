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
import CMS_lumi as CMS_lumi 

# Makes B, D vs var1 plot and B/D ratio + fit plot and saves both
#### Est: The instance of Alphabet used for the background estimate
#### F: The form of the fit function
#### bins: The bins to find the ratio B/D for
#### var1: The name of the variable to fit as a function of (for the axis label)
#### var2: The name of the variable used to define B vs D (for the axis label)
#### var_array: bins to use for the 2D plot
#### presel: Preselection cuts
#### antitag: The inverse of the tag used to define A vs B
#### tagB: Cuts to define B region
#### tagD: Cuts to define D region
#### cut: the cut to determine B vs D, in the form [ variableName, "<" or ">" ]
#### center: Where to center the 2D plot, can be 0
#### Est2: If staying blinded, this is the set of distributions... with the MC instead of data to run on
#### F2: If staying blinded, this is the function to fit the MC to
#### folder: The folder to save all the plots in
#### blinded: Whether or not to stay blinded
def MakeFitPlots( Est, F, bins, var1, var2, var_array, presel, antitag, cut, center, Est2, F2, folder, binBoundaries, fit=False, blinded=True ):

    gStyle.SetOptStat(0) # No stat box
    gStyle.SetOptFit(kFALSE) # No fit box

    Est.SetRegions( var_array, presel+"&"+antitag ) # Makes the 2D plot
    Est.TwoDPlot.SetStats(0)

    EstProf = Est.TwoDPlot.ProfileX("EstProfX") # Makes the X Profile of the 2D plot, not necessary

    C1 = TCanvas( "C1", "", 800, 600 )
    C1.cd()

    # Make the 2D plot prettier, save    
    Est.TwoDPlot.Draw( "COLZ" )
    Est.TwoDPlot.GetXaxis().SetTitle( var1 )
    Est.TwoDPlot.GetYaxis().SetTitle( var2 )
    C1.SaveAs( folder+"_2D.png" )
    # Find the ratio B/D in the bins and fit to F
    Est.GetRates( cut, bins, [], center, F, binBoundaries )
    
    if blinded: # If staying blinded:
        print "Staying blinded"
        Est2.SetRegions( var_array, presel+"&"+antitag  ) # Makes the 2D plot for the MC instead of data
        Est2.GetRates( cut, bins, center, F2, binBoundaries ) # Finds the ratio B/D and fits to F2

    # Making TLatex for legend
    chi2Test = TLatex( 0.2, 0.85, '#chi^{2}/ndF = '+ str( round( ComputeChi2(Est.G, Est.Fit.fit), 2 ) )+'/'+str( int( Est.Fit.fit.GetNDF() ) ) )
    p0 = TLatex( 0.2, 0.80, 'p0 = '+ '{:0.2e}'.format(Est.Fit.fit.GetParameter( 0 )) +' #pm '+ '{:0.2e}'.format(Est.Fit.fit.GetParError( 0 )))
    p1 = TLatex( 0.2, 0.75, 'p1 = '+ '{:0.2e}'.format(Est.Fit.fit.GetParameter( 1 )) +' #pm '+ '{:0.2e}'.format(Est.Fit.fit.GetParError( 1 )))
    p2 = TLatex( 0.2, 0.70, 'p2 = '+ '{:0.2e}'.format(Est.Fit.fit.GetParameter( 2 )) +' #pm '+ '{:0.2e}'.format(Est.Fit.fit.GetParError( 2 )) )

    chi2Test.SetNDC()
    chi2Test.SetTextFont(42) ### 62 is bold, 42 is normal
    chi2Test.SetTextSize(0.04)
    p0.SetNDC()
    p0.SetTextFont(42) ### 62 is bold, 42 is normal
    p0.SetTextSize(0.04)
    p1.SetNDC()
    p1.SetTextFont(42) ### 62 is bold, 42 is normal
    p1.SetTextSize(0.04)
    p2.SetNDC()
    p2.SetTextFont(42) ### 62 is bold, 42 is normal
    p2.SetTextSize(0.04)


    # Pretty up G, Fit, and save
    C2 = TCanvas( "C2", "", 10, 10, 750, 500 )
    C2.cd()

    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.relPosX = 0.13

    Est.G.SetTitle("")
    
    # Draw Pass/Fail, set titles...
    if not fit: Est.G.GetFunction("QuadraticFitMass").SetBit(TF1.kNotDraw)
    Est.G.Draw("AP")
    Est.G.GetXaxis().SetTitle( "Average Mass" )
    Est.G.GetXaxis().SetTitleSize(Est.G.GetXaxis().GetTitleSize()*1.3)
    Est.G.GetYaxis().SetTitle( "R_{p/f}" )
    Est.G.GetYaxis().SetTitleOffset( 1.0 )
    Est.G.GetYaxis().SetTitleSize(Est.G.GetYaxis().GetTitleSize()*1.3)
    Est.G.GetYaxis().SetNdivisions( 28 )

    # Draw fit, err up, err down
    if Est.G.GetN() > 0:
        Est.Fit.ConvFactUp.SetLineStyle(2)
        Est.Fit.ConvFactUp.SetLineWidth(2)
        Est.Fit.ConvFactUp.SetLineColor(kRed)
        Est.Fit.ConvFactDn.SetLineStyle(2)
        Est.Fit.ConvFactDn.SetLineWidth(2)
        Est.Fit.ConvFactDn.SetLineColor(kRed)
        if fit:
            Est.Fit.fit.Draw("same") 
            Est.Fit.ConvFactUp.Draw("same pc")
            Est.Fit.ConvFactDn.Draw("same pc")
            chi2Test.Draw('same')
    CMS_lumi.CMS_lumi(C2, 4, 0)
    
    C2.SaveAs(folder+"Est_Fit.png")

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
#### folder: folder to save everyting in
#### isMC: running over MC or data
#### blinded: If running on data, should keep signal region blinded; If true, will plot the estimate on top of the MC signal region 
#### Pull: Pretty sure you can ignore, just something I was trying
def MakeEstPlots( Est, variable, varTitle, binBoundaries, antitag, tag, var1, Est2, folder, rhoBinBoundaries, fit=False, isMC=True, blinded=True, log=True, Pull=TH1D()  ):
    Est.MakeEst( variable, binBoundaries, antitag, tag, fit, rhoBinBoundaries ) # Makes actual estimate

    FILE = TFile( folder+var1+"Est.root", "RECREATE" ) # Creates a root file to store plots in
    FILE.cd()
    
    V = TH1F( "data_obs", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Histogram for actual signal region plot
    VStack = THStack( "data_obs", "" )

    # If the data is blinded, look at the MC signal region instead of the data
    if blinded:
        print "Staying blinded"
        col = 41
        Est2.MakeEst( variable, binBoundaries, antitag, tag, fit ) # Makes actual estimation for MC
        for i in Est2.hists_MSR: # Loops through signal region plots
            i.Sumw2()
            i.SetLineWidth(2)
            col = col+1
            i.SetStats(0)
            VStack.Add(i)
            V.Add(i)
#            for bin in xrange(1, i.GetNbinsX()+1):
#                V.SetBinContent(bin, V.GetBinContent(bin)+i.GetBinContent(bin))
    # Otherwise:
    else:
        col = 41
        for i in Est.hists_MSR: # Loops through signal region plots
            i.Sumw2()
            i.SetFillColor(0)
            i.SetMarkerStyle(20)
            i.SetMarkerColor(col)
            col = col+1
            V.Add(i)
#            for bin in xrange(1, i.GetNbinsX()+1):
#                V.SetBinContent(bin, V.GetBinContent(bin)+i.GetBinContent(bin))
            VStack.Add(i)

    if len(Est.hists_MSR_SUB) == 3:
        Est.hists_MSR_SUB[0].SetFillColor(6)
        Est.hists_MSR_SUB[1].SetFillColor(8)
        Est.hists_MSR_SUB[2].SetFillColor(2)        
    else:
        n = 7
        for hist in Est.hists_MSR_SUB:
            hist.SetFillColor(n)
            n += 1

    # The estimate is the sum of the histograms in self.hists_EST and self.hists_MSR_SUB minus the histograms in self.hists_EST_SUB
    N = TH1F( "EST", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Nominal estimate histogram
    N1 = TH1F( "EST1", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Nominal estimate histogram WITHOUT the subtracted histograms added back in!!!
    NStack = THStack( "EST", "" ) # Nominal estimate stack histogram

    for i in Est.hists_MSR_SUB: # Loops through the signal region plots of all subtracted distributions
        N.Add(i)
#        for bin in xrange(1, N.GetNbinsX()+1):
#            N.SetBinContent(bin, N.GetBinContent(bin)+i.GetBinContent(bin))
        NStack.Add(i) # Adds plots individually to NStack (nominal estimate stack plot)
        i.SetLineColor(kBlack)

    for i in Est.hists_EST: # Loops through all plots to add to the estimation
        N.Add(i)
        N1.Add(i)
#        for bin in xrange(1, N.GetNbinsX()+1):
#            N.SetBinContent(bin, N.GetBinContent(bin)+i.GetBinContent(bin))
#        for bin in xrange(1, N1.GetNbinsX()+1):
#            N1.SetBinContent(bin, N1.GetBinContent(bin)+i.GetBinContent(bin))

    for i in Est.hists_EST_SUB: # Loops through all plots to subtract from the estimation
        N.Add(i,-1)
        N1.Add(i,-1)
#        for bin in xrange(1, N.GetNbinsX()+1):
#            N.SetBinContent(bin, N.GetBinContent(bin)-i.GetBinContent(bin))
#        for bin in xrange(1, N1.GetNbinsX()+1):
#            N1.SetBinContent(bin, N1.GetBinContent(bin)-i.GetBinContent(bin))

    removeNegativeBins( N )
    removeNegativeBins( N1 )

    NStack.Add(N1) # Adds the background estimate WITHOUT subtracted added back in to NStack, which already has the subtracted plots signal regions

    # We can do the same thing for the Up and Down shapes:
    NU = TH1F( "EST_Up", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Up estimate histogram
    for i in Est.hists_EST_UP: # Adds background estimations for distributions to be added together
        NU.Add(i)
#        for bin in xrange(1, NU.GetNbinsX()+1):
#            NU.SetBinContent(bin, NU.GetBinContent(bin)+i.GetBinContent(bin))
    for i in Est.hists_EST_SUB_UP: # Subtracts background estimations for distributions to be subtracted from the final estimate
        NU.Add( i, -1. )
#        for bin in xrange(1, NU.GetNbinsX()+1):
#            NU.SetBinContent(bin, NU.GetBinContent(bin)-i.GetBinContent(bin))
    removeNegativeBins(NU)
    for i in Est.hists_MSR_SUB: # Adds the signal regions for the distributions to be subtracted in
#        for bin in xrange(1, NU.GetNbinsX()+1):
#            NU.SetBinContent(bin, NU.GetBinContent(bin)+i.GetBinContent(bin))
        NU.Add( i, 1. )

    ND = TH1F( "EST_Down", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Down estimate histogram
    for i in Est.hists_EST_DN: # Adds background estimations for distributions to be added together
        ND.Add(i)
#        for bin in xrange(1, ND.GetNbinsX()+1):
#            ND.SetBinContent(bin, ND.GetBinContent(bin)+i.GetBinContent(bin))
    for i in Est.hists_EST_SUB_DN: # Subtracts background estimations for distributions to be subtracted from the final estimate
        ND.Add(i, -1)
#        for bin in xrange(1, ND.GetNbinsX()+1):
#            ND.SetBinContent(bin, ND.GetBinContent(bin)-i.GetBinContent(bin))
    removeNegativeBins(ND)
    for i in Est.hists_MSR_SUB: # Adds the signal regions for the distributions to be subtracted in
        ND.Add(i)
#        for bin in xrange(1, ND.GetNbinsX()+1):
#            ND.SetBinContent(bin, ND.GetBinContent(bin)+i.GetBinContent(bin))
    
    # Anti-tag region (C) Plot
    A = TH1F( "EST_Antitag", "", len(binBoundaries)-1, array('d',binBoundaries)) # anti-tag region (C) histogram
    for i in Est.hists_ATAG: # Adds all the C Plots together
        A.Add(i)
#        for bin in xrange(1, A.GetNbinsX()+1):
#            A.SetBinContent(bin, A.GetBinContent(bin)+i.GetBinContent(bin))

    for i in xrange(len(Est.hists_SIG)):
        if i%2==0:
            Est.hists_SIG[i].SetLineColor(kViolet+4)
            Est.hists_SIG[i].SetFillStyle(3454)
        else:
            Est.hists_SIG[i].SetLineColor(kGray+3)
            Est.hists_SIG[i].SetFillStyle(3445)
        Est.hists_SIG[i].SetLineWidth(3)
        Est.hists_SIG[i].SetFillColorAlpha(kGray+3, 0.5)
    Est.G.Write()
    FILE.Write() # Writes all the previously created plots to the root file
    FILE.Save() 

    # Pretty up plots for saving
    NU.SetLineColor( kBlack )
    ND.SetLineColor( kBlack )
    NU.SetLineStyle(2)
    ND.SetLineStyle(2)
    N1.SetLineColor( kBlack )
    N1.SetFillColor( kAzure-4 )
    N.SetLineColor( kBlack )
    N.SetFillColor( kAzure-4 )

    V.SetLineColor(kBlack)
    V.SetMarkerColor(1)
    V.SetMarkerStyle(20)

    N1.GetYaxis().SetTitle("events")
    N1.GetXaxis().SetTitle( varTitle )

    Pull = V.Clone( "Pull_quad" ) # Ratio (actual - est)/sqrt(sigma_actual^2 + sigma_sys^2) plot
    Pull.Add( N, -1 )

    Pull2 = V.Clone( "Pull2" ) # Ratio (actual/est) plot
    Pull2.Divide( N )
    Pull_norm = V.Clone( "Pull_norm" ) # Ratio (actual - est)/sigma_actual plot
    Pull_norm.Add( N, -1 )
    
    Boxes = [] # Errors on estimation
    sBoxes = [] # Systematic errors on estimation
    pBoxes = [] # Errors on pull
    maxy = 0.

    for i in range(1, N.GetNbinsX()+1): # Loop through all bins in N (nominal estimation)
        P = Pull.GetBinContent(i)
        Ve = V.GetBinError(i)
        Pull.SetBinError(i, 1.) # Sets pull bin error 1
        Pull_norm.SetBinError(i, 1.) # Sets pull bin error 1
        if A.GetBinContent(i)==0: # If antitag region bin content is 0
            a = 0 # a, some some part of the error on the bkg est? = 0
        else:
            a = A.GetBinError(i)*N.GetBinContent(i)/A.GetBinContent(i) # otherwise, this expression
        u = NU.GetBinContent(i) - N.GetBinContent(i) # u, upper error on estimation
        d = N.GetBinContent(i) - ND.GetBinContent(i) # d, lower error on estimation
        x1 = Pull.GetBinCenter(i) - (0.5*Pull.GetBinWidth(i)) # Start of bin
        y1 = N.GetBinContent(i) - math.sqrt((d*d) + (a*a)) # Bottom of error on estimation
        s1 = N.GetBinContent(i) - a # Bottom of systematic error on estimation?
        if y1 < 0.: # Don't want the lower error to be negative, set to 0
            y1 = 0
        if s1 < 0: # Don't want the lower error to be negative, set to 0
            s1 = 0
        x2 = Pull.GetBinCenter(i) + (0.5*Pull.GetBinWidth(i)) # End of bin
        y2 = N.GetBinContent(i) + math.sqrt((u*u) + (a*a)) # Top of error on estimation
        s2 = N.GetBinContent(i) + a # Top of systematic error on estimation?
        if maxy < y2: # Don't want the upper error to be above the max, set to max
            maxy = y2
        if Ve > 1.: # If error on V (signal region plots) is > 1
            yP1 = -math.sqrt((d*d) + (a*a))/Ve # Bottom of pull error
            yP2 = math.sqrt((u*u) + (a*a))/Ve # Top of pull error
        else:
            yP1 = -math.sqrt((d*d) + (a*a)) # Bottom of pull error
            yP2 = math.sqrt((u*u) + (a*a)) # Top of pull error
        if Ve*Ve + yP1*yP1 > 1: # For quad pull
            Pull.SetBinContent( i, P / math.sqrt( Ve*Ve + yP1*yP1 ) ) # Filling quad pull
        if Ve > 1:
            Pull_norm.SetBinContent( i, P/Ve ) # Filling normal pull

        # TBoxes with the errors on the various plots
        tempbox = TBox(x1,y1,x2,y2)
        temppbox = TBox(x1,yP1,x2,yP2)
        tempsbox = TBox(x1,s1,x2,s2)
        Boxes.append(tempbox)
        sBoxes.append(tempsbox)
        pBoxes.append(temppbox)

    # Pretty up pull plot
    Pull2.GetXaxis().SetTitle("Average Mass [GeV]")
    Pull2.SetStats(0)
    Pull2.SetLineColor(1)
    Pull2.SetFillColor(0)
    Pull2.SetMarkerColor(1)
    Pull2.SetMarkerStyle(20)
    Pull2.GetYaxis().SetNdivisions(4)
    if isMC: Pull2.GetYaxis().SetTitle("#frac{QCD MC}{Est}")
    else: Pull2.GetYaxis().SetTitle("#frac{Data}{Est}")
    Pull2.GetYaxis().SetLabelSize(55/15*Pull_norm.GetYaxis().GetLabelSize())
    Pull2.GetYaxis().SetTitleSize(4.5*Pull_norm.GetYaxis().GetTitleSize())
    Pull2.GetYaxis().SetTitleOffset(0.25)
    Pull2.GetYaxis().SetRangeUser(0,2.)
    Pull2.GetXaxis().SetLabelSize(.12)
    Pull2.GetXaxis().SetTitleSize(.14)

    Pull_norm.GetXaxis().SetTitle("Average Mass [GeV]")
    Pull_norm.SetStats(0)
    Pull_norm.SetLineColor(1)
    Pull_norm.SetFillColor(0)
    Pull_norm.SetMarkerColor(1)
    Pull_norm.SetMarkerStyle(20)
    Pull_norm.GetYaxis().SetNdivisions(4)
    if isMC: Pull_norm.GetYaxis().SetTitle("#frac{QCD MC - Est}{#sigma_{stat}}")
    else: Pull_norm.GetYaxis().SetTitle("#frac{Data - Est}{#sigma_{Data}}")
    Pull_norm.GetYaxis().SetLabelSize(50/15*Pull_norm.GetYaxis().GetLabelSize())
    Pull_norm.GetYaxis().SetTitleSize(3.8*Pull_norm.GetYaxis().GetTitleSize())
    Pull_norm.GetYaxis().SetTitleOffset(0.25)
    Pull_norm.GetYaxis().SetRangeUser(-5,5.)
    Pull_norm.GetXaxis().SetLabelSize(.12)
    Pull_norm.GetXaxis().SetTitleSize(.14)

    # Pretty up errors
    for i in Boxes:
        i.SetFillColor(12)
        i.SetFillStyle(3244)
    for i in pBoxes:
        i.SetFillColor(9)
        i.SetFillStyle(3144)
    for i in sBoxes:
        i.SetFillColor(12)
        i.SetFillStyle(3002)

    leg = TLegend(.35,.70,.89,.89)
    leg.SetNColumns(2)
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)

    # Make the legend for the estimation plot
    if isMC: leg.AddEntry(V, "QCD MC", "PL")
    else: leg.AddEntry(V, "Data", "PL")
    if isMC: leg.AddEntry( N1, "QCD Est from QCD MC", "F")
    else: leg.AddEntry( N1, "QCD Est from Data", "F")
    n = 0
    if len(Est.hists_MSR_SUB)>2:
        leg.AddEntry( Est.hists_MSR_SUB[2], "t #bar{t} + Jets", "F")
        leg.AddEntry( Est.hists_MSR_SUB[1], "W + Jets", "F")
        leg.AddEntry( Est.hists_MSR_SUB[0], "Single Top", "F")
    if len(Est.hists_MSR_SUB)==1:
        leg.AddEntry( Est.hists_MSR_SUB[0], "t #bar{t} + Jets", "F")
    leg.AddEntry( Boxes[0], "total uncertainty", "F")
    leg.AddEntry( sBoxes[0], "bkg statistical component", "F")
    if len(Est.hists_SIG)>1:
        leg.AddEntry( Est.hists_SIG[0], "RPV Stop UDD323 M-120, 100 pb", "F")
        leg.AddEntry( Est.hists_SIG[1], "RPV Stop UDD323 M-240, 100 pb", "F")
    
    # A line at -2, -1, 0, 1, 2 for pull plot
    minx = 60
    maxx = 350
    T0 = TLine(minx,0.,maxx,0.)
    T0.SetLineColor(kRed)
    T0.SetLineWidth(2)
    T2 = TLine(minx,2.,maxx,2.)
    T2.SetLineColor(kRed)
    T2.SetLineStyle(2)
    T2.SetLineWidth(2)
    Tm2 = TLine(minx,-2.,maxx,-2.)
    Tm2.SetLineColor(kRed)
    Tm2.SetLineStyle(2)
    Tm2.SetLineWidth(2)
    T1 = TLine(minx,1.,maxx,1.)
    T1.SetLineColor(kRed)
    T1.SetLineStyle(3)
    T1.SetLineWidth(2)
    Tm1 = TLine(minx,-1.,maxx,-1.)
    Tm1.SetLineColor(kRed)
    Tm1.SetLineStyle(3)
    Tm1.SetLineWidth(2)
    C4 = TCanvas("C4", "", 800, 800)

    # Draw all plots and save
    plot = TPad("pad1", "The pad 80% of the height",0,0.30,1,1)
    pull = TPad("pad2", "The pad 20% of the height",0,0.20,1.0,0.30)
    pull2 = TPad("pad2", "The pad 20% of the height",0,0.,1.0,0.20)
    plot.Draw()
    plot.SetBottomMargin(0)
    plot.Draw()
    pull.SetTopMargin(0)
    pull.SetBottomMargin(0)
    pull.Draw()
    pull2.SetTopMargin(0)
    pull2.Draw()
    plot.cd()

    NStack.Draw("Hist")

    if log: 
        NStack.GetYaxis().SetRangeUser( 0.001, 5000 )
    else: 
        NStack.GetYaxis().SetRangeUser( 0, 5000 )

    NStack.GetXaxis().SetTitle("")
    NStack.GetYaxis().SetTitle("Events / 5 GeV")
    NStack.GetYaxis().SetTitleSize(NStack.GetYaxis().GetTitleSize()*1.3)
    if not log: FindAndSetMax([NStack, V], False)
    else: FindAndSetMax([NStack, V], True)
    NStack.GetXaxis().SetLabelSize(0)
    NStack.GetYaxis().SetLabelSize(NStack.GetYaxis().GetLabelSize()*3/4)
    NStack.Draw("Hist") # Draw estimate
    V.SetLineWidth(2)
    V.Draw("same E0")

    for i in Est.hists_SIG:
        i.Draw("histsame")
    if log: 
        plot.SetLogy()

    # Draw errors
    for i in Boxes:
        i.Draw("same")
    for i in sBoxes:
        i.Draw("same")

    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.relPosX = 0.13
    CMS_lumi.CMS_lumi(plot, 4, 0)

    leg.Draw()
    plot.RedrawAxis()

    # Draw and save pull plot
    pull2.cd()
    pull2.SetTopMargin(0)
    pull2.SetBottomMargin(0.3)
    pull2.Draw()
    Pull_norm.Draw()
    # Draw errors on pull
    for i in pBoxes:
        i.Draw("same")
    # Draw lines on pull plot
    T0.Draw("same")
    T2.Draw("same")
    Tm2.Draw("same")
    T1.Draw("same")
    Tm1.Draw("same")
    Pull_norm.Draw("same")
    pull.cd()
    Pull2.GetXaxis().SetTitle("")
    Pull2.Draw("E0")
    T1.Draw("same")
    Pull2.Draw("E0same")

    C4.SaveAs(folder+"Est_Plot.png")

    # For pull plotter, saves variations on pull plot
    fitMetric = Pull_norm.Clone("fitMetric_div") # The pull plot divided by the systematic error
    fitMetric.Reset()

    for i in range(1, Pull_norm.GetNbinsX()+1): # Fills divided pull plot
        error = pBoxes[i-1].GetY1() - pBoxes[i-1].GetY2()
        if error == 0: fitMetric.SetBinContent( i, 0 )
        else: fitMetric.SetBinContent( i, Pull_norm.GetBinContent(i)/abs(error) )

    fitMetric2 = Pull.Clone("fitMetric_quad") # The pull plot with errors in quadrature
    
    FILE3 = TFile( folder+"pull.root", "RECREATE" ) # Makes a root file to save pull plots
    FILE3.cd()
    Pull.Write() # Pull plot with quadrature errors
    Pull_norm.Write() # Normal pull plot
    fitMetric.Write() # Pull plot divided by sys err
    fitMetric2.Write() # The pull plot with quad err again, not sure why
    FILE3.Write()
    FILE3.Save()
