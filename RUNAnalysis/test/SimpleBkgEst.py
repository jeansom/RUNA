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

gROOT.SetBatch()

def SimpleBkgEst():
    TTScale = "1"
    TransFun = "1/(1.829+exp(0.3742-3.046e-07*prunedMassAve*prunedMassAve*prunedMassAve))"

    ACuts = "(jet1Tau21<0.45&jet2Tau21<0.45&deltaEtaDijet<1.5&prunedMassAsym<0.1)"
    CCuts = "(jet1Tau21<0.45&jet2Tau21<0.45&deltaEtaDijet<1.5&prunedMassAsym>0.1)"

    DATA_A = TH1D( "DATA_A", "", 58, 60, 350 )
    DATA_C = TH1D( "DATA_C", "", 58, 60, 350 )
    TTJETS_A = TH1D( "TTJETS_A", "", 58, 60, 350 )
    TTJETS_C = TH1D( "TTJETS_C", "", 58, 60, 350 )
    WJETS_A = TH1D( "WJETS_A", "", 58, 60, 350 )
    WJETS_C = TH1D( "WJETS_C", "", 58, 60, 350 )
    ZJETS_A = TH1D( "ZJETS_A", "", 58, 60, 350 )
    WW_A = TH1D( "WW_A", "", 58, 60, 350 )
    WZ_A = TH1D( "WZ_A", "", 58, 60, 350 )
    ZZ_A = TH1D( "ZZ_A", "", 58, 60, 350 )

    print CCuts
    print "lumiWeight*puWeight*2666*("+TransFun+")*("+TTScale+")"
    
    quickplot("RootFiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", DATA_A, "prunedMassAve", ACuts, "1" )
    quickplot("RootFiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", DATA_C, "prunedMassAve", CCuts, TransFun )
    for bin in xrange((DATA_C.GetNbinsX()+1)):
        print DATA_C.GetBinContent(bin)
    print "--------------------------------------"
    quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", TTJETS_A, "prunedMassAve", ACuts, "lumiWeight*puWeight*2666*("+TTScale+")")
    quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", TTJETS_C, "prunedMassAve", CCuts, "lumiWeight*puWeight*2666*("+TransFun+")*("+TTScale+")")
    
    quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", WJETS_A, "prunedMassAve", ACuts, "lumiWeight*puWeight*2666")
    quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", WJETS_C, "prunedMassAve", CCuts, "lumiWeight*puWeight*2666*("+TransFun+")")
    for bin in xrange((WJETS_C.GetNbinsX()+1)):
        print WJETS_C.GetBinContent(bin)
    print "--------------------------------------"
    for bin in xrange((WJETS_A.GetNbinsX()+1)):
        print WJETS_A.GetBinContent(bin)
    print "--------------------------------------"
    for bin in xrange((TTJETS_C.GetNbinsX()+1)):
        print TTJETS_C.GetBinContent(bin)
    print "--------------------------------------"
    for bin in xrange((TTJETS_A.GetNbinsX()+1)):
        print TTJETS_A.GetBinContent(bin)

    quickplot("RootFiles/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", ZJETS_A, "prunedMassAve", ACuts, "lumiWeight*puWeight*2666")

    quickplot("RootFiles/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", WW_A, "prunedMassAve", ACuts, "lumiWeight*puWeight*2666")

    quickplot("RootFiles/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", ZZ_A, "prunedMassAve", ACuts, "lumiWeight*puWeight*2666")

    quickplot("RootFiles/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", WZ_A, "prunedMassAve", ACuts, "lumiWeight*puWeight*2666")

    DATA_C.Add( TTJETS_C, -1 )
    DATA_C.Add( WJETS_C, -1 )

    DATA_C.Add( TTJETS_A )
    DATA_C.Add( WJETS_A )

    stack = THStack()
    
    OTHER = ZJETS_A.Clone()
    OTHER.Reset()

    OTHER.Add(ZJETS_A)
    OTHER.Add(WW_A)
    OTHER.Add(WZ_A)
    OTHER.Add(ZZ_A)
    OTHER.SetFillColor(8)
    OTHER.SetLineColor(1)
    OTHER.SetLineWidth(1)

    TTJETS_A.SetFillColor(2)
    TTJETS_A.SetLineColor(1)
    TTJETS_A.SetLineWidth(1)

    WJETS_A.SetFillColor(8)
    WJETS_A.SetLineColor(1)
    WJETS_A.SetLineWidth(1)

    DATA_C.SetFillColor(kBlue)
    DATA_C.SetLineColor(1)
    DATA_C.SetLineWidth(1)
    DATA_C.SetStats(0)

    DATA_A.SetLineColor(kBlack)
    DATA_A.SetMarkerColor(1)
    DATA_A.SetMarkerStyle(20)

    stack.Add(OTHER)
    stack.Add(WJETS_A)
    stack.Add(TTJETS_A)

    C = TCanvas("C", "", 800,800)

    plot = TPad("pad1", "The pad 80% of the height",0,0.10,1,1)
    pull = TPad("pad2", "The pad 20% of the height",0,0,1.0,0.20)
    plot.Draw()
    pull.Draw()
    plot.cd()

    DATA_C.GetYaxis().SetRangeUser(0.5,5000)
    DATA_C.GetXaxis().SetTitle("")
    DATA_C.GetYaxis().SetTitle("Events / 5 GeV")
    DATA_C.GetXaxis().SetLabelSize(0)
    DATA_C.Draw("hist")
    DATA_A.Draw("sameE0hist")
    stack.Draw("samehist")
    plot.SetLogy()

    pull.cd()
    Pull = DATA_A.Clone()
    Pull.Divide(DATA_C)

    Pull.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
    Pull.SetStats(0)
    Pull.SetLineColor(1)
    Pull.SetFillColor(0)
    Pull.SetMarkerColor(1)
    Pull.SetMarkerStyle(20)
    Pull.GetYaxis().SetNdivisions(4)
    Pull.GetYaxis().SetTitle("#frac{MC}{Data Est}")
    Pull.GetYaxis().SetLabelSize(50/15*Pull.GetYaxis().GetLabelSize())
    Pull.GetYaxis().SetTitleSize(3.8*Pull.GetYaxis().GetTitleSize())
    Pull.GetYaxis().SetTitleOffset(0.2)
    Pull.GetYaxis().SetRangeUser(0, 2)
    Pull.GetXaxis().SetLabelSize(.12)
    Pull.GetXaxis().SetTitleSize(.12)

    T0 = TLine(60,0.5,350,.5)
    T0.SetLineColor(kRed)
    T0.SetLineWidth(2)
    T2 = TLine(60,1.5,350,1.5)
    T2.SetLineColor(kRed)
    T2.SetLineStyle(2)
    T2.SetLineWidth(2)
    T1 = TLine(60,1.,350,1.)
    T1.SetLineColor(kRed)
    T1.SetLineStyle(3)
    T1.SetLineWidth(2)

    Pull.Draw("E0")
    T0.Draw("same")
    T2.Draw("same")
    T1.Draw("same")

    C.SaveAs("TCutPlots/SimpleBkg.png")

SimpleBkgEst()