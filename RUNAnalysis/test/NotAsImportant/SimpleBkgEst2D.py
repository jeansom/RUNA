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

def SimpleBkgEst2D(tau21,NAME):

    ACuts = "("+tau21+"&deltaEtaDijet<1.5&prunedMassAsym<0.1)"
    BCuts = "("+tau21+"&deltaEtaDijet>1.5&prunedMassAsym<0.1)"
    CCuts = "("+tau21+"&deltaEtaDijet<1.5&prunedMassAsym>0.1)"
    DCuts = "("+tau21+"&deltaEtaDijet>1.5&prunedMassAsym>0.1)"

    DATA_A = TH1D( "DATA_A", "", 29, 60, 350 )
    DATA_B = TH1D( "DATA_B", "", 25, 300, 5000 )
    DATA_C = TH2D( "DATA_C", "", 29, 60, 350, 25, 300, 5000 )
    DATA_D = TH1D( "DATA_D", "", 25, 300, 5000 )

    for i in [ "QCDPt170to300", "QCDPt300to470", "QCDPt470to600", "QCDPt600to800", "QCDPt800to1000", "QCDPt1000to1400", "QCDPt1400to1800", "QCDPt1800to2400", "QCDPt2400to3200", "QCDPt3200toInf" ]:
#    for i in [ "QCDPt300to470", "QCDPt470to600", "QCDPt600to800", "QCDPt800to1000", "QCDPt1000to1400", "QCDPt1400to1800", "QCDPt1800to2400", "QCDPt2400to3200", "QCDPt3200toInf" ]:
        print i
        quickplot("80XRootFilesUpdated/RUNAnalysis_"+i+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", DATA_A, "prunedMassAve", ACuts, "0.85*puWeight*36555.21/15*"+str(scaleFactor(i)) )     
        quickplot("80XRootFilesUpdated/RUNAnalysis_"+i+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", DATA_B, "jet1Pt+jet2Pt", BCuts, "0.85*puWeight*36555.21/15*"+str(scaleFactor(i)) )     
        quick2dplot("80XRootFilesUpdated/RUNAnalysis_"+i+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", DATA_C, "prunedMassAve", "jet1Pt+jet2Pt", CCuts, "0.85*puWeight*36555.21/15*"+str(scaleFactor(i)) )     
        quickplot("80XRootFilesUpdated/RUNAnalysis_"+i+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", DATA_D, "jet1Pt+jet2Pt", DCuts, "0.85*puWeight*36555.21/15*"+str(scaleFactor(i)) )     


    DATA_B.Divide(DATA_D)

    DATA_EST = TH1D( "DATA_EST", "", 29, 60, 350 )

    for binX in xrange(1, (DATA_C.GetXaxis().GetNbins())+1 ):
        for binY in xrange(1, (DATA_C.GetYaxis().GetNbins())+1 ):
            HT = DATA_C.GetYaxis().GetBinCenter(binY)
            MASS = DATA_C.GetXaxis().GetBinCenter(binX)

            TF = DATA_B.GetBinContent(DATA_B.FindBin(HT))

            DATA_EST.Fill( MASS, TF*DATA_C.GetBinContent(binX, binY) )

    C = TCanvas("C", "", 800,800)

    plot = TPad("pad1", "The pad 80% of the height",0,0.20,1,1)
    pull = TPad("pad2", "The pad 20% of the height",0,0,1.0,0.20)
    plot.SetBottomMargin(0)
    pull.SetTopMargin(0)
    plot.Draw()
    pull.Draw()
    plot.cd()

    DATA_A.SetLineColor(kRed)

    FindAndSetMax([DATA_A,DATA_EST],False)
    DATA_EST.GetXaxis().SetTitle("")
    DATA_EST.GetYaxis().SetTitle("Events")
    DATA_EST.GetXaxis().SetLabelSize(0)
    DATA_EST.Draw("hist")
    DATA_A.Draw("sameE0hist")

    pull.cd()
    Pull = DATA_A.Clone()
    Pull.Divide(DATA_EST)

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
    
tau21 = "((jet1Tau21-DDT_tau21_2d)<0&(jet2Tau21-DDT_tau21_2d)<0)"
SimpleBkgEst2D(tau21, "pres")
