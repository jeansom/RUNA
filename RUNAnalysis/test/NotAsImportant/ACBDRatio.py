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
from RUNA.RUNAnalysis.scaleFactors import *
gROOT.SetBatch()
gStyle.SetOptStat(0)
def ABCDRatio():
    weight = "(36555.21/15*lumiWeight*puWeight)"
    TTScale = "1.06*exp(-0.0005*HT/2)"

    PRES = "jet1Tau21<0.45&jet2Tau21<0.45"
    A = "deltaEtaDijet<1.5&prunedMassAsym<0.1"
    B = "deltaEtaDijet>1.5&prunedMassAsym<0.1"
    C = "deltaEtaDijet<1.5&prunedMassAsym>0.1"
    D = "deltaEtaDijet>1.5&prunedMassAsym>0.1" 

    DATA_A = TH1D( "DATA_A", "", 20, 50, 350 )
    DATA_B = TH1D( "DATA_B", "", 20, 50, 350 )
    DATA_C = TH1D( "DATA_C", "", 20, 50, 350 )
    DATA_D = TH1D( "DATA_D", "", 20, 50, 350 )

    TTJETS_A = TH1D( "T_A", "", 20, 50, 350 )
    TTJETS_B = TH1D( "T_B", "", 20, 50, 350 )
    TTJETS_C = TH1D( "T_C", "", 20, 50, 350 )
    TTJETS_D = TH1D( "T_D", "", 20, 50, 350 )

    WJETS_A = TH1D( "W_A", "", 20, 50, 350 )
    WJETS_B = TH1D( "W_B", "", 20, 50, 350 )
    WJETS_C = TH1D( "W_C", "", 20, 50, 350 )
    WJETS_D = TH1D( "W_D", "", 20, 50, 350 )

    DATA = DIST( "DATA", "80XRootFilesUpdated/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut15.root", "BoostedAnalysisPlotsPuppi/RUNATree", "1" )
    TTJETS = DIST( "TTJets", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScale+")" )
    WJETS = DIST( "WJets0", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+")" )
    QCD1000to1400 = DIST( "QCD1000to1400", "80XRootFilesUpdated/RUNAnalysis_QCDPt1000to1400_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1000to1400" )))
    QCD1400to1800 = DIST( "QCD1400to1800", "80XRootFilesUpdated/RUNAnalysis_QCDPt1400to1800_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1400to1800" )))
    QCD170to300 = DIST( "QCD170to300", "80XRootFilesUpdated/RUNAnalysis_QCDPt170to300_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_170to300" )))
    QCD1800to2400 = DIST( "QCD1800to2400", "80XRootFilesUpdated/RUNAnalysis_QCDPt1800to2400_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1800to2400" )))
    QCD2400to3200 = DIST( "QCD2400to3200", "80XRootFilesUpdated/RUNAnalysis_QCDPt2400to3200_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_2400to3200" )))
    QCD300to470 = DIST( "QCD300to470", "80XRootFilesUpdated/RUNAnalysis_QCDPt300to470_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_300to470" )))
    QCD3200toInf = DIST( "QCD3200toInf", "80XRootFilesUpdated/RUNAnalysis_QCDPt3200toInf_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_3200toInf" )))
    QCD470to600 = DIST( "QCD470to600", "80XRootFilesUpdated/RUNAnalysis_QCDPt470to600_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_470to600" )))
    QCD800to1000 = DIST( "QCD800to1000", "80XRootFilesUpdated/RUNAnalysis_QCDPt800to1000_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_800to1000" )))
    QCD600to800 = DIST( "QCD600to800", "80XRootFilesUpdated/RUNAnalysis_QCDPt600to800_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_600to800" )))
    QCD800to1000 = DIST( "QCD800to1000", "80XRootFilesUpdated/RUNAnalysis_QCDPt800to1000_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_800to1000" )))

    for i in [ QCD170to300, QCD300to470, QCD470to600, QCD600to800, QCD800to1000, QCD1000to1400, QCD1400to1800, QCD1800to2400, QCD2400to3200, QCD3200toInf ]:
        quickplot( i.File, i.Tree, DATA_A, "prunedMassAve", PRES+"&"+A, i.weight)
        quickplot( i.File, i.Tree, DATA_B, "prunedMassAve", PRES+"&"+B, i.weight)
        quickplot( i.File, i.Tree, DATA_C, "prunedMassAve", PRES+"&"+C, i.weight)
        quickplot( i.File, i.Tree, DATA_D, "prunedMassAve", PRES+"&"+D, i.weight)
#    quickplot( DATA.File, DATA.Tree, DATA_A, "prunedMassAve", PRES+"&"+A , DATA.weight )
#    quickplot( DATA.File, DATA.Tree, DATA_B, "prunedMassAve", PRES+"&"+B , DATA.weight )
#    quickplot( DATA.File, DATA.Tree, DATA_C, "prunedMassAve", PRES+"&"+C , DATA.weight )
#    quickplot( DATA.File, DATA.Tree, DATA_D, "prunedMassAve", PRES+"&"+D , DATA.weight )
    quickplot( TTJETS.File, TTJETS.Tree, TTJETS_A, "prunedMassAve", PRES+"&"+A , TTJETS.weight )
    quickplot( TTJETS.File, TTJETS.Tree, TTJETS_B, "prunedMassAve", PRES+"&"+B , TTJETS.weight )
    quickplot( TTJETS.File, TTJETS.Tree, TTJETS_C, "prunedMassAve", PRES+"&"+C , TTJETS.weight )
    quickplot( TTJETS.File, TTJETS.Tree, TTJETS_D, "prunedMassAve", PRES+"&"+D , TTJETS.weight )
    quickplot( WJETS.File, WJETS.Tree, WJETS_A, "prunedMassAve", PRES+"&"+A , WJETS.weight )
    quickplot( WJETS.File, WJETS.Tree, WJETS_B, "prunedMassAve", PRES+"&"+B , WJETS.weight )
    quickplot( WJETS.File, WJETS.Tree, WJETS_C, "prunedMassAve", PRES+"&"+C , WJETS.weight )
    quickplot( WJETS.File, WJETS.Tree, WJETS_D, "prunedMassAve", PRES+"&"+D , WJETS.weight )

    A = DATA_A.Clone("A")
    B = DATA_B.Clone("B")
    C = DATA_C.Clone("C")
    D = DATA_D.Clone("D")

#    A.Add(TTJETS_A, -1)
#    B.Add(TTJETS_B, -1)
#    C.Add(TTJETS_C, -1)
#    D.Add(TTJETS_D, -1)

#    A.Add(WJETS_A, -1)
#    B.Add(WJETS_B, -1)
#    C.Add(WJETS_C, -1)
#    D.Add(WJETS_D, -1)

    f = TF1("f", "1/(1.55+exp(.454-2.57e-07*x*x*x))",50, 350) 
    B.Divide(D)
#    B.Multiply(C)
    A.Divide(C)
    '''
    for bin in xrange(1, C.GetNbinsX()+1):
        binCenter = C.GetBinCenter(bin)
#        TF = B.GetBinContent(B.FindBin(binCenter))
        TF = f.Eval(binCenter)
        print TF
        C.SetBinContent(bin,C.GetBinContent(bin)*TF)
        '''
    A.SetLineColor(kRed)
    C1 = TCanvas("C","",800,800)
#    A.GetYaxis().SetRangeUser(0,1)
    A.GetXaxis().SetRangeUser(100,250)
    A.GetYaxis().SetTitle("R_{p/f}")
    A.GetXaxis().SetTitle("Pruned Average Mass [GeV]")
    A.Draw("E0")
    B.Draw("E0same")
    leg = TLegend(.15, .75, .50, .89)
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.AddEntry( A, "A", "L" )
    leg.AddEntry( C, "C*B/D", "L" )
#    leg.Draw("same")
    C1.SaveAs("TCutPlots/RatioABCD.png")
ABCDRatio()
