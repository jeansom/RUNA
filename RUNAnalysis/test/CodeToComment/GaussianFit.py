#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

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
import RUNA.RUNAnalysis.Plotting
from RUNA.RUNAnalysis.Plotting import *

B = TH1D( "B", "", 58, 60, 350 )
B.GetXaxis().SetTitle( "Average Pruned Mass [GeV]" )
B.GetYaxis().SetTitle( "N Events" )
gStyle.SetOptStat(0)

zerobtag = "(jet1btagCSVv2<0.800&jet2btagCSVv2<0.800)"
onebtag = "((jet1btagCSVv2<0.800&jet2btagCSVv2>0.800)||(jet1btagCSVv2>0.800&jet2btagCSVv2<0.800))"
twobtag = "(jet1btagCSVv2>0.800&jet2btagCSVv2>0.800)"
jet1btag = "((jet1btagCSVv2>0.800&jet2btagCSVv2<0.800))"
jet2btag = "((jet1btagCSVv2<0.800&jet2btagCSVv2>0.800))"

zeroTop = "(jet1Tau32>0.51&jet2Tau32>.51)"
oneTop = "((jet1Tau32<=0.51&jet2Tau32>=0.51)||(jet1Tau32>0.51&jet2Tau32<0.51))"
twoTop = "(jet1Tau32<0.51&jet2Tau32<0.51)"
jet1Top = "((jet1Tau32>0.51&jet2Tau32<0.51))"
jet2Top = "((jet1Tau32<0.51&jet2Tau32>0.51))"


quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", B, "massAve", "jet1Tau21<0.6&jet2Tau21<0.6&prunedMassAsym>0.1&deltaEtaDijet>1.0&"+zerobtag+"&"+zeroTop, "lumiWeight*puWeight*2666")
#quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", B, "massAve", "jet1Tau21<0.6&jet2Tau21<0.6&"+zerobtag+"&"+zeroTop, "lumiWeight*puWeight*2666")

GResult = B.Fit("gaus", "S", "", 60, 130)
gFit = (B.GetFunction("gaus")).Clone()
LResult = B.Fit( "pol1", "S", "", 130, 200)
lFit = (B.GetFunction("pol1")).Clone()

C = TCanvas( "C", "", 600, 800 )
C.cd()
B.Draw()
gFit.SetLineColor(kBlue)
gFit.Draw("same")
lFit.Draw("same")

lSlope = LResult.Parameter(1)
g = GResult.Parameter(0)

latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.01)
latex.SetTextAlign(13)
latex.DrawLatex(.6,.8,"MC b0t0 D Region")
latex.DrawLatex(.63,.76,"#color[4]{Gaussian Fit:}" ) 
latex.DrawLatex( .63, .73, "#color[4]{#mu: " + str("%.4f" % GResult.Parameter(1)) + "}" )
latex.DrawLatex( .63, .70, "#color[4]{#sigma: " + str("%.4f" % GResult.Parameter(2)) + "}" )

latex.DrawLatex(.63,.66,"#color[2]{Linear Fit:}" ) 
latex.DrawLatex( .63, .63, "#color[2]{m: " + str("%.4f" % LResult.Parameter(1)) + "}" )

C.SaveAs("outputs/Db0t0.png")
