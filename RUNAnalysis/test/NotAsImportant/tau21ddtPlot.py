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

def tau21ddtPlot():
    PlotsQCDDDT = []
    jet1Tau21 = "(jet1Tau21-DDT_20_tau21)"
    jet2Tau21 = "(jet2Tau21-DDT_20_tau21)"
    CUT = jet1Tau21+">-1"

#    SAMPLES = [ ["QCDPt170to300", "QCDPt300to470", "QCDPt470to600", "QCDPt600to800", "QCDPt800to1000", "QCDPt1000to1400", "QCDPt1400to1800", "QCDPt1800to2400", "QCDPt2400to3200", "QCDPt3200toInf"] ]
    SAMPLES = [[ "RPVStopStopToJets_UDD323_M-120" ], [ "RPVStopStopToJets_UDD323_M-180" ],[ "RPVStopStopToJets_UDD323_M-220" ],[ "RPVStopStopToJets_UDD323_M-300" ] ]
    for i in SAMPLES:
#    for i in [ "RPVStopStopToJets_UDD323_M-120" ]:
        PlotsQCDDDT.append(TH1F("QCDDDT"+i[0],"",100,-1,1))
        for j in i:
            print j
            quickplot("80XRootFilesUpdated/Signals/RUNAnalysis_"+j+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", PlotsQCDDDT[-1], jet1Tau21, CUT, ".85*puWeight*36555.21/15*"+str(scaleFactor(j) ) )
            quickplot("80XRootFilesUpdated/Signals/RUNAnalysis_"+j+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", PlotsQCDDDT[-1], jet2Tau21, CUT, ".85*puWeight*36555.21/15*"+str(scaleFactor(j) ) )

    n = 0
    for col in [ kRed, kBlue, kOrange, kBlack ]:
        PlotsQCDDDT[n].SetLineColor(col)
        n = n+1
    for Plot in PlotsQCDDDT:
        Plot.SetLineWidth(1)
        Plot.GetXaxis().SetTitle("")
        Plot.GetYaxis().SetTitle("Events")
        Plot.GetYaxis().SetTitleOffset(1.3)
    
    PlotsQCD = []
    jet1Tau21 = "(jet1Tau21)"
    jet2Tau21 = "(jet2Tau21)"
    CUT = jet1Tau21+">-1"

    for i in SAMPLES:
        PlotsQCD.append(TH1F("QCD"+i[0],"",100,-1,1))
        for j in i:
            quickplot("80XRootFilesUpdated/Signals/RUNAnalysis_"+j+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", PlotsQCD[-1], jet1Tau21, CUT, ".85*puWeight*36555.21/15*"+str(scaleFactor(j) ) )
            quickplot("80XRootFilesUpdated/Signals/RUNAnalysis_"+j+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", PlotsQCD[-1], jet2Tau21, CUT, ".85*puWeight*36555.21/15*"+str(scaleFactor(j) ) )

    n = 0
    for col in [ kRed, kBlue, kOrange, kBlack ]:
        PlotsQCD[n].SetLineColor(col)
        n = n+1
    for Plot in PlotsQCD:
        Plot.SetLineWidth(1)
        Plot.GetXaxis().SetTitle("")
        Plot.GetYaxis().SetTitle("Events")
        Plot.GetYaxis().SetTitleOffset(1.3)
        Plot.SetLineStyle(2)
    
    FindAndSetMax( PlotsQCD+PlotsQCDDDT, False )

    leg = TLegend(0.11,0.7,0.8,0.89)
    leg.SetNColumns(1)
    leg.SetFillStyle(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetLineColor(0)
    for i in xrange(len(PlotsQCD)):
        leg.AddEntry(PlotsQCD[i], "#tau_{21}, "+SAMPLES[i][0]+", Passing Events = "+str(PlotsQCD[i].Integral(0,PlotsQCD[i].FindBin(0.45))), "L")
        leg.AddEntry(PlotsQCDDDT[i], "#tau_{21}^{DDT}, "+SAMPLES[i][0]+", Passing Events = "+str(PlotsQCDDDT[i].Integral(0,PlotsQCDDDT[i].FindBin(0))), "L")

    C = TCanvas( "C", "", 800, 800 )
    
    PlotsQCD[0].Draw("hist")
    for i in PlotsQCD:
        i.Draw("samehist")
    for i in PlotsQCDDDT:
        i.Draw("samehist")

    leg.Draw("same")

    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.relPosX = 0.17
    CMS_lumi.CMS_lumi( (C), 4, 0)
    C.RedrawAxis()

    C.SaveAs("TCutPlots/tau21DDT_120.png")
tau21ddtPlot()
