import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

import RUNA.RUNAnalysis.Plotting_Header
from RUNA.RUNAnalysis.Plotting_Header import *
import RUNA.RUNAnalysis.Distribution_Header
from RUNA.RUNAnalysis.Distribution_Header import *

rootFiles = "v08/"
QCDHT = DIST( "QCDPt", rootFiles+"/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", ".62*puWeight*36555.21/15*lumiWeight")

def Make2DPlotOfQCD(H, Cuts, VarX, VarY):
	T = "BoostedAnalysisPlots/RUNATree"
	qcdfilestring = "v08/RUNAnalysis_QCDPt"
	qcdfileend = "_80X_V2p3_v06.root"
	qcdfiles = [
				"All"
				]
	for i in [QCDHT]:
		quick2dplot(i.File, T, H, VarX, VarY, Cuts, "36555.21/15*puWeight*lumiWeight*.85")


def GetABCDCorr(Cut, N):
	H = TH2F("H"+N, "", 50, 0, 1, 50, 0, 5)
	Make2DPlotOfQCD(H, Cut, "prunedMassAsym", "deltaEtaDijet")
	Ax1 = H.GetXaxis().FindBin(0.)
	Ax2 = H.GetXaxis().FindBin(0.0999999)
	Ay1 = H.GetYaxis().FindBin(0.)
	Ay2 = H.GetYaxis().FindBin(1.4999999)
	A = H.Integral(Ax1,Ax2,Ay1,Ay2)

	Cx1 = H.GetXaxis().FindBin(0.1)
	Cx2 = H.GetXaxis().FindBin(1.)
	Cy1 = H.GetYaxis().FindBin(0.)
	Cy2 = H.GetYaxis().FindBin(1.499999)
	C = H.Integral(Cx1,Cx2,Cy1,Cy2)


	F = []
	P = []
	B = 0
	D = 0
	b = [[1.5,1.99999], [2.0, 2.99999],[3.0,5.0]]
	for i in b:
		B1x1 = H.GetXaxis().FindBin(0.)
		B1x2 = H.GetXaxis().FindBin(0.09999)
		B1y1 = H.GetYaxis().FindBin(i[0])
		B1y2 = H.GetYaxis().FindBin(i[1])
		D1x1 = H.GetXaxis().FindBin(0.1)
		D1x2 = H.GetXaxis().FindBin(1.)
		D1y1 = H.GetYaxis().FindBin(i[0])
		D1y2 = H.GetYaxis().FindBin(i[1])

		B1 = H.Integral(B1x1,B1x2,B1y1,B1y2)
		D1 = H.Integral(D1x1,D1x2,D1y1,D1y2)
		B+= B1
		D+= D1
		F.append(B1/D1)
		P.append((i[1]+i[0])/2.)		

	G = TGraph(len(P), scipy.array(P), scipy.array(F))

	L  = TF1("lin"+N, "[0] +[1]*(x)", 0 , 5)
	G.Fit(L, "B0")
	c = TCanvas("CLOSURE_c"+N, "", 300, 300)
	c.cd()
	G.Draw("AP")
	L.Draw("same")
	c.Print("ccc"+N+".png")

	v = L.Eval(0.75)
	v2 = B/D
	return [A, C, v, v2]

QCD = TH1F("qcd_", "", 60, 50, 350)
quickplot(QCDHT.File, "BoostedAnalysisPlots/RUNATree", QCD, "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&deltaEtaDijet<1.5&prunedMassAsym>0.1", "puWeight*.62*36555.21/15*lumiWeight")
QCD.SetStats(0)
QCD.SetFillStyle(3013)
QCD.SetFillColor(38)
QCD.SetLineColor(38)
QCD.GetXaxis().SetTitle("pruned mass average (GeV)")
QCD.GetYaxis().SetTitle("events")
QCD.GetXaxis().SetTitleOffset(1.3)
QCD.GetYaxis().SetTitleOffset(1.365)

TRUTH = TH1F("est_", "", 60, 50, 350)
quickplot(QCDHT.File, "BoostedAnalysisPlots/RUNATree", TRUTH, "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&deltaEtaDijet<1.5&prunedMassAsym<0.1", "puWeight*.62*36555.21/15*lumiWeight")
TRUTH.SetLineColor(1)
TRUTH.SetFillColor(0)
TRUTH.SetMarkerColor(1)
TRUTH.SetMarkerStyle(20)

Bins = []
BinnedTF = []
BinnedTF2 = []

EtaBins = [["0.0","2.4"]]

masses = []
i = 50
while i < 200:
        masses.append([i,i+25])
        i=i+25
masses.append([200,350])

for j in EtaBins:
	EtaPart = "&((jet1Eta<"+j[1]+"&jet1Eta>"+j[0]+")||(jet1Eta>-"+j[1]+"&jet1Eta<-"+j[0]+"))&((jet2Eta<"+j[1]+"&jet2Eta>"+j[0]+")||(jet2Eta>-"+j[1]+"&jet2Eta<-"+j[0]+"))"
	for i in masses:
		binstart = str(i[0])
		binend = str(i[1])
		Cuts = "prunedMassAve>"+binstart+"&prunedMassAve<"+binend+"&jet1Tau21<0.45&jet2Tau21<0.45"
		TF = GetABCDCorr(Cuts, binstart)
		print " --- " + binstart + " to " + binend + " ---"
		print TF
#		TRUTH.Fill(float((i[0]+i[1])/2), TF[0])
#		QCD.Fill(float((i[0]+i[1])/2), TF[1]*TF[2])
		Bins.append(float((i[0]+i[1])/2))
		BinnedTF.append(TF[2])
		BinnedTF2.append(TF[3])

G = TGraph(len(Bins), scipy.array(Bins), scipy.array(BinnedTF))
for i in xrange(1,QCD.GetNbinsX()+1):
	QCD.SetBinContent(i, QCD.GetBinContent(i)*G.Eval(QCD.GetBinCenter(i)))
G2 = TGraph(len(Bins), scipy.array(Bins), scipy.array(BinnedTF2))
G2.SetLineColor(2)
FindAndSetMax([QCD, TRUTH])
C = TCanvas("C", "", 650, 650)
C.cd()
QCD.Draw("hist")
TRUTH.Sumw2()
TRUTH.Draw("same")
C.Print("CLOSURE_result.png")

C2 = TCanvas("C2", "", 650, 650)
C2.cd()
G.SetMarkerSize(1.5)
G.SetMarkerStyle(21)
G.Draw("AP")
#G2.Draw("L")
C2.Print("CLOSURE_TF.png")






	
