#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy
from RUNA.RUNAnalysis.Plotting_Header import *
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi

gStyle.SetOptStat(0)
gStyle.SetOptFit(False)
bt = "b0t0"
FILE = TFile.Open("outputs/BeforeThetaQCD/126170CMVAv2BCDDATA/LIM_FITb0t0.root")
FIT = FILE.Get("Fit_"+bt).Clone()
FITUP = FILE.Get("FitUp_"+bt).Clone()
FITDN = FILE.Get("FitDn_"+bt).Clone()
G = FILE.Get("FitDn_"+bt).Clone()
chi2Test = TLatex( 0.2, 0.85, '#chi^{2}/ndF = '+ str( round( G.GetChisquare(), 2 ) )+'/'+str( int( G.GetNDF() ) ) )
p0 = TLatex( 0.2, 0.80, 'p0 = '+ '{:0.2e}'.format(G.GetParameter( 0 )) +' #pm '+ '{:0.2e}'.format(G.GetParError( 0 )))
p1 = TLatex( 0.2, 0.75, 'p1 = '+ '{:0.2e}'.format(G.GetParameter( 1 )) +' #pm '+ '{:0.2e}'.format(G.GetParError( 1 )))
p2 = TLatex( 0.2, 0.70, 'p2 = '+ '{:0.2e}'.format(G.GetParameter( 2 )) +' #pm '+ '{:0.2e}'.format(G.GetParError( 2 )) )

chi2Test.SetNDC()
chi2Test.SetTextFont(42) ### 62 is bold, 42 is normal
chi2Test.SetTextSize(0.04)
p0.SetNDC()
p0.SetTextFont(42) ### 62 is bold, 42 is normal
p0.SetTextSize(0.04)
p1.SetNDC()
p1.SetTextFont(42) ### 62 is bold, 42 is normal
p1.SetTextSize(0.04)
p2.SetNDC()
p2.SetTextFont(42) ### 62 is bold, 42 is normal
p2.SetTextSize(0.04)


# Pretty up G, Fit, and save
C2 = TCanvas( "C2", "", 10, 10, 750, 500 )
C2.cd()
C2.SetGrid( 4 )

CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.13

G.SetTitle("")

G.GetYaxis().SetRangeUser(0,2.4)
G.Draw("AP")
G.GetXaxis().SetTitle( "Average Pruned Mass [GeV]" )
G.GetYaxis().SetTitle( "R_{p/f}" )
G.GetYaxis().SetTitleOffset( 1.3 )
G.GetYaxis().SetNdivisions( 28 )

#        leg.AddEntry( G.ErrDn, "fit errors", "L" )
FITUP.SetLineStyle(2)
FITUP.Draw("same")
FITDN.SetLineStyle(2)
FITDN.Draw("same")
chi2Test.Draw('same')
p0.Draw('same')
p1.Draw('same')
p2.Draw('same')
CMS_lumi.CMS_lumi(C2, 4, 0)
#    leg.Draw()

C2.SaveAs(bt+"Est_Fit.png")

