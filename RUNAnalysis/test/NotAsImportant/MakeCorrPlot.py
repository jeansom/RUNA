import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
from ROOT import TColor
import scipy
# Our functions:
import RUNA.RUNAnalysis.Alphabet_Header
from RUNA.RUNAnalysis.Alphabet_Header import *
import RUNA.RUNAnalysis.Plotting_Header
from RUNA.RUNAnalysis.Plotting_Header import *
import RUNA.RUNAnalysis.Converters
from RUNA.RUNAnalysis.Converters import *
import RUNA.RUNAnalysis.Distribution_Header
from RUNA.RUNAnalysis.Distribution_Header import *
import RUNA.RUNAnalysis.Alphabet
from RUNA.RUNAnalysis.Alphabet import *
import RUNA.RUNAnalysis.CorrPlotter_Header
from RUNA.RUNAnalysis.CorrPlotter_Header import *
from RUNA.RUNAnalysis.scaleFactors import *

weight = "36555.21*lumiWeight*puWeight"
DATA = DIST( "DATA", "80XRootFilesUpdated/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut15.root", "BoostedAnalysisPlotsPuppi/RUNATree", "1" )
QCD1000to1400 = DIST( "QCD1000to1400", "80XRootFilesUpdated/RUNAnalysis_QCDPt1000to1400_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1000to1400" )))
QCD1400to1800 = DIST( "QCD1400to1800", "80XRootFilesUpdated/RUNAnalysis_QCDPt1400to1800_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1400to1800" )))
QCD170to300 = DIST( "QCD170to300", "80XRootFilesUpdated/RUNAnalysis_QCDPt170to300_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_170to300" )))
QCD1800to2400 = DIST( "QCD1800to2400", "80XRootFilesUpdated/RUNAnalysis_QCDPt1800to2400_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1800to2400" )))
QCD2400to3200 = DIST( "QCD2400to3200", "80XRootFilesUpdated/RUNAnalysis_QCDPt2400to3200_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_2400to3200" )))
QCD300to470 = DIST( "QCD300to470", "80XRootFilesUpdated/RUNAnalysis_QCDPt300to470_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_300to470" )))
QCD3200toInf = DIST( "QCD3200toInf", "80XRootFilesUpdated/RUNAnalysis_QCDPt3200toInf_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_3200toInf" )))
QCD470to600 = DIST( "QCD470to600", "80XRootFilesUpdated/RUNAnalysis_QCDPt470to600_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_470to600" )))
QCD600to800 = DIST( "QCD600to800", "80XRootFilesUpdated/RUNAnalysis_QCDPt600to800_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_600to800" )))
QCD800to1000 = DIST( "QCD800to1000", "80XRootFilesUpdated/RUNAnalysis_QCDPt800to1000_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_800to1000" )))
TTScaleStr = "(1.06*exp(-0.0005*HT/2))"
WScaleStr = "(1)"
TTJets = DIST( "TTJets", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleStr+")" )
WJets = DIST( "WJets", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+WScaleStr+")" )

WDists = [ QCD170to300, QCD300to470, QCD470to600, QCD600to800, QCD800to1000, QCD1000to1400, QCD1400to1800, QCD1800to2400, QCD2400to3200, QCD3200toInf ]

nopreselection = "jet1Tau21<0.45&jet2Tau21<0.45"
Tau32DistP = TH1F("Tau32DistP", "", 100, 0, 1)
Tau32DistF = TH1F("Tau32DistF", "", 100, 0, 1)
for i in WDists:
        quickplot(i.File, i.Tree, Tau32DistP, "prunedMassAsym", nopreselection+"&prunedMassAsym<0.1", i.weight)
        quickplot(i.File, i.Tree, Tau32DistF, "prunedMassAsym", nopreselection+"&prunedMassAsym>0.1", i.weight)
CutEff = Tau32DistP.Integral()/Tau32DistF.Integral()
print str(100.*CutEff) + "% retained"
EffCutString = '{0:4.2f}'.format(CutEff*100.)
VarComp_array_Mass = ["deltaEtaDijet", "prunedMassAsym", 20,0,5, 20, 0., 1.]
VarTitle = "Delta Eta Dijet"
Wtau32Comp_Mass = Alphabet("prunedMassAsym", WDists, [], [])
Wtau32Comp_Mass.SetRegions(VarComp_array_Mass, nopreselection, "", "")
Wtau32Comp_Mass.TwoDPlot.SetStats(0)
Wtau32Comp_Mass.TwoDPlot.GetYaxis().SetTitle("Pruned Mass Asymmetry")
Wtau32Comp_Mass.TwoDPlot.GetXaxis().SetTitle(VarTitle)
Wtau32Comp_Mass.TwoDPlot.SetFillColor(30)
Wtau32Comp_Mass.TwoDPlot.SetLineColor(30)
Wtau32Comp_Mass.TwoDPlot.SetMarkerColor(30)
CutLine = TLine(50,0.1,350,0.1)
CutLine.SetLineStyle(2)
CutLine.SetLineColor(7)
CutLine.SetLineWidth(2)
Profs = []
#for i in [9,8,7,6,5,4,3,2,1,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5]:
#    Profs.append(GetQuantileProfiles(Wtau32Comp_Mass.TwoDPlot, 0.1*i, "Mass_"+str(i)))
#V0 = [ "prunedMassAve", 12, 50., 350., "Average Pruned Mass" ]
V0 = [ "deltaEtaDijet", 20, 0., 5., "Delta Eta Dijet" ]
V1 = [ "prunedMassAsym", 20, 0., 1., "Pruned Mass Asymmetry" ]
presel = "jet1Tau21<0.45&jet2Tau21<0.45"

zerobtag = "(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484)"
onebtag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484)||(jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
twobtag = "(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)"

zeroTop = "(jet1Tau32>0.67&jet2Tau32>.51)"
oneTop = "((jet1Tau32<=0.67&jet2Tau32>=0.67)||(jet1Tau32>0.67&jet2Tau32<0.67))"
twoTop = "(jet1Tau32<0.67&jet2Tau32<0.67)"

cuts = presel
cutsB = "prunedMassAsym<0.1&deltaEtaDijet>1.5"
cutsD = "prunedMassAsym>0.1&deltaEtaDijet>1.5"

Profs = CorrPlotter( "PtCorrelation", WDists, V0, V1, cuts, presel, cutsB, cutsD )
CutValLine = GetQuantileProfiles(Wtau32Comp_Mass.TwoDPlot, CutEff, "Mass_CutVal")
CutValLine.SetLineColor(kViolet-3)
CutValLine.SetLineWidth(2)
CutShowLeg = TLegend(0.5,0.7,0.84849,0.84843)
CutShowLeg.AddEntry(CutLine, "Cut (Average Efficiency = "+EffCutString+"%)", "L")
CutShowLeg.AddEntry(CutValLine, EffCutString+"% Efficiency (per bin)", "L")
CutShowLeg.AddEntry(Profs[0], "5% efficiency grades", "L")
CutShowLeg.SetLineColor(0)
CutShowLeg.SetFillColor(0)
C_2D = TCanvas("C_2D", "", 800, 600)
C_2D.cd()
gStyle.SetPalette(90)
Wtau32Comp_Mass.TwoDPlot.Draw("COL")
CutValLine.Draw("same")
CutLine.Draw("same")
for i in Profs[1]:
    i.SetLineColor(46)
    i.SetLineStyle(3)
    i.SetLineWidth(2)
    i.Draw("same")
CutShowLeg.Draw("same")
C_2D.SaveAs("TCutPlots/QuantileProfilesPlot.png")
