#
import os
import math
from array import array
import optparse
import argparse
import ROOT
from ROOT import *
import scipy
import random
from scipy.stats import chisqprob

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
import RUNA.RUNAnalysis.Plotting
from RUNA.RUNAnalysis.Plotting import *
from RUNA.RUNAnalysis.scaleFactors import *

def ThetaFileMaker( chan, chanCuts, bins, minBin, maxBin, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleAlpha, scaleAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBins, HT, fit=False, isMC=True, log=True ):

    gStyle.SetOptStat(0)
    gStyle.SetOptFit(kFALSE) # No fit box

    # Setting basic distributions
    weight = "(36555.21/15*lumiWeight*puWeight)"

    # The T and W scales
    TTNorm = "( (1.06)*(1+.2*"+str(scaleTT)+"))" # The scale that determines the nominal TTBar normalization
    TTNormUp = "( (1.06)*(1+.2*" + str(scaleTT) + "+.2*" + str(scaleTTErr) + ") )" # Upper TTBar normalization
    TTNormDn = "( (1.06)*(1+.2*" + str(scaleTT) + "-.2*" + str(scaleTTErr) + ") )" # Lower TTBar normalization

#    TTAlpha = "exp( (-0.0005*(genPartonPt1+genPartonPt2))*(1-.2*" + str(scaleAlpha) + ") )" # The scale that determines the nominal alpha NOTE: subtracting = adding because -0.0005
#    TTAlphaUp = "exp( (-0.0005*(genPartonPt1+genPartonPt2))*(1-.2*" + str(scaleAlpha) + "-.2*" + str(scaleAlphaErr) + ") )" # Upper alpha NOTE: subtracting = adding because -0.0005
#    TTAlphaDn = "exp( (-0.0005*(genPartonPt1+genPartonPt2))*(1-.2*" + str(scaleAlpha) + "+.2*" + str(scaleAlphaErr) + ") )" # Lower alpha NOTE: subtracting = adding because -0.0005
    TTAlpha = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + ") )" # The scale that determines the nominal alpha NOTE: subtracting = adding because -0.0005
    TTAlphaUp = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "-.2*" + str(scaleAlphaErr) + ") )" # Upper alpha NOTE: subtracting = adding because -0.0005
    TTAlphaDn = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "+.2*" + str(scaleAlphaErr) + ") )" # Lower alpha NOTE: subtracting = adding because -0.0005

#    TTScaleStrNorm = "(1.06*exp( (-0.0005*(genPartonPt1+genPartonPt2)) ))"
    TTScaleStrNorm = "(1.06*exp( (-0.0005*(HT/2)) ))"
    TTScaleStr = "(" + TTNorm + "*" + TTAlpha + ")" # Total string to scale TT by, norm*alpha
    TTScaleErrUpStr = "(" + TTNormUp + "*" + TTAlpha + ")" # String for scaling TT with norm up, normUp*alpha
    TTScaleErrDnStr = "(" + TTNormDn + "*" + TTAlpha + ")" # String for scaling TT with norm dn, normDn*alpha
    AlphaScaleUpStr = "(" + TTNorm + "*" + TTAlphaUp + ")" # Total string to scale TT by with alpha up, norm*alphaUp
    AlphaScaleDnStr = "(" + TTNorm + "*" + TTAlphaDn + ")" # Total string to scale TT by with alpha dn, norm*alphaDn

    print TTScaleStr

    WScaleStr = "(1+.2*"+str(scaleW)+")" # The scale that determines the nominal W normalization
    WScaleUpStr = "(1+.2*"+str(scaleW)+"+.2*"+str(scaleWErr)+")" # Upper W normalization
    WScaleDnStr = "(1+.2*"+str(scaleW)+"-.2*"+str(scaleWErr)+")" # Lower W normalization

    TopScaleStr = "(1+.2*"+str(scaleTop)+")"
    TopScaleUpStr = "(1+.2*"+str(scaleTop)+"+2*"+str(scaleTopErr)+")"
    TopScaleDnStr = "(1+.2*"+str(scaleTop)+"-2*"+str(scaleTopErr)+")"

    # Create the distributions
    DATA = DIST( "DATA", "80XRootFilesUpdated/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut15.root", "BoostedAnalysisPlotsPuppi/RUNATree", "1" )
    QCD = DIST( "QCD", "80XRootFilesUpdated/RUNAnalysis_QCDHTAll_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*"+weight )
    QCD1000to1400 = DIST( "QCD1000to1400", "80XRootFilesUpdated/RUNAnalysis_QCDPt1000to1400_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1000to1400" )))
    QCD1400to1800 = DIST( "QCD1400to1800", "80XRootFilesUpdated/RUNAnalysis_QCDPt1400to1800_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1400to1800" )))
    QCD170to300 = DIST( "QCD170to300", "80XRootFilesUpdated/RUNAnalysis_QCDPt170to300_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_170to300" )))
    QCD1800to2400 = DIST( "QCD1800to2400", "80XRootFilesUpdated/RUNAnalysis_QCDPt1800to2400_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1800to2400" )))
    QCD2400to3200 = DIST( "QCD2400to3200", "80XRootFilesUpdated/RUNAnalysis_QCDPt2400to3200_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_2400to3200" )))
    QCD300to470 = DIST( "QCD300to470", "80XRootFilesUpdated/RUNAnalysis_QCDPt300to470_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_300to470" )))
    QCD3200toInf = DIST( "QCD3200toInf", "80XRootFilesUpdated/RUNAnalysis_QCDPt3200toInf_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_3200toInf" )))
    QCD470to600 = DIST( "QCD470to600", "80XRootFilesUpdated/RUNAnalysis_QCDPt470to600_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_470to600" )))
    QCD600to800 = DIST( "QCD600to800", "80XRootFilesUpdated/RUNAnalysis_QCDPt600to800_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_600to800" )))
    QCD800to1000 = DIST( "QCD800to1000", "80XRootFilesUpdated/RUNAnalysis_QCDPt800to1000_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_800to1000" )))

    TTJetsNorm = DIST( "TTJets", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleStrNorm+")" )
    TTJets = DIST( "TTJets", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleStr+")" )

    WJetsNorm = DIST( "WJets", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+")" )
    WJets = DIST( "WJets", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+WScaleStr+")" )

    TopNorm = DIST( "TopNorm", "80XRootFilesUpdated/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+")" )
    Top = DIST( "Top", "80XRootFilesUpdated/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+TopScaleStr+")" )

    Sig120 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-120_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*689.799/746680*100" )
    Sig280 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-240_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*26.476/153653*100" )

    # Creating Alphabet objects to run estimate on    
    if isMC: # If running over the MC
        Dists = [ QCD170to300, QCD300to470, QCD470to600, QCD600to800, QCD800to1000, QCD1000to1400, QCD1400to1800, QCD1800to2400, QCD2400to3200, QCD3200toInf ] # Use the MC distributions
        DistsSub = []
    else:  # Otherwise
        Dists = [DATA] # Use data 
        DistsSub = [ Top, WJets, TTJets ] # Nominal distributions to subtract
    DistSig = [Sig120, Sig280]

    presel = tau21
    cuts = Xcut[0]+"<"+Xcut[1]+"&"+Ycut[0]+"<"+Ycut[1]
    anticuts = Xcut[0]+">"+Xcut[1]+"&"+Ycut[0]+"<"+Ycut[1]
    cutsB = Xcut[0]+"<"+Xcut[1]+"&"+Ycut[0]+">"+Ycut[1]
    cutsD = Xcut[0]+">"+Xcut[1]+"&"+Ycut[0]+">"+Ycut[1]
    cut = [ float(Xcut[1]), "<" ] # For defining B vs D regions

#    binsMass = [ [50,60], [60,70], [70,80], [80,90], [90,100], [100,110], [110,120], [120,130], [130,140], [140,150], [150,160], [160,170], [170,180], [180,200], [200,220], [220,250], [250,300], [300,350] ]
    binsMass = [ [50,350] ]

    var_array = [ "prunedMassAsym", Xcut[0], 50, 0., 1., Xcut[2], Xcut[3], Xcut[4] ]

    binsMassAsym = []
    bin = 0
    binWidth = 1/50.
    while bin < 1:
        binsMassAsym.append([bin, bin+binWidth])
        bin = bin+binWidth

    FMass = []
    EstMass = []

    binBoundaries = []
    dBin = float(bins)
    i = minBin
    print minBin
    print maxBin
    while i<=maxBin:
        binBoundaries.append(i)
        i=i+dBin

    prelimFit = [0,0,0]
    folder = "outputs/4617/MassBinsTest/"
    for massBin in xrange(len(binsMass)):
        preselBin = presel+"&prunedMassAve>="+str(binsMass[massBin][0])+"&prunedMassAve<"+str(binsMass[massBin][1])
        FMass.append(LinearFit(prelimFit, 0, 1, "MassAsym"+str(massBin), "SEMR"))
        EstMass.append(Alphabet( "BkgEstMass"+str(massBin), Dists, DistsSub, DistSig ))

        EstMass[massBin].SetRegions( var_array, preselBin + "&" + Ycut[0]+">"+Ycut[1], cutsB, cutsD )
        EstMass[massBin].TwoDPlot.SetStats(0)

        C1 = TCanvas( "C1", "", 800, 600 )
        C1.cd()

        EstMass[massBin].TwoDPlot.Draw("COLZ")
        EstMass[massBin].TwoDPlot.SetTitle("Pruned Mass Asymmetry")
        EstMass[massBin].TwoDPlot.GetYaxis().SetTitle("Pruned Mass Asymmetry")
        C1.SaveAs( folder+"/Mass"+chan+"_"+str(massBin)+"_2D.png" )

        EstMass[massBin].GetRates( cut, binsMassAsym, "0", FMass[massBin], binBoundaries )

        C2 = TCanvas( "C2", "", 10, 10, 750, 500 )
        C2.cd()
        CMS_lumi.extraText = "Simulation Preliminary"
        CMS_lumi.relPosX = 0.13

        EstMass[massBin].G.SetTitle("")

        EstMass[massBin].G.Draw("AP")
        EstMass[massBin].G.GetXaxis().SetTitle( var1 )
        EstMass[massBin].G.GetXaxis().SetTitleSize(EstMass[massBin].G.GetXaxis().GetTitleSize()*1.3)
        EstMass[massBin].G.GetYaxis().SetTitle( "R_{p/f}" )
        EstMass[massBin].G.GetYaxis().SetTitleOffset( 1.0 )
        EstMass[massBin].G.GetYaxis().SetTitleSize(EstMass[massBin].G.GetYaxis().GetTitleSize()*1.3)
        EstMass[massBin].G.GetYaxis().SetNdivisions( 28 )

        CMS_lumi.CMS_lumi(C2, 4, 0)
    
        C2.SaveAs(folder+"Est_"+str(massBin)+"_Fit.png")

        EstMass[massBin].MakeEst("prunedMassAve", binBoundaries, presel+"&"+anticuts, presel+"&"+cuts, False )

    FILE = TFile( folder+"prunedMassAveEst.root", "RECREATE" )
    FILE.cd()

    V = TH1F( "data_obs", "", len(binBoundaries)-1, array('d', binBoundaries) )
    for Est in EstMass:
        for i in Est.hists_MSR:
            i.Sumw2()
            i.SetStats(0)
            V.add(i)

    N = TH1F( "EST", "", len(binBoundaries)-1, array('d', binBoundaries) )
    N1 = TH1F( "EST1", "", len(binBoundaries)-1, array('d', binBoundaries) )
    NStack = THStack( "EST", "" )

    for Est in EstMass:
        for i in Est.hists_EST:
            N.Add(i, 1.)
            N1.Add(i, 1.)
            i.SetLineColor(kBlack)

        for i in Est.hists_EST_SUB:
            N.Add( i, -1 )
            N1.Add( i, -1 )

    removeNegativeBins( N )
    removeNegativeBins( N1 )

    for Est in EstMass:
        if len(Est.hists_MSR_SUB) == 3:
            Est.hists_MSR_SUB[0].SetFillColor(6)
            Est.hists_MSR_SUB[1].SetFillColor(8)
            Est.hists_MSR_SUB[2].SetFillColor(2)        
        for i in Est.hists_MSR_SUB:
            N.Add( i, 1. )
            NStack.Add(i)
            i.SetLineColor(kBlack)
    NStack.Add(N1)

    NU = TH1F( "EST_Up", "", len(binBoundaries)-1, array('d', binBoundaries) )
    for Est in EstMass:
        for i in Est.hists_EST_UP:
            NU.Add(i, 1. )
        for i in Est.hists_EST_SUB_UP:
            NU.Add( i, -1. )
        for i in Est.hists_MSR_SUB:
            NU.Add( i, 1. )

    ND = TH1F( "EST_Dn", "", len(binBoundaries)-1, array('d', binBoundaries) )
    for Est in EstMass:
        for i in Est.hists_EST_Dn:
            ND.Add(i, 1. )
        for i in Est.hists_EST_SUB_Dn:
            ND.Add( i, -1. )
        for i in Est.hists_MSR_SUB:
            ND.Add( i, 1. )

    
    for i in xrange(len(EstMass)):
        EstMass[i].G.Write(str(i)+"_G")
    FILE.Write()
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

    V.SetStats(0)
    V.SetLineColor(kBlack)
    V.SetMarkerColor(1)
    V.SetMarkerStyle(20)

    N1.GetYaxis().SetTitle("events")
    N1.GetXaxis().SetTitle( varTitle )

    FindAndSetMax( [ N, NU, ND ], False ) # Set maximum and minimum of all the plots

    Pull_norm = V.Clone( "Pull_norm" ) # Ratio (actual - est)/sigma_actual plot
    Pull_norm.Add( N, -1 ) # Pull now is actual - est, still need to divide

    Pull2 = V.Clone( "Pull2" ) # Ratio (actual - est)/sqrt(sigma_actual^2 + sigma_sys^2) plot
    Pull2.Divide( N ) # Pull now is actual - est, still need to divide

    
    Boxes = [] # Errors on estimation
    sBoxes = [] # Systematic errors on estimation
    pBoxes = [] # Errors on pull
    maxy = 0.

    for i in range(1, N.GetNbinsX()+1): # Loop through all bins in N (nominal estimation)
        P = Pull.GetBinContent(i)
        Ve = V.GetBinError(i)
        Pull_norm.SetBinError(i, 1.) # Sets pull bin error 1
        if A.GetBinContent(i)==0: # If antitag region bin content is 0
            a = 0 # a, some some part of the error on the bkg est? = 0
        else:
            a = A.GetBinError(i)*N.GetBinContent(i)/A.GetBinContent(i) # otherwise, this expression
        u = NU.GetBinContent(i) - N.GetBinContent(i) # u, upper error on estimation
        d = N.GetBinContent(i) - ND.GetBinContent(i) # d, lower error on estimation
        x1 = Pull_norm.GetBinCenter(i) - (0.5*Pull_norm.GetBinWidth(i)) # Start of bin
        y1 = N.GetBinContent(i) - math.sqrt((d*d) + (a*a)) # Bottom of error on estimation
        s1 = N.GetBinContent(i) - a # Bottom of systematic error on estimation?
        if y1 < 0.: # Don't want the lower error to be negative, set to 0
            y1 = 0
        if s1 < 0: # Don't want the lower error to be negative, set to 0
            s1 = 0
        x2 = Pull_norm.GetBinCenter(i) + (0.5*Pull_norm.GetBinWidth(i)) # End of bin
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
    Pull2.GetYaxis().SetTitle("#frac{Data}{Est}")
    Pull2.GetYaxis().SetLabelSize(55/15*Pull_norm.GetYaxis().GetLabelSize())
    Pull2.GetYaxis().SetTitleSize(4.5*Pull_norm.GetYaxis().GetTitleSize())
    Pull2.GetYaxis().SetTitleOffset(0.25)
    Pull2.GetYaxis().SetRangeUser(0,2.)
    Pull2.GetXaxis().SetLabelSize(.12)
    Pull2.GetXaxis().SetTitleSize(.14)

    Pull_norm.GetXaxis().SetTitle("Average Soft Drop Mass [GeV]")
    Pull_norm.SetStats(0)
    Pull_norm.SetLineColor(1)
    Pull_norm.SetFillColor(0)
    Pull_norm.SetMarkerColor(1)
    Pull_norm.SetMarkerStyle(20)
    Pull_norm.GetYaxis().SetNdivisions(4)
    Pull_norm.GetYaxis().SetTitle("#frac{Data - Est}{#sigma_{Data}}")
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
    plot = TPad("pad1", "The pad 80% of the height",0,0.20,1,1)
    pull = TPad("pad2", "The pad 20% of the height",0,0.,1.0,0.20)

    plot.Draw()
    plot.SetBottomMargin(0)
    plot.Draw()

    pull.Draw()
    plot.cd()

    NStack.Draw("Hist")
    # Should fix setrangeusers... setmaximums...

    if log: 
        print "here2"
        NStack.GetYaxis().SetRangeUser( 0.001, 5000 )
    else: 
        NStack.GetYaxis().SetRangeUser( 0, 5000 )
        print "here"
    NStack.GetXaxis().SetTitle("")
    NStack.GetYaxis().SetTitle("Events / 10 GeV")
    NStack.GetYaxis().SetTitleSize(NStack.GetYaxis().GetTitleSize()*1.3)
    if log: NStack.SetMaximum( NStack.GetMaximum()*10 )
    else: NStack.SetMaximum( NStack.GetMaximum()*2 )
    NStack.GetXaxis().SetLabelSize(0)
    NStack.GetYaxis().SetLabelSize(NStack.GetYaxis().GetLabelSize()*3/4)
    NStack.Draw("Hist") # Draw estimate
    V.SetLineWidth(2)
    V.Draw("same E0") # Draw actual signal region

    for i in Est.hists_SIG:
        i.Draw("histsame")
    if log: plot.SetLogy()

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
    pull.cd()
    pull.SetTopMargin(0)
    pull.SetBottomMargin(0.3)
    pull.Draw()
    if log: 
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
        
    else: 
        Pull2.Draw()
        T1.Draw("same")    

    C4.SaveAs(folder+"Est_Plot.png")

scaleTT = 0
scaleTTErr = 1
scaleW = 0
scaleWErr = 1
scaleTTAlpha = 0
scaleTTAlphaErr = 1
scaleTop = 0
scaleTopErr = 0

Xcut = [ "prunedMassAsym", "0.1", 50, 0., 1. ]
Ycut = [ "deltaEtaDijet", "1.5", 50, 0., 5. ]

ThetaFileMaker( "pres", "(abs(jet1Pt)>-999)", 10, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, "jet1Tau21<0.60&jet2Tau21<0.60", [0,0,0], 25, "jet1Tau21>-1.", False, False, False )
