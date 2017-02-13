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

if True:
    PullPlots.append( [ TFile.Open("outputs/"+directory+"0"+method+"/Massb0t0pull.root"), "Zero btags, Zero top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"1"+method+"/Massb1t0pull.root"), "One btag, Zero top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"2"+method+"/Massb2t0pull.root"), "Two btags, Zero top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"3"+method+"/Massb0t1pull.root"), "Zero btags, One top-tag" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"4"+method+"/Massb1t1pull.root"), "One btag, One top-tag" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"5"+method+"/Massb2t1pull.root"), "Two btags, One top-tag" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"6"+method+"/Massb0t2pull.root"), "Zero btags, Two top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"7"+method+"/Massb1t2pull.root"), "One btag, Two top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"8"+method+"/Massb2t2pull.root"), "Two btags, Two top-tags" ] )

    directory2 = directory.replace("After","Before")
    method2 = method.replace("After","")

    print directory2
    print method2

    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"0"+method2+"/Massb0t0pull.root"), "Zero btags, Zero top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"1"+method2+"/Massb1t0pull.root"), "One btag, Zero top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"2"+method2+"/Massb2t0pull.root"), "Two btags, Zero top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"3"+method2+"/Massb0t1pull.root"), "Zero btags, One top-tag" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"4"+method2+"/Massb1t1pull.root"), "One btag, One top-tag" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"5"+method2+"/Massb2t1pull.root"), "Two btags, One top-tag" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"6"+method2+"/Massb0t2pull.root"), "Zero btags, Two top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"7"+method2+"/Massb1t2pull.root"), "One btag, Two top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"8"+method2+"/Massb2t2pull.root"), "Two btags, Two top-tags" ] )

    ###### FIT METRIC DIV 9 REGIONS WITH FIT ######

    C = TCanvas( "C", "", 800, 800 )
    C.Divide(3,3)
    C.SetTitle( "Pull/Error" )

    T0 = TLine(60,0,350,0)
    T0.SetLineColor(kGreen+3)
    
    T1 = TLine(60,1,350,1)
    T1.SetLineColor(kGreen+3)
    T1.SetLineStyle(3)
    Tm1 = TLine(60,-1,350,-1)
    Tm1.SetLineColor(kGreen+3)
    Tm1.SetLineStyle(3)
    
    T2 = TLine(60,2,350,2)
    T2.SetLineColor(kGreen+3)
    T2.SetLineStyle(2)
    Tm2 = TLine(60,-2,350,-2)
    Tm2.SetLineColor(kGreen+3)
    Tm2.SetLineStyle(2)
    sum1 = 0
    FitMet = []
    Fits = []
    Results = []
    for i in xrange(len(PullPlots)):
        C.cd(i+1)

        FitMet.append(TH1D("h"+str(i),"", PullPlots[i][0].Get("fitMetric_div").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_div").GetBinContent(bin) )

        FitMet[i].GetXaxis().SetNdivisions(504)
        FitMet[i].GetYaxis().SetLabelSize(.06)
        FitMet[i].GetXaxis().SetLabelSize(.06)
        FitMet[i].GetYaxis().SetTitleSize(0)
        FitMet[i].GetXaxis().SetTitle("Average Pruned Mass [GeV]")
        FitMet[i].GetXaxis().SetTitleSize(0.06)
        FitMet[i].SetFillColor(kBlue)

        FitMet[i].Sumw2()
        Fits.append(TF1("f"+str(i), "[0] + [1]*x", 60, 350 ))
        Fits[i].SetLineColor(kRed)
        Results.append(FitMet[i].Fit("f"+str(i), "S", "", 60, 350))
        FitMet[i].Draw("hist")
        Fits[i].Draw("same")
        FitMet[i].GetYaxis().SetRangeUser(-5,5)
        T2.Draw("same")
        T1.Draw("same")
        T0.Draw("same")
        Tm1.Draw("same")
        Tm2.Draw("same")
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.05)
        latex.SetTextAlign(13)
        latex.DrawLatex( .2, 1, PullPlots[i][1] )
        latex.DrawLatex( .2, .95, "#color[2]{Linear Fit: " + str( "%.4f" % Results[i].Parameter(1)) + "*x + " + str( "%.4f" % Results[i].Parameter(0)) + "}" )
        latex.DrawLatex( .2, .90, "Integral: " + "{0:.5f}".format(FitMet[i].Integral()) )
        sum1 = sum1+FitMet[i].Integral()

    print sum1

    C.SaveAs( "outputs/"+directory+method+"/PullPlotDivMetric"+method+".png" )

    ###### FIT METRIC QUAD WITH FIT #######

    C5 = TCanvas( "C", "", 800, 800 )
    C5.Divide(3,3)
    C5.SetTitle( "Pull/Error" )

    sum5 = 0
    FitMet = []
    FitMet2 = []
    Fits = []
    Results = []
    for i in xrange(len(PullPlots)):
        C5.cd(i+1)

        FitMet.append(TH1D("h"+str(i),"", PullPlots[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_quad").GetBinContent(bin) )

        FitMet2.append(TH1D("h"+str(i),"", PullPlots2[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1):
            FitMet2[i].SetBinContent( bin, PullPlots2[i][0].Get("fitMetric_quad").GetBinContent(bin) )

        FitMet[i].GetXaxis().SetNdivisions(504)
        FitMet[i].GetYaxis().SetLabelSize(.06)
        FitMet[i].GetXaxis().SetLabelSize(.06)
        FitMet[i].GetYaxis().SetTitleSize(0)
        FitMet[i].GetXaxis().SetTitle("Average Pruned Mass [GeV]")
        FitMet[i].GetXaxis().SetTitleSize(0.06)
        FitMet[i].SetFillColor(kBlue)
        FitMet[i].SetLineColor(kBlue)
        FitMet[i].SetFillStyle(3315)
        FitMet[i].SetLineWidth(2)
        gStyle.SetHatchesSpacing(1)
        FitMet[i].Sumw2()

        Fits.append(TF1("f"+str(i), "[0] + [1]*x", 60, 350 ))
        Fits[i].SetLineColor(kRed)
        Results.append(FitMet[i].Fit("f"+str(i), "S", "", 60, 350))
        FitMet[i].Draw("hist")
#        Fits[i].Draw("same")
        FitMet2[i].SetFillColor(kRed)
        FitMet2[i].SetLineColor(kRed)
        FitMet2[i].SetFillStyle(3004)
        FitMet2[i].SetLineWidth(2)
        FitMet2[i].Draw("same hist")
        FitMet[i].GetYaxis().SetRangeUser(-5,5)
        T2.Draw("same")
        T1.Draw("same")
        T0.Draw("same")
        Tm1.Draw("same")
        Tm2.Draw("same")
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.05)
        latex.SetTextAlign(13)
        latex.DrawLatex( .2, 1, PullPlots[i][1] )
#        latex.DrawLatex( .2, .95, "#color[2]{Before Theta: Integral="+"{0:.5f}".format(FitMet2[i].Integral())+"}" )
#        latex.DrawLatex( .2, .90, "#color[4]{After Theta: Integral="+"{0:.5f}".format(FitMet[i].Integral())+"}" )
        latex.DrawLatex( .2, .90, "#color[2]{Linear Fit: " + str( "%.4f" % Results[i].Parameter(1)) + "*x + " + str( "%.4f" % Results[i].Parameter(0)) + "}" )
        latex.DrawLatex( .2, .95, "Integral: " + "{0:.5f}".format(FitMet[i].Integral()) )
        sum5 = sum5+FitMet[i].Integral()

    print sum5

    C5.SaveAs( "outputs/"+directory+method+"/PullPlotQuadMetric"+method+".png" )

    ###### FIT METRIC NORM WITH FIT  ######

    C6 = TCanvas( "C", "", 800, 800 )
    C6.Divide(3,3)
    C6.SetTitle( "Pull/Error" )

    sum6 = 0
    FitMet = []
    Fits = []
    Results = []
    for i in xrange(len(PullPlots)):
        C6.cd(i+1)

        FitMet.append(TH1D("h"+str(i),"", PullPlots[i][0].Get("Pull_norm").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("Pull_norm").GetBinContent(bin) )

        FitMet[i].GetXaxis().SetNdivisions(504)
        FitMet[i].GetYaxis().SetLabelSize(.06)
        FitMet[i].GetXaxis().SetLabelSize(.06)
        FitMet[i].GetYaxis().SetTitleSize(0)
        FitMet[i].GetXaxis().SetTitle("Average Pruned Mass [GeV]")
        FitMet[i].GetXaxis().SetTitleSize(0.06)
        FitMet[i].SetFillColor(kBlue)
        FitMet[i].Sumw2()
        Fits.append(TF1("f"+str(i), "[0] + [1]*x", 60, 350 ))
        Fits[i].SetLineColor(kRed)
        Results.append(FitMet[i].Fit("f"+str(i), "S", "", 60, 350))
        FitMet[i].Draw("hist")
        Fits[i].Draw("same")

        FitMet[i].GetYaxis().SetRangeUser(-20,20)
        T2.Draw("same")
        T1.Draw("same")
        T0.Draw("same")
        Tm1.Draw("same")
        Tm2.Draw("same")
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.05)
        latex.SetTextAlign(13)
        latex.DrawLatex( .2, 1, PullPlots[i][1] )
        latex.DrawLatex( .2, .95, "#color[2]{Linear Fit: " + str( "%.4f" % Results[i].Parameter(1)) + "*x + " + str( "%.4f" % Results[i].Parameter(0)) + "}" )
        latex.DrawLatex( .2, .90, "Integral: " + "{0:.5f}".format(FitMet[i].Integral()) )
        sum6 = sum6+FitMet[i].Integral()

    print sum6

    C6.SaveAs( "outputs/"+directory+method+"/PullPlotNormMetric"+method+".png" )

    ###### SUM OF NORM PULL  ######

    C2 = TCanvas( "C2", "", 800, 800 )
    C2.cd()
    allPull = PullPlots[0][0].Get("Pull_norm").Clone()
    allPull.Reset()
    for i in xrange(len(PullPlots)):
        allPull.Add(PullPlots[i][0].Get("Pull_norm").Clone())

    allPull.GetXaxis().SetNdivisions(504)
    allPull.GetYaxis().SetLabelSize(.03)
    allPull.GetYaxis().SetTitleSize(0)
    allPull.GetXaxis().SetTitle( "Average Pruned Mass [GeV]" )
    
    allPull.Draw()
    latex2 = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.05)
    latex.SetTextAlign(13)
    latex.DrawLatex( .4, .8, "Sum of pull plots" )
    
    C2.SaveAs("outputs/"+directory+method+"/sumPull.png")
    
    ###### AVERAGE OF NORM PULL  ######

    C3 = TCanvas( "C3", "", 800, 800 )
    C3.cd()
    avePull = PullPlots[0][0].Get("Pull_norm").Clone()
    avePull.Reset()
    for i in xrange(len(PullPlots)):
        avePull.Add(PullPlots[i][0].Get("Pull_norm").Clone())

    for i in range(1, avePull.GetNbinsX()+1 ):
        bin = avePull.GetBinContent(i)
        avePull.SetBinContent( i, bin/9 )

    avePull.GetXaxis().SetNdivisions(504)
    avePull.GetYaxis().SetLabelSize(.03)
    avePull.GetYaxis().SetTitleSize(0)
    avePull.GetXaxis().SetTitle( "Average Pruned Mass [GeV]" )
    avePull.SetFillColor(kBlue)
    avePull.Draw("hist")
#T2.Draw("same")
    T1.Draw("same")
    T0.Draw("same")
    Tm1.Draw("same")
    Tm2.Draw("same")
    latex2 = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.03)
    latex.SetTextAlign(13)
    latex.DrawLatex( .4, .35, "Average Pull" )
    latex.DrawLatex( .4, .3, "CMVAv2 btag Cut, C*(B/D)" )
#latex.DrawLatex( .4, .25, "Integral: " + "{0:.5f}".format(avePull.Integral()) )
    
    C3.SaveAs("outputs/"+directory+method+"/avePull.png")
    
    ###### FIT METRIC NORM PULL WITH FIT ######

    C4 = TCanvas( "C4", "", 800, 800 )
    C4.Divide(3,3)
    C4.SetTitle( "Pull/Error" )
    
    T0 = TLine(60,0,350,0)
    T0.SetLineColor(kGreen+3)
    
    T1 = TLine(60,1,350,1)
    T1.SetLineColor(kGreen+3)
    T1.SetLineStyle(3)
    Tm1 = TLine(60,-1,350,-1)
    Tm1.SetLineColor(kGreen+3)
    Tm1.SetLineStyle(3)
    
    T2 = TLine(60,2,350,2)
    T2.SetLineColor(kGreen+3)
    T2.SetLineStyle(2)
    Tm2 = TLine(60,-2,350,-2)
    Tm2.SetLineColor(kGreen+3)
    Tm2.SetLineStyle(2)
    sum7 = 0
    P = []
    PFit = []
    PResult = []
    for i in xrange(len(PullPlots)):
        gStyle.SetOptStat(0)
        C4.cd(i+1)
        P.append(TH1D("h"+str(i),"", PullPlots[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) )
        for bin in range(0, P[i].GetNbinsX()+1):
            P[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_quad").GetBinContent(bin) )
        PFit.append(TF1("f"+str(i), "[0] + [1]*x", 60, 350 ))
        PResult.append(P[i].Fit("f"+str(i), "S", "", 60, 350))
    #    PFit = (P[i].GetFunction(f1)).Clone()
        PFit[i].SetLineColor(kRed)
        P[i].GetXaxis().SetNdivisions(504)
        P[i].GetYaxis().SetLabelSize(.06)
        P[i].GetXaxis().SetLabelSize(.06)
        P[i].GetYaxis().SetTitleSize(0)
        P[i].GetXaxis().SetTitle("Average Pruned Mass [GeV]")
        P[i].GetXaxis().SetTitleSize(.06)
        P[i].SetFillColor(kBlue)
        P[i].Draw("hist")
        P[i].GetYaxis().SetRangeUser(-20,20)
        PFit[i].Draw("same")
        T2.Draw("same")
        T1.Draw("same")
        T0.Draw("same")
        Tm1.Draw("same")
        Tm2.Draw("same")
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.05)
        latex.SetTextAlign(13)
        latex.DrawLatex( .2, 1, PullPlots[i][1] )
        latex.DrawLatex( .2, .95, "#color[2]{Linear Fit: " + str( "%.4f" % PResult[i].Parameter(1)) + "*x + " + str( "%.4f" % PResult[i].Parameter(0)) + "}" )
        #    latex.DrawLatex( .23, .90, "#color[2]{m: " + str( "%.4f" % PResult[i].Parameter(1)) + "}" )
        #    latex.DrawLatex( .23, .85, "#color[2]{b: " + str( "%.4f" % PResult[i].Parameter(0)) + "}" )
        latex.DrawLatex( .2, .90, "Integral: " + "{0:.5f}".format(P[i].Integral()) )
        sum7 = sum7+P[i].Integral()

    print sum7
    
    print "sum1: " + str(sum1)
    print "sum5: " + str(sum5)
    print "sum6: " + str(sum6)

    C4.SaveAs( "outputs/"+directory+method+"/PullPlotQuadFit"+method+".png" )
    
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
    latex.DrawLatex( .12, .85, "#color[2]{Before Theta}" )
    latex.DrawLatex( .15, .81, "#color[2]{#mu: " + str("%.4f" % FitResultBefore.Parameter(1)) + "}" )
    latex.DrawLatex( .15, .78, "#color[2]{#sigma: " + str("%.4f" % FitResultBefore.Parameter(2)) + "}" )
    
    latex.DrawLatex( .12, .73, "#color[4]{After Theta}" )
    latex.DrawLatex( .15, .70, "#color[4]{#mu: " + str("%.4f" % FitResultAfter.Parameter(1)) + "}" )
    latex.DrawLatex( .15, .67, "#color[4]{#sigma: " + str("%.4f" % FitResultAfter.Parameter(2)) + "}" )

    C7.SaveAs( "outputs/"+directory+method+"/PullPlotQuadMetricAll"+method+".png" )

    ###### DIST OF PULLS WITH FIT 9 REGIONS  ######

    C8 = TCanvas( "C", "", 800, 800 )
    C8.Divide(3,3)
    sum6 = 0
    FitMet = []
    FitMet2 = []
    Fits = []
    Results = []
    for i in xrange(len(PullPlots)):
        C8.cd(i+1)

        FitMet.append(TH1D("h0"+str(i),"", PullPlots[i][0].Get("Pull_norm").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("Pull_norm").GetBinContent(bin) )

        FitMet2.append(TH1D("h1"+str(i),"", PullPlots2[i][0].Get("Pull_norm").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1):
            FitMet2[i].SetBinContent( bin, PullPlots2[i][0].Get("Pull_norm").GetBinContent(bin) )

    pullDistBefore = []
    pullDistAfter = []
    FitResultBefore = []
    FitBefore = []
    FitResultAfter = []
    FitAfter = []

    for i in xrange(len(FitMet)):
        C8.cd(i+1)
        pullDistBefore.append(TH1D( "pullDistBefore" + str(i), "", 20, -10, 10 ))
        pullDistAfter.append(TH1D( "pullDistAfter[i]" + str(i), "", 20, -10, 10 ))

        for bin in range(0, FitMet[i].GetNbinsX()+1):
            pullDistAfter[i].Fill( FitMet[i].GetBinContent(bin) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1):
            pullDistBefore[i].Fill( FitMet2[i].GetBinContent(bin) )

        pullDistBefore[i].GetXaxis().SetTitle("#sigma")
        pullDistBefore[i].GetYaxis().SetTitle("Bins")
        
        pullDistAfter[i].GetXaxis().SetTitle("#sigma")
        pullDistAfter[i].GetYaxis().SetTitle("Bins")
        pullDistAfter[i].GetYaxis().SetLabelOffset(.0004)
        pullDistAfter[i].GetXaxis().SetLabelOffset(.0004)
        pullDistAfter[i].GetYaxis().SetLabelSize(.03)
        pullDistAfter[i].GetXaxis().SetLabelSize(.03)
        
        pullDistAfter[i].GetYaxis().SetTitleOffset(1.2)
#    pullDistAfter[i].GetXaxis().SetTitleOffset(1.4)
        
        pullDistAfter[i].GetYaxis().SetTitleSize(0.04)
        pullDistAfter[i].GetXaxis().SetTitleSize(0.04)
        
        FitResultBefore.append(pullDistBefore[i].Fit( "gaus", "S", "", -10, 10 ))
        FitBefore.append(pullDistBefore[i].GetFunction("gaus").Clone())
        FitResultAfter.append(pullDistAfter[i].Fit( "gaus", "S", "", -10, 10 ))
        FitAfter.append(pullDistAfter[i].GetFunction("gaus").Clone())
        
        pullDistAfter[i].SetLineColor(kBlue)
        pullDistAfter[i].SetLineWidth(2)
        gStyle.SetHatchesSpacing(1)
        
        pullDistBefore[i].SetLineColor(kRed)
        pullDistBefore[i].SetLineWidth(2)
        
        FindAndSetMax( [pullDistAfter[i], pullDistBefore[i]], False)
        
        pullDistAfter[i].Draw("hist")
#        pullDistBefore[i].Draw("hist")
        
        FitBefore[i].SetLineColor(kRed)
        FitAfter[i].SetLineColor(kBlue)
        FitBefore[i].SetLineStyle(2)
        FitAfter[i].SetLineStyle(2)
        
#        FitBefore[i].Draw("same")
        FitAfter[i].Draw("same hist")
        
        T0 = TLine(0,0,0,pullDistAfter[i].GetMaximum())
        T0.SetLineWidth(2)
        T0.SetLineColor(19)
        #    T0.SetLineStyle(3)
        #    T0.Draw("same")
        
        CMS_lumi.extraText = "Preliminary"
        CMS_lumi.relPosX = 0.15
        CMS_lumi.CMS_lumi( gPad, 4, 0)
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.03)
        latex.SetTextAlign(13)
        latex.DrawLatex( .12, .88, PullPlots[i][1] )
#        latex.DrawLatex( .12, .85, "#color[2]{Before Theta}" )
#        latex.DrawLatex( .15, .81, "#color[2]{#mu: " + str("%.4f" % FitResultBefore[i].Parameter(1)) + "}" )
#        latex.DrawLatex( .15, .78, "#color[2]{#sigma: " + str("%.4f" % FitResultBefore[i].Parameter(2)) + "}" )
        
        latex.DrawLatex( .12, .85, "#color[4]{Before Theta}" )
        latex.DrawLatex( .15, .81, "#color[4]{#mu: " + str("%.4f" % FitResultAfter[i].Parameter(1)) + "}" )
        latex.DrawLatex( .15, .78, "#color[4]{#sigma: " + str("%.4f" % FitResultAfter[i].Parameter(2)) + "}" )
        
    C8.SaveAs( "outputs/"+directory+method+"/PullPlotDist"+method+".png" )
