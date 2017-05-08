#
import os
import math
from array import array
import optparse
import argparse
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
import RUNA.RUNAnalysis.scaleFactors
from RUNA.RUNAnalysis.scaleFactors import *
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi
import RUNA.RUNAnalysis.ABCDEF_Functions
from RUNA.RUNAnalysis.ABCDEF_Functions import *
import RUNA.RUNAnalysis.ABCDEF_Ester
from RUNA.RUNAnalysis.ABCDEF_Ester import *

def DrawEst( StackEst, EST, DATA, Boxes, pBoxes, sBoxes, Pull, Pull2, NAME, NAMEF):
    FindAndSetMax([StackEst,DATA],False)
    Pull2.GetXaxis().SetTitle("Average Mass [GeV]")
    Pull2.SetStats(0)
    Pull2.SetLineColor(1)
    Pull2.SetFillColor(0)
    Pull2.SetMarkerColor(1)
    Pull2.SetMarkerStyle(20)
    Pull2.GetYaxis().SetNdivisions(4)
    Pull2.GetYaxis().SetTitle("#frac{QCD MC - Est}{#sigma_{stat}}")
    Pull2.GetYaxis().SetLabelSize(55/15*Pull2.GetYaxis().GetLabelSize())
    Pull2.GetYaxis().SetTitleSize(3.5*Pull2.GetYaxis().GetTitleSize())
    Pull2.GetYaxis().SetTitleOffset(0.20)
    Pull2.GetYaxis().SetRangeUser(-5,5.)
    Pull2.GetXaxis().SetLabelSize(.12)
    Pull2.GetXaxis().SetTitleSize(.12)
        
    for i in Boxes:
        i.SetFillColor(12)
        i.SetFillStyle(3244)
    for i in pBoxes:
        i.SetFillColor(9)
        i.SetFillStyle(3144)
    for i in sBoxes:
        i.SetFillColor(12)
        i.SetFillStyle(3002)
    
    C = TCanvas("C", "", 650, 650)
    C.cd()
    plot = TPad("pad1", "The pad 80% of the height",0,0.3,1,1)
    pull = TPad("pad2", "The pad 20% of the height",0,0.20,1.0,0.30)
    pull2 = TPad("pad3", "The pad 20% of the height",0,0.,1.0,0.20)
    plot.Draw()
    plot.SetBottomMargin(0)
    pull.SetTopMargin(0)
    pull.SetBottomMargin(0.)
    pull2.SetTopMargin(0)
    pull2.SetBottomMargin(0.3)
    plot.Draw()
    pull.Draw()
    pull2.Draw()
    plot.cd()
    StackEst.Draw("hist")
    print DATA.GetMaximum()
    StackEst.GetXaxis().SetTitle("")
    StackEst.GetYaxis().SetTitle("Events / 5 GeV")
    StackEst.GetXaxis().SetLabelSize(0)
        
    for i in Boxes:
        i.Draw("same")
    for i in sBoxes:
        i.Draw("same")
    DATA.Sumw2()
    DATA.SetLineWidth(2)
    DATA.Draw("sameE0")
    
    leg = TLegend(.35,.70,.89,.89)
    leg.SetNColumns(2)
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.AddEntry(DATA, "QCD MC", "PL")
    leg.AddEntry(EST, "QCD Est from QCD MC, "+NAME+" Fit", "F")
    leg.Draw("same")
    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.relPosX = 0.14
    CMS_lumi.CMS_lumi(plot, 4, 0)
        
    plot.RedrawAxis()
    pull.cd()
    Pull.GetXaxis().SetTitle("")
    Pull.SetLineColor(1)
    Pull.SetFillColor(0)
    Pull.SetMarkerColor(1)
    Pull.SetMarkerStyle(20)
    Pull.GetYaxis().SetNdivisions(4)
    Pull.GetYaxis().SetTitle("#frac{MC}{Est}")
    Pull.GetYaxis().SetLabelSize(55/15*Pull.GetYaxis().GetLabelSize())
    Pull.GetYaxis().SetTitleSize(5.5*Pull.GetYaxis().GetTitleSize())
    Pull.GetYaxis().SetTitleOffset(0.25)
    Pull.GetYaxis().SetRangeUser(0,2.)
    Pull.GetXaxis().SetLabelSize(.12)
    Pull.GetXaxis().SetTitleSize(.14)
    T01=TLine(50,1,350,1)
    T01.SetLineColor(kRed)
    Pull.Draw()
    T01.Draw("same")
    Pull.Draw("same")
    pull2.cd()
    Pull2.Draw()
    for i in pBoxes:
        i.Draw("same")

    T0 = TLine(50,0.,350,0.)
    T0.SetLineColor(kRed)
    T0.SetLineWidth(2)
    T2 = TLine(50,2.,350,2.)
    T2.SetLineColor(kRed)
    T2.SetLineStyle(2)
    T2.SetLineWidth(2)
    Tm2 = TLine(50,-2.,350,-2.)
    Tm2.SetLineColor(kRed)
    Tm2.SetLineStyle(2)
    Tm2.SetLineWidth(2)
    T1 = TLine(50,1.,350,1.)
    T1.SetLineColor(kRed)
    T1.SetLineStyle(3)
    T1.SetLineWidth(2)
    Tm1 = TLine(50,-1.,350,-1.)
    Tm1.SetLineColor(kRed)
    Tm1.SetLineStyle(3)
    Tm1.SetLineWidth(2)
    T0.Draw("same")
    T2.Draw("same")
    Tm2.Draw("same")
    T1.Draw("same")
    Tm1.Draw("same")
    Pull2.Draw("same")
        
    C.Print("TCutPlots/EstEtaBins_"+NAME+".png")
    del C, T0, T2, Tm2, T1, T01, Tm1


def DrawG(G, G2, F, FitUp, FitDn, NAME, NAMEF):
    C2 = TCanvas("C2", "", 650, 650)
    C2.cd()
    
    chi2Test = '#chi^{2}/ndF = '+ str( round( ComputeChi2(G, F), 2 ) )+'/'+str( int( F.GetNDF() ))
    G.Draw("AP")
    FitUp.SetLineColor(kRed)
    FitUp.SetLineStyle(2)
    FitUp.SetLineWidth(2)
    FitDn.SetLineColor(kRed)
    FitDn.SetLineColor(kRed)
    FitDn.SetLineStyle(2)
    FitDn.SetLineWidth(2)
    FitUp.Draw("PC")
    FitDn.Draw("PC")
    F.SetLineColor(kRed)
    F.SetLineWidth(2)
    F.Draw("same")
#    G2.Draw("PL")
    leg = TLegend(.11,.70,.40,.89)
    leg.SetNColumns(1)
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.AddEntry(G, "Extrapolated B/D", "PL")
#    leg.AddEntry(G2, "Old B/D", "PL")
    leg.AddEntry(F, NAME+" Fit, " + chi2Test, "L")
    leg.Draw("same")
    CMS_lumi.relPosX = 0.17
    CMS_lumi.CMS_lumi(C2, 4, 0)
    C2.RedrawAxis()
    C2.Print("TCutPlots/TFEtaBins"+NAMEF+".png")
    del C2
    return chi2Test

def EstComp(N, D, NAME, NAMEF):    
    C3 = TCanvas( "C3", "", 800, 800 )
    C3.cd()
    FILE = TFile.Open("outputs/5217/MCBCD/9_0CBDMC/Masspres_prunedMassAveEst.root")
    ESTOLD = FILE.Get("EST")
    ESTOLD.SetLineColor(kRed)
    N.SetLineColor(kAzure-4)
    N.SetFillColor(0)
    N.SetLineWidth(2)
    ESTOLD.SetLineWidth(2)
    FindAndSetMax([N, ESTOLD], False)
    D.Draw("E0")
    N.Draw("samehist")
    ESTOLD.Draw("histsame")
    leg2 = TLegend(.55,.70,.89,.89)
    leg2.SetLineColor(0)
    leg2.SetFillColor(0)
    leg2.SetFillStyle(0)
    leg2.AddEntry(N, "New Estimate, "+NAME+" Fit", "L")
    leg2.AddEntry(ESTOLD, "Old Estimate", "L")
    leg2.AddEntry(D, "QCD MC", "PL")
    leg2.Draw("same")
    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.relPosX = 0.14
    CMS_lumi.CMS_lumi(C3, 4, 0)
    
    C3.Print("TCutPlots/EstComp"+NAMEF+".png")

def FitComp(N,G, NAME, NAMEF):    
    C3 = TCanvas( "C3", "", 800, 800 )
    C3.cd()
    FILE = TFile.Open("outputs/5217/MCBCD/9_0CBDMC/LIM_FITpres_.root")
    ESTOLD = FILE.Get("G_pres")
    ESTOLD.GetFunction("QuadraticFitMass").SetBit(TF1.kNotDraw)
    ESTOLD.SetLineColor(kRed)
    ESTOLD.SetMarkerColor(kRed)
    N.SetLineWidth(2)
    ESTOLD.SetLineWidth(2)
#    FindAndSetMax([N, ESTOLD], False)
    N.Draw("PA")
    ESTOLD.Draw("XL")
    N.Draw("P")
    leg2 = TLegend(.55,.70,.89,.89)
    leg2.SetLineColor(0)
    leg2.SetFillColor(0)
    leg2.SetFillStyle(0)
    leg2.AddEntry(N, "New Transfer Function", "PL")
    leg2.AddEntry(ESTOLD, "Old Transfer Function", "PL")
    leg2.Draw("same")
    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.relPosX = 0.14
    CMS_lumi.CMS_lumi(C3, 4, 0)
    
    C3.Print("TCutPlots/FitComp"+NAMEF+".png")
