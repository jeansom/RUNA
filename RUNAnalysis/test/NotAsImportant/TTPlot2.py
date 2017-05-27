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

#not1
scaleTT = 0.5320057340507436
scaleTTErr = 0.5951743976448869
scaleAlpha = 0.21453961072229255
scaleAlphaErr = 0.9876010610787747

TTNorm = "( (1.06)*(1+.2*"+str(scaleTT)+"))" # The scale that determines the nominal TTBar normalization
TTNormUp = "( (1.06)*(1+.2*" + str(scaleTT) + "+.2*" + str(scaleTTErr) + ") )" # Upper TTBar normalization
TTNormDn = "( (1.06)*(1+.2*" + str(scaleTT) + "-.2*" + str(scaleTTErr) + ") )" # Lower TTBar normalization

TTAlpha = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + ") )" # The scale that determines the nominal alpha NOTE: subtracting = adding because -0.0005
TTAlphaUp = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "-.2*" + str(scaleAlphaErr) + ") )" # Upper alpha NOTE: subtracting = adding because -0.0005
TTAlphaDn = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "+.2*" + str(scaleAlphaErr) + ") )" # Lower alpha NOTE: subtracting = adding because -0.0005

TTScaleStr = "(" + TTNorm + "*" + TTAlpha + ")" # Total string to scale TT by, norm*alpha
TTScaleErrUpStr = "(" + TTNormUp + "*" + TTAlphaUp + ")" # String for scaling TT with norm up, normUp*alpha
TTScaleErrDnStr = "(" + TTNormDn + "*" + TTAlphaDn + ")" # String for scaling TT with norm dn, normDn*alpha
AlphaScaleUpStr = "(" + TTNorm + "*" + TTAlphaUp + ")" # Total string to scale TT by with alpha up, norm*alphaUp
AlphaScaleDnStr = "(" + TTNorm + "*" + TTAlphaDn + ")" # Total string to scale TT by with alpha dn, norm*alphaDn

PlotsTTnot1 = TH1F("Nomnot1", "", 29, 60, 350 )
PlotsTTUpnot1 = TH1F("Upnot1", "", 29, 60, 350 )
PlotsTTDnnot1 = TH1F("Dnnot1", "", 29, 60, 350 )

#cuts = "jet1Tau21<0.60&jet2Tau21<0.60&prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1btagCSVv2>0.800&jet2btagCSVv2>0.800&jet1Tau32>0.51&jet2Tau32>0.51"
cuts = "jet1Tau21<0.60&jet2Tau21<0.60&prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1btagCSVv2>0.800&jet2btagCSVv2>0.800&jet1Tau32<0.51&jet2Tau32<0.51"

PlotsDATA = TH1F("Nom", "", 29, 60, 350 )
quickplot("RootFiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsDATA, "prunedMassAve", cuts, "1" )

#not1
scaleW = -0.5173549554281323
scaleWErr = 0.846699757449402

WScaleStr = "(1+.2*"+str(scaleW)+")" # The scale that determines the nominal W normalization
WScaleUpStr = "(1+.2*"+str(scaleW)+"+.2*"+str(scaleWErr)+")" # Upper W normalization
WScaleDnStr = "(1+.2*"+str(scaleW)+"-.2*"+str(scaleWErr)+")" # Lower W normalization

PlotsWnot1 = TH1F("Nomnot1W", "", 29, 60, 350 )
PlotsWUpnot1 = TH1F("Upnot1W", "", 29, 60, 350 )
PlotsWDnnot1 = TH1F("Dnnot1W", "", 29, 60, 350 )

quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWnot1, "prunedMassAsym", cuts, "lumiWeight*puWeight*2666*"+WScaleStr )
quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWUpnot1, "prunedMassAsym", cuts, "lumiWeight*puWeight*2666*"+WScaleUpStr )
quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWDnnot1, "prunedMassAsym", cuts, "lumiWeight*puWeight*2666*"+WScaleDnStr )

quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTTnot1, "prunedMassAve", cuts, "lumiWeight*puWeight*2666*"+TTScaleStr)
quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTTUpnot1, "prunedMassAve", cuts, "lumiWeight*puWeight*2666*"+TTScaleErrUpStr)
quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTTDnnot1, "prunedMassAve", cuts, "lumiWeight*puWeight*2666*"+TTScaleErrDnStr)

PlotsTTnot1.SetLineColor(kBlue)
PlotsTTUpnot1.SetLineColor(kBlue)
PlotsTTDnnot1.SetLineColor(kBlue)

PlotsTTnot1.SetLineWidth(2)
PlotsTTUpnot1.SetLineWidth(2)
PlotsTTDnnot1.SetLineWidth(2)

PlotsTTUpnot1.SetLineStyle(2)
PlotsTTDnnot1.SetLineStyle(2)

#t1or2
scaleTT = 0.4229557215949402
scaleTTErr = 0.7034626331063345
scaleAlpha = 0.48407728506571246
scaleAlphaErr = 0.8990781789954703

TTNorm = "( (1.06)*(1+.2*"+str(scaleTT)+"))" # The scale that determines the nominal TTBar normalization
TTNormUp = "( (1.06)*(1+.2*" + str(scaleTT) + "+.2*" + str(scaleTTErr) + ") )" # Upper TTBar normalization
TTNormDn = "( (1.06)*(1+.2*" + str(scaleTT) + "-.2*" + str(scaleTTErr) + ") )" # Lower TTBar normalization

TTAlpha = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + ") )" # The scale that determines the nominal alpha NOTE: subtracting = adding because -0.0005
TTAlphaUp = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "-.2*" + str(scaleAlphaErr) + ") )" # Upper alpha NOTE: subtracting = adding because -0.0005
TTAlphaDn = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "+.2*" + str(scaleAlphaErr) + ") )" # Lower alpha NOTE: subtracting = adding because -0.0005

TTScaleStr = "(" + TTNorm + "*" + TTAlpha + ")" # Total string to scale TT by, norm*alpha
TTScaleErrUpStr = "(" + TTNormUp + "*" + TTAlpha + ")" # String for scaling TT with norm up, normUp*alpha
TTScaleErrDnStr = "(" + TTNormDn + "*" + TTAlpha + ")" # String for scaling TT with norm dn, normDn*alpha
AlphaScaleUpStr = "(" + TTNorm + "*" + TTAlphaUp + ")" # Total string to scale TT by with alpha up, norm*alphaUp
AlphaScaleDnStr = "(" + TTNorm + "*" + TTAlphaDn + ")" # Total string to scale TT by with alpha dn, norm*alphaDn

PlotsTTt1or2 = TH1F("Nomt1or2", "", 29, 60, 350 )
PlotsTTUpt1or2 = TH1F("Upt1or2", "", 29, 60, 350 )
PlotsTTDnt1or2 = TH1F("Dnt1or2", "", 29, 60, 350 )

#t1or2
scaleW = -0.6669036320440132
scaleWErr = 0.8375321845733996

WScaleStr = "(1+.2*"+str(scaleW)+")" # The scale that determines the nominal W normalization
WScaleUpStr = "(1+.2*"+str(scaleW)+"+.2*"+str(scaleWErr)+")" # Upper W normalization
WScaleDnStr = "(1+.2*"+str(scaleW)+"-.2*"+str(scaleWErr)+")" # Lower W normalization

PlotsWt1or2 = TH1F("Nomt1or2W", "", 29, 60, 350 )
PlotsWUpt1or2 = TH1F("Upt1or2W", "", 29, 60, 350 )
PlotsWDnt1or2 = TH1F("Dnt1or2W", "", 29, 60, 350 )

quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWt1or2, "prunedMassAsym", cuts, "lumiWeight*puWeight*2666*"+WScaleStr )
quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWUpt1or2, "prunedMassAsym", cuts, "lumiWeight*puWeight*2666*"+WScaleUpStr )
quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWDnt1or2, "prunedMassAsym", cuts, "lumiWeight*puWeight*2666*"+WScaleDnStr )

quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTTt1or2, "prunedMassAve", cuts, "lumiWeight*puWeight*2666*"+TTScaleStr)
quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTTUpt1or2, "prunedMassAve", cuts, "lumiWeight*puWeight*2666*"+TTScaleErrUpStr)
quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTTDnt1or2, "prunedMassAve", cuts, "lumiWeight*puWeight*2666*"+TTScaleErrDnStr)

PlotsTTt1or2.SetLineColor(kRed)
PlotsTTUpt1or2.SetLineColor(kRed)
PlotsTTDnt1or2.SetLineColor(kRed)

PlotsTTt1or2.SetLineWidth(2)
PlotsTTUpt1or2.SetLineWidth(2)
PlotsTTDnt1or2.SetLineWidth(2)

PlotsTTUpt1or2.SetLineStyle(2)
PlotsTTDnt1or2.SetLineStyle(2)

#11reg
scaleTT = 0.4605362349315474
scaleTTErr = 0.5116115744868042
scaleAlpha = 0.14975059785032485
scaleAlphaErr = 0.9816886681742449

TTNorm = "( (1.06)*(1+.2*"+str(scaleTT)+"))" # The scale that determines the nominal TTBar normalization
TTNormUp = "( (1.06)*(1+.2*" + str(scaleTT) + "+.2*" + str(scaleTTErr) + ") )" # Upper TTBar normalization
TTNormDn = "( (1.06)*(1+.2*" + str(scaleTT) + "-.2*" + str(scaleTTErr) + ") )" # Lower TTBar normalization

TTAlpha = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + ") )" # The scale that determines the nominal alpha NOTE: subtracting = adding because -0.0005
TTAlphaUp = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "-.2*" + str(scaleAlphaErr) + ") )" # Upper alpha NOTE: subtracting = adding because -0.0005
TTAlphaDn = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "+.2*" + str(scaleAlphaErr) + ") )" # Lower alpha NOTE: subtracting = adding because -0.0005

TTScaleStr = "(" + TTNorm + "*" + TTAlpha + ")" # Total string to scale TT by, norm*alpha
TTScaleErrUpStr = "(" + TTNormUp + "*" + TTAlpha + ")" # String for scaling TT with norm up, normUp*alpha
TTScaleErrDnStr = "(" + TTNormDn + "*" + TTAlpha + ")" # String for scaling TT with norm dn, normDn*alpha
AlphaScaleUpStr = "(" + TTNorm + "*" + TTAlphaUp + ")" # Total string to scale TT by with alpha up, norm*alphaUp
AlphaScaleDnStr = "(" + TTNorm + "*" + TTAlphaDn + ")" # Total string to scale TT by with alpha dn, norm*alphaDn

PlotsTT11reg = TH1F("Nom11reg", "", 29, 60, 350 )
PlotsTTUp11reg = TH1F("Up11reg", "", 29, 60, 350 )
PlotsTTDn11reg = TH1F("Dn11reg", "", 29, 60, 350 )

#11reg
scaleW = -0.7843545751297061
scaleWErr = 0.8272868942461518

WScaleStr = "(1+.2*"+str(scaleW)+")" # The scale that determines the nominal W normalization
WScaleUpStr = "(1+.2*"+str(scaleW)+"+.2*"+str(scaleWErr)+")" # Upper W normalization
WScaleDnStr = "(1+.2*"+str(scaleW)+"-.2*"+str(scaleWErr)+")" # Lower W normalization

PlotsW11reg = TH1F("Nom11regW", "", 29, 60, 350 )
PlotsWUp11reg = TH1F("Up11regW", "", 29, 60, 350 )
PlotsWDn11reg = TH1F("Dn11regW", "", 29, 60, 350 )

quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsW11reg, "prunedMassAsym", cuts, "lumiWeight*puWeight*2666*"+WScaleStr )
quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWUp11reg, "prunedMassAsym", cuts, "lumiWeight*puWeight*2666*"+WScaleUpStr )
quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWDn11reg, "prunedMassAsym", cuts, "lumiWeight*puWeight*2666*"+WScaleDnStr )

quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTT11reg, "prunedMassAve", cuts, "lumiWeight*puWeight*2666*"+TTScaleStr)
quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTTUp11reg, "prunedMassAve", cuts, "lumiWeight*puWeight*2666*"+TTScaleErrUpStr)
quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTTDn11reg, "prunedMassAve", cuts, "lumiWeight*puWeight*2666*"+TTScaleErrDnStr)

PlotsTT11reg.SetLineColor(kViolet)
PlotsTTUp11reg.SetLineColor(kViolet)
PlotsTTDn11reg.SetLineColor(kViolet)

PlotsTT11reg.SetLineWidth(2)
PlotsTTUp11reg.SetLineWidth(2)
PlotsTTDn11reg.SetLineWidth(2)

PlotsTTUp11reg.SetLineStyle(2)
PlotsTTDn11reg.SetLineStyle(2)


PlotsTT11reg.Sumw2()
PlotsTTUp11reg.Sumw2()
PlotsTTDn11reg.Sumw2()
PlotsTTt1or2.Sumw2()
PlotsTTUpt1or2.Sumw2()
PlotsTTDnt1or2.Sumw2()
PlotsTTnot1.Sumw2()
PlotsTTUpnot1.Sumw2()
PlotsTTDnnot1.Sumw2()
PlotsW11reg.Sumw2()
PlotsWUp11reg.Sumw2()
PlotsWDn11reg.Sumw2()
PlotsWt1or2.Sumw2()
PlotsWUpt1or2.Sumw2()
PlotsWDnt1or2.Sumw2()
PlotsWnot1.Sumw2()
PlotsWUpnot1.Sumw2()
PlotsWDnnot1.Sumw2()

PlotsTT11reg.Add(PlotsW11reg)
PlotsTTUp11reg.Add(PlotsWUp11reg)
PlotsTTDn11reg.Add(PlotsWDn11reg)
PlotsTTt1or2.Add(PlotsWt1or2)
PlotsTTUpt1or2.Add(PlotsWUpt1or2)
PlotsTTDnt1or2.Add(PlotsWDnt1or2)
PlotsTTnot1.Add(PlotsWnot1)
PlotsTTUpnot1.Add(PlotsWUpnot1)
PlotsTTDnnot1.Add(PlotsWDnnot1)

FindAndSetMax( [PlotsTT11reg, PlotsTTUp11reg, PlotsTTDn11reg, PlotsTTnot1, PlotsTTUpnot1, PlotsTTDnnot1, PlotsTTUpt1or2, PlotsTTDnt1or2, PlotsTTt1or2, PlotsDATA], False )

PlotsTT11reg.Draw("hist")
PlotsTTUp11reg.Draw("histsame")
PlotsTTDn11reg.Draw("histsame")
PlotsTTt1or2.Draw("histsame")
PlotsTTUpt1or2.Draw("histsame")
PlotsTTDnt1or2.Draw("histsame")
PlotsTTnot1.Draw("histsame")
PlotsTTUpnot1.Draw("histsame")
PlotsTTDnnot1.Draw("histsame")

PlotsDATA.SetLineColor(1)
PlotsDATA.SetMarkerColor(1)
PlotsDATA.SetMarkerStyle(20)
PlotsDATA.Draw("sameE0")

leg = TLegend(0.13, 0.80, 0.95, 0.89)
leg.SetNColumns(3)
leg.SetTextSize(0.03)
leg.SetFillStyle(0)
leg.SetLineColor(0)
leg.SetFillColor(4001)
leg.AddEntry(PlotsTT11reg, "All 11 Reg", "L")
leg.AddEntry(PlotsTTt1or2, "1 or 2 Top Reg", "L")
leg.AddEntry(PlotsTTnot1, "No 1 Top Reg", "L")
leg.AddEntry(PlotsDATA, "Data", "PL")
leg.Draw("same")

C.SaveAs("TCutPlots/TTPlot_CSVCBD_b2t2.png")
