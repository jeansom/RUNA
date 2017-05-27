#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
from ROOT import TF1
import scipy
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi
from RUNA.RUNAnalysis.Plotting_Header import *

FILEMCFIT = TFile.Open("outputs/5217/MCNoNJets/9_0CBDMC/LIM_FITpres_.root")
FILEDATAFIT = TFile.Open("outputs/5217/DATANoNJets/9_0CBDDATA/LIM_FITpres_.root")

FILEMCEST = TFile.Open("outputs/5217/MCNoNJets/9_0CBDMC/LIM_FEEDpres_.root")
FILEDATAEST = TFile.Open("outputs/5217/DATANoNJets/9_0CBDDATA/LIM_FEEDpres_.root")

FILEMCA = TFile.Open("outputs/5217/MCNoNJets/9_0CBDMC/Masspres_prunedMassAveEst.root")
FILEDATAA = TFile.Open("outputs/5217/DATANoNJets/9_0CBDDATA/Masspres_prunedMassAveEst.root")

FITMC = FILEMCFIT.Get("Fit_pres")
FITDATA = FILEDATAFIT.Get("Fit_pres")

GMC = FILEMCFIT.Get("G_pres")
GDATA = FILEDATAFIT.Get("G_pres")
GMC.GetFunction("QuadraticFitMass").SetBit(TF1.kNotDraw)
GDATA.GetFunction("QuadraticFitMass").SetBit(TF1.kNotDraw)

ESTMC = FILEMCEST.Get("pres__QCD")
ESTDATA = FILEDATAEST.Get("pres__QCD")

AMC = FILEMCA.Get("EST_Antitag")
ADATA = FILEDATAA.Get("EST_Antitag")

SMC = FILEMCA.Get("data_obs")
SDATA = FILEDATAA.Get("data_obs")

C = TCanvas("C1","",800,800)

ESTMC.SetLineColor(kBlack)
ESTMC.SetFillColor(kAzure-4)

ESTDATA.SetLineColor(kBlack)
ESTDATA.SetMarkerColor(kBlack)
ESTDATA.SetLineWidth(2)
FindAndSetMax( [ESTMC, ESTDATA], False )
ESTMC.GetXaxis().SetTitle("Average Soft Drop Mass")
ESTMC.GetYaxis().SetTitle("N Events / 5 GeV")
ESTMC.GetYaxis().SetTitleOffset(1.3)
ESTMC.GetYaxis().SetLabelSize(ESTMC.GetYaxis().GetLabelSize()*.9)
ESTMC.Draw("hist")
ESTDATA.Draw("samehist")

leg = TLegend(0.11,0.80,0.89,0.89)
leg.SetNColumns(2)
leg.SetFillStyle(0)
leg.SetFillStyle(0)
leg.SetLineColor(0)
leg.SetLineColor(0)
leg.SetFillColor(4001)

leg.AddEntry(ESTMC, "QCD Est from QCD MC", "F")
leg.AddEntry(ESTDATA, "QCD Est from Data", "PL")
leg.Draw("same")

CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.17
CMS_lumi.CMS_lumi( (C), 4, 0)
C.RedrawAxis()

C.SaveAs("TCutPlots/EstDATAMC.png")

C2 = TCanvas("C2","",750,500)
GMC.GetXaxis().SetTitle("Average Soft Drop Mass")
GMC.GetYaxis().SetTitle("R_{p/f}")

FITMC.SetLineColor(kAzure-4)
FITMC.SetMarkerColor(kAzure-4)
GMC.SetLineColor(kAzure-4)
GMC.SetMarkerColor(kAzure-4)

FITDATA.SetLineColor(kBlack)
FITDATA.SetMarkerColor(kBlack)
GDATA.SetLineColor(kBlack)
GDATA.SetMarkerColor(kBlack)

GMC.Draw("AP")
#FITMC.Draw("samehist")
GDATA.Draw("Psame")
#FITDATA.Draw("SAMEhist")

leg2 = TLegend(0.11,0.80,0.89,0.89)
leg2.SetNColumns(2)
leg2.SetFillStyle(0)
leg2.SetFillStyle(0)
leg2.SetLineColor(0)
leg2.SetLineColor(0)
leg2.SetFillColor(4001)

leg2.AddEntry(FITMC, "TF from QCD MC", "F")
leg2.AddEntry(FITDATA, "TF from Data", "PL")
leg2.Draw("same")

CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.17
CMS_lumi.CMS_lumi( (C), 4, 0)
C.RedrawAxis()

C2.SaveAs("TCutPlots/FitDATAMC.png")

C3 = TCanvas("C3","",800,800)

AMC.SetLineColor(kBlack)
AMC.SetFillColor(kAzure-4)

ADATA.SetLineColor(kBlack)
ADATA.SetMarkerColor(kBlack)
ADATA.SetLineWidth(2)
FindAndSetMax( [AMC, ADATA], False )
AMC.GetXaxis().SetTitle("Average Soft Drop Mass")
AMC.GetYaxis().SetTitle("N Events / 5 GeV")
AMC.GetYaxis().SetTitleOffset(1.5)
AMC.GetYaxis().SetLabelSize(AMC.GetYaxis().GetLabelSize()*.9)
AMC.Draw("hist")
ADATA.Draw("samehist")

leg = TLegend(0.11,0.80,0.89,0.89)
leg.SetNColumns(2)
leg.SetFillStyle(0)
leg.SetFillStyle(0)
leg.SetLineColor(0)
leg.SetLineColor(0)
leg.SetFillColor(4001)

leg.AddEntry(AMC, "QCD MC Antitag Region (C)", "F")
leg.AddEntry(ADATA, "Data Antitag Region (C)", "PL")
leg.Draw("same")

CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.17
CMS_lumi.CMS_lumi( (C3), 4, 0)
C3.RedrawAxis()

C3.SaveAs("TCutPlots/ADATAMC.png")

C4 = TCanvas("C4","",800,800)

SMC.SetLineColor(kBlack)
SMC.SetFillColor(kAzure-4)

SDATA.SetLineColor(kBlack)
SDATA.SetMarkerColor(kBlack)
SDATA.SetLineWidth(2)
FindAndSetMax( [SMC, SDATA], False )
SMC.GetXaxis().SetTitle("Average Soft Drop Mass")
SMC.GetYaxis().SetTitle("N Events / 5 GeV")
SMC.GetYaxis().SetTitleOffset(1.5)
SMC.GetYaxis().SetLabelSize(SMC.GetYaxis().GetLabelSize()*.9)
SMC.Draw("hist")
SDATA.Draw("samehist")

print SMC.Integral(SMC.FindBin(60), SMC.FindBin(350))
print SDATA.Integral(SDATA.FindBin(60), SDATA.FindBin(350))

leg = TLegend(0.11,0.80,0.89,0.89)
leg.SetNColumns(2)
leg.SetFillStyle(0)
leg.SetFillStyle(0)
leg.SetLineColor(0)
leg.SetLineColor(0)
leg.SetFillColor(4001)

leg.AddEntry(SMC, "QCD MC Signal Region (A)", "F")
leg.AddEntry(SDATA, "Data Signal Region (A)", "PL")
leg.Draw("same")

CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.17
CMS_lumi.CMS_lumi( (C4), 4, 0)
C4.RedrawAxis()

C4.SaveAs("TCutPlots/ADATSMC.png")
