#
import os
import math
from array import array
import optparse
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
import RUNA.RUNAnalysis.CorrPlotter_Header
from RUNA.RUNAnalysis.CorrPlotter_Header import *

gStyle.SetOptStat(0)
gStyle.SetOptFit(0)

QCD1000to1400 = DIST( "QCD1000to1400", "80XRootFilesUpdated/RUNAnalysis_QCDPt1000to1400_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1000to1400" )))
QCD1400to1800 = DIST( "QCD1400to1800", "80XRootFilesUpdated/RUNAnalysis_QCDPt1400to1800_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1400to1800" )))
QCD170to300 = DIST( "QCD170to300", "80XRootFilesUpdated/RUNAnalysis_QCDPt170to300_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_170to300" )))
QCD1800to2400 = DIST( "QCD1800to2400", "80XRootFilesUpdated/RUNAnalysis_QCDPt1800to2400_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1800to2400" )))
QCD2400to3200 = DIST( "QCD2400to3200", "80XRootFilesUpdated/RUNAnalysis_QCDPt2400to3200_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_2400to3200" )))
QCD300to470 = DIST( "QCD300to470", "80XRootFilesUpdated/RUNAnalysis_QCDPt300to470_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_300to470" )))
QCD3200toInf = DIST( "QCD3200toInf", "80XRootFilesUpdated/RUNAnalysis_QCDPt3200toInf_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_3200toInf" )))
QCD470to600 = DIST( "QCD470to600", "80XRootFilesUpdated/RUNAnalysis_QCDPt470to600_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_470to600" )))
QCD600to800 = DIST( "QCD600to800", "80XRootFilesUpdated/RUNAnalysis_QCDPt600to800_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_600to800" )))
QCD800to1000 = DIST( "QCD800to1000", "80XRootFilesUpdated/RUNAnalysis_QCDPt800to1000_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_800to1000" )))
Sig120 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-120_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*689.799/746680*36555.21/15" )
Sig280 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-240_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*26.476/153653*36555.21/15" )
QCDPtAll = DIST( "QCDPtAll", "v08/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "puWeight*36555.21/15*lumiWeight" )

#S = [ QCD170to300, QCD300to470, QCD470to600, QCD600to800, QCD800to1000, QCD1000to1400, QCD1400to1800, QCD1800to2400, QCD2400to3200, QCD3200toInf ] # Use the MC distributions

def SlopePlot(PRES, S, NAME):
    rhovstau21 = TH2F("rhovstau21_"+NAME, "", 40, 0., 400., 50, 0., 1.)

#    jet1Rho = "log((jet1PrunedMass*jet1PrunedMass)/(jet1Pt))"
#    jet2Rho = "log((jet2PrunedMass*jet2PrunedMass)/(jet2Pt))"
#    rho = "("+jet1Rho + "+" + jet2Rho + ")" + "/2"
#    rho = jet2Rho
    rho = "prunedMassAve"
    tau21 = "prunedMassAsym"
#    jet1Tau21DDT = "(jet1Tau21 + 7.65e-02*"+jet1Rho+")"
#    jet2Tau21DDT = "(jet2Tau21 + 7.65e-02*"+jet2Rho+")"
#    tau21 = "("+jet1Tau21DDT+"+"+jet2Tau21DDT+")/2"
#    tau21 = "(jet1Tau21+jet2Tau21)/2"
    for i in S:
        quick2dplot( i.File, i.Tree, rhovstau21, rho, tau21, PRES, i.weight )
    
#    profX = quickprofiles("rhovstau21_"+NAME, rhovstau21)[0]
    profX = GetQuantileProfiles(rhovstau21, 0.285106414797, "prof" )

    if "QCD" in NAME: fit = TF1( "fit", "[0]+[1]*x", 0, 400 )
    else: fit = TF1( "fit", "[0]+[1]*x", 0, 400 )
    profX.Fit(fit, "R")
    
    p0 = TLatex( 0.2, 0.80, "p0 = " + '{:0.2e}'.format(fit.GetParameter(0)))
    p1 = TLatex( 0.2, 0.75, "p1 = " + '{:0.2e}'.format(fit.GetParameter(1)))

    p0.SetNDC()
    p0.SetTextFont(42) ### 62 is bold, 42 is normal
    p0.SetTextSize(0.04)
    p1.SetNDC()
    p1.SetTextFont(42) ### 62 is bold, 42 is normal
    p1.SetTextSize(0.04)

    C = TCanvas("C","",800,800)
    C.cd()

    rhovstau21.GetXaxis().SetTitle("2nd Leading Jet #rho'")
    rhovstau21.GetYaxis().SetTitleOffset(1.3)
    rhovstau21.GetYaxis().SetTitle("2nd Leading Jet #tau_{21}")
    
    profX.SetLineColor(kBlack)
    profX.SetLineWidth(2)

    rhovstau21.Draw("COL")
    profX.Draw("sameE0")

    p0.Draw("same")
    p1.Draw("same")

    C.SaveAs("TCutPlots/rhovstau21_"+NAME+".png")

S = [ QCDPtAll ]
SlopePlot("jet1Tau21<0.45&jet2Tau21<0.45", S, "QCD_jet2")
#S = [Sig120]
#SlopePlot("jet1Tau21>0.", S, "Sig120")
#S = [Sig280]
#SlopePlot("jet1Tau21>0.", S, "Sig280")
