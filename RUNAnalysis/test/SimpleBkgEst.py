#!/usr/bin/env python

import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

from RUNA.RUNAnalysis.Plotting_Header import *
from RUNA.RUNAnalysis.Distribution_Header import *
from RUNA.RUNAnalysis.scaleFactors import *
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 

gROOT.SetBatch()
gStyle.SetOptStat(0)

#### Runs the background estimate, either bin by bin or given a transfer function. For debugging purposes
# tau21: preselection
# NAME: name for saving
def SimpleBkgEst(tau21,NAME):

    # Cuts defining A, B, C, D regions
    ACuts = "("+tau21+"&deltaEtaDijet<1.5&prunedMassAsym<0.1)" 
    BCuts = "("+tau21+"&deltaEtaDijet>1.5&prunedMassAsym<0.1)" 
    CCuts = "("+tau21+"&deltaEtaDijet<1.5&prunedMassAsym>0.1)"
    DCuts = "("+tau21+"&deltaEtaDijet>1.5&prunedMassAsym>0.1)"

    # Data (or QCD), TTJets, and WJets A, B, C, D histos
    DATA_A = TH1D( "DATA_A", "", 58, 60, 350 )
    DATA_B = TH1D( "DATA_B", "", 58, 50, 350 )
    DATA_C = TH1D( "DATA_C", "", 58, 60, 350 )
    DATA_D = TH1D( "DATA_D", "", 58, 50, 350 )

    TTJETS_A = TH1D( "TTJETS_A", "", 58, 60, 350 )
    TTJETS_B = TH1D( "TTJETS_B", "", 58, 50, 350 )
    TTJETS_C = TH1D( "TTJETS_C", "", 58, 60, 350 )
    TTJETS_D = TH1D( "TTJETS_D", "", 58, 50, 350 )

    WJETS_A = TH1D( "WJETS_A", "", 58, 60, 350 )
    WJETS_B = TH1D( "WJETS_B", "", 58, 50, 350 )
    WJETS_C = TH1D( "WJETS_C", "", 58, 60, 350 )
    WJETS_D = TH1D( "WJETS_D", "", 58, 50, 350 )


    # Fills QCD A, B, C, D
    quickplot("v08/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", DATA_A, "prunedMassAve", ACuts, "puWeight*36555.21/15*lumiWeight*.62" )
    quickplot("v08/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", DATA_B, "prunedMassAve", BCuts, "puWeight*36555.21/15*lumiWeight*.62" )
    quickplot("v08/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", DATA_C, "prunedMassAve", CCuts, "puWeight*36555.21/15*lumiWeight*.62" )
    quickplot("v08/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", DATA_D, "prunedMassAve", DCuts, "puWeight*36555.21/15*lumiWeight*.62" )

    # Fills TTJets A, B, C, D
    quickplot("v08/RUNAnalysis_TT_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", TTJETS_A, "prunedMassAve", ACuts, "puWeight*36555.21/15*1.06*exp(-0.0005*HT/2)*lumiWeight")
    quickplot("v08/RUNAnalysis_TT_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", TTJETS_B, "prunedMassAve", BCuts, "puWeight*36555.21/15*1.06*exp(-0.0005*HT/2)*lumiWeight" )     
    quickplot("v08/RUNAnalysis_TT_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", TTJETS_C, "prunedMassAve", CCuts, "puWeight*36555.21/15*1.06*exp(-0.0005*HT/2)*lumiWeight" )     
    quickplot("v08/RUNAnalysis_TT_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", TTJETS_D, "prunedMassAve", DCuts, "puWeight*36555.21/15*1.06*exp(-0.0005*HT/2)*lumiWeight" )

    # Fills WJets A, B, C, D
    quickplot("v08/RUNAnalysis_WJetsToQQ_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", WJETS_A, "prunedMassAve", ACuts, "puWeight*36555.21/15*lumiWeight" )     
    quickplot("v08/RUNAnalysis_WJetsToQQ_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", WJETS_B, "prunedMassAve", BCuts, "puWeight*36555.21/15*lumiWeight" )     
    quickplot("v08/RUNAnalysis_WJetsToQQ_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", WJETS_C, "prunedMassAve", CCuts, "puWeight*36555.21/15*lumiWeight" )     
    quickplot("v08/RUNAnalysis_WJetsToQQ_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", WJETS_D, "prunedMassAve", DCuts, "puWeight*36555.21/15*lumiWeight" )

    # If actually using data, uncomment to subtract TTJets and WJets
#    DATA_B.Add(TTJETS_B, -1)
#    DATA_C.Add(TTJETS_C, -1)
#    DATA_D.Add(TTJETS_D, -1)

#    DATA_B.Add(WJETS_B, -1)
#    DATA_C.Add(WJETS_C, -1)
#    DATA_D.Add(WJETS_D, -1)

    # Find TF and save 
    DATA_B.Divide(DATA_D)
    DATA_B.GetYaxis().SetRangeUser(0,1.9)
    C1 = TCanvas("C","",800,600)
    DATA_B.Draw("E0")
    C1.SaveAs("TCutPlots/fit.png")

    # If you already have the fit, define it here
    TF = TF1("FIT", "(1/([0]+exp([1]+[2]*x*x*x)))", 60, 350)
    TF.SetParameters(1.88232e+00, 7.20927e-01, -5.68495e-07)

    # Run the estimate
    for bin in xrange(DATA_C.GetNbinsX()):
        cen = DATA_C.GetXaxis().GetBinCenter(bin) 
#        TF = DATA_B.GetBinContent(DATA_B.FindBin(cen)) #For bin-by-bin estimate
        TF = FIT.Eval(cen) #For fitted TF estimate
        DATA_C.SetBinContent(bin, DATA_C.GetBinContent(bin)*TF)

    # Add resonant backgrounds back in
    DATA_C.Add(TTJETS_A)
    DATA_C.Add(WJETS_A)

    DATA_C.SetFillColor(kBlue)
    DATA_C.SetLineColor(1)
    DATA_C.SetLineWidth(1)

    DATA_A.SetLineColor(kBlack)
    DATA_A.SetMarkerColor(1)
    DATA_A.SetMarkerStyle(20)

    C = TCanvas("C", "", 800,800)

    plot = TPad("pad1", "The pad 80% of the height",0,0.20,1,1)
    pull = TPad("pad2", "The pad 20% of the height",0,0,1.0,0.20)
    plot.SetBottomMargin(0)
    pull.SetTopMargin(0)
    plot.Draw()
    pull.Draw()
    plot.cd()

    FindAndSetMax([DATA_A,DATA_C],False)
    DATA_C.GetXaxis().SetTitle("")
    DATA_C.GetYaxis().SetTitle("Events")
    DATA_C.GetXaxis().SetLabelSize(0)
    DATA_C.Draw("hist")
    DATA_A.Draw("sameE0hist")

    pull.cd()
    # Make ratio plot, save est and ratio plot
    Pull = DATA_A.Clone()
    Pull.Divide(DATA_C)

    Pull.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
    Pull.SetLineColor(1)
    Pull.SetFillColor(0)
    Pull.SetMarkerColor(1)
    Pull.SetMarkerStyle(20)
    Pull.GetYaxis().SetNdivisions(4)
    Pull.GetYaxis().SetTitle("#frac{MC}{Est}")
    Pull.GetYaxis().SetLabelSize(50/15*Pull.GetYaxis().GetLabelSize())
    Pull.GetYaxis().SetTitleSize(3.8*Pull.GetYaxis().GetTitleSize())
    Pull.GetYaxis().SetTitleOffset(0.2)
    Pull.GetYaxis().SetRangeUser(0, 2)
    Pull.GetXaxis().SetLabelSize(.12)
    Pull.GetXaxis().SetTitleSize(.12)
    
    T = []
    for i in [ .5, 1.5, 1. ]:
        T.append(TLine(60, i, 350, i))
        T[-1].SetLineColor(kRed)
        T[-1].SetLineWidth(2)

    Pull.Draw("E0")
    for TX in T:
        TX.Draw("same")

    C.SaveAs("TCutPlots/SimpleBkg_"+NAME+".png")
    
zerobtag = "(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484)"
onebtag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484)||(jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
twobtag = "(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)"

zeroTop = "(jet1Tau32>0.67&jet2Tau32>.67)"
oneTop = "((jet1Tau32<=0.67&jet2Tau32>=0.67)||(jet1Tau32>0.67&jet2Tau32<0.67))"
twoTop = "(jet1Tau32<0.67&jet2Tau32<0.67)"

tau21 = "jet1Tau21<0.45&jet2Tau21<0.45&"+zerobtag+"&"+zeroTop
SimpleBkgEst(tau21, "pres")
