#
import os
import math
from array import array
import optparse
import argparse
import ROOT
from ROOT import *
import scipy
import random
from scipy.stats import chisqprob

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

gStyle.SetOptStat(0)
C = TCanvas( "C", "", 800, 800 )

FILE = TFile.Open("outputs//BeforeThetaQCD/21174CMVAv2BCDDATA//LIM_FEEDb1t1.root")
chan__QCD__TTAlphaScale__up = FILE.Get("b1t1__QCD__TTAlphaScale__up").Clone()
chan__QCD__TTScale__up = FILE.Get("b1t1__QCD__TTScale__up").Clone()
chan__QCD__TTAlphaScale__down = FILE.Get("b1t1__QCD__TTAlphaScale__down").Clone()
chan__QCD__TTScale__down = FILE.Get("b1t1__QCD__TTScale__down").Clone()
chan__QCD = FILE.Get("b1t1__QCD").Clone()

#chan__QCD__TTAlphaScale__up.Rebin(3)
#chan__QCD__TTScale__up.Rebin(3)
#chan__QCD__TTAlphaScale__down.Rebin(3)
#chan__QCD__TTScale__down.Rebin(3)
#chan__QCD.Rebin(3)

leg = TLegend( 0.12, 0.80, 0.96, 0.89 )
#leg.SetFillColor(4001)
leg.SetLineColor(0)
leg.SetNColumns(2)
FindAndSetMax( [chan__QCD__TTAlphaScale__up, chan__QCD__TTAlphaScale__down, chan__QCD__TTScale__up, chan__QCD__TTScale__down, chan__QCD], False )
leg.SetFillStyle(0)
leg.SetTextSize(0.02)
leg.AddEntry( chan__QCD, "Nominal Estimation", "L" )
leg.AddEntry( chan__QCD__TTScale__up, "Estimation w/ t#bar{t} Normalization #pm 50%", "L" )
leg.AddEntry( chan__QCD__TTAlphaScale__up, "Estimation w/ t#bar{t} Alpha #pm 50%", "L" )
leg.Draw()

chan__QCD__TTAlphaScale__up.SetLineColor(kRed)
chan__QCD__TTAlphaScale__up.SetTitle("")
chan__QCD__TTAlphaScale__up.GetXaxis().SetTitle("Average Pruned Mass [GeV]")
chan__QCD__TTAlphaScale__up.GetYaxis().SetTitle("Events / " + str(chan__QCD__TTAlphaScale__up.GetBinWidth(1)))
chan__QCD__TTAlphaScale__up.GetYaxis().SetTitleOffset(1.2)
chan__QCD__TTAlphaScale__up.GetYaxis().SetLabelSize(0.03)
chan__QCD__TTAlphaScale__up.GetXaxis().SetLabelSize(0.03)
chan__QCD__TTAlphaScale__up.Draw("hist")
chan__QCD__TTScale__up.SetLineColor(kGreen)
chan__QCD__TTScale__up.Draw("hist same")
chan__QCD__TTScale__down.SetLineColor(kGreen)
chan__QCD__TTScale__down.Draw("hist same")
chan__QCD.Draw("hist same")
chan__QCD__TTAlphaScale__down.SetLineColor(kRed)
chan__QCD__TTAlphaScale__down.Draw("hist same")
#C.SetLogy()
leg.Draw()
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.14
CMS_lumi.CMS_lumi(C, 4, 0)    
C.RedrawAxis()
C.SaveAs("outputs/QCD__TT.png")

btag1 = "(subjet11btagCMVAv2>0.185||subjet12btagCMVAv2>0.185)"
btag2 = "(subjet21btagCMVAv2>0.185||subjet22btagCMVAv2>0.185)"
nobtag1 = "(subjet11btagCMVAv2<0.185&subjet12btagCMVAv2<0.185)"
nobtag2 = "(subjet21btagCMVAv2<0.185&subjet22btagCMVAv2<0.185)"
onebtag1 = "("+btag1+"&"+nobtag2+")"
onebtag2 = "("+nobtag1+"&"+btag2+")"

#zerobtag = nobtag1+"&"+nobtag2
#onebtag = onebtag1+"||"+onebtag2
#twobtag = btag1+"&"+btag2

zerobtag = "(jet1btagCMVAv2<0.185&jet2btagCMVAv2<0.185)"
onebtag = "((jet1btagCMVAv2<0.185&jet2btagCMVAv2>0.185)||(jet1btagCMVAv2>0.185&jet2btagCMVAv2<0.185))"
twobtag = "(jet1btagCMVAv2>0.185&jet2btagCMVAv2>0.185)"
#twobtag = "(jet1btagCMVAv2>0.185&jet2btagCMVAv2>0.185)"

zeroTop = "(jet1Tau32>0.51&jet2Tau32>.51)"
oneTop = "((jet1Tau32<=0.51&jet2Tau32>=0.51)||(jet1Tau32>0.51&jet2Tau32<0.51))"
twoTop = "(jet1Tau32<0.51&jet2Tau32<0.51)"

jet1Top = "((jet1Tau32>0.51&jet2Tau32<0.51))"
jet2Top = "((jet1Tau32<0.51&jet2Tau32>0.51))"
jet1btag = "((jet1btagCSVv2>0.800&jet2btagCSVv2<0.800))"
jet2btag = "((jet1btagCSVv2<0.800&jet2btagCSVv2>0.800))"

TT_nowt = chan__QCD.Clone()
TT_nowt.Reset()
TT_wt = TT_nowt.Clone()
quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", TT_nowt, "prunedMassAve", "jet1Tau21<0.6&jet2Tau21<0.6&deltaEtaDijet<1.0&prunedMassAsym<0.1", "lumiWeight*puWeight*2666")
quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", TT_wt, "prunedMassAve", "jet1Tau21<0.6&jet2Tau21<0.6&deltaEtaDijet<1.0&prunedMassAsym<0.1", "lumiWeight*puWeight*2666*1.06*exp(-0.0005*HT/2)")
TT_nowt.SetLineColor(kRed)
TT_nowt.GetXaxis().SetTitle("Pruned Average Mass [GeV]")
TT_nowt.GetYaxis().SetTitle("Events / " + str(TT_nowt.GetBinWidth(1)))
TT_nowt.SetTitle("")
TT_nowt.GetYaxis().SetTitleOffset(1.2)
TT_nowt.GetYaxis().SetLabelSize(0.03)
TT_nowt.GetXaxis().SetLabelSize(0.03)
TT_nowt.Draw("hist")
TT_wt.SetLineColor(kBlue)
TT_wt.Draw("histsame")
FindAndSetMax( [TT_nowt, TT_wt ], False )
leg = TLegend( 0.12, 0.80, 0.96, 0.89 )
#leg.SetFillColor(4001)
leg.SetLineColor(0)
leg.SetNColumns(2)
leg.SetFillStyle(0)
leg.SetTextSize(0.02)
leg.AddEntry( TT_nowt, "t#bar{t}, no reweighting", "L" )
leg.AddEntry( TT_wt, "t#bar{t}, reweighting", "L" )
leg.Draw()
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.14
CMS_lumi.CMS_lumi(C, 4, 0)    
C.RedrawAxis()
C.SaveAs("outputs/TT_wt.png")
