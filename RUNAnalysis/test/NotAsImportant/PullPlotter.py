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

directory = "42017/Tau21DDTNoFit/"
method = "CBDMC"

PullPlots = []
PullPlots2 = []
if True:
    '''
    PullPlots.append( [ TFile.Open("outputs/"+directory+"0_0"+method+"/Massb0t0_pull.root"), "Zero btags, Zero top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"1_0"+method+"/Massb1t0_pull.root"), "One btag, Zero top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"2_0"+method+"/Massb2t0_pull.root"), "Two btags, Zero top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"3_0"+method+"/Massb0t1_pull.root"), "Zero btags, One top-tag" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"4_0"+method+"/Massb1t1_pull.root"), "One btag, One top-tag" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"5_0"+method+"/Massb2t1_pull.root"), "Two btags, One top-tag" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"6_0"+method+"/Massb0t2_pull.root"), "Zero btags, Two top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"7_0"+method+"/Massb1t2_pull.root"), "One btag, Two top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"8_0"+method+"/Massb2t2_pull.root"), "Two btags, Two top-tags" ] )
    '''
    PullPlots.append( [ TFile.Open("outputs/"+directory+"9_0"+method+"/Masspres_pull.root"), "Pres" ] )

    directory2 = "42017/Tau21DDTFit/"
    method2 = "CBDMC"

    print directory2
    print method2

    '''
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"0_0"+method2+"/Massb0t0_pull.root"), "Zero btags, Zero top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"1_0"+method2+"/Massb1t0_pull.root"), "One btag, Zero top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"2_0"+method2+"/Massb2t0_pull.root"), "Two btags, Zero top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"3_0"+method2+"/Massb0t1_pull.root"), "Zero btags, One top-tag" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"4_0"+method2+"/Massb1t1_pull.root"), "One btag, One top-tag" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"5_0"+method2+"/Massb2t1_pull.root"), "Two btags, One top-tag" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"6_0"+method2+"/Massb0t2_pull.root"), "Zero btags, Two top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"7_0"+method2+"/Massb1t2_pull.root"), "One btag, Two top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"8_0"+method2+"/Massb2t2_pull.root"), "Two btags, Two top-tags" ] )
    '''
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"9_0"+method2+"/Masspres_pull.root"), "Preselection" ] )
    ###### FIT METRIC DISTRIBUTION QUAD WITH FIT  ######

    C7 = TCanvas( "C", "", 800, 800 )
    sum6 = 0
    FitMet = []
    FitMet2 = []
    Fits = []
    Results = []
    for i in xrange(len(PullPlots)):
        C7.cd(i+1)

        FitMet.append(TH1D("h0"+str(i),"", PullPlots[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_quad").GetBinContent(bin) )

        FitMet2.append(TH1D("h1"+str(i),"", PullPlots2[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1):
            FitMet2[i].SetBinContent( bin, PullPlots2[i][0].Get("fitMetric_quad").GetBinContent(bin) )

    pullDistBefore = TH1D( "pullDistBefore", "", 20, -10, 10 )
    pullDistAfter = TH1D( "pullDistAfter", "", 20, -10, 10 )

    for i in xrange(len(FitMet)):
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            pullDistAfter.Fill( FitMet[i].GetBinContent(bin) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1):
            pullDistBefore.Fill( FitMet2[i].GetBinContent(bin) )

    pullDistBefore.GetXaxis().SetTitle("#sigma")
    pullDistBefore.GetYaxis().SetTitle("Bins")

    pullDistAfter.GetXaxis().SetTitle("#sigma")
    pullDistAfter.GetYaxis().SetTitle("Bins")
    pullDistAfter.GetYaxis().SetLabelOffset(.0004)
    pullDistAfter.GetXaxis().SetLabelOffset(.0004)
    pullDistAfter.GetYaxis().SetLabelSize(.03)
    pullDistAfter.GetXaxis().SetLabelSize(.03)
    
    pullDistAfter.GetYaxis().SetTitleOffset(1.2)
#    pullDistAfter.GetXaxis().SetTitleOffset(1.4)

    pullDistAfter.GetYaxis().SetTitleSize(0.04)
    pullDistAfter.GetXaxis().SetTitleSize(0.04)

    FitResultBefore = pullDistBefore.Fit( "gaus", "S", "", -10, 10 )
    FitBefore = pullDistBefore.GetFunction("gaus").Clone()
    FitResultAfter = pullDistAfter.Fit( "gaus", "S", "", -10, 10 )
    FitAfter = pullDistAfter.GetFunction("gaus").Clone()
    
    pullDistAfter.SetLineColor(kBlue)
    pullDistAfter.SetLineWidth(2)
    gStyle.SetHatchesSpacing(1)
    
    pullDistBefore.SetLineColor(kRed)
    pullDistBefore.SetLineWidth(2)
    
    FindAndSetMax( [pullDistAfter, pullDistBefore], False)
    
    pullDistAfter.Draw("hist")
    pullDistBefore.Draw("hist same")
    
    FitBefore.SetLineColor(kRed)
    FitAfter.SetLineColor(kBlue)
    FitBefore.SetLineStyle(2)
    FitAfter.SetLineStyle(2)
    
    FitBefore.Draw("same")
    FitAfter.Draw("same")

    T0 = TLine(0,0,0,pullDistAfter.GetMaximum())
    T0.SetLineWidth(2)
    T0.SetLineColor(19)
#    T0.SetLineStyle(3)
#    T0.Draw("same")
    
    CMS_lumi.extraText = "Preliminary"
    CMS_lumi.relPosX = 0.15
    CMS_lumi.CMS_lumi(C7, 4, 0)
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.03)
    latex.SetTextAlign(13)
    latex.DrawLatex( .12, .85, "#color[2]{Fitted TF}" )
    latex.DrawLatex( .15, .81, "#color[2]{#mu: " + str("%.4f" % FitResultBefore.Parameter(1)) + "}" )
    latex.DrawLatex( .15, .78, "#color[2]{#sigma: " + str("%.4f" % FitResultBefore.Parameter(2)) + "}" )
    
    latex.DrawLatex( .12, .73, "#color[4]{Unfitted TF}" )
    latex.DrawLatex( .15, .69, "#color[4]{#mu: " + str("%.4f" % FitResultAfter.Parameter(1)) + "}" )
    latex.DrawLatex( .15, .66, "#color[4]{#sigma: " + str("%.4f" % FitResultAfter.Parameter(2)) + "}" )

    C7.SaveAs( "outputs/"+directory+method+"/PullPlotQuadMetricAllPres"+method+".png" )
