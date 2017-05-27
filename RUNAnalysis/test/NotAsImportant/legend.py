#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

C = TCanvas("C","",800,800)
leg = TLegend(.11,.11,.89,.89)
leg.SetTextSize(0.03)
leg.SetLineColor(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)

N1=TH1F()
N1.SetFillColor(kAzure-4)
N1.SetLineColor(kBlack)
hists_SIG = []
hists_SIG.append(TH1F())
hists_SIG.append(TH1F())
hists_SIG.append(TH1F())
hists_SIG.append(TH1F())
#for i in xrange(len(hists_SIG)):
#    if i%2==0:
#        hists_SIG[i].SetLineColor(kViolet+4)
#    else:
#        hists_SIG[i].SetLineColor(kGray+3)
#    hists_SIG[i].SetLineWidth(3)
#    hists_SIG[i].SetFillColorAlpha(kGray+3, 0.5)
#    hists_SIG[i].SetFillStyle(3454)
hists_SIG[0].SetFillColorAlpha(kGray+3,0.5)
hists_SIG[0].SetLineColor(kViolet+4)
hists_SIG[0].SetLineWidth(6)
hists_SIG[0].SetFillStyle(3454)
hists_SIG[1].SetFillColorAlpha(kGray+3,0.5)
hists_SIG[1].SetLineColor(14)
hists_SIG[1].SetLineWidth(6)
hists_SIG[1].SetFillStyle(3454)
hists_SIG[2].SetFillColorAlpha(kGray+3,0.5)
hists_SIG[2].SetLineColor(kBlue-4)
hists_SIG[2].SetLineWidth(6)
hists_SIG[2].SetFillStyle(3445)
hists_SIG[3].SetFillColorAlpha(kGray+3,0.5)
hists_SIG[3].SetLineColor(12)
hists_SIG[3].SetLineWidth(6)
hists_SIG[3].SetFillStyle(3445)

V = TH1F()
V.SetLineColor(kBlack)
V.SetMarkerColor(1)
V.SetMarkerStyle(20)
hists_MSR_SUB = []
hists_MSR_SUB.append(TH1F())
hists_MSR_SUB.append(TH1F())
hists_MSR_SUB.append(TH1F())
hists_MSR_SUB[0].SetFillColor(6)
hists_MSR_SUB[0].SetLineColor(1)
hists_MSR_SUB[0].SetLineWidth(1)
hists_MSR_SUB[1].SetFillColor(8)
hists_MSR_SUB[1].SetLineColor(1)
hists_MSR_SUB[1].SetLineWidth(1)
hists_MSR_SUB[2].SetFillColor(2)        
hists_MSR_SUB[2].SetLineColor(1)
hists_MSR_SUB[2].SetLineWidth(1)
Boxes = [] # Errors on estimation
sBoxes = [] # Systematic errors on estimation
tempbox = TBox(0,0,1,1)
tempsbox = TBox(0,0,1,1)
Boxes.append(tempbox)
sBoxes.append(tempsbox)
for i in Boxes:
    i.SetFillColor(12)
    i.SetFillStyle(3244)
for i in sBoxes:
    i.SetFillColor(12)
    i.SetFillStyle(3002)

leg.AddEntry(V, "Data", "PL")
leg.AddEntry( N1, "QCD", "F")
leg.AddEntry( hists_MSR_SUB[2], "t #bar{t} + Jets", "F")
leg.AddEntry( hists_MSR_SUB[1], "W + Jets", "F")
leg.AddEntry( hists_MSR_SUB[0], "Single Top", "F")
#leg.AddEntry(Boxes[0], "total uncertainty", "F")
#leg.AddEntry(sBoxes[0], "bkg statistical component", "F")
leg.AddEntry( hists_SIG[0], "RPV Stop UDD323 M-120, 100 pb", "F")
leg.AddEntry( hists_SIG[1], "RPV Stop UDD323 M-180, 100 pb", "F")
leg.AddEntry( hists_SIG[2], "RPV Stop UDD323 M-240, 100 pb", "F")
leg.AddEntry( hists_SIG[3], "RPV Stop UDD323 M-280, 100 pb", "F")

leg.Draw()
C.SaveAs("TCutPlots/legend.png")
