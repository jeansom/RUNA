#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
from ROOT import TF1
import scipy
from RUNA.RUNAnalysis.Plotting_Header import *
gStyle.SetOptStat(0)
gStyle.SetOptFit(False)

GCHSG = TFile.Open( "outputs/33117/PuppiSoftDrop/15_80X_NPVG20CSVv2M_Before_CBDMC/MasspresprunedMassAveEst.root" ).Get("Graph")
GCHSL = TFile.Open( "outputs/33117/PuppiSoftDrop/14_80X_NPVL20CSVv2M_Before_CBDMC/MasspresprunedMassAveEst.root" ).Get("Graph")
GPUPPIG = TFile.Open( "outputs/33117/PuppiSoftDrop/15_80X_NPVG20_PuppiCSVv2M_Before_CBDMC/MasspresprunedMassAveEst.root" ).Get("Graph")
GPUPPIL = TFile.Open( "outputs/33117/PuppiSoftDrop/14_80X_NPVL20_PuppiCSVv2M_Before_CBDMC/MasspresprunedMassAveEst.root" ).Get("Graph")

GCHSG.SetLineColor(kBlue)
GCHSL.SetLineColor(kCyan)
GPUPPIG.SetLineColor(kRed)
GPUPPIL.SetLineColor(kRed+3)

C = TCanvas("C","",800,800)
P = TPad( "P", "", 0, 0.1, 1, 1 )
L = TPad( "L", "", 0, 0, 1, 0.1 )
P.Draw()
#P.SetBottomMargin(0)
L.Draw()
L.SetTopMargin(0)
P.cd()
GCHSG.GetXaxis().SetRangeUser(-6,0)
GCHSL.GetXaxis().SetRangeUser(-6,0)
GPUPPIG.GetXaxis().SetRangeUser(-6,0)
GPUPPIL.GetXaxis().SetRangeUser(-6,0)
GCHSG.Draw("APC")
GCHSL.Draw("samePC")
GPUPPIG.Draw("samePC")
GPUPPIL.Draw("samePC")

L.cd()
L.Draw()
legend = TLegend( 0,0,1,1 )
legend.AddEntry( GCHSG, "CHS+Pruned B/D, NPV>20, pT binned QCD", "PL" )
legend.AddEntry( GCHSL, "CHS+Pruned B/D, NPV<20, pT binned QCD", "PL" )
legend.AddEntry( GPUPPIG, "PuPPI+Soft Drop B/D, NPV>20, pT binned QCD", "PL" )
legend.AddEntry( GPUPPIL, "PuPPI+Soft Drop B/D, NPV<20, pT binned QCD", "PL" )

legend.SetNColumns(2)
legend.Draw()

C.SaveAs("TCutPlots/GNPV.png")
