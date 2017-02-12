#!/usr/bin/env python

import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

from RUNA.RUNAnalysis.Plotting_Header import *
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 

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

	quickplot("RootFiles/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsSig323, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-100_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsSig312, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTT, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWJets, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsZJets, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWW, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsZZ, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWZ, VAR, CUT, "lumiWeight*puWeight*2666")

	quickplot("RootFiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsDATA, VAR, CUT, "1/(1.829+exp(0.3742-3.046e-07*prunedMassAve*prunedMassAve*prunedMassAve))" )

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
	PlotsWZ.Add(PlotsZJets)
	PlotsWZ.Add(PlotsWW)
	PlotsWZ.Add(PlotsZZ)
	
#	PlotsZJets.SetFillColor(800)
#	PlotsZJets.SetLineColor(800)
#	PlotsZJets.SetLineWidth(0)
	PlotsWZ.SetFillColor(800)
	PlotsWZ.SetLineColor(1)
	PlotsWZ.SetLineWidth(1)
#	PlotsWW.SetFillColor(800)
##	PlotsWW.SetLineColor(800)
#	PlotsWW.SetLineWidth(0)
#	PlotsZZ.SetFillColor(800)
##	PlotsZZ.SetLineColor(800)
#	PlotsZZ.SetLineWidth(0)

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
#	for i in [PlotsQCD, PlotsTT, PlotsWJets ]:
	for i in [PlotsQCD, PlotsTT, PlotsWJets, PlotsWW, PlotsWZ, PlotsZZ ]:
		i.SetStats(0)
		i.GetXaxis().SetTitle(Title)
		i.GetYaxis().SetTitle("Events")
		i.SetLineWidth(2)
#		i.Scale(1/i.Integral())
		Plots.Add(i)
		
	B = Plots.Integral(-90, 110)
	S = PlotsSig323.Integral(-90,110)
	print "***********************"
	print S/math.sqrt(B)
	print "***********************"
	PlotsSig323.SetLineWidth(6)
	PlotsSig312.SetLineWidth(6)
	FindAndSetMax([PlotsQCD,PlotsTT,PlotsWJets, PlotsSig323, PlotsSig312, Plots])
	FindAndSetMax([PlotsWJets])
#	stackPlots.Add(PlotsZJets)
#	stackPlots.Add(PlotsWW)
#	stackPlots.Add(PlotsZZ)
	stackPlots.Add(PlotsWZ)
	stackPlots.Add(PlotsWJets)
	stackPlots.Add(PlotsTT)
	stackPlots.Add(PlotsQCD)



	stackPlots.SetMaximum( max(PlotsDATA.GetMaximum(), stackPlots.GetMaximum())*10 )
#	stackPlots.SetMaximum( PlotsDATA.GetMaximum() )

#	stackPlots.SetMaximum( PlotsWJets.GetMaximum() )
	stackPlots.SetMinimum( .5 )
#	leg = TLegend(0.55,0.7,0.89,0.89)

	leg = TLegend(0.15,0.80,0.85,0.89)
#	leg.SetHeader(cutName)
	leg.SetNColumns(2)
	leg.SetLineColor(0)
	leg.SetFillStyle(0)
	leg.AddEntry(PlotsQCD, "QCD", "F")
	leg.AddEntry(PlotsTT, "t#bar{t}", "F")
	leg.AddEntry(PlotsWJets, "W + Jets", "F")
	leg.AddEntry(PlotsWZ, "Other", "F")
	leg.AddEntry(PlotsSig323, "RPV UDD323 Signal, M=100 GeV", "F")
#	leg.AddEntry(PlotsSig312, "RPV UDD312 Signal, M=100 GeV", "F")
	leg.AddEntry(PlotsDATA, "Data", "PL")

	C = TCanvas("C"+VAR+CUT, "", 800, 800)
#	C.cd()
#	C.SetLogy()
#	pad1 = TPad( "pad1", "", 0, 0.15, 1, 1 )
	pad1 = TPad( "pad1", "", 0, 0, 1, 1 )
#	pad2 = TPad( "pad2", "", 0, 0, 1.0, 0.23 )
	pad1.Draw()
#	pad2.Draw()
	pad1.cd()
#	FindAndSetMax( [stackPlots] )

#	stackPlots.Draw()
#	stackPlots.GetXaxis().SetTitle(cutName)
#	stackPlots.GetYaxis().SetTitle("Events / 10" )
#	stackPlots.GetYaxis().SetTitleOffset(1.3)
#	stackPlots.Draw("hist")
	PlotsDATA.SetStats(0)
	PlotsDATA.Draw("E0")
	PlotsDATA.GetXaxis().SetTitle(cutName)
	PlotsDATA.GetYaxis().SetTitle("Events")
	pad1.SetLogy()
		
#	PlotsQCD.Draw("hist")
#	for i in [PlotsTT, PlotsWJets, PlotsSig323, PlotsSig312]:
#		i.Draw("hist same")
#	PlotsQCD.Draw("hist")
#	PlotsSig323.Draw("hist same")
#	PlotsSig312.Draw("hist same")
#	PlotsTT.Draw("hist same")
#	PlotsTT.Draw("hist same")
#	latex = TLatex()
#	latex.SetNDC()
#	latex.SetTextSize(0.025)
#	latex.SetTextAlign(13)
#	latex.DrawLatex(.6, .88, NAME )
#	latex.SetTextSize(0.02)
#	latex.DrawLatex(.63, .85, "#color[1]{Data}")
#	latex.DrawLatex(.63, .83, "#color[9]{QCD}")
#	latex.DrawLatex( .63, .81, "#color[2]{t#bar{t}}" )
#	latex.DrawLatex( .63, .79, "#color[4]{W + Jets}" )
#	latex.DrawLatex( .63, .77, "#color[800]{Z + Jets}" )
#	latex.DrawLatex( .63, .75, "#color[616]{WW}" )
#	latex.DrawLatex( .63, .73, "#color[803]{ZZ}" )
#	latex.DrawLatex( .63, .71, "#color[432]{WZ}" )
#	latex.DrawLatex(.63, .69, "#color[884]{RPV Stop, UDD323, M=100 GeV}" ) 
#	latex.DrawLatex( .63, .67, "#color[13]{RPV Stop, UDD312, M=100 GeV}" )
	CMS_lumi.extraText = "Preliminary"
	CMS_lumi.relPosX = 0.14
	CMS_lumi.CMS_lumi( (pad1), 4, 0)
	pad1.RedrawAxis()
#	leg.Draw("same")
	'''
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
	'''
	C.SaveAs("TCutPlots/"+NAME+".png")

	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print ""
	print ""


btag1 = "(subjet11btagCMVAv2>0.185||subjet12btagCMVAv2>0.185)"
btag2 = "(subjet21btagCMVAv2>0.185||subjet22btagCMVAv2>0.185)"
nobtag1 = "(subjet11btagCMVAv2<0.185&subjet12btagCMVAv2<0.185)"
nobtag2 = "(subjet21btagCMVAv2<0.185&subjet22btagCMVAv2<0.185)"
onebtag1 = "("+btag1+"&"+nobtag2+")"
onebtag2 = "("+nobtag1+"&"+btag2+")"

#zerobtag = nobtag1+"&"+nobtag2
#onebtag = onebtag1+"||"+onebtag2
#twobtag = btag1+"&"+btag2

zerobtag = "(jet1btagCSVv2<0.800&jet2btagCSVv2<0.800)"
onebtag = "((jet1btagCSVv2<0.800&jet2btagCSVv2>0.800)||(jet1btagCSVv2>0.800&jet2btagCSVv2<0.800))"
twobtag = "(jet1btagCSVv2>0.800&jet2btagCSVv2>0.800)"
#twobtag = "(jet1btagCMVAv2>0.185&jet2btagCMVAv2>0.185)"

zeroTop = "(jet1Tau32>0.51&jet2Tau32>.51)"
oneTop = "((jet1Tau32<=0.51&jet2Tau32>=0.51)||(jet1Tau32>0.51&jet2Tau32<0.51))"
twoTop = "(jet1Tau32<0.51&jet2Tau32<0.51)"

jet1Top = "((jet1Tau32>0.51&jet2Tau32<0.51))"
jet2Top = "((jet1Tau32<0.51&jet2Tau32>0.51))"
jet1btag = "((jet1btagCSVv2>0.800&jet2btagCSVv2<0.800))"
jet2btag = "((jet1btagCSVv2<0.800&jet2btagCSVv2>0.800))"

MakePlot("prunedMassAve", [58, 60, 350], "jet1Tau21<0.45&jet2Tau21<0.45&deltaEtaDijet<1.5&prunedMassAsym>0.1", "prunedMassAve", "prunedMassAve", "Average Pruned Mass")
#MakePlot( "jet1Pt", [ 2000 , 0, 2000 ], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+zerobtag+"&"+oneTop, "jet1Ptb0t1", "jet1Pt", "Leading Jet pT" )
#MakePlot( "jet2Pt", [ 2000 , 0, 2000 ], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+zerobtag+"&"+oneTop, "jet2Ptb0t1", "jet2Pt", "2nd Leading Jet pT" )
#MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+onebtag+"&"+oneTop, "prunedMassAveb1t1A", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym>0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+ "( ("+jet1Top+"&"+jet2btag+")||("+jet2Top+"&"+jet1btag+") )", "prunedMassAveb2t0C", "prunedMassAve", "Average Pruned Mass")
#for i in [ ["b0t0", "("+zerobtag+"&"+zeroTop+")"], ["b1t0", "("+onebtag+"&"+zeroTop+")"], ["b2t0", "("+twobtag+"&"+zeroTop+")"], ["b0t1", "("+zerobtag+"&"+oneTop+")"], ["b1t1", "("+onebtag+"&"+oneTop+")"], ["b2t1", "("+twobtag+"&"+oneTop+")"], ["b0t2", "("+zerobtag+"&"+twoTop+")"], ["b1t2", "("+onebtag+"&"+twoTop+")"], ["b2t2", "("+twobtag+"&"+twoTop+")"] ]:
#	MakePlot("prunedMassAve", [29, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+ i[1], "prunedMassAve"+i[0]+"A", "prunedMassAve", "Average Pruned Mass")
#	MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet>1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+i[1], "prunedMassAve"+i[0]+"B", "prunedMassAve", "Average Pruned Mass")
#	MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym>0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+i[1], "prunedMassAve"+i[0]+"C", "prunedMassAve", "Average Pruned Mass")
#	MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym>0.1&deltaEtaDijet>1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+i[1], "prunedMassAve"+i[0]+"D", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [29, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&jet1btagCSVv2>0.8&jet2btagCSVv2>0.8&jet1Tau32>0.51&jet2Tau32>0.51", "prunedMassAveCSVv2A", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [29, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&jet1btagCMVAv2>0.185&jet2btagCMVAv2>0.185&jet1Tau32>0.51&jet2Tau32>0.51", "prunedMassAveCMVAv2A", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet>1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+twobtag+"&"+zeroTop, "prunedMassAveb2t0B", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym>0.1&deltaEtaDijet>1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+twobtag+"&"+zeroTop, "prunedMassAveb2t0D", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [58, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet>1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+zerobtag+"&"+zeroTop, "prunedMassAveb0t0B", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+onebtag+"&"+zeroTop, "prunedMassAveb1t0", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+twobtag+"&"+zeroTop, "prunedMassAveb2t0", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+zerobtag+"&"+oneTop, "prunedMassAveb0t1", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+onebtag+"&"+oneTop, "prunedMassAveb1t1", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+twobtag+"&"+oneTop, "prunedMassAveb2t1", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+zerobtag+"&"+twoTop, "prunedMassAveb0t2", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [29, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+onebtag+"&"+twoTop, "prunedMassAveb1t2", "prunedMassAve", "Average Pruned Mass")
#MakePlot("prunedMassAve", [58, 60, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6"+"&"+twobtag+"&"+twoTop, "prunedMassAveb2t2", "prunedMassAve", "Average Pruned Mass")
#MakePlot("jet1Tau32", [20, 0, 1], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6", "jet1Tau32", "jet1Tau32", "Leading Jet Tau32")
#MakePlot("jet2Tau32", [20, 0, 1], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet2Tau21<0.6&jet2Tau21<0.6", "jet2Tau32", "jet2Tau32", "2nd Leading Jet Tau32")

