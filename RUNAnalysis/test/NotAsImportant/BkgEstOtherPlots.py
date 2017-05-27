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

#TT Plot

C = TCanvas( "C", "", 800, 800 )
plotPad = TPad("plotPad", "", 0, 0.10, 1, 1)
legPad = TPad("legPad", "", 0, 0, 1, 0.10 )
plotPad.Draw()
legPad.Draw()
plotPad.cd()
plotPad.Divide(3,3)

FILE = TFile.Open("outputs/51417/NJets/LIM_FEED.root")
chans = [ "b0t0", "b0t2", "b0t2", "b1t0", "b1t1", "b1t2", "b2t0", "b2t1", "b2t2" ]
TTNom = []
TTUp = []
TTDn = []
TTAUp = []
TTADn = []

for i in xrange(len(chans)):
    plotPad.cd(i+1)

    TTNom.append(FILE.Get(chans[i]+"__TTBAR"))
    TTNom[-1].SetLineColor(kRed)

    TTNom[-1].GetXaxis().SetTitle("Average Mass")
    TTNom[-1].GetYaxis().SetTitle("Events")
    TTNom[-1].SetTitle(chans[i])

    TTUp.append(FILE.Get(chans[i]+"__TTBAR__TTScale__up"))
    TTUp[-1].SetLineColor(kRed)
    TTUp[-1].SetLineStyle(2)

    TTDn.append(FILE.Get(chans[i]+"__TTBAR__TTScale__down"))
    TTDn[-1].SetLineColor(kRed)
    TTDn[-1].SetLineStyle(2)

    TTAUp.append(FILE.Get(chans[i]+"__TTBAR__TTAlphaScale__up"))
    TTAUp[-1].SetLineColor(kBlue)
    TTAUp[-1].SetLineStyle(3)

    TTADn.append(FILE.Get(chans[i]+"__TTBAR__TTAlphaScale__down"))
    TTADn[-1].SetLineColor(kBlue)
    TTADn[-1].SetLineStyle(3)

    FindAndSetMax( [TTNom[-1], TTUp[-1], TTDn[-1], TTAUp[-1], TTADn[-1]], False )

    TTNom[-1].Draw("hist")
    TTUp[-1].Draw("histsame")
    TTDn[-1].Draw("histsame")
    TTAUp[-1].Draw("histsame")
    TTADn[-1].Draw("histsame")

legPad.cd()
leg = TLegend(0.11,0.11,0.89,0.89)
leg.SetNColumns(3)
leg.AddEntry(TTNom[-1], "Nominal", "L")
leg.AddEntry(TTUp[-1], "Normalization #pm 50%", "L")
leg.AddEntry(TTAUp[-1], "Alpha #pm 50%", "L")
leg.Draw()

C.Print("TCutPlots/TTChange.png")

#W Plot

C = TCanvas( "C", "", 800, 800 )
plotPad = TPad("plotPad", "", 0, 0.10, 1, 1)
legPad = TPad("legPad", "", 0, 0, 1, 0.10 )
plotPad.Draw()
legPad.Draw()
plotPad.cd()
plotPad.Divide(3,3)

FILE = TFile.Open("outputs/51417/NJets/LIM_FEED.root")
chans = [ "b0t0", "b0t2", "b0t2", "b1t0", "b1t1", "b1t2", "b2t0", "b2t1", "b2t2" ]
WJNom = []
WJUp = []
WJDn = []

for i in xrange(len(chans)):
    plotPad.cd(i+1)

    WJNom.append(FILE.Get(chans[i]+"__WJETS"))
    WJNom[-1].SetLineColor(kRed)

    WJNom[-1].GetXaxis().SetTitle("Average Mass")
    WJNom[-1].GetYaxis().SetTitle("Events")
    WJNom[-1].SetTitle(chans[i])

    WJUp.append(FILE.Get(chans[i]+"__WJETS__WJScale__up"))
    WJUp[-1].SetLineColor(kRed)
    WJUp[-1].SetLineStyle(2)

    WJDn.append(FILE.Get(chans[i]+"__WJETS__WJScale__down"))
    WJDn[-1].SetLineColor(kRed)
    WJDn[-1].SetLineStyle(2)

    FindAndSetMax( [WJNom[-1], WJUp[-1], WJDn[-1] ], False )

    WJNom[-1].Draw("hist")
    WJUp[-1].Draw("histsame")
    WJDn[-1].Draw("histsame")

legPad.cd()
leg = TLegend(0.11,0.11,0.89,0.89)
leg.SetNColumns(3)
leg.AddEntry(WJNom[-1], "Nominal", "L")
leg.AddEntry(WJUp[-1], "Normalization #pm 50%", "L")
leg.Draw()

C.Print("TCutPlots/WJChange.png")

#QCD TT Plot

C = TCanvas( "C", "", 800, 800 )
plotPad = TPad("plotPad", "", 0, 0.10, 1, 1)
legPad = TPad("legPad", "", 0, 0, 1, 0.10 )
plotPad.Draw()
legPad.Draw()
plotPad.cd()
plotPad.Divide(3,3)

FILE = TFile.Open("outputs/51417/NJets/LIM_FEED.root")
chans = [ "b0t0", "b0t2", "b0t2", "b1t0", "b1t1", "b1t2", "b2t0", "b2t1", "b2t2" ]
QCDNom = []
QCDUp = []
QCDDn = []
QCDAUp = []
QCDADn = []

for i in xrange(len(chans)):
    plotPad.cd(i+1)

    QCDNom.append(FILE.Get(chans[i]+"__QCD"))
    QCDNom[-1].SetLineColor(kRed)

    QCDNom[-1].GetXaxis().SetTitle("Average Mass")
    QCDNom[-1].GetYaxis().SetTitle("Events")
    QCDNom[-1].SetTitle(chans[i])

    QCDUp.append(FILE.Get(chans[i]+"__QCD__TTScale__up"))
    QCDUp[-1].SetLineColor(kRed)
    QCDUp[-1].SetLineStyle(2)

    QCDDn.append(FILE.Get(chans[i]+"__QCD__TTScale__down"))
    QCDDn[-1].SetLineColor(kRed)
    QCDDn[-1].SetLineStyle(2)

    QCDAUp.append(FILE.Get(chans[i]+"__QCD__TTAlphaScale__up"))
    QCDAUp[-1].SetLineColor(kBlue)
    QCDAUp[-1].SetLineStyle(3)

    QCDADn.append(FILE.Get(chans[i]+"__QCD__TTAlphaScale__down"))
    QCDADn[-1].SetLineColor(kBlue)
    QCDADn[-1].SetLineStyle(3)

    FindAndSetMax( [QCDNom[-1], QCDUp[-1], QCDDn[-1], QCDAUp[-1], QCDADn[-1]], False )

    QCDNom[-1].Draw("hist")
    QCDUp[-1].Draw("histsame")
    QCDDn[-1].Draw("histsame")
    QCDAUp[-1].Draw("histsame")
    QCDADn[-1].Draw("histsame")

legPad.cd()
leg = TLegend(0.11,0.11,0.89,0.89)
leg.SetNColumns(3)
leg.AddEntry(QCDNom[-1], "Nominal t#bar{t}", "L")
leg.AddEntry(QCDUp[-1], "t#bar{t} normalization #pm 50%", "L")
leg.AddEntry(QCDAUp[-1], "t#bar{t} alpha #pm 50%", "L")
leg.Draw()

C.Print("TCutPlots/QCDTTChange.png")

#QCD WJ Plot

C = TCanvas( "C", "", 800, 800 )
plotPad = TPad("plotPad", "", 0, 0.10, 1, 1)
legPad = TPad("legPad", "", 0, 0, 1, 0.10 )
plotPad.Draw()
legPad.Draw()
plotPad.cd()
plotPad.Divide(3,3)

FILE = TFile.Open("outputs/51417/NJets/LIM_FEED.root")
chans = [ "b0t0", "b0t2", "b0t2", "b1t0", "b1t1", "b1t2", "b2t0", "b2t1", "b2t2" ]
QCDNom = []
QCDUp = []
QCDDn = []

for i in xrange(len(chans)):
    plotPad.cd(i+1)

    QCDNom.append(FILE.Get(chans[i]+"__QCD"))
    QCDNom[-1].SetLineColor(kRed)

    QCDNom[-1].GetXaxis().SetTitle("Average Mass")
    QCDNom[-1].GetYaxis().SetTitle("Events")
    QCDNom[-1].SetTitle(chans[i])

    QCDUp.append(FILE.Get(chans[i]+"__QCD__WJScale__up"))
    QCDUp[-1].SetLineColor(kRed)
    QCDUp[-1].SetLineStyle(2)

    QCDDn.append(FILE.Get(chans[i]+"__QCD__WJScale__down"))
    QCDDn[-1].SetLineColor(kRed)
    QCDDn[-1].SetLineStyle(2)

    FindAndSetMax( [QCDNom[-1], QCDUp[-1], QCDDn[-1]], False )

    QCDNom[-1].Draw("hist")
    QCDUp[-1].Draw("histsame")
    QCDDn[-1].Draw("histsame")

legPad.cd()
leg = TLegend(0.11,0.11,0.89,0.89)
leg.SetNColumns(3)
leg.AddEntry(QCDNom[-1], "Nominal W + Jets", "L")
leg.AddEntry(QCDUp[-1], "W + Jets normalization #pm 50%", "L")
leg.Draw()

C.Print("TCutPlots/QCDWJChange.png")
