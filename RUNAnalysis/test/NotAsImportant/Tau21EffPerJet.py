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

def CutEff(cut, TITLE):

    PRES = TH1F("PRES", "", 100, 0, 1)
    TAU21 = TH1F("TAU21", "", 100, 0, 1)
    TAU21DDT = TH1F("TAU21DDT", "", 100, 0, 1)
    
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

    TTScaleStr = "(1.06*exp( (-0.0005*(HT/2)) ))"
    TTJets = DIST( "TTJets", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "(36555.21/15*puWeight*lumiWeight*"+TTScaleStr+")" )
    WJets = DIST( "WJets", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "(36555.21/15*puWeight*lumiWeight)" )


    presel = "1"

    for i in [ QCD170to300, QCD300to470, QCD470to600, QCD600to800, QCD800to1000, QCD1000to1400, QCD1400to1800, QCD1800to2400, QCD2400to3200, QCD3200toInf ]:
        quickplot(i.File, "BoostedAnalysisPlotsPuppi/RUNATree", PRES, "jet1Tau21", presel, i.weight)
#        quickplot(i.File, "BoostedAnalysisPlotsPuppi/RUNATree", PRES, "jet2Tau21", presel, i.weight)

    for i in [0.85,0.75,0.65,0.55,0.45]:
        presel = PRES.Integral(PRES.FindBin(0), PRES.FindBin(1))
        cut = PRES.Integral(PRES.FindBin(0),PRES.FindBin(i))
        print "tau21 < " + str(i)+" Efficiency = " + str(float(cut)/float(presel))
    

CutEff("jet1Tau21<0.45&jet2Tau21<0.45", "Tau21 < 0.45" )
