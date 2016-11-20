#!/usr/bin/env python

import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

from RUNA.RUNAnalysis.Plotting_Header import *

gROOT.SetBatch()

def MakePlot(VAR, BINS, CUT, NAME, Title, cutName):
	PlotsQCD = TH1F("QCD_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsSig323 = TH1F("Sig323_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsSig312 = TH1F("Sig312_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsTT = TH1F("TT_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsWJets = TH1F("WJets_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsZJets = TH1F("ZJets_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsWW = TH1F("WW_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsZZ = TH1F("ZZ_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsWZ = TH1F("WZ_"+VAR, "", BINS[0], BINS[1], BINS[2])

	PlotsDATA = TH1F("DATA_"+VAR, "", BINS[0], BINS[1], BINS[2])

	quickplot("RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsSig323, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-100_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsSig312, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTT, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWJets, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsZJets, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWW, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsZZ, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWZ, VAR, CUT, "lumiWeight*puWeight*2666")

	quickplot("RootFiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsDATA, VAR, CUT, "1")
#	PlotsQCD.SetLineColor(9)
#	PlotsWJets.SetLineColor(8)
#	PlotsTT.SetLineColor(2)
#	PlotsSig323.SetLineColor(kViolet)
#	PlotsSig312.SetLineColor(kGray)
	PlotsQCD.SetFillColor(9)
	PlotsQCD.SetLineColor(1)
	PlotsQCD.SetLineWidth(1)
	PlotsTT.SetFillColor(2)
	PlotsTT.SetLineColor(1)
	PlotsTT.SetLineWidth(1)
	PlotsWJets.SetFillColor(8)
	PlotsWJets.SetLineColor(1)
	PlotsWJets.SetLineWidth(1)
	PlotsSig323.SetFillColorAlpha(kGray+3,0.5)
	PlotsSig323.SetLineColor(kViolet+4)
	PlotsSig323.SetFillStyle(3454)
	gStyle.SetHatchesLineWidth(2)
	PlotsSig312.SetFillColorAlpha(kGray+3,0.5)
	PlotsSig312.SetLineColor(13)
	PlotsSig312.SetFillStyle(3445)	
	gStyle.SetHatchesLineWidth(2)

	PlotsDATA.SetLineColor(1)
	PlotsDATA.SetFillColor(0)
	PlotsDATA.SetMarkerColor(1)
	PlotsDATA.SetMarkerStyle(20)

	stackPlots = THStack( "Stack", "" )
	Plots = PlotsQCD.Clone()
	Plots.Reset()
	for i in [PlotsQCD, PlotsTT, PlotsWJets ]:
#	for i in [PlotsQCD, PlotsTT, PlotsWJets, PlotsWW, PlotsWZ, PlotsZZ ]:
		i.SetStats(0)
		i.GetXaxis().SetTitle(Title)
		i.GetYaxis().SetTitle("Events")
		i.SetLineWidth(2)
#		i.Scale(1/i.Integral())
		Plots.Add(i)
		

	PlotsSig323.SetLineWidth(6)
	PlotsSig312.SetLineWidth(6)

	FindAndSetMax([PlotsQCD,PlotsTT,PlotsWJets, PlotsSig323, PlotsSig312, Plots])
	stackPlots.Add(PlotsWJets)
	stackPlots.Add(PlotsTT)
#	stackPlots.Add(PlotsZJets)
#	stackPlots.Add(PlotsWW)
#	stackPlots.Add(PlotsZZ)
#	stackPlots.Add(PlotsWZ)
	stackPlots.Add(PlotsQCD)


#	stackPlots.SetMaximum( stackPlots.GetMaximum() )
	stackPlots.SetMaximum( 15000 )
	stackPlots.SetMinimum( 0.3 )
	leg = TLegend(0.55,0.7,0.89,0.89)
	leg.SetHeader(cutName)
	leg.SetLineColor(0)
	leg.SetFillColor(4001)
	leg.AddEntry(PlotsQCD, "QCD", "F")
	leg.AddEntry(PlotsTT, "t#bar{t}", "F")
	leg.AddEntry(PlotsWJets, "W + Jets", "F")
	leg.AddEntry(PlotsSig323, "RPV UDD323 Signal, M=100 GeV", "F")
	leg.AddEntry(PlotsSig312, "RPV UDD312 Signal, M=100 GeV", "F")
#	leg.AddEntry(PlotsDATA, "Data", "PL")

	C = TCanvas("C"+VAR+CUT, "", 800, 800)
#	C.cd()
#	C.SetLogy()
	pad1 = TPad( "pad1", "", 0, 0.15, 1, 1 )
	pad2 = TPad( "pad2", "", 0, 0, 1.0, 0.23 )
	pad1.Draw()
	pad2.Draw()
	pad1.cd()
	pad1.SetLogy()
#	FindAndSetMax( [stackPlots] )

	stackPlots.Draw("hist")
#	stackPlots.GetXaxis().SetTitle(cutName)
	stackPlots.GetYaxis().SetTitle("Events" )
#	stackPlots.GetXaxis().SetLabelSize(0)
#	stackPlots.GetXaxis().SetLabelOffset(999)
#	PlotsDATA.Draw("hist same")
#	PlotsQCD.Draw("hist")
#	for i in [PlotsTT, PlotsWJets, PlotsSig323, PlotsSig312]:
#		i.Draw("hist same")
#	PlotsQCD.Draw("hist")
	PlotsSig323.Draw("hist same")
	PlotsSig312.Draw("hist same")
#	PlotsTT.Draw("hist same")
	leg.Draw("same")

	pad2.cd()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	SOverSqrtBUDD312 = TH1F("SOverSqrtBUDD312", "", BINS[0], BINS[1], BINS[2])
	SOverSqrtBUDD323 = TH1F("SOverSqrtBUDD323", "", BINS[0], BINS[1], BINS[2])
	for b in xrange( BINS[0] ):
		signalUDD312 = PlotsSig312.GetBinContent(b)
		signalUDD323 = PlotsSig323.GetBinContent(b)
		bkg = Plots.GetBinContent(b)
		try:
			SBUDD312 = float(signalUDD312)/math.sqrt(bkg)
		except ZeroDivisionError: continue
		try:
			SBUDD323 = float(signalUDD323)/math.sqrt(bkg)
		except ZeroDivisionError: continue
		SOverSqrtBUDD312.SetBinContent(b,SBUDD312)
		SOverSqrtBUDD323.SetBinContent(b,SBUDD323)

	SOverSqrtBUDD312.Draw("histe")
	SOverSqrtBUDD323.Draw("samehiste")

	SOverSqrtBUDD323.SetFillColorAlpha(kGray+3,0.5)
	SOverSqrtBUDD323.SetLineColor(kViolet+4)
	SOverSqrtBUDD323.SetLineWidth(2)
	SOverSqrtBUDD323.SetFillStyle(3454)
	gStyle.SetHatchesLineWidth(2)
	SOverSqrtBUDD312.SetFillColorAlpha(kGray+3,0.5)
	SOverSqrtBUDD312.SetLineColor(13)
	SOverSqrtBUDD312.SetLineWidth(2)
	SOverSqrtBUDD312.SetFillStyle(3445)	
	SOverSqrtBUDD312.GetXaxis().SetTitle(cutName)
	SOverSqrtBUDD312.GetXaxis().SetTitleSize(0.12)
	SOverSqrtBUDD312.GetXaxis().SetLabelSize(0.12)
	SOverSqrtBUDD312.GetYaxis().SetTitle("S / #sqrt{B}")	
	SOverSqrtBUDD312.GetYaxis().SetLabelSize(0.12)	
	SOverSqrtBUDD312.GetYaxis().SetTitleSize(0.12)
	SOverSqrtBUDD312.GetYaxis().SetTitleOffset(0.45)
	SOverSqrtBUDD312.GetYaxis().CenterTitle()
	gStyle.SetHatchesLineWidth(2)

	FindAndSetMax( [ SOverSqrtBUDD312, SOverSqrtBUDD323 ], False )
	
	SOverSqrtBUDD312.Draw("hist")
	SOverSqrtBUDD323.Draw("samehist")
	C.SaveAs("TCutPlots/"+NAME+".png")

	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print ""
	print ""


onlysubjet11 = "(subjet11btagCSVv2>=0.8&subjet12btagCSVv2<0.8&subjet21btagCSVv2<0.8&subjet22btagCSVv2<0.8)"
onlysubjet12 = "(subjet11btagCSVv2<0.8&subjet12btagCSVv2>=0.8&subjet21btagCSVv2<0.8&subjet22btagCSVv2<0.8)"
onlysubjet21 = "(subjet11btagCSVv2<0.8&subjet12btagCSVv2<0.8&subjet21btagCSVv2>=0.8&subjet22btagCSVv2<0.8)"
onlysubjet22 = "(subjet11btagCSVv2<0.8&subjet12btagCSVv2<0.8&subjet21btagCSVv2<0.8&subjet22btagCSVv2>=0.8)"

only11and21 =  "(subjet11btagCSVv2>=0.8&subjet12btagCSVv2<0.8&subjet21btagCSVv2>=0.8&subjet22btagCSVv2<0.8)"
only11and22 = "(subjet11btagCSVv2>=0.8&subjet12btagCSVv2<0.8&subjet21btagCSVv2<0.8&subjet22btagCSVv2>=0.8)"
only12and21 = "(subjet11btagCSVv2<0.8&subjet12btagCSVv2>=0.8&subjet21btagCSVv2>=0.8&subjet22btagCSVv2<0.8)"
only21and22 = "(subjet11btagCSVv2<0.8&subjet12btagCSVv2>=0.8&subjet21btagCSVv2<0.8&subjet22btagCSVv2>=0.8)"

zerobtag = "(subjet11btagCSVv2<0.8&subjet12btagCSVv2<0.8&subjet21btagCSVv2<0.8&subjet22btagCSVv2<0.8)"
onebtag = "("+onlysubjet11+"||"+onlysubjet12+"||"+onlysubjet21+"||"+onlysubjet22+")"
twobtag = "("+only11and21+"||"+only11and22+"||"+only12and21+"||"+only21and22+")"

zeroTop = "(jet1Tau32>0.51&jet2Tau32>.51)"
oneTop = "((jet1Tau32<=0.51&jet2Tau32>=0.51)||(jet1Tau32>0.51&jet2Tau32<0.51))"
twoTop = "(jet1Tau32<0.51&jet2Tau32<0.51)"


MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+zerobtag+"&"+zeroTop, "prunedMassAveb0t0", "prunedMassAve", "Average Pruned Mass")
MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+onebtag+"&"+zeroTop, "prunedMassAveb1t0", "prunedMassAve", "Average Pruned Mass")
MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+twobtag+"&"+zeroTop, "prunedMassAveb2t0", "prunedMassAve", "Average Pruned Mass")
MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+zerobtag+"&"+oneTop, "prunedMassAveb0t1", "prunedMassAve", "Average Pruned Mass")
MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+onebtag+"&"+oneTop, "prunedMassAveb1t1", "prunedMassAve", "Average Pruned Mass")
MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+twobtag+"&"+oneTop, "prunedMassAveb2t1", "prunedMassAve", "Average Pruned Mass")
MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+zerobtag+"&"+twoTop, "prunedMassAveb0t2", "prunedMassAve", "Average Pruned Mass")
MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+onebtag+"&"+twoTop, "prunedMassAveb1t2", "prunedMassAve", "Average Pruned Mass")
MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+twobtag+"&"+twoTop, "prunedMassAveb2t2", "prunedMassAve", "Average Pruned Mass")
