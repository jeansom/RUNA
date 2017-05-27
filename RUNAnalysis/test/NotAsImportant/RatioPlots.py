#!/usr/bin/env python

import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

from RUNA.RUNAnalysis.Plotting_Header import *
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
from RUNA.RUNAnalysis.Distribution_Header import *
gROOT.SetBatch()

def RatioPlots():
    weight = "(36555.21/15*lumiWeight*puWeight)"
    TTScale = "1.06*exp(-0.0005*HT/2)"
    WScale1 = "1"
    WScale0 = "0"
    WScale2 = "2"

    zerobtag = "(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484)"
    onebtag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484)||(jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
    twobtag = "(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)"
    zeroTop = "(jet1Tau32>0.67&jet2Tau32>.67)"
    oneTop = "((jet1Tau32<=0.67&jet2Tau32>=0.67)||(jet1Tau32>0.67&jet2Tau32<0.67))"
    twoTop = "(jet1Tau32<0.67&jet2Tau32<0.67)"


    PRES = "jet1Tau21<0.45&jet2Tau21<0.45"
    REG = zerobtag+"&"+zeroTop

    A = "deltaEtaDijet<1.0&prunedMassAsym<0.1"
    B = "deltaEtaDijet>1.0&prunedMassAsym<0.1"
    C = "deltaEtaDijet<1.0&prunedMassAsym>0.1"
    D = "deltaEtaDijet>1.0&prunedMassAsym>0.1" 
    NBins = int((-3+5)/0.0625)
    DATA_B = TH1D( "DATA_B", "", NBins, -5, -3 )
    DATA_D = TH1D( "DATA_D", "", NBins, -5, -3 )
    TTJETS_B = TH1D( "TTJETS_B", "", NBins, -5, -3 )
    TTJETS_D = TH1D( "TTJETS_D", "", NBins, -5, -3 )
    WJETS0_B = TH1D( "WJETS0_B", "", NBins, -5, -3 )
    WJETS0_D = TH1D( "WJETS0_D", "", NBins, -5, -3 )
    WJETS1_B = TH1D( "WJETS1_B", "", NBins, -5, -3 )
    WJETS1_D = TH1D( "WJETS1_D", "", NBins, -5, -3 )
    WJETS2_B = TH1D( "WJETS2_B", "", NBins, -5, -3 )
    WJETS2_D = TH1D( "WJETS3_D", "", NBins, -5, -3 )

    DATA = DIST( "DATA", "80XRootFilesUpdated/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut15.root", "BoostedAnalysisPlots/RUNATree", "1" )
    TTJETS = DIST( "TTJets", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+TTScale+")" )
    WJETS0 = DIST( "WJets0", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*"+WScale0+")" )
    WJETS1 = DIST( "WJets1", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*"+WScale1+")" )
    WJETS2 = DIST( "WJets2", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*"+WScale2+")" )
                   
    rho = "(log((jet1PrunedMass*jet1PrunedMass)/(jet1Pt*jet1Pt))+log((jet2PrunedMass*jet2PrunedMass)/(jet2Pt*jet2Pt)))"

    quickplot( DATA.File, DATA.Tree, DATA_B, rho, PRES+"&"+REG+"&"+B, DATA.weight )
    quickplot( DATA.File, DATA.Tree, DATA_D, rho, PRES+"&"+REG+"&"+D, DATA.weight )
    quickplot( TTJETS.File, TTJETS.Tree, TTJETS_B, rho, PRES+"&"+REG+"&"+B, TTJETS.weight )
    quickplot( TTJETS.File, TTJETS.Tree, TTJETS_D, rho, PRES+"&"+REG+"&"+D, TTJETS.weight )
    quickplot( WJETS0.File, WJETS0.Tree, WJETS0_B, rho, PRES+"&"+REG+"&"+B, WJETS0.weight )
    quickplot( WJETS0.File, WJETS0.Tree, WJETS0_D, rho, PRES+"&"+REG+"&"+D, WJETS0.weight )
    quickplot( WJETS1.File, WJETS1.Tree, WJETS1_B, rho, PRES+"&"+REG+"&"+B, WJETS1.weight )
    quickplot( WJETS1.File, WJETS1.Tree, WJETS1_D, rho, PRES+"&"+REG+"&"+D, WJETS1.weight )
    quickplot( WJETS2.File, WJETS2.Tree, WJETS2_B, rho, PRES+"&"+REG+"&"+B, WJETS2.weight )
    quickplot( WJETS2.File, WJETS2.Tree, WJETS2_D, rho, PRES+"&"+REG+"&"+D, WJETS2.weight )

    BPlots = []
    DPlots = []

    B0 = DATA_B.Clone("B0")
    B0.Add(TTJETS_B, -1)
    D0 = DATA_D.Clone("D0")
    D0.Add(TTJETS_D, -1)

    B1 = B0.Clone("B1")
    B2 = B0.Clone("B2")
    D1 = D0.Clone("D1")
    D2 = D0.Clone("D2")

    B0.Add(WJETS0_B, -1)
    B1.Add(WJETS1_B, -1)
    B2.Add(WJETS2_B, -1)
    D0.Add(WJETS0_D, -1)
    D1.Add(WJETS1_D, -1)
    D2.Add(WJETS2_D, -1)

    BPlots.append(B0)
    BPlots.append(B1)
    BPlots.append(B2)
    DPlots.append(D0)
    DPlots.append(D1)
    DPlots.append(D2)

    binsMass = []
    for i in xrange( 0, 8 ):
        binsMass.append( [ -5+0.0625*i, -5+0.0625*(i+1) ] )
    for i in xrange( 0, 4 ):
        binsMass.append( [ (-4.5)+0.125*i, (-4.5)+0.125*(i+1) ] )
    for i in xrange( 0, 4 ):
        binsMass.append( [ -4+0.125*i, -4+0.125*(i+1) ] )
    for i in xrange( 0, 2 ):
        binsMass.append( [ -3.5+0.25*i, -3.5+0.25*(i+1) ] )       

    Graphs = []
    print binsMass
    for j in xrange(len(BPlots)):

        x = []
        y = []
        exl = []
        eyl = []
        exh = []
        eyh = []

        for b in binsMass:
            passed = 0
            failed = 0

            for i in xrange( 1, BPlots[j].GetNbinsX()+1 ):
                if BPlots[j].GetXaxis().GetBinCenter(i) < b[1] and BPlots[j].GetXaxis().GetBinCenter(i) > b[0]:
                    passed = passed + BPlots[j].GetBinContent(i)
                    failed = failed + DPlots[j].GetBinContent(i)
                
            ep = math.sqrt(passed)
            ef = math.sqrt(failed)
            
            if passed == 0 or failed == 0:
                continue
            
            err = (passed/(failed))*(ep/passed+ef/failed) # Error on ratio

            x.append( (float( (b[0]+b[1])/2. ) ) ) # X value = bin center - center
            exl.append( float( (b[1]-b[0])/2. ) ) # X low error = bin width
            exh.append( float( (b[1]-b[0])/2. ) ) # X high error = bin width
            print str(b[0])+" "+str(b[1])
            print float((b[1]-b[0])/2.)
            
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
        
        Graphs.append(G)


    C = TCanvas("C","",800,800)
    Graphs[0].SetLineColor(kRed)
    Graphs[1].SetLineColor(kBlack)
    Graphs[2].SetLineColor(kBlue)

    Graphs[0].SetTitle("")
    Graphs[0].GetXaxis().SetTitle("#rho")
    Graphs[0].GetXaxis().SetTitleSize(Graphs[0].GetXaxis().GetTitleSize()*1.3)
    Graphs[0].GetYaxis().SetTitle( "R_{p/f}" )
    Graphs[0].GetYaxis().SetTitleOffset( 1.2 )
    Graphs[0].GetYaxis().SetTitleSize(Graphs[0].GetYaxis().GetTitleSize()*1.1)
    Graphs[0].GetYaxis().SetNdivisions( 28 )

    leg = TLegend(.15,.75,.50,.89)
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.AddEntry( Graphs[0], "WJets Scale = 0", "L" )
    leg.AddEntry( Graphs[1], "WJets Scale = 1", "L" )
    leg.AddEntry( Graphs[2], "WJets Scale = 2", "L" )

    Graphs[0].Draw("AP")
    Graphs[1].Draw("same P")
    Graphs[2].Draw("same P")

    leg.Draw("same")
    
    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.relPosX = 0.14
    CMS_lumi.CMS_lumi(C, 4, 0)
    C.RedrawAxis()
    C.SaveAs("TCutPlots/WScaleRatio.png")


RatioPlots()
