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
import RUNA.RUNAnalysis.ABCDEF_EstMaker
from RUNA.RUNAnalysis.ABCDEF_EstMaker import *

weight = "(36555.21/15*lumiWeight*puWeight)"
TTScaleStr = "1.06*exp(-0.0005*HT/2)"
WScaleStr = "1"
TopScaleStr = "1"

rootFiles = "80XRootFilesUpdated/"

DATA = DIST( "DATA", rootFiles+"/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut15.root", "BoostedAnalysisPlotsPuppi/RUNATree", "1" )

QCDHT = DIST( "QCDHT", "v08/RUNAnalysis_QCDHTAll_80X_V2p4_v08.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".62*puWeight*36555.21/15*lumiWeight")
QCDPT = DIST( "QCDPT", "v08/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".66*puWeight*36555.21/15*lumiWeight")
QCD = []
for i in [ "QCDPt170to300", "QCDPt300to470", "QCDPt470to600", "QCDPt600to800", "QCDPt800to1000", "QCDPt1000to1400", "QCDPt1400to1800", "QCDPt1800to2400", "QCDPt2400to3200", "QCDPt3200toInf" ]:
    QCD.append( DIST( i, rootFiles + "/RUNAnalysis_"+i+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*"+weight+"*"+str(scaleFactor(i))))
TTJets = DIST( "TTJets", rootFiles+"/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleStr+")" )
WJets = DIST( "WJets", rootFiles+"/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+WScaleStr+")" )
Top = DIST( "Top", rootFiles+"/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+TopScaleStr+")" )

Dists = [QCDHT]
#DistsSub = [Top,WJets,TTJets]
DistsSub = []
FILE = TFile( "TCutPlots/TFs.root", "RECREATE" )
FILE.cd()

def ABCDEF_Est():
    ABCDEF = TH3F("H3","",50, 0., 1., 50, 0., 5., 60, 50., 350.)
    ABCDEFSUB = TH3F("H3SUB","",50, 0., 1., 50, 0., 5., 60, 50., 350.)
    for i in Dists:
        quick3dplot(i.File, "BoostedAnalysisPlotsPuppi/RUNATree", ABCDEF, "prunedMassAsym", "deltaEtaDijet", "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&numJets==2", i.weight)
    for i in DistsSub:
        quick3dplot(i.File, "BoostedAnalysisPlotsPuppi/RUNATree", ABCDEFSUB, "prunedMassAsym", "deltaEtaDijet", "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&numJets==2", i.weight)

    ABCDEF.Add(ABCDEFSUB, -1)
    AList = []
    CList = []
    VList = []
    TList = []
    TEHList = []
    TELList = []
    MList = []
    EHList = []
    ELList = []
    masses = []
    i = 50
    while i < 200:
        masses.append([i,i+25])
        i=i+25
    masses.append([200,275])
    masses.append([275,350])

    for mass in masses:
        bM1 = ABCDEF.GetZaxis().FindBin((mass[0]))
        bM2 = ABCDEF.GetZaxis().FindBin(mass[1])-1

        Ax1 = ABCDEF.GetXaxis().FindBin(0.)
        Ax2 = ABCDEF.GetXaxis().FindBin(0.099999)
        Ay1 = ABCDEF.GetYaxis().FindBin(0.)
        Ay2 = ABCDEF.GetYaxis().FindBin(1.499999)

        Cx1 = ABCDEF.GetXaxis().FindBin(0.1)
        Cx2 = ABCDEF.GetXaxis().FindBin(1.0)
        Cy1 = ABCDEF.GetYaxis().FindBin(0.)
        Cy2 = ABCDEF.GetYaxis().FindBin(1.499999)
        detaBins = [ [1.5,1.99999], [2.0, 2.9999], [3.0, 5.0] ]
        Bx1, Bx2, By1, By2 = ([] for i in range(4))
        Dx1, Dx2, Dy1, Dy2 = ([] for i in range(4))
        
        for deta in detaBins:
            Bx1.append(ABCDEF.GetXaxis().FindBin(0.))
            Bx2.append(ABCDEF.GetXaxis().FindBin(0.09999999))
            By1.append(ABCDEF.GetYaxis().FindBin(deta[0]))
            By2.append(ABCDEF.GetYaxis().FindBin(deta[1]))

            Dx1.append(ABCDEF.GetXaxis().FindBin(0.1))
            Dx2.append(ABCDEF.GetXaxis().FindBin(1.0))
            Dy1.append(ABCDEF.GetYaxis().FindBin(deta[0]))
            Dy2.append(ABCDEF.GetYaxis().FindBin(deta[1]))

        A = ABCDEF.Integral(Ax1, Ax2, Ay1, Ay2, bM1, bM2)
        C = ABCDEF.Integral(Cx1, Cx2, Cy1, Cy2, bM1, bM2)
        B, D, EYH, EYL, EXH, EXL = ([] for i in range(6))
        BSum, DSum = 0, 0

        for i in xrange(len(Bx1)):
            BP = ABCDEF.Integral(Bx1[i], Bx2[i], By1[i], By2[i], bM1, bM2)
            DP = ABCDEF.Integral(Dx1[i], Dx2[i], Dy1[i], Dy2[i], bM1, bM2)
            if BP<0: BP = 0
            if DP<0: DP = 0

            eB = math.sqrt(BP)
            eD = math.sqrt(DP)
            if DP == 0 or BP == 0: Ei = 0.
            else: Ei = float((BP/DP)*(eB/BP+eD/DP))
            EXL.append(float((detaBins[i][1]-detaBins[i][0])/2.))
            EXH.append(float((detaBins[i][1]-detaBins[i][0])/2.))

            EYH.append(float(Ei))
            if DP > 0 and float(BP/DP)-Ei > 0:
                EYL.append(float(Ei))
            else:
                if DP == 0 or BP == 0: EYL.append(0.)
                else: EYL.append(float(BP/DP))
            
            B.append(BP)
            D.append(DP)
            BSum = BSum + B[-1]
            DSum = DSum + D[-1]

        BP = BSum
        DP = DSum
        if BP<0: BP = 0
        if DP<0: DP = 0
        
        eB = math.sqrt(BP)
        eD = math.sqrt(DP)
        if DP == 0 or BP == 0: Ei = 0.
        else: Ei = float((BP/DP)*(eB/BP+eD/DP))
        EXLSum = float((detaBins[i][1]-detaBins[i][0])/2.)
        EXHSum = (float((detaBins[i][1]-detaBins[i][0])/2.))
        
        EYHSum = (float(Ei))
        if DP > 0 and float(BP/DP)-Ei > 0:
            EYLSum = (float(Ei))
        else:
            if DP == 0 or BP == 0: EYLSum = (0.)
            else: EYLSum = (float(BP/DP))
            
        if DSum == 0: BOverD = 0
        else: BOverD = float(BSum/DSum)

        F = []
        P = []
        for i in xrange(len(B)):
            if not D[i]==0: 
                F.append(float(float(B[i])/float(D[i])))
            else: 
                F.append(0.)
        for deta in detaBins:
            P.append(float((deta[0]+deta[1])/2))
        G = TGraphAsymmErrors(len(detaBins), scipy.array(P), scipy.array(F), scipy.array(EXL), scipy.array(EXH), scipy.array(EYL), scipy.array(EYH))
        L = TF1("lin", "[0]+[1]*(x)", 0, 5)
#        if not(mass[0]==100) and not(mass[0]==125) and not(mass[0]==150) and not (mass[0]==115) and not (mass[0]==130) and not (mass[0]==160) and not (mass[0]==110):
#        if not(mass[0]==100):
        L.SetParameter(0, .1)
        L.SetParameter(1, -.1)

        G.Write("BOverDDeta_"+str(mass[0]))
        fitResult = TFitResultPtr(G.Fit(L, "SB"))
        truthBins = [[0,.5],[.5,1.0],[1.0,1.5]]
        bins = truthBins + detaBins
        listBinCenter = []
        fitErrors = []
        fitValues = []
        for i in xrange(0,len(bins)):
            binCenter = float((bins[i][0]+bins[i][1])/2.)
            listBinCenter.append(float(binCenter))
            err = array('d',[0])
            fitResult.GetConfidenceIntervals( 1, 1, 1, array('d', [binCenter]), err, 0.683, False )
            fitErrors.append(float(err[0]))
            fitValues.append(float(L.Eval(binCenter)))
        print numpy.add(fitValues, fitErrors)
        print numpy.subtract(fitValues, fitErrors)
        ConvFactUp = TGraph( len(fitValues), array('d', listBinCenter ), numpy.add( fitValues, fitErrors ) )
	ConvFactDn = TGraph( len(fitValues), array('d', listBinCenter ), numpy.subtract( fitValues, fitErrors ) )
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

        C3 = TCanvas("C3", "", 750, 500)
        C3.cd()
        G.Draw("AP")
        ConvFactUp.Draw("samepc")
        ConvFactDn.Draw("samepc")
        L.Draw("same")
        C3.SaveAs("TCutPlots/TFDEtaBins"+str(mass[0])+".png")

        V = L.Eval(0.75)
        EVH = ConvFactUp.Eval(0.75)-V
        EVL = V-ConvFactDn.Eval(0.75)
        AList.append(A)
        CList.append(C)
        VList.append(V)
        TList.append(BOverD)
        TEHList.append(EYHSum)
        TELList.append(EYLSum)
        EHList.append(EVH)
        ELList.append(EVL)
        MList.append([mass[0],mass[1]])
    return AList, CList, VList, TList, TEHList, TELList, EHList, ELList, MList
