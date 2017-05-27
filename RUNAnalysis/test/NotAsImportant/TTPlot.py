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

'''
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

leg = TLegend( 0.8, 0.80, 0.96, 0.89 )
#leg.SetFillColor(4001)
leg.SetLineColor(0)
#leg.SetNColumns(2)
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
'''
TT_1 = TH1D( "TT_1", "", 29, 60, 350 )
TT_1.Reset()
TT_2 = TT_1.Clone("TT_2")
TT_3 = TT_1.Clone("TT_3")
TT_4 = TT_1.Clone("TT_4")
TT_5 = TT_1.Clone("TT_5")

scaleArray = {'TopScale': [(-0.7427314755125245, 0.9428324651261439)], 'WJScale': [(-0.6757656878426674, 0.9403926665437488)], '__nll': [-13259.45071148731], 'TTAlphaScale': [(-0.29360622417322, 0.9711899626519114)], 'TTScale': [(-1.1867808817559706, 0.7305627415552938)]}

TopPtWeight1 = "1.06*exp(-0.0005*HT/2)"
TopPtWeight2 = "1.06*(1-.2*1.1867808817559706)*exp(-(0.0005*(1+.2*0.29360622417322))*HT/2)"
TopPtWeight3 = "1.06*exp(-(0.0)*HT/2)"
TopPtWeight4 = "1.06*exp(-(0.01)*HT/2)"
TopPtWeight5 = "1.06*exp(-(0.05)*HT/2)"
#TopPtSF2 = "exp(0.0615-0.0005*genPartPt2)"
#TopPtWeight = "sqrt("+TopPtSF1+"*"+TopPtSF2+")"
#oneTop = "&((jet1Tau32<0.67&jet2Tau32>.67)||(jet1Tau32>0.67&jet2Tau32<.67))"
oneTop = "&((jet1Tau32<0.67&jet2Tau32<.67))"
zerobtag = "&((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484)||(jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
rho = "(log((jet1PrunedMass*jet1PrunedMass)/(jet1Pt*jet1Pt))+log((jet2PrunedMass*jet2PrunedMass)/(jet2Pt*jet2Pt)))"
rhoCut = "(-3>"+rho+"&-5<"+rho+")"
quickplot("80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", TT_1, "prunedMassAve", "jet1Tau21<0.6&jet2Tau21<0.6&deltaEtaDijet<1.0&prunedMassAsym<0.1&"+zerobtag+"&"+oneTop, "lumiWeight*puWeight*36555.21/15*"+TopPtWeight1)
quickplot("80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", TT_2, "prunedMassAve", "jet1Tau21<0.6&jet2Tau21<0.6&deltaEtaDijet<1.0&prunedMassAsym<0.1&"+zerobtag+"&"+oneTop, "lumiWeight*puWeight*36555.21/15*"+TopPtWeight2)
quickplot("80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", TT_3, "prunedMassAve", "jet1Tau21<0.6&jet2Tau21<0.6&deltaEtaDijet<1.0&prunedMassAsym<0.1&"+zerobtag+"&"+oneTop, "lumiWeight*puWeight*36555.21/15*"+TopPtWeight1)
quickplot("80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", TT_4, "prunedMassAve", "jet1Tau21<0.6&jet2Tau21<0.6&deltaEtaDijet<1.0&prunedMassAsym<0.1&"+zerobtag+"&"+oneTop, "lumiWeight*puWeight*36555.21/15*"+TopPtWeight4)
quickplot("80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", TT_5, "prunedMassAve", "jet1Tau21<0.6&jet2Tau21<0.6&deltaEtaDijet<1.0&prunedMassAsym<0.1&"+zerobtag+"&"+oneTop, "lumiWeight*puWeight*36555.21/15*"+TopPtWeight5)

print "Integral 1: " + str(TT_2.Integral())
print "Integral 2: " + str(TT_1.Integral())
TT_1.GetYaxis().SetRangeUser(0,.13)
#TT_1.Scale(1/TT_1.Integral())
#TT_2.Scale(1/TT_2.Integral())
#TT_3.Scale(1/TT_3.Integral())
#TT_4.Scale(1/TT_4.Integral())
#TT_5.Scale(1/TT_5.Integral())
TT_1.SetLineWidth(2)
TT_2.SetLineWidth(2)
TT_3.SetLineWidth(2)
TT_4.SetLineWidth(2)
TT_5.SetLineWidth(2)
TT_1.SetLineColor(kBlack)
TT_3.GetXaxis().SetTitle("Pruned Average Mass [GeV]")
TT_3.GetYaxis().SetTitle("Events / " + str(TT_1.GetBinWidth(1)))
TT_3.SetTitle("")
TT_3.GetYaxis().SetTitleOffset(1.3)
TT_3.GetYaxis().SetLabelSize(0.03)
TT_3.GetXaxis().SetLabelSize(0.03)
TT_3.Draw("hist")
TT_2.SetLineColor(kRed)
TT_3.SetLineColor(kBlue)
TT_4.SetLineColor(kOrange)
TT_5.SetLineColor(kRed)
TT_2.Draw("histsame")
#TT_1.Draw("histsame")
#TT_4.Draw("histsame")
#TT_5.Draw("histsame")
#FindAndSetMax( [TT_1, TT_2, TT_3, TT_4, TT_5 ], False )
leg = TLegend( 0.60, 0.60, 0.96, 0.89 )
#leg.SetFillColor(4001)
leg.SetLineColor(0)
#leg.SetNColumns(2)
leg.SetFillStyle(0)
#leg.SetTextSize(0.02)
leg.AddEntry( TT_3, "Before Theta", "L" )
leg.AddEntry( TT_2, "After Theta", "L" )
#leg.AddEntry( TT_1, "#alpha = 0.005", "L" )
#leg.AddEntry( TT_4, "#alpha = 0.01", "L" )
#leg.AddEntry( TT_5, "#alpha = 0.05", "L" )
leg.Draw()
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.14
CMS_lumi.CMS_lumi(C, 4, 0)    
C.RedrawAxis()
C.SaveAs("outputs/TT_2.png")
