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

def TTPlots(DISTS, PRES, CUT, NAME):
    Plot1 = TH1F("Plot1", "", 80, 0, 400)
    Plot2 = TH1F("Plot2", "", 80, 0, 400)

    for i in DISTS:
        quickplot(i.File, i.Tree, Plot1, "prunedMassAve", PRES, i.weight )
        quickplot(i.File, i.Tree, Plot2, "prunedMassAve", PRES+"&"+CUT, i.weight )

    Plot1.SetLineColor(kRed)
    Plot2.SetLineColor(kBlue)

    Plot1.GetXaxis().SetTitle("Average Mass [GeV]")
    Plot1.GetYaxis().SetTitle("Events / 5 GeV")

    FindAndSetMax( [Plot1, Plot2], False )

    C = TCanvas("C","",800,800)
    C.cd()
    plotPad = TPad("plotPad", "", 0, 0.10, 1, 1)
    legPad = TPad("legPad", "", 0, 0, 1, 0.10 )
    plotPad.Draw()
    legPad.Draw()
    plotPad.cd()
    Plot1.Draw("hist")
    Plot2.Draw("samehist")
    legPad.cd()
    leg = TLegend(0.11,0.11,0.89,0.89)
    leg.SetNColumns(2)
    leg.AddEntry(Plot1, "N Jets > 1", "L")
    leg.AddEntry(Plot2, "N Jets == 2", "L")
    leg.Draw()
    C.SaveAs("TCutPlots/Plot"+NAME+".png")

TTScaleStr = "(1.06*exp( (-0.0005*(HT/2)) ))"
weight = "(36555.21/15)"
TTJets = DIST( "TTJets", "v08/RUNAnalysis_TT_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight*"+TTScaleStr+")" )
SIGUDD312_M160 = DIST( "SIGUDD312_M-160", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-160_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight)" )
SIGUDD312_M200 = DIST( "SIGUDD312_M-200", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-200_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight)" )
SIGUDD312_M200 = DIST( "SIGUDD312_M-200", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-200_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight)" )
SIGUDD312_M220 = DIST( "SIGUDD312_M-220", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-220_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight)" )
SIGUDD312_M240 = DIST( "SIGUDD312_M-240", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-240_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight)" )
SIGUDD312_M300 = DIST( "SIGUDD312_M-300", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-300_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight)" )
SIGUDD323_M180 = DIST( "SIGUDD323_M-180", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-180_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight)" )
SIGUDD323_M200 = DIST( "SIGUDD323_M-200", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-200_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight)" )
SIGUDD323_M220 = DIST( "SIGUDD323_M-220", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-220_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight)" )
SIGUDD323_M240 = DIST( "SIGUDD323_M-240", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-240_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight)" )
SIGUDD323_M280 = DIST( "SIGUDD323_M-280", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-280_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight)" )
SIGUDD323_M300 = DIST( "SIGUDD323_M-300", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-300_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight)" )

zerobtag = "(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484)"
onebtag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484)||(jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
twobtag = "(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)"
jet1btag = "((jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
jet2btag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484))"

zeroTop = "(jet1Tau32>0.67&jet2Tau32>.67)"
oneTop = "((jet1Tau32<=0.67&jet2Tau32>=0.67)||(jet1Tau32>0.67&jet2Tau32<0.67))"
twoTop = "(jet1Tau32<0.67&jet2Tau32<0.67)"
jet1Top = "((jet1Tau32>0.67&jet2Tau32<0.67))"
jet2Top = "((jet1Tau32<0.67&jet2Tau32>0.67))"

for chan in [ [zerobtag+"&"+zeroTop, "b0t0"], [onebtag+"&"+zeroTop, "b1t0"], [twobtag+"&"+zeroTop, "b2t0"], [zerobtag+"&"+oneTop, "b0t1"], [onebtag+"&"+oneTop, "b1t1"], [twobtag+"&"+oneTop, "b2t1"], [zerobtag+"&"+twoTop, "b0t2"], [onebtag+"&"+twoTop, "b1t2"], [twobtag+"&"+twoTop, "b2t2"] ]:
    TTPlots( [TTJets], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&"+chan[0], "numJets==2", "TTJets"+chan[1] )
    for i in [ [SIGUDD312_M160, "SIGUDD312_M160"], [SIGUDD312_M200, "SIGUDD312_M200"], [SIGUDD312_M220, "SIGUDD312_M220"], [SIGUDD312_M240, "SIGUDD312_M240"], [SIGUDD312_M300, "SIGUDD312_M300"], [SIGUDD323_M180, "SIGUDD323_M180"], [SIGUDD323_M200, "SIGUDD323_M200"], [SIGUDD323_M220, "SIGUDD323_M220"], [SIGUDD323_M240, "SIGUDD323_M240"], [SIGUDD323_M280, "SIGUDD323_M280"], [SIGUDD323_M300, "SIGUDD323_M300"] ]:
        TTPlots( [i[0]], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&"+chan[0], "numJets==2", i[1]+chan[1] )



TTPlots( [TTJets], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "numJets==2", "TTJets" )
for i in [ [SIGUDD312_M160, "SIGUDD312_M160"], [SIGUDD312_M200, "SIGUDD312_M200"], [SIGUDD312_M220, "SIGUDD312_M220"], [SIGUDD312_M240, "SIGUDD312_M240"], [SIGUDD312_M300, "SIGUDD312_M300"], [SIGUDD323_M180, "SIGUDD323_M180"], [SIGUDD323_M200, "SIGUDD323_M200"], [SIGUDD323_M220, "SIGUDD323_M220"], [SIGUDD323_M240, "SIGUDD323_M240"], [SIGUDD323_M280, "SIGUDD323_M280"], [SIGUDD323_M300, "SIGUDD323_M300"] ]:
    TTPlots( [i[0]], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "numJets==2", i[1] )
