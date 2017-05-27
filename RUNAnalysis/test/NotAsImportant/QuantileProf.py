#!/usr/bin/env python

import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

from RUNA.RUNAnalysis.Plotting_Header import *
from RUNA.RUNAnalysis.Distribution_Header import *
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
from RUNA.RUNAnalysis.scaleFactors import *
from RUNA.RUNAnalysis.CorrPlotter_Header import *

gROOT.SetBatch()
gStyle.SetOptStat(0)

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
Sig120 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-120_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*"+str(scaleFactor("RPVStopStopToJets_UDD323_M-120"))+"*36555.21/15" )
Sig280 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-280_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*"+str(scaleFactor("RPVStopStopToJets_UDD323_M-280"))+"*36555.21/15" )
Sig100 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-100_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*"+str(scaleFactor("RPVStopStopToJets_UDD323_M-100"))+"*36555.21/15" )
Sig220 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-220_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*"+str(scaleFactor("RPVStopStopToJets_UDD312_M-220"))+"*36555.21/15" )
Sig180 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-180_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*"+str(scaleFactor("RPVStopStopToJets_UDD323_M-180"))+"*36555.21/15" )
Sig240 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-240_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*"+str(scaleFactor("RPVStopStopToJets_UDD323_M-240"))+"*36555.21/15" )
def QuantileProf(V0, V1, CUTS, NAME):
    DISTS = [ QCD170to300, QCD300to470, QCD470to600, QCD600to800, QCD800to1000, QCD1000to1400, QCD1400to1800, QCD1800to2400, QCD2400to3200, QCD3200toInf ] # Use the MC distributions
#    DISTS = [ Sig100, Sig120, Sig180, Sig220, Sig240, Sig280 ]

#    rho = jet1Rho
#    tau21 = "jet1Tau21"
    
    Plots = CorrPlotter("QCD", DISTS, V0, V1, CUTS,"","","")
    
    Profs = Plots[1]

    CutValLine = GetQuantileProfiles( Plots[0], 0.0373370489491, "CutVal" )

    CutValLine.SetLineColor(kBlack)
    CutValLine.SetLineWidth(2)
    '''
    fit = TF1( "fit", "[0]+[1]*x", -4, 6 )
    CutValLine.Fit(fit,"R")


    p0 = TLatex( 0.2, 0.80, "p0 = " + '{:0.2e}'.format(fit.GetParameter(0)))
    p1 = TLatex( 0.2, 0.75, "p1 = " + '{:0.2e}'.format(fit.GetParameter(1)))

    p0.SetNDC()
    p0.SetTextFont(42) ### 62 is bold, 42 is normal
    p0.SetTextSize(0.04)
    p1.SetNDC()
    p1.SetTextFont(42) ### 62 is bold, 42 is normal
    p1.SetTextSize(0.04)
    '''
    C = TCanvas("C","",800,800)
    C.cd()
#    gStyle.SetPalette(90)
    Plots[0].Draw("COL")
    CutValLine.Draw("same")

    for i in Profs:
        i.SetLineColor(46)
        i.SetLineStyle(3)
        i.SetLineWidth(2)
        i.Draw("same")

#    p0.Draw("same")
#    p1.Draw("same")

    C.SaveAs("TCutPlots/QuantProf_QCD_"+NAME+".png")

jet1Rho = "log((jet1PrunedMass*jet1PrunedMass)/(jet1Pt))"
jet2Rho = "log((jet2PrunedMass*jet2PrunedMass)/(jet2Pt))"
rho = "("+jet1Rho + "+" + jet2Rho + ")" + "/2"
tau21 = "(jet1Tau21+jet2Tau21)/2"

j1tau21 = "jet1Tau21 + 4.35e-02*"+jet1Rho
j2tau21 = "jet2Tau21 + 4.35e-02*"+jet2Rho
#tau21 = "("+j1tau21+"+"+j2tau21+")/2"
V1AveTau21 = [tau21, 50, 0, 1, "Average #tau_{21}"]
V1Jet1Tau21 = ["jet1Tau21", 50, 0, 1, "Leading Jet #tau_{21}"]
V1Jet2Tau21 = ["jet2Tau21", 50, 0, 1, "2nd Leading Jet #tau_{21}"]
V0AveRho = [rho, 140, -10, 10, "Average #rho'"]
V0Jet1Rho = [jet1Rho, 140, -10, 10, "Leading Jet #rho'"]
V0Jet2Rho = [jet2Rho, 140, -10, 10, "2nd Leading Jet #rho'"]
V0AveMass = ["prunedMassAve", 40, 0, 400, "Average Soft Drop Mass"]

pres = "jet1Tau21>0."
jet1T = "jet1Tau21<0.45"
jet1AT = "jet1Tau21>0.45"
jet2T = "jet2Tau21<0.45"
jet2AT = "jet2Tau21>0.45"

presA = "prunedMassAsym<0.1&deltaEtaDijet<1.5"
presB = "prunedMassAsym<0.1&deltaEtaDijet>1.5"
presC = "prunedMassAsym>0.1&deltaEtaDijet<1.5"
presD = "prunedMassAsym>0.1&deltaEtaDijet>1.5"

QuantileProf(V0AveRho, V1AveTau21, presA, "_Rho_Average_A")
QuantileProf(V0AveRho, V1AveTau21, presB, "_Rho_Average_B")
QuantileProf(V0AveRho, V1AveTau21, presC, "_Rho_Average_C")
QuantileProf(V0AveRho, V1AveTau21, presD, "_Rho_Average_D")
#QuantileProf(V0AveMass, V1AveTau21, pres, "_Mass_Average_PRES")
'''
QuantileProf(V0AveRho, V1Jet1Tau21, pres, "_Rho_LeadT_PRES")
QuantileProf(V0Jet1Rho, V1Jet1Tau21, pres, "_Rho_Lead_PRES")
#QuantileProf(V0AveRho, V1AveTau21, jet2T, "_Rho_Average_Jet2T")
QuantileProf(V0AveRho, V1Jet1Tau21, jet2T, "_Rho_LeadT_Jet2T")
QuantileProf(V0Jet1Rho, V1Jet1Tau21, jet2T, "_Rho_Lead_Jet2T")
#QuantileProf(V0AveRho, V1AveTau21, jet2AT, "_Rho_Average_Jet2AT")
QuantileProf(V0AveRho, V1Jet1Tau21, jet2AT, "_Rho_LeadT_Jet2AT")
QuantileProf(V0Jet1Rho, V1Jet1Tau21, jet2AT, "_Rho_Lead_Jet2AT")

QuantileProf(V0AveRho, V1Jet2Tau21, pres, "_Rho_Lead2T_PRES")
QuantileProf(V0Jet2Rho, V1Jet2Tau21, pres, "_Rho_Lead2_PRES")
#QuantileProf(V0AveRho, V1AveTau21, jet1T, "_Rho_Average_Jet1T")
QuantileProf(V0AveRho, V1Jet2Tau21, jet1T, "_Rho_Lead2T_Jet1T")
QuantileProf(V0Jet2Rho, V1Jet2Tau21, jet1T, "_Rho_Lead2_Jet1T")
#QuantileProf(V0AveRho, V1AveTau21, jet1AT, "_Rho_Average_Jet1AT")
QuantileProf(V0AveRho, V1Jet2Tau21, jet1AT, "_Rho_Lead2T_Jet1AT")
QuantileProf(V0Jet2Rho, V1Jet2Tau21, jet1AT, "_Rho_Lead2_Jet1AT")
'''
