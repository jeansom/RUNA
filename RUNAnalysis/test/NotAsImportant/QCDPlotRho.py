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

def QCDPlotRho():
    PlotsQCD1 = TH1F("QCD_1", "", 15, 50, 350)
    PlotsQCD2 = TH1F("QCD_2", "", 15, 50, 350)
    PlotsQCD3 = TH1F("QCD_3", "", 15, 50, 350)
    PlotsQCD4 = TH1F("QCD_4", "", 15, 50, 350)
    PlotsQCD5 = TH1F("QCD_5", "", 15, 50, 350)
    MCScale = "(36555.21/15)"

    PRES = "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.0&(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484)&(jet1Tau32>0.67&jet2Tau32>0.67)&prunedMassAve>60"
    rho = "(log((jet1PrunedMass*jet1PrunedMass)/(jet1Pt*jet1Pt))+log((jet2PrunedMass*jet2PrunedMass)/(jet2Pt*jet2Pt)))"

    CUT1 = PRES+"&"+"(-5<"+rho+"&"+rho+"<-4.6)"
    CUT2 = PRES+"&"+"(-4.6<"+rho+"&"+rho+"<-4.2)"
    CUT3 = PRES+"&"+"(-4.2<"+rho+"&"+rho+"<-3.8)"
    CUT4 = PRES+"&"+"(-3.8<"+rho+"&"+rho+"<-3.4)"
    CUT5 = PRES+"&"+"(-3.4<"+rho+"&"+rho+"<-3.0)"

    quickplot("80XRootFilesUpdated/RUNAnalysis_QCDHTAll_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD1, "prunedMassAve", "("+CUT1+")", "puWeight*lumiWeight*"+MCScale+"*.85")
    quickplot("80XRootFilesUpdated/RUNAnalysis_QCDHTAll_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD2, "prunedMassAve", "("+CUT2+")", "puWeight*lumiWeight*"+MCScale+"*.85")
    quickplot("80XRootFilesUpdated/RUNAnalysis_QCDHTAll_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD3, "prunedMassAve", "("+CUT3+")", "puWeight*lumiWeight*"+MCScale+"*.85")
    quickplot("80XRootFilesUpdated/RUNAnalysis_QCDHTAll_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD4, "prunedMassAve", "("+CUT4+")", "puWeight*lumiWeight*"+MCScale+"*.85")
    quickplot("80XRootFilesUpdated/RUNAnalysis_QCDHTAll_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD5, "prunedMassAve", "("+CUT5+")", "puWeight*lumiWeight*"+MCScale+"*.85")

    PlotsQCD1.SetLineColor(kBlack)
    PlotsQCD1.SetFillColor(41)
    PlotsQCD2.SetLineColor(kBlack)
    PlotsQCD2.SetFillColor(42)
    PlotsQCD3.SetLineColor(kBlack)
    PlotsQCD3.SetFillColor(43)
    PlotsQCD4.SetLineColor(kBlack)
    PlotsQCD4.SetFillColor(44)
    PlotsQCD5.SetLineColor(kBlack)
    PlotsQCD5.SetFillColor(45)

    stack = THStack("h","")
    stack.Add(PlotsQCD1)
    stack.Add(PlotsQCD2)
    stack.Add(PlotsQCD3)
    stack.Add(PlotsQCD4)
    stack.Add(PlotsQCD5)

    C = TCanvas("C","",800,800)
    C.SetLogy()

    stack.Draw()
    stack.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
    stack.GetXaxis().SetRangeUser(60,350)
    stack.GetYaxis().SetRangeUser(.5,1000)
    stack.SetMaximum(1000)
    stack.GetYaxis().SetTitle("Events / 10")
    stack.GetYaxis().SetTitleOffset(1.3)
    stack.Draw("hist")

    leg = TLegend(0.50, 0.75, 0.89, 0.89)
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.AddEntry(PlotsQCD1, "-5 < #rho < -4.6", "F")
    leg.AddEntry(PlotsQCD2, "-4.6 < #rho < -4.2", "F")
    leg.AddEntry(PlotsQCD3, "-4.2 < #rho < -3.8", "F")
    leg.AddEntry(PlotsQCD4, "-3.8 < #rho < -3.4", "F")
    leg.AddEntry(PlotsQCD5, "-3.4 < #rho < -3.0", "F")
    
    leg.Draw("same")
    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.relPosX = 0.17
    CMS_lumi.CMS_lumi( (C), 4, 0)
    C.RedrawAxis()
    C.SaveAs("TCutPlots/QCDRho.png")
QCDPlotRho()
