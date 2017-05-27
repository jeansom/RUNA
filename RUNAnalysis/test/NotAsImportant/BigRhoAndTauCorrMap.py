#

import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

import RUNA.RUNAnalysis.Plotting_Header
from RUNA.RUNAnalysis.Plotting_Header import *

import RUNA.RUNAnalysis.scaleFactors
from RUNA.RUNAnalysis.scaleFactors import *

def Make2DPlotOfQCD(H, Cuts, VarX, VarY):
	T = "BoostedAnalysisPlotsPuppi/RUNATree"
	qcdfilestring = "80XRootFilesUpdated/RUNAnalysis_QCDPt"
	qcdfileend = "_80X_V2p3_v06.root"
	qcdfiles = [
				"170to300",
				"300to470",
				"470to600",
				"600to800",
				"800to1000",
				"1000to1400",
				"1400to1800",
				"1800to2400",
				"2400to3200",
				"3200toInf"
				]
	for i in qcdfiles:
		print i
		quick2dplot(qcdfilestring+i+qcdfileend, T, H, VarX, VarY, Cuts, str(scaleFactor(i)))



def GetABCDCorr(Cut, N, P):
	H = TH2F("H"+N, P, 50, 0, 5, 50, 0, 1)
	Make2DPlotOfQCD(H, Cut, "deltaEtaDijet", "prunedMassAsym")
	Ax1 = H.GetXaxis().FindBin(0.)
	Ax2 = H.GetXaxis().FindBin(0.1)
	Ay1 = H.GetYaxis().FindBin(0.)
	Ay2 = H.GetYaxis().FindBin(1.5)
	Bx1 = H.GetXaxis().FindBin(0.)
	Bx2 = H.GetXaxis().FindBin(0.1)
	By1 = H.GetYaxis().FindBin(1.5)
	By2 = H.GetYaxis().FindBin(5.)
	Cx1 = H.GetXaxis().FindBin(0.1)
	Cx2 = H.GetXaxis().FindBin(1.)
	Cy1 = H.GetYaxis().FindBin(0.)
	Cy2 = H.GetYaxis().FindBin(1.5)
	Dx1 = H.GetXaxis().FindBin(0.1)
	Dx2 = H.GetXaxis().FindBin(1.)
	Dy1 = H.GetYaxis().FindBin(1.5)
	Dy2 = H.GetYaxis().FindBin(5.)
	A = H.Integral(Ax1,Ax2,Ay1,Ay2)
	B = H.Integral(Bx1,Bx2,By1,By2)
	C = H.Integral(Cx1,Cx2,Cy1,Cy2)
	D = H.Integral(Dx1,Dx2,Dy1,Dy2)
	if A==0:
		print "A = 0"
	if D==0:
		print "D = 0"

	if not(A==0 or D==0): Bias = 100.*(A - (C*(B/D)))/A
	else: Bias = 0
	return Bias
	

PTTAU = TH2F("mapPTTAU", "", 5, 0, 5, 7, 0, 7)
PTTAU.SetStats(0)
PTTAU.GetXaxis().SetTitle("#tau_{2}/#tau_{1} cut (both jets)")
PTTAU.GetXaxis().SetTitleOffset(1.35)

MTAU = TH2F("mapPTTAU", "", 5, 0, 5, 7, 0, 7)
MTAU.SetStats(0)
MTAU.GetXaxis().SetTitle("#tau_{2}/#tau_{1} cut (both jets)")
MTAU.GetXaxis().SetTitleOffset(1.35)

F = []
taus = [
	["jet1Tau21-DDT_20_tau21<0&jet2Tau21-DDT_20_tau21<0", 45]
#	["jet1Tau21-DDT_jet1Tau21DDT_55<0&jet2Tau21-DDT_jet2Tau21DDT_55<0", 55],
#	["jet1Tau21-DDT_jet1Tau21DDT_65<0&jet2Tau21-DDT_jet2Tau21DDT_65<0", 65],
#	["jet1Tau21-DDT_jet1Tau21DDT_75<0&jet2Tau21-DDT_jet2Tau21DDT_75<0", 75],
#	["jet1Tau21-DDT_jet1Tau21DDT_85<0&jet2Tau21-DDT_jet2Tau21DDT_85<0", 85]
	]

pts = [150., 200., 250., 300., 350., 400., 450.]
ms = [50., 60., 70., 80., 90., 120., 150.]
for i in taus :
	for j in pts :
		print str(i) + " " + str(j)
		C = str(i[0])
		K = str(j)
		A = GetABCDCorr(C+"&jet1Pt>"+K+"&jet2Pt>"+K, str(int(10000*i[1]+j)), "")
		ptN = pts.index(j)
		tauN = taus.index(i)
		PTTAU.Fill(tauN, ptN, A)
		PTTAU.GetXaxis().SetBinLabel(1+ tauN, "< "+ C)
		PTTAU.GetYaxis().SetBinLabel(1 + ptN, "p_{T}> "+ K)
	for j in ms:
		C = str(i[0])
		K = str(j)
		A = GetABCDCorr(C+"&prunedMassAve>"+K, str(int(20000*i[1]+j)), "")
		mN = ms.index(j)
		tauN = taus.index(i)
		MTAU.Fill(tauN, mN, A)
		MTAU.GetXaxis().SetBinLabel(1+ tauN, "< "+ C)
		MTAU.GetYaxis().SetBinLabel(1 + mN, "#hat{m} > "+ K)



C_pttau = TCanvas("pttau", "", 800, 700)
C_pttau
PTTAU.Draw("col text")
C_pttau.Print("pttau_plot.png")


C_mtau = TCanvas("pttau", "", 800, 700)
C_mtau
MTAU.Draw("col text")
C_mtau.Print("mtau_plot.png")
