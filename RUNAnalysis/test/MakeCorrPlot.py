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

weight = "2666*lumiWeight*puWeight"
DATA = DIST( "DATA", "RootFiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "1" )
QCD = DIST( "QCD", "RootFiles/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
SIG = DIST( "SIG", "RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
TTJets = DIST( "TTJets", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
WJets = DIST( "WJets", "RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
WW = DIST( "WW", "RootFiles/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
WZ = DIST( "WZ", "RootFiles/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
ZZ = DIST( "ZZ", "RootFiles/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
ZJets = DIST( "ZJets", "RootFiles/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
WDists = [ DATA ]

nopreselection = "jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.800||subjet12btagCSVv2>0.800)&(subjet21btagCSVv2>0.800||subjet22btagCSVv2>0.800)&deltaEtaDijet>1.0"
Tau32DistP = TH1F("Tau32DistP", "", 100, 0, 1)
Tau32DistF = TH1F("Tau32DistF", "", 100, 0, 1)
for i in WDists:
        quickplot(i.File, i.Tree, Tau32DistP, "prunedMassAsym", nopreselection+"&prunedMassAsym<0.1", i.weight)
        quickplot(i.File, i.Tree, Tau32DistF, "prunedMassAsym", nopreselection+"&prunedMassAsym>0.1", i.weight)
CutEff = Tau32DistP.Integral()/Tau32DistF.Integral()
print str(100.*CutEff) + "% retained"
EffCutString = '{0:4.2f}'.format(CutEff*100.)
VarComp_array_Mass = ["prunedMassAve", "prunedMassAsym", 12,50,350, 20, 0., 1.]
VarTitle = "Average Pruned Mass (GeV)"
Wtau32Comp_Mass = Alphabet("prunedMassAsym", WDists, [])
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
V0 = [ "prunedMassAve", 12, 50., 350., "Average Pruned Mass" ]
V1 = [ "prunedMassAsym", 20, 0., 1., "Pruned Mass Asymmetry" ]
presel = "jet1Tau21<0.6&jet2Tau21<0.6"
cutsB = "prunedMassAsym<0.1&deltaEtaDijet>1.0"
cutsD = "prunedMassAsym>0.1&deltaEtaDijet>1.0"

zerobtag = "(jet1btagCSVv2<0.8&jet2btagCSVv2<0.8)"
onebtag = "((jet1btagCSVv2<0.8&jet2btagCSVv2>0.8)||(jet1btagCSVv2>0.8&jet2btagCSVv2<0.8))"
twobtag = "(jet1btagCSVv2>0.8&jet2btagCSVv2>0.8)"

zeroTop = "(jet1Tau32>0.51&jet2Tau32>.51)"
oneTop = "((jet1Tau32<=0.51&jet2Tau32>=0.51)||(jet1Tau32>0.51&jet2Tau32<0.51))"
twoTop = "(jet1Tau32<0.51&jet2Tau32<0.51)"

cuts = presel
Profs = CorrPlotter( "PtCorrelation", WDists, V0, V1, cuts, presel, cutsB, cutsD )
CutValLine = GetQuantileProfiles(Wtau32Comp_Mass.TwoDPlot, CutEff, "Mass_CutVal")
CutValLine.SetLineColor(kViolet-3)
CutValLine.SetLineWidth(2)
CutShowLeg = TLegend(0.5,0.7,0.89,0.83)
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
C_2D.SaveAs("outputs/QuantileProfilesPlot.png")
