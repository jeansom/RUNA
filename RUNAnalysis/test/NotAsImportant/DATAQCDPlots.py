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
def DATAQCD(VAR, BINS, CUT, NAME, Title, cutName, log):
    PlotsQCD = TH1F("QCD_"+VAR, "", BINS[0], BINS[1], BINS[2])
    PlotsTT = TH1F("TT_"+VAR, "", BINS[0], BINS[1], BINS[2])
    PlotsT = TH1F("T_"+VAR, "", BINS[0], BINS[1], BINS[2])
    PlotsWJets = TH1F("WJets_"+VAR, "", BINS[0], BINS[1], BINS[2])
    PlotsDATA = TH1F("DATA_"+VAR, "", BINS[0], BINS[1], BINS[2])
    
    MCScale = "(36555.21/15)"
    rootFiles = "v08/"
    quickplot(rootFiles+"/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "36555.21/15*lumiWeight*puWeight" )
    quickplot("80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", PlotsTT, VAR, CUT, "puWeight*lumiWeight*1.06*exp(-0.0005*HT/2)*"+MCScale)
    quickplot("80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", PlotsWJets, VAR, CUT, "puWeight*lumiWeight*"+MCScale)
    quickplot("v08/RUNAnalysis_JetHT_Run2016_80X_V2p4_v08_cut15_pruned.root", "BoostedAnalysisPlots/RUNATree", PlotsDATA, VAR, CUT, "1")
    quickplot("80XRootFilesUpdated/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", PlotsT, VAR, CUT, "puWeight*lumiWeight*"+MCScale)

    PlotsDATA.Add(PlotsT, -1)
    PlotsDATA.Add(PlotsWJets, -1)
    PlotsDATA.Add(PlotsTT, -1)

    nEventsData = PlotsDATA.Integral(0,1000000)
    nEventsQCD = PlotsQCD.Integral(0,1000000)

    print "Ratio: " + str(float(nEventsData/nEventsQCD))

    PlotsDATA.Divide(PlotsQCD)
    f = TF1("f", "[0]")
    PlotsDATA.Fit(f)
    print f.GetParameter(0)

    C = TCanvas("C","",800,800)
    C.cd()
    PlotsDATA.Draw()
    C.SaveAs("TCutPlots/DATAQCDRatio.png")

DATAQCD( "prunedMassAve", [ 40, 0, 400 ], "1.", "prunedMassAve_NoCuts", "Average Mass", "prunedMassAve_NoCuts", True )
DATAQCD( "HT", [ 130, 700, 2000 ], "1.", "HT_NoCuts", "HT", "HT_NoCuts", True )
