import os
import ROOT
from ROOT import *
from array import array
import math
from math import *
import sys
import scipy
import RUNA.RUNAnalysis.Plotting_Header
from RUNA.RUNAnalysis.Plotting_Header import *
import RUNA.RUNAnalysis.scaleFactors
from RUNA.RUNAnalysis.scaleFactors import *

def ComputeDDT(name, point, nPtBins, nRhoBins, H):
	DDT = TH2F(name, "", nRhoBins, -60, 60, nPtBins, 150, 1200)
	DDT.SetStats(0)
	nXb = H.GetXaxis().GetNbins()
	nYb = H.GetYaxis().GetNbins()
	for x in range(nXb):
		for y in range(nYb):
			proj = H.ProjectionZ("H3"+str(x)+str(y),x+1,x+1,y+1,y+1)
			p = array('d', [point])
			q = array('d', [0.0]*len(p))
			proj.GetQuantiles(len(p), q, p)
			DDT.SetBinContent( x+1, y+1, q[0] )
	return DDT

def DisplayDDT(DDT):
	gStyle.SetNumberContours(5)
	C = TCanvas("TempCanvas", "Title", 820, 640)
	C.cd()
	DDT.SetStats(0)
	DDT.GetXaxis().SetTitle("Average Mass")
	DDT.GetYaxis().SetTitle("Average p_{T}")
	DDT.GetYaxis().SetTitleOffset(1.35)
	DDT.SetLineColor(kBlack)
	DDT.Draw("COLZ")
	DDT.Draw("CONT3 same")
	C.Print("DDT_Map_jet1Tau21DDT.png")

def DrawRho(DDT):
	C = TCanvas("TempCanvas", "Title", 820, 640)
	GA = []
	rho = 0.001
	while rho <= 0.3:
		x = []
		y = []
		for i in xrange(1,DDT.GetXaxis().GetNbins()+1):
			for j in xrange(1,DDT.GetYaxis().GetNbins()+1):
				m = DDT.GetXaxis().GetBinCenter(i)
				pT = DDT.GetYaxis().GetBinCenter(j)
				if ((m*m)/(pT*pT) < (rho+0.001)) and ((m*m)/(pT*pT)>(rho-0.001)):
					print "rho: " + str(rho) + ", m: " + str(m) + ", pT: " + str(pT)
					x.append(float(m))
					y.append(float(pT))
		if len(x)!=0: GA.append(TGraph(len(x),scipy.array(x), scipy.array(y) ))
		if rho == 0.001: rho = 0.009
		else: rho = rho+0.02
	DDT.Draw("COL")
	for i in xrange(len(GA)):
		if i%4 == 0: GA[i].SetLineColor(kRed)
		if i%4 == 1: GA[i].SetLineColor(kYellow)
		if i%4 == 2: GA[i].SetLineColor(kViolet)
		GA[i].Draw("C")
	C.SaveAs("DDT_Map_jet1Tau21DDT.png")
def FriendTree(DDT, Bkgs):
	for B in Bkgs:
		F = TFile(B[0])
		T1 = F.Get("BoostedAnalysisPlotsPuppi/RUNATree")
		n = T1.GetEntries()

		print '-'*40
		print '------> ', B[1]
		print '------> Number of events: ' + str(n)
		d = 0
		
		NAMEF = B[0].replace(".root","")
		FF = TFile(NAMEF+"_friendDDT_jet1Tau21DDT.root", "RECREATE")
		TF = TTree("RUNATreeFriend", "")
		TF.SetName("TF_jet1Tau21DDT")
		DDTVal = array( 'd', [0] )
		TF.Branch("DDT_jet1Tau21DDT", DDTVal, "DDT/D")
		for j in range(0,n):
			T1.GetEntry(j)
			fraction = 10.*j/(1.*n)
			if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
			d = TMath.FloorNint(fraction)
			
			PT = (T1.jet1Pt)
#			PRERHO = (T1.jet1PrunedMass*T1.jet1PrunedMass/(T1.jet1Pt*T1.jet1Pt))*(T1.jet2PrunedMass*T1.jet2PrunedMass/(T1.jet2Pt*T1.jet2Pt))
			PRERHO = (T1.jet1PrunedMass*T1.jet1PrunedMass/(T1.jet1Pt*T1.jet1Pt))
			if PRERHO <= 0: RHO = 0
			else: RHO = log(PRERHO)
#			RHO = T1.prunedMassAve
			rind = DDT.GetXaxis().FindBin(RHO)
			pind = DDT.GetYaxis().FindBin(PT)
			
			if RHO >  DDT.GetXaxis().GetBinUpEdge( DDT.GetXaxis().GetNbins() ) :
				rind = DDT.GetXaxis().GetNbins()
			if RHO <  DDT.GetXaxis().GetBinLowEdge( 1 ) :
				rind = 1 
			if PT >  DDT.GetYaxis().GetBinUpEdge( DDT.GetYaxis().GetNbins() ) :
				pind = DDT.GetYaxis().GetNbins()
			if PT < DDT.GetYaxis().GetBinLowEdge( 1 ) :
				pind = 1
			DDTVal[0] = DDT.GetBinContent(rind,pind)
			TF.Fill()
		TF.Write("",TObject.kOverwrite)
		FF.Close()
		
RB = 15
PB = 15
H3 = TH3F("H3", "", RB, -60, 60, PB, 150, 1200, 500, 0, 1.0)
H3.SetStats(0)
Bkgs =[]
for i in [ "QCDPt170to300", "QCDPt300to470", "QCDPt470to600", "QCDPt600to800", "QCDPt800to1000", "QCDPt1000to1400", "QCDPt1400to1800", "QCDPt1800to2400", "QCDPt2400to3200", "QCDPt3200toInf" ]:
	Bkgs.append(["80XRootFilesUpdated/RUNAnalysis_"+i+"_80X_V2p3_v06.root", i])

print '*'*20+"MAKING HISTO"+'*'*20
PT = "(jet1Pt)"
#RHO = "log(jet1PrunedMass*jet1PrunedMass/(jet1Pt*jet1Pt))+log(jet2PrunedMass*jet2PrunedMass/(jet2Pt*jet2Pt))"
RHO = "log(jet1PrunedMass*jet1PrunedMass/(jet1Pt*jet1Pt))"
#RHO = "prunedMassAve"
#TAU21 = "(jet1Tau21+jet2Tau21)/2"
TAU21 = "jet1Tau21"
for B in Bkgs:
	weight = "puWeight*"+str(scaleFactor(B[1]))+"*36555.21/15"
	quick3dplot(B[0], "BoostedAnalysisPlotsPuppi/RUNATree", H3, RHO, PT, TAU21, "jet1Tau21>0.", weight)
print '*'*20+"COMPUTING DDT"+'*'*20
#DDT = ComputeDDT("DDT", 0.185312444484, PB, RB, H3) #ave
DDT = ComputeDDT("DDT", 0.187840180174, PB, RB, H3) #jet1
#DDT = ComputeDDT("DDT", 0.182784721132, PB, RB, H3) #jet2
#DDT = ComputeDDT("DDT", 0.7, PB, RB, H3)
DisplayDDT(DDT)

print '*'*20+"MAKING FRIEND"+'*'*20
for i in [ "RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root" ]:
	Bkgs.append(["80XRootFilesUpdated/"+i, i])
for i in [ "M-120", "M-180", "M-200", "M-220", "M-300" ]:
	Bkgs.append(["80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_"+i+"_80X_V2p3_v06.root", i])
FriendTree(DDT, Bkgs)

Fout = TFile("PhotonDDTs_jet1Tau21DDT.root", "recreate")
Fout.cd()
DDT.Write()
Fout.Close()

