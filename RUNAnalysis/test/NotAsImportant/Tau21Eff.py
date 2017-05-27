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
from RUNA.RUNAnalysis.CorrPlotter_Header import *

gROOT.SetBatch()

def CutEff(cut, TITLE):

    PRES = TH1F("PRES", "", 40, 0, 400)
    TAU21 = TH1F("TAU21", "", 40, 0, 400)
    TAU21DDT = TH1F("TAU21DDT", "", 40, 0, 400)
    
    SIG120PRES = TH1F("SIG120PRES", "", 40, 0, 400)
    SIG120TAU21 = TH1F("SIG120TAU21", "", 40, 0, 400)
    SIG120TAU21DDT = TH1F("SIG120TAU21DDT", "", 40, 0, 400)
    SIG180PRES = TH1F("SIG180PRES", "", 40, 0, 400)
    SIG180TAU21 = TH1F("SIG180TAU21", "", 40, 0, 400)
    SIG180TAU21DDT = TH1F("SIG180TAU21DDT", "", 40, 0, 400)
    SIG200PRES = TH1F("SIG200PRES", "", 40, 0, 400)
    SIG200TAU21 = TH1F("SIG200TAU21", "", 40, 0, 400)
    SIG200TAU21DDT = TH1F("SIG200TAU21DDT", "", 40, 0, 400)
    SIG220PRES = TH1F("SIG220PRES", "", 40, 0, 400)
    SIG220TAU21 = TH1F("SIG220TAU21", "", 40, 0, 400)
    SIG220TAU21DDT = TH1F("SIG220TAU21DDT", "", 40, 0, 400)
    SIG300PRES = TH1F("SIG300PRES", "", 40, 0, 400)
    SIG300TAU21 = TH1F("SIG300TAU21", "", 40, 0, 400)
    SIG300TAU21DDT = TH1F("SIG300TAU21DDT", "", 40, 0, 400)
    
    QCDPtAll = DIST( "QCDPtAll", "v08/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".62*puWeight*36555.21/15*lumiWeight")

    TTScaleStr = "(1.06*exp( (-0.0005*(HT/2)) ))"
    TTJets = DIST( "TTJets", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "(36555.21/15*puWeight*lumiWeight*"+TTScaleStr+")" )
    WJets = DIST( "WJets", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "(36555.21/15*puWeight*lumiWeight)" )

    SIG120 = DIST( "SIG100", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-100_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "36555.21/15*puWeight*"+str(scaleFactor('RPVStopStopToJets_UDD312_M-100')) )
    SIG180 = DIST( "SIG160", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-160_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "36555.21/15*puWeight*"+str(scaleFactor('RPVStopStopToJets_UDD312_M-160')) )
    SIG200 = DIST( "SIG200", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-200_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "36555.21/15*puWeight*"+str(scaleFactor('RPVStopStopToJets_UDD312_M-200')) )
    SIG220 = DIST( "SIG220", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-220_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "36555.21/15*puWeight*"+str(scaleFactor('RPVStopStopToJets_UDD312_M-220')) )
    SIG300 = DIST( "SIG300", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-300_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "36555.21/15*puWeight*"+str(scaleFactor('RPVStopStopToJets_UDD312_M-300')) )


    presel = "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5"

    for i in [ QCDPtAll ]:
        quickplot(i.File, "BoostedAnalysisPlotsPuppi/RUNATree", PRES, "prunedMassAve", presel, i.weight)
        quickplot(i.File, "BoostedAnalysisPlotsPuppi/RUNATree", TAU21, "prunedMassAve", presel+"&"+cut, i.weight)

    quickplot(SIG120.File, "BoostedAnalysisPlotsPuppi/RUNATree", SIG120PRES, "prunedMassAve", presel, SIG120.weight)
    quickplot(SIG120.File, "BoostedAnalysisPlotsPuppi/RUNATree", SIG120TAU21, "prunedMassAve", presel+"&"+cut, SIG120.weight)
    quickplot(SIG180.File, "BoostedAnalysisPlotsPuppi/RUNATree", SIG180PRES, "prunedMassAve", presel, SIG180.weight)
    quickplot(SIG180.File, "BoostedAnalysisPlotsPuppi/RUNATree", SIG180TAU21, "prunedMassAve", presel+"&"+cut, SIG180.weight)
    quickplot(SIG200.File, "BoostedAnalysisPlotsPuppi/RUNATree", SIG200PRES, "prunedMassAve", presel, SIG200.weight)
    quickplot(SIG200.File, "BoostedAnalysisPlotsPuppi/RUNATree", SIG200TAU21, "prunedMassAve", presel+"&"+cut, SIG200.weight)
    quickplot(SIG220.File, "BoostedAnalysisPlotsPuppi/RUNATree", SIG220PRES, "prunedMassAve", presel, SIG220.weight)
    quickplot(SIG220.File, "BoostedAnalysisPlotsPuppi/RUNATree", SIG220TAU21, "prunedMassAve", presel+"&"+cut, SIG220.weight)
    quickplot(SIG300.File, "BoostedAnalysisPlotsPuppi/RUNATree", SIG300PRES, "prunedMassAve", presel, SIG300.weight)
    quickplot(SIG300.File, "BoostedAnalysisPlotsPuppi/RUNATree", SIG300TAU21, "prunedMassAve", presel+"&"+cut, SIG300.weight)
    
    print "EFF: " + str(float(TAU21.Integral()/PRES.Integral()))

    bin60 = TAU21.FindBin(100)
    bin350 = TAU21.FindBin(110)
    presel120 = float(SIG120PRES.Integral(bin60,bin350))/float(math.sqrt(PRES.Integral(bin60,bin350)))
    afterTau21120 = float(SIG120TAU21.Integral(bin60,bin350))/float(math.sqrt(TAU21.Integral(bin60,bin350)))
    bin60 = TAU21.FindBin(150)
    bin350 = TAU21.FindBin(170)
    presel180 = float(SIG180PRES.Integral(bin60,bin350))/float(math.sqrt(PRES.Integral(bin60,bin350)))
    afterTau21180 = float(SIG180TAU21.Integral(bin60,bin350))/float(math.sqrt(TAU21.Integral(bin60,bin350)))
    bin60 = TAU21.FindBin(190)
    bin350 = TAU21.FindBin(210)
    presel200 = float(SIG200PRES.Integral(bin60,bin350))/float(math.sqrt(PRES.Integral(bin60,bin350)))
    afterTau21200 = float(SIG200TAU21.Integral(bin60,bin350))/float(math.sqrt(TAU21.Integral(bin60,bin350)))
    bin60 = TAU21.FindBin(210)
    bin350 = TAU21.FindBin(230)
    presel220 = float(SIG220PRES.Integral(bin60,bin350))/float(math.sqrt(PRES.Integral(bin60,bin350)))
    afterTau21220 = float(SIG220TAU21.Integral(bin60,bin350))/float(math.sqrt(TAU21.Integral(bin60,bin350)))
    bin60 = TAU21.FindBin(290)
    bin350 = TAU21.FindBin(310)
    presel300 = float(SIG300PRES.Integral(bin60,bin350))/float(math.sqrt(PRES.Integral(bin60,bin350)))
    afterTau21300 = float(SIG300TAU21.Integral(bin60,bin350))/float(math.sqrt(TAU21.Integral(bin60,bin350)))
    print "***************M-120***************"
    print "Preselection: S/#sqrt{B} = " + str(presel120)
    print TITLE+": S/#sqrt{B} = " + str(afterTau21120)
    print "***************M-180***************"
    print "Preselection: S/#sqrt{B} = " + str(presel180)
    print TITLE+": S/#sqrt{B} = " + str(afterTau21180)
    print "***************M-200***************"
    print "Preselection: S/#sqrt{B} = " + str(presel200)
    print TITLE+": S/#sqrt{B} = " + str(afterTau21200)
    print "***************M-220***************"
    print "Preselection: S/#sqrt{B} = " + str(presel220)
    print TITLE+": S/#sqrt{B} = " + str(afterTau21220)
    print "***************M-300***************"
    print "Preselection: S/#sqrt{B} = " + str(presel300)
    print TITLE+": S/#sqrt{B} = " + str(afterTau21300)

#    print TITLE+" Efficiency = " + str(float(TAU21.Integral(bin60,bin350))/float(PRES.Integral(bin60,bin350)))
    

CutEff("numJets==2", "N Jets = 2" )
