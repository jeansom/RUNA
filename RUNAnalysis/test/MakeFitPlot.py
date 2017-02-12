#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy
from RUNA.RUNAnalysis.Plotting_Header import *
gStyle.SetOptStat(0)
gStyle.SetOptFit(False)
FILE = []
#for bt in [ "b0t0", "b0t1", "b0t2", "b1t0", "b1t1", "b1t2", "b2t0", "b2t1", "b2t2" ]:
for bt in [ "b0t0", "b0t1", "b1t0", "b1t1", "b2t0" ]:
    FILE.append(TFile.Open( "LIM_FIT/LIM_FIT"+bt+".root" ))

G = []
Fit = []
Fit_up = []
Fit_dn = []

n=0
#for bt in [ "b0t0", "b0t1", "b0t2", "b1t0", "b1t1", "b1t2", "b2t0", "b2t1" ]:
for bt in [ "b0t0", "b0t1", "b1t0", "b1t1", "b2t0" ]:
    G.append( FILE[n].Get("G_"+bt) )
    Fit.append( FILE[n].Get("Fit_"+bt) )
    Fit_up.append( FILE[n].Get( "FitUp_"+bt ) )
    Fit_dn.append( FILE[n].Get( "FitDn_"+bt ) )
    n=n+1
'''
mh=0
ml = 100
for n in xrange(6):
    h = ROOT.TMath.MaxElement(9,G[n].GetY());
    if h > mh: mh = h
    l = ROOT.TMath.MinElement(9,G[n].GetY());
    if l < ml: ml = l
for n in xrange(6):
    G[n].GetYaxis().SetRangeUser(ml*(1-.35), mh*1.35)
'''
C = TCanvas( "C", "", 800, 800 )
P = TPad( "P", "", 0, 0.05, 1, 1 )
L = TPad( "L", "", 0, 0, 1, 0.1 )

P.Draw()
L.Draw()

P.cd()

n=0
gr = TMultiGraph()
g1 = TMultiGraph()
gr.SetMaximum(1.75)
g1.SetMaximum(1.75)
#for i in  [ kRed, kMagenta, kBlue, kCyan, kGreen, kRed+3, kMagenta+3, kBlue+3, kCyan+3 ]:
for i in  [ kRed, kBlue, kRed, kBlue, kRed ]:
    G[n].SetMarkerColor(i)
    G[n].SetMarkerStyle(20)
    G[n].SetLineColor(i)
    G[n].SetLineWidth(2)
    G[n].SetLineStyle(2)
    np = G[n].GetN();
    for j in xrange(np):
      G[n].SetPointEXhigh(j,0)
      G[n].SetPointEXlow(j,0)

    gr.Add(G[n])
#    G2 = G[n].Clone()
#    G2.SetLineStyle(1)
#    G2.SetLineWidth(1)
#    g1.Add(G2)
    Fit[n].SetLineColor(i)
    n=n+1
g1 = gr.Clone()

#g1.SetLineWidth(1)
#g1.SetLineStyle(1)
gr.Draw("APC")
#g1.Draw("AP")
#Fit[4].Draw()
#Fit[4].GetXaxis().SetRangeUser( 0, 1.7 )
#Fit[4].Draw()
for n in xrange(5):
#    G[n].Draw("AP same")
    Fit[5-n-1].Draw("same")
    n=n+1

L.cd()
legend = TLegend( 0, 0, 1, 1 )
n=0
for bt in [ "b0t0", "b0t1", "b1t0", "b1t1","b2t0" ]:
    legend.AddEntry( G[n], bt, "PL" )
    n=n+1
legend.SetNColumns(3)
legend.Draw()

C.SaveAs("outputs/Fit.png")
