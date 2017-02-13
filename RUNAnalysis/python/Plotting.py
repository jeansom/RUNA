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
def MakeFitPlots( Est, F, bins, var1, var2, var_array, presel, antitag, tagB, tagD, cut, center, Est2, F2, folder, blinded=True ):

    gStyle.SetOptStat(0) # No stat box
    gStyle.SetOptFit(kFALSE) # No fit box

    Est.SetRegions( var_array, presel+"&"+antitag, tagB, tagD ) # Makes the 2D plot
    Est.TwoDPlot.SetStats(0) # Gets rid of stat box

    EstProf = Est.TwoDPlot.ProfileX("EstProfX") # Makes the X Profile of the 2D plot, not necessary

    C1 = TCanvas( "C1", "", 800, 600 )
    C1.cd()

    # Make the 2D plot prettier, save    
    Est.TwoDPlot.Draw( "COLZ" )
    Est.TwoDPlot.GetXaxis().SetTitle( var1 )
    Est.TwoDPlot.GetYaxis().SetTitle( var2 )
    C1.SaveAs( folder+var1+"_2D.png" )

    # Find the ratio B/D in the bins and fit to F
    Est.GetRates( cut, bins, center, F )
    
    if blinded: # If staying blinded:
        print "Staying blinded"
        Est2.SetRegions( var_array, presel+"&"+antitag, tagB, tagD ) # Makes the 2D plot for the MC instead of data
        Est2.GetRates( cut, bins, center, F2 ) # Finds the ratio B/D and fits to F2

    # Making TLatex for legend
    chi2Test = TLatex( 0.2, 0.85, '#chi^{2}/ndF = '+ str( round( Est.Fit.fit.GetChisquare(), 2 ) )+'/'+str( int( Est.Fit.fit.GetNDF() ) ) ) # chi2/ndf
    p0 = TLatex( 0.2, 0.80, 'p0 = '+ '{:0.2e}'.format(Est.Fit.fit.GetParameter( 0 )) +' #pm '+ '{:0.2e}'.format(Est.Fit.fit.GetParError( 0 ))) # p0
    p1 = TLatex( 0.2, 0.75, 'p1 = '+ '{:0.2e}'.format(Est.Fit.fit.GetParameter( 1 )) +' #pm '+ '{:0.2e}'.format(Est.Fit.fit.GetParError( 1 ))) # p1
    p2 = TLatex( 0.2, 0.70, 'p2 = '+ '{:0.2e}'.format(Est.Fit.fit.GetParameter( 2 )) +' #pm '+ '{:0.2e}'.format(Est.Fit.fit.GetParError( 2 )) ) # p2

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
    C2.SetGrid( 4 )

    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.relPosX = 0.13

    Est.G.SetTitle("")
    
    # Setting range of G, SHOULD CHANGE!!!
    if "BCD" in folder:
        Est.G.GetYaxis().SetRangeUser(0,5.0)
    else:
        Est.G.GetYaxis().SetRangeUser(0,0.87)

    # Draw Pass/Fail, set titles...
    Est.G.Draw("AP")
    Est.G.GetXaxis().SetTitle( "Average Pruned Mass [GeV]" )
    Est.G.GetYaxis().SetTitle( "R_{p/f}" )
    Est.G.GetYaxis().SetTitleOffset( 1.3 )
    Est.G.GetYaxis().SetNdivisions( 28 )

    # Draw fit, err up, err down
    Est.Fit.fit.Draw("same")
    if Est.G.GetN() > 0:
        Est.Fit.ErrUp.SetLineStyle(2)
        Est.Fit.ErrUp.Draw("same")
        Est.Fit.ErrDn.SetLineStyle(2)
        Est.Fit.ErrDn.Draw("same")

    # Draw TLatex legend
    chi2Test.Draw('same')
    p0.Draw('same')
    p1.Draw('same')
    p2.Draw('same')

    CMS_lumi.CMS_lumi(C2, 4, 0)
    
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
#### folder: folder to save everyting in
#### isMC: running over MC or data
#### blinded: If running on data, should keep signal region blinded; If true, will plot the estimate on top of the MC signal region 
#### Pull: Pretty sure you can ignore, just something I was trying
def MakeEstPlots( Est, variable, varTitle, binBoundaries, antitag, tag, var1, Est2, folder, isMC=True, blinded=True, Pull=TH1D()  ):

    Est.MakeEst( variable, binBoundaries, antitag, tag ) # Makes actual estimate

    FILE = TFile( folder+var1+"Est.root", "RECREATE" ) # Creates a root file to store plots in
    FILE.cd()
    
    V = TH1F( "data_obs", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Histogram for actual signal region plot
    VStack = THStack( "data_obs", "" ) # Stacked histogram for signal region plot, unnecessary

    # If the data is blinded, look at the MC signal region instead of the data
    if blinded:
        print "Staying blinded"
        Est2.MakeEst( variable, binBoundaries, antitag, tag ) # Makes actual estimation for MC
        for i in Est2.hists_MSR: # Loops through signal region plots
            i.Sumw2()
            i.SetStats(0)
            for bin in range(0,i.GetNbinsX()): # Fills V (signal region plot)
                VCon = V.GetBinContent(bin) # N Events in V
                VCon = VCon + i.GetBinContent(bin) # Adds N Events in i (one of the signal region plots) to N Events in V
                V.SetBinContent(bin, VCon) # Sets V bin content as this increased value
                #V.Add(i) # This function does the above four lines in one
            VStack.Add(i) # Adds i to the stack plot, unnecessary
    # Otherwise:
    else:
        for i in Est.hists_MSR: # Loops through signal region plots
            i.Sumw2()
            i.SetStats(0)
            V.Add(i) # This function does the above four lines in one
            VStack.Add(i) # Adds i to the stack plot, unnecessary

    # The estimate is the sum of the histograms in self.hists_EST and self.hists_MSR_SUB minus the histograms in self.hists_EST_SUB
    N = TH1F( "EST", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Nominal estimate histogram
    N1 = TH1F( "EST1", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Nominal estimate histogram WITHOUT the subtracted histograms added back in!!!
    NStack = THStack( "EST", "" ) # Nominal estimate stack histogram

    for i in Est.hists_EST: # Loops through all plots to add to the estimation
        N.Add( i, 1. ) # Adds plot to N (nominal estimate)
        N1.Add( i, 1. ) # Adds plot to N1 (nominal estimate WITHOUT subtracted added back in)
        i.SetLineColor(kBlack)

    for i in Est.hists_EST_SUB: # Loops through all plots to subtract from the estimation
        N.Add( i, -1. ) # Subtracts plot from N (nominal estimate)
        N1.Add( i, -1. ) # Subtracts plot from N1 (nominal estimate WITHOUT subtracted added back in)

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

    for i in Est.hists_MSR_SUB: # Loops through the signal region plots of all subtracted distributions
        N.Add( i, 1. ) # Adds plot to N (nominal estimate)
        NStack.Add(i) # Adds plots individually to NStack (nominal estimate stack plot)
        i.SetLineColor(kBlack)

    NStack.Add(N1) # Adds the background estimate WITHOUT subtracted added back in to NStack, which already has the subtracted plots signal regions
    
    # We can do the same thing for the Up and Down shapes:
    NU = TH1F( "EST_Up", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Up estimate histogram
    for i in Est.hists_EST_UP: # Adds background estimations for distributions to be added together
        NU.Add( i, 1. )
    for i in Est.hists_EST_SUB_UP: # Subtracts background estimations for distributions to be subtracted from the final estimate
        NU.Add( i, -1. )
    for i in Est.hists_MSR_SUB: # Adds the signal regions for the distributions to be subtracted in
        NU.Add( i, 1. )

    ND = TH1F( "EST_Down", "", len(binBoundaries)-1, array('d',binBoundaries) ) # Down estimate histogram
    for i in Est.hists_EST_DN: # Adds background estimations for distributions to be added together
        ND.Add( i, 1. )
    for i in Est.hists_EST_SUB_DN: # Subtracts background estimations for distributions to be subtracted from the final estimate
        ND.Add( i, -1. )
    for i in Est.hists_MSR_SUB: # Adds the signal regions for the distributions to be subtracted in
        ND.Add( i, 1. )
    
    # Anti-tag region (C) Plot
    A = TH1F( "EST_Antitag", "", len(binBoundaries)-1, array('d',binBoundaries)) # anti-tag region (C) histogram
    for i in Est.hists_ATAG: # Adds all the C Plots together
        A.Add( i, 1. )

    FILE.Write() # Writes all the previously created plots to the root file
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
    Pull = V.Clone( "Pull_quad" ) # Ratio (actual - est)/sqrt(sigma_actual^2 + sigma_sys^2) plot
    Pull.Add( N, -1 ) # Pull now is actual - est, still need to divide

    Pull_norm = V.Clone( "Pull_norm" ) # Ratio (actual - est)/sigma_actual plot
    Pull_norm.Add( N, -1 ) # Pull now is actual - est, still need to divide
    
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
    Pull.GetXaxis().SetTitle("")
    Pull.SetStats(0)
    Pull.SetLineColor(1)
    Pull.SetFillColor(0)
    Pull.SetMarkerColor(1)
    Pull.SetMarkerStyle(20)
    Pull.GetXaxis().SetNdivisions(0)
    Pull.GetYaxis().SetNdivisions(4)
    Pull.GetYaxis().SetTitle("#frac{MC - Data Est}{#sigma_{MC}}")
#    Pull.GetYaxis().SetTitle("#frac{MC}{Data Est}")
    Pull.GetYaxis().SetLabelSize(75/15*Pull.GetYaxis().GetLabelSize())
    Pull.GetYaxis().SetTitleSize(3.8*Pull.GetYaxis().GetTitleSize())
    Pull.GetYaxis().SetTitleOffset(0.175)
    Pull.GetYaxis().SetRangeUser(0.,2.)

    Pull_norm.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
    Pull_norm.SetStats(0)
    Pull_norm.SetLineColor(1)
    Pull_norm.SetFillColor(0)
    Pull_norm.SetMarkerColor(1)
    Pull_norm.SetMarkerStyle(20)
    Pull_norm.GetYaxis().SetNdivisions(4)
    Pull_norm.GetYaxis().SetTitle("#frac{MC - Data Est}{#sigma_{MC}}")
    Pull_norm.GetYaxis().SetLabelSize(50/15*Pull_norm.GetYaxis().GetLabelSize())
    Pull_norm.GetYaxis().SetTitleSize(3.8*Pull_norm.GetYaxis().GetTitleSize())
    Pull_norm.GetYaxis().SetTitleOffset(0.2)
    Pull_norm.GetYaxis().SetRangeUser(-50.,50.)
    Pull_norm.GetXaxis().SetLabelSize(.12)
    Pull_norm.GetXaxis().SetTitleSize(.12)

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

    # Make the legend for the estimation plot
    leg2 = TLegend(0.15,0.80,0.95,0.89)
    leg2.SetNColumns(2)
    leg2.SetTextSize(0.03)
    leg2.SetLineColor(0)
    leg2.SetFillColor(0)
    leg2.SetFillStyle(0)
    leg2.AddEntry(V, "Data", "PL")
    leg2.AddEntry( N1, "QCD Est from Data", "F")
    leg2.AddEntry( Est.hists_MSR_SUB[0], "W + Jets", "F")
    leg2.AddEntry( Est.hists_MSR_SUB[1], "t #bar{t} + Jets", "F")
    leg2.AddEntry(Boxes[0], "total uncertainty", "F")
    leg2.AddEntry(sBoxes[0], "bkg statistical component", "F")

    # A line at -2, -1, 0, 1, 2 for pull plot
    T0 = TLine(60,0.,350,0.)
    T0.SetLineColor(kRed)
    T0.SetLineWidth(2)
    T2 = TLine(60,2.,350,2.)
    T2.SetLineColor(kRed)
    T2.SetLineStyle(2)
    T2.SetLineWidth(2)
    Tm2 = TLine(60,-2.,350,-2.)
    Tm2.SetLineColor(kRed)
    Tm2.SetLineStyle(2)
    Tm2.SetLineWidth(2)
    T1 = TLine(60,1.,350,1.)
    T1.SetLineColor(kRed)
    T1.SetLineStyle(3)
    T1.SetLineWidth(2)
    Tm1 = TLine(60,-1.,350,-1.)
    Tm1.SetLineColor(kRed)
    Tm1.SetLineStyle(3)
    Tm1.SetLineWidth(2)
    C4 = TCanvas("C4", "", 800, 800)

    # Draw all plots and save
    plot = TPad("pad1", "The pad 80% of the height",0,0.10,1,1)
    pull = TPad("pad2", "The pad 20% of the height",0,0,1.0,0.20)
    plot.Draw()
    pull.Draw()
    plot.cd()

    NStack.Draw("Hist")
    # Should fix setrangeusers... setmaximums...
    NStack.GetYaxis().SetRangeUser( .5, 5000 )
    NStack.GetXaxis().SetTitle("")
    NStack.GetYaxis().SetTitle("Events / 10 GeV")
    NStack.SetMaximum( NStack.GetMaximum()*10 )
    NStack.GetXaxis().SetLabelSize(0)
    NStack.GetYaxis().SetLabelSize(NStack.GetYaxis().GetLabelSize()*3/4)
    NStack.SetMinimum( .5 )
    NStack.Draw("Hist") # Draw estimate
    V.SetLineWidth(2)
    V.GetYaxis().SetRangeUser( .5, 5000 )
    V.Draw("same E0") # Draw actual signal region
    plot.SetLogy()

    # Draw errors
    for i in Boxes:
        i.Draw("same")
    for i in sBoxes:
        i.Draw("same")

    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.relPosX = 0.13
    CMS_lumi.CMS_lumi(plot, 4, 0)

    leg2.Draw()
    plot.RedrawAxis()

    # Draw and save pull plot
    pull.cd()
    pull.SetTopMargin(0)
    pull.SetBottomMargin(0.3)
    pull.Draw()
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

    C4.SaveAs(folder+var1+"Est_Plot.png")

    print str(N.Integral())
    print str(V.Integral())

    print(Pull)


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
