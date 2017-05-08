#
import os
import math
from array import array
import optparse
import argparse
import ROOT
from ROOT import *
import scipy
import pickle 

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

def ABCDEF_Est(Dists, DistsSub, masses, detaBins):
    ABCDEF_EstFile = TFile( "TCutPlots/ABCDEF_EstFile.root", "RECREATE" )
    ABCDEF = TH3F("H3","",50, 0., 1., 50, 0., 5., 60, 50., 350.)
    ABCDEFSUB = TH3F("H3SUB","",50, 0., 1., 50, 0., 5., 60, 50., 350.)

    for i in Dists: quick3dplot(i.File, "BoostedAnalysisPlotsPuppi/RUNATree", ABCDEF, "prunedMassAsym", "deltaEtaDijet", "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&numJets==2", i.weight)
    for i in DistsSub: quick3dplot(i.File, "BoostedAnalysisPlotsPuppi/RUNATree", ABCDEFSUB, "prunedMassAsym", "deltaEtaDijet", "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&numJets==2", i.weight)

    ABCDEF.Add(ABCDEFSUB, -1)
    AList, CList, VList, TList, TEHList, TELList, MList, EHList, ELList = ([] for i in range(9))

    for mass in masses:
        bM1 = ABCDEF.GetZaxis().FindBin((mass[0]))
        bM2 = ABCDEF.GetZaxis().FindBin(mass[1])-1

        Ax1, Ax2, Ay1, Ay2 = GetBins(ABCDEF, 0., 0.099999, 0., 1.4999999)
        Cx1, Cx2, Cy1, Cy2 = GetBins(ABCDEF, 0.1, 1.0, 0., 1.4999999)
        Bx1, Bx2, By1, By2 = ([] for i in range(4))
        Dx1, Dx2, Dy1, Dy2 = ([] for i in range(4))
        
        for deta in detaBins:
            AppendMultiple( [Bx1, Bx2, By1, By2], list(GetBins(ABCDEF, 0., 0.0999999, deta[0], deta[1])) )
            AppendMultiple( [Dx1, Dx2, Dy1, Dy2], list(GetBins(ABCDEF, 0.1, 1.0, deta[0], deta[1])) )
        A = ABCDEF.Integral(Ax1, Ax2, Ay1, Ay2, bM1, bM2)
        C = ABCDEF.Integral(Cx1, Cx2, Cy1, Cy2, bM1, bM2)
        B, D, EYH, EYL, EXH, EXL = ([] for i in range(6))
        BSum, DSum = 0, 0

        for i in xrange(len(Bx1)):
            BP = ABCDEF.Integral(Bx1[i], Bx2[i], By1[i], By2[i], bM1, bM2)
            DP = ABCDEF.Integral(Dx1[i], Dx2[i], Dy1[i], Dy2[i], bM1, bM2)
            ERR = list(RatioErr(BP, DP))
            exl = (float((detaBins[i][1]-detaBins[i][0])/2.))
            exh = (float((detaBins[i][1]-detaBins[i][0])/2.))
            AppendMultiple( [EXL, EXH, EYL, EYH], [exl, exh]+ERR )
            AppendMultiple( [B, D], [BP, DP] )
            BSum = BSum + B[-1]
            DSum = DSum + D[-1]
        EYLSum, EYHSum = RatioErr(BSum, DSum)            
        if DSum == 0: BOverD = 0
        else: BOverD = float(BSum/DSum)

        F, P = [], []
        for i in xrange(len(B)):
            if not D[i]==0: F.append(float(B[i]/D[i]))
            else: F.append(0.)
        for deta in detaBins: P.append(float((deta[0]+deta[1])/2))
        G = TGraphAsymmErrors(len(detaBins), scipy.array(P), scipy.array(F), scipy.array(EXL), scipy.array(EXH), scipy.array(EYL), scipy.array(EYH))

        L = TF1("lin", "[0]+[1]*(x)", 0, 5)
        L.SetParameters(.1, -.1)
        if mass[0]==125: L.SetParameters(0,1)
#        G.Write("BOverDDeta_"+str(mass[0]))

        fitResult = TFitResultPtr(G.Fit(L, "SFE"))
        truthBins = [[0,.5],[.5,1.0],[1.0,1.5]]
        bins = truthBins + detaBins
        ConvFactUp, ConvFactDn = FitErrors( bins, L, fitResult)

        G.SetTitle("")
        G.GetXaxis().SetTitle( "Delta Eta Dijet" )
        G.GetXaxis().SetTitleSize(G.GetXaxis().GetTitleSize()*1.3)
        G.GetYaxis().SetTitle( "R_{p/f}" )
        G.GetYaxis().SetTitleOffset( 1.0 )
        G.GetYaxis().SetTitleSize(G.GetYaxis().GetTitleSize()*1.3)
        G.GetYaxis().SetNdivisions( 28 )
        G.GetXaxis().SetLimits(0,5)
        G.SetMarkerSize(1.5)
        G.SetMarkerStyle(8)

        ConvFactUp.SetLineStyle(2)
        ConvFactUp.SetLineWidth(2)
        ConvFactUp.SetLineColor(kRed)
        ConvFactDn.SetLineStyle(2)
        ConvFactDn.SetLineWidth(2)
        ConvFactDn.SetLineColor(kRed)

        chi2Test = '#chi^{2}/ndF = '+ str( round( ComputeChi2(G, L), 2 ) )+'/'+str( int( L.GetNDF() ))
        leg = TLegend(.11,.11,.40,.30)
        leg.SetNColumns(1)
        leg.SetLineColor(0)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.AddEntry(G, "B/D", "PL")
        leg.AddEntry(L, "Linear Fit, " + chi2Test, "L")
        C3 = TCanvas("C3", "", 750, 500)
        C3.cd()
        G.Draw("AP")
        ConvFactUp.Draw("samepc")
        ConvFactDn.Draw("samepc")
        leg.Draw("same")
        L.Draw("same")
        CMS_lumi.relPosX = 0.17
        CMS_lumi.CMS_lumi(C3, 4, 0)
        C3.SaveAs("TCutPlots/TFDEtaBins"+str(mass[0])+".png")
        V = L.Eval(0.75)
        print "Difference between old and new (old-new): " + str(V) + " Old: " + str(BOverD)
        EVH = ConvFactUp.Eval(0.75)-V
        EVL = V-ConvFactDn.Eval(0.75)
        AppendMultiple( [AList, CList, VList, TList, TEHList, TELList, EHList, ELList, MList], [A, C, V, BOverD, EYHSum, EYLSum, EVH, EVL, [mass[0],mass[1]]] )
    with open("ABCDEF_Est_output.py", "w") as f:
        f.write('AL = %s\n' % AList)
        f.write('CL = %s\n' % CList)
        f.write('VL = %s\n' % VList)
        f.write('TL = %s\n' % TList)
        f.write('TEHL = %s\n' % TEHList)
        f.write('TELL = %s\n' % TELList)
        f.write('EHL = %s\n' % EHList)
        f.write('ELL = %s\n' % ELList)
        f.write('ML = %s\n' % MList)
#    return AList, CList, VList, TList, TEHList, TELList, EHList, ELList, MList
