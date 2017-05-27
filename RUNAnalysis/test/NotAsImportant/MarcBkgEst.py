import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

import RUNA.RUNAnalysis.Plotting_Header
from RUNA.RUNAnalysis.Plotting_Header import *

import RUNA.RUNAnalysis.scaleFactors
from RUNA.RUNAnalysis.scaleFactors import *


def Make2DPlotOfQCD(H, Cuts, VarX, VarY):
    T = "BoostedAnalysisPlotsPuppi/RUNATree"
    qcdfilestring = "v08/RUNAnalysis_QCDPt"
    qcdfileend = "_80X_V2p4_v08.root"
    qcdfiles = [
        "All",
        ]
    for i in qcdfiles:
        quick2dplot(qcdfilestring+i+qcdfileend, T, H, VarX, VarY, Cuts, "36555.21/15*.62*puWeight*lumiWeight")

def GetABCDCorr(Cut, N):
    H = TH2F("H"+N, "", 50, 0, 1, 50, 0, 5)
    Make2DPlotOfQCD(H, Cut, "prunedMassAsym", "deltaEtaDijet")
    Ax1 = H.GetXaxis().FindBin(0.)
    Ax2 = H.GetXaxis().FindBin(0.099999)
    Ay1 = H.GetYaxis().FindBin(0.)
    Ay2 = H.GetYaxis().FindBin(1.4999999)
    Bx1 = H.GetXaxis().FindBin(0.)
    Bx2 = H.GetXaxis().FindBin(0.0999999)
    By1 = H.GetYaxis().FindBin(1.4999999)
    By2 = H.GetYaxis().FindBin(5.)
    Cx1 = H.GetXaxis().FindBin(0.0999999)
    Cx2 = H.GetXaxis().FindBin(1.)
    Cy1 = H.GetYaxis().FindBin(0.)
    Cy2 = H.GetYaxis().FindBin(1.499999)
    Dx1 = H.GetXaxis().FindBin(0.099999)
    Dx2 = H.GetXaxis().FindBin(1.)
    Dy1 = H.GetYaxis().FindBin(1.499999)
    Dy2 = H.GetYaxis().FindBin(5.)
    A = H.Integral(Ax1,Ax2,Ay1,Ay2)
    B = H.Integral(Bx1,Bx2,By1,By2)
    C = H.Integral(Cx1,Cx2,Cy1,Cy2)
    D = H.Integral(Dx1,Dx2,Dy1,Dy2)
    return [A, B, C, D]

QCD = TH1F("qcd_", "", 25, 50, 300)
QCD.SetStats(0)
QCD.SetFillStyle(3013)
QCD.SetFillColor(38)
QCD.SetLineColor(38)
QCD.GetXaxis().SetTitle("pruned mass average (GeV)")
QCD.GetYaxis().SetTitle("events")
QCD.GetXaxis().SetTitleOffset(1.3)
QCD.GetYaxis().SetTitleOffset(1.365)

TRUTH = TH1F("est_", "", 25, 50, 300)
TRUTH.SetLineColor(1)
TRUTH.SetFillColor(0)
TRUTH.SetMarkerColor(1)
TRUTH.SetMarkerStyle(20)

Bins = []
BinnedTF = []

for i in range(0,25):
    binstart = str(50+(i*10))
    binend = str(50+((i+1)*10))
    Cuts = "prunedMassAve>"+binstart+"&prunedMassAve<"+binend+"&jet1Tau21<0.45&jet2Tau21<0.45"
    TF = GetABCDCorr(Cuts, binstart)
    print " --- " + binstart + " to " + binend + " ---"
    TRUTH.Fill(55 + i*10, TF[0])
    QCD.Fill(55 + i*10, TF[2]*(TF[1]/TF[3]))
    Bins.append(55. + i*10.)
    BinnedTF.append(TF[1]/TF[3])

G = TGraph(len(Bins), scipy.array(Bins), scipy.array(BinnedTF))

FindAndSetMax([QCD, TRUTH])
C = TCanvas("C", "", 650, 650)
C.cd()
QCD.Draw("hist")
TRUTH.Sumw2()
TRUTH.Draw("e0 same")
C.Print("CLOSURE_result.png")

C2 = TCanvas("C2", "", 650, 650)
C2.cd()
G.Draw("AC")
C2.Print("CLOSURE_TF.png")



