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
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
from RUNA.RUNAnalysis.scaleFactors import *

gROOT.SetBatch()
gStyle.SetOptStat(0)
QCD1000to1400 = DIST( "QCD1000to1400", "80XRootFilesUpdated/RUNAnalysis_QCDPt1000to1400_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1000to1400" )))
QCD1400to1800 = DIST( "QCD1400to1800", "80XRootFilesUpdated/RUNAnalysis_QCDPt1400to1800_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1400to1800" )))
QCD170to300 = DIST( "QCD170to300", "80XRootFilesUpdated/RUNAnalysis_QCDPt170to300_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_170to300" )))
QCD1800to2400 = DIST( "QCD1800to2400", "80XRootFilesUpdated/RUNAnalysis_QCDPt1800to2400_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1800to2400" )))
QCD2400to3200 = DIST( "QCD2400to3200", "80XRootFilesUpdated/RUNAnalysis_QCDPt2400to3200_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_2400to3200" )))
QCD300to470 = DIST( "QCD300to470", "80XRootFilesUpdated/RUNAnalysis_QCDPt300to470_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_300to470" )))
QCD3200toInf = DIST( "QCD3200toInf", "80XRootFilesUpdated/RUNAnalysis_QCDPt3200toInf_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_3200toInf" )))
QCD470to600 = DIST( "QCD470to600", "80XRootFilesUpdated/RUNAnalysis_QCDPt470to600_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_470to600" )))
QCD600to800 = DIST( "QCD600to800", "80XRootFilesUpdated/RUNAnalysis_QCDPt600to800_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_600to800" )))
QCD800to1000 = DIST( "QCD800to1000", "80XRootFilesUpdated/RUNAnalysis_QCDPt800to1000_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_800to1000" )))

QCD = [ QCD170to300, QCD300to470, QCD470to600, QCD600to800, QCD800to1000, QCD1000to1400, QCD1400to1800, QCD1800to2400, QCD2400to3200, QCD3200toInf ]

def NPVPlot(directory):
    L = TH1F("L","",29,60,350)
    G = TH1F("G","",29,60,350)
    rho = "(log((jet1PrunedMass*jet1PrunedMass)/(jet1Pt*jet1Pt))+log((jet2PrunedMass*jet2PrunedMass)/(jet2Pt*jet2Pt)))"
    rhoCut = "(0>"+rho+"&-5.5<"+rho+")"

    PRES = rhoCut+"&jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5"
    for i in QCD:
        quickplot(i.File, directory+"/RUNATree", L, "prunedMassAve", PRES+"&numPV<=20", i.weight)
        quickplot(i.File, directory+"/RUNATree", G, "prunedMassAve", PRES+"&numPV>20", i.weight)
        

    SUM = L.Clone("SUM")
    SUM.Add(G)

    L.SetLineColor(kRed)
    G.SetLineColor(kBlue)

    C = TCanvas("C","",800,800)
    pad1 = TPad( "pad1", "", 0, 0.20, 1, 0.9 )
    pad2 = TPad( "pad2", "", 0, 0, 1.0, 0.20 )
    pad3 = TPad( "pad3", "", 0, 0.9, 1, 1 )
    
    pad1.SetBottomMargin(0)
    pad1.SetTopMargin(0)
    pad2.SetTopMargin(0)
    pad3.SetBottomMargin(0)

    pad1.Draw()
    pad2.Draw()
    pad3.Draw()

    pad1.cd()

    SUM.GetYaxis().SetTitle("Events / 10 GeV")
    SUM.GetYaxis().SetTitleOffset(1.3)
    SUM.GetXaxis().SetTitle("")
    SUM.GetXaxis().SetLabelSize(0)

    SUM.Draw("hist")
    L.Draw("samehist")
    G.Draw("samehist")

    pad2.cd()

    ratio = L.Clone("ratio")
    ratio.Divide(G)
    
    ratio.GetXaxis().SetTitle("Average Mass")
    ratio.GetXaxis().SetTitleSize(0.12)
    ratio.GetXaxis().SetLabelSize(0.12)
    ratio.GetYaxis().SetTitleSize(0.12)
    ratio.GetYaxis().SetLabelSize(0.12)
    ratio.GetYaxis().SetTitle("#frac{QCD, NPV < 20}{QCD, NPV > 20}")
    ratio.Draw("histE")

    pad3.cd()
    leg = TLegend(0,0,1,1)
    leg.SetNColumns(3)
    leg.AddEntry(SUM, "No NPV Cut (= sum NPV<20, NPV>=20)", "L")
    leg.AddEntry(L, "NPV<20", "L")
    leg.AddEntry(G, "NPV>20", "L")
    leg.Draw()
    C.SaveAs("TCutPlots/NPVCutPlot"+directory+".png")

NPVPlot("BoostedAnalysisPlots")
NPVPlot("BoostedAnalysisPlotsPuppi")
