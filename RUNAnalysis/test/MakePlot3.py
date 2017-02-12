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

#	MCScale = "36.6*2.74297e-01*1000./15."
	MCScale = "36.6/15*1000"

#	quickplot("80XRootFiles/RUNBoostedAnalysis_QCD_PtAllv03.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "lumiWeight*puWeight*"+MCScale+"*1000.*.77")

	quickplot("RootFiles/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "lumiWeight*2666*.77")
	quickplot("RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsSig323, VAR, CUT, "lumiWeight*2666")
	quickplot("RootFiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-100_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsSig312, VAR, CUT, "lumiWeight*2666")
	quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTT, VAR, CUT, "lumiWeight*2666")
	quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWJets, VAR, CUT, "lumiWeight*2666")
	quickplot("RootFiles/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsZJets, VAR, CUT, "lumiWeight*2666")
	quickplot("RootFiles/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWW, VAR, CUT, "lumiWeight*2666")
	quickplot("RootFiles/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsZZ, VAR, CUT, "lumiWeight*2666")
	quickplot("RootFiles/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWZ, VAR, CUT, "lumiWeight*2666")

	quickplot("RootFiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsDATA, VAR, CUT, "1" )

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
	PlotsZJets.SetFillColor(800)
	PlotsZJets.SetLineColor(1)
	PlotsZJets.SetLineWidth(1)
#	PlotsWZ.SetFillColor(432)
#	PlotsWZ.SetLineColor(1)
#	PlotsWZ.SetLineWidth(1)
	PlotsWW.SetFillColor(616)
	PlotsWW.SetLineColor(1)
	PlotsWW.SetLineWidth(1)
	PlotsZZ.SetFillColor(803)
	PlotsZZ.SetLineColor(1)
	PlotsZZ.SetLineWidth(1)
	
	bin1 = PlotsQCD.FindBin(60)
	bin2 = PlotsQCD.FindBin(350)
	print "---------------------------------"
	print PlotsQCD.Integral(bin1, bin2)
	print PlotsTT.Integral(bin1, bin2)
	print PlotsWJets.Integral(bin1, bin2)
	print PlotsZJets.Integral(bin1, bin2)
	print PlotsWW.Integral(bin1, bin2)
	print PlotsZZ.Integral(bin1, bin2)
	print PlotsDATA.Integral(bin1, bin2)
	print "---------------------------------"
 
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

	PlotsBkg = PlotsQCD.Clone()
	PlotsBkg.Reset()
	PlotsBkg.Add(PlotsQCD)
	PlotsBkg.Add(PlotsTT)
	PlotsBkg.Add(PlotsWJets)
	PlotsBkg.Add(PlotsZJets)
	PlotsBkg.Add(PlotsWW)
	PlotsBkg.Add(PlotsZZ)

	stackPlots = THStack( "Stack", "" )
	Plots = PlotsQCD.Clone()
	Plots.Reset()
	for i in [PlotsQCD, PlotsTT, PlotsWJets ]:
#	for i in [PlotsQCD, PlotsTT, PlotsWJets, PlotsWW, PlotsZZ ]:
		i.SetStats(0)
		i.GetXaxis().SetTitle(Title)
		i.GetYaxis().SetTitle("Events/10 GeV")
		i.SetLineWidth(2)
#		i.Scale(1/i.Integral())
		Plots.Add(i)
		

	PlotsSig323.SetLineWidth(6)
#	PlotsSig312.SetLineWidth(6)
	FindAndSetMax([PlotsQCD,PlotsTT,PlotsWJets, PlotsSig323, Plots])
#	FindAndSetMax([PlotsWJets])
	stackPlots.Add(PlotsZJets)
	stackPlots.Add(PlotsWW)
	stackPlots.Add(PlotsZZ)
	stackPlots.Add(PlotsWZ)
	stackPlots.Add(PlotsWJets)
	stackPlots.Add(PlotsTT)
	stackPlots.Add(PlotsQCD)


	stackPlots.SetMaximum( max(PlotsSig323.GetMaximum(), stackPlots.GetMaximum())*1.35 )
#	stackPlots.SetMaximum( PlotsDATA.GetMaximum() )

#	stackPlots.SetMaximum( PlotsWJets.GetMaximum() )
	stackPlots.SetMinimum( 0.5 )
#	leg = TLegend(0.55,0.7,0.89,0.89)

	leg = TLegend(0.15,0.80,0.95,0.89)
	leg.SetNColumns(2)
	leg.SetTextSize(0.03)
	leg.SetFillStyle(0)
#	leg.SetHeader(cutName)
	leg.SetLineColor(0)
	leg.SetFillColor(4001)
	leg.AddEntry(PlotsQCD, "QCD", "F")
	leg.AddEntry(PlotsTT, "t#bar{t}", "F")
	leg.AddEntry(PlotsWJets, "W + Jets", "F")
#	leg.AddEntry(PlotsSig323, "RPV UDD323 Signal, M=100 GeV", "F")
#	leg.AddEntry(PlotsSig312, "RPV UDD312 Signal, M=100 GeV", "F")
	leg.AddEntry(PlotsDATA, "Data", "PL")

	C = TCanvas("C"+VAR+CUT, "", 800, 800)
#	C.cd()
#	C.SetLogy()
#	pad1 = TPad( "pad1", "", 0, 0.15, 1, 1 )
	pad1 = TPad( "pad1", "", 0, 0.10, 1, 1 )
	pad2 = TPad( "pad2", "", 0, 0, 1.0, 0.20 )
	pad1.Draw()
	pad2.Draw()
	pad1.cd()
#	FindAndSetMax( [stackPlots] )
	stackPlots.Draw()
#	stackPlots.SetMaximum(500e03)
#	stackPlots.GetXaxis().SetTitle(cutName)
	stackPlots.GetYaxis().SetTitle("Events / 10 GeV" )
	stackPlots.GetYaxis().SetTitleOffset(1.3)
	stackPlots.GetXaxis().SetTitle("")
	stackPlots.GetXaxis().SetLabelSize(0)
	stackPlots.Draw("hist")
	PlotsDATA.SetStats(0)
	PlotsDATA.Draw("E0same")
#	PlotsDATA.GetXaxis().SetTitle(cutName)
#	PlotsDATA.GetYaxis().SetTitle("Events")
	pad1.SetLogy()
#	pad1.SetLogx()
#	PlotsQCD.Draw("hist")
#	for i in [PlotsTT, PlotsWJets, PlotsSig323, PlotsSig312]:
#		i.Draw("hist same")
#	PlotsQCD.Draw("hist")
#	PlotsSig323.Draw("samehist")
	CMS_lumi.extraText = "Simulation Preliminary"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi( (pad1), 4, 0)
	pad1.RedrawAxis()
#	PlotsSig312.Draw("hist same")
#	PlotsTT.Draw("hist same")
#	PlotsTT.Draw("hist same")
	'''
	leg2 = TLegend(0.15,0.80,0.95,0.89)
	leg2.SetNColumns(2)
	leg2.SetTextSize(0.03)
	leg2.SetLineColor(0)
	leg2.SetFillColor(0)
	leg2.SetFillStyle(0)
	leg2.AddEntry(V, "All SM Bkg from MC", "PL")
	leg2.AddEntry( N1, "QCD Est from MC", "F")
	leg2.AddEntry( Est.hists_MSR_SUB[0], "W + Jets", "F")
	leg2.AddEntry( Est.hists_MSR_SUB[1], "t #bar{t} + Jets", "F")

	latex = TLatex()
	latex.SetNDC()
	latex.SetTextSize(0.025)
	latex.SetTextAlign(13)
	latex.DrawLatex(.6, .88, NAME )
	latex.SetTextSize(0.02)
	latex.DrawLatex(.63, .85, "#color[1]{Data}")
	latex.DrawLatex(.63, .83, "#color[9]{QCD}")
	latex.DrawLatex( .63, .81, "#color[2]{t#bar{t}}" )
	latex.DrawLatex( .63, .79, "#color[4]{W + Jets}" )
	latex.DrawLatex( .63, .77, "#color[800]{Z + Jets}" )
	latex.DrawLatex( .63, .75, "#color[616]{WW}" )
	latex.DrawLatex( .63, .73, "#color[803]{ZZ}" )
#	latex.DrawLatex( .63, .71, "#color[432]{WZ}" )
	latex.DrawLatex(.63, .69, "#color[884]{RPV Stop, UDD323, M=100 GeV}" ) 
	latex.DrawLatex( .63, .67, "#color[13]{RPV Stop, UDD312, M=100 GeV}" )
	'''
	leg.Draw("same")

	pad2.cd()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	pad2.Draw()
#	SOverSqrtBUDD312 = TH1F("SOverSqrtBUDD312", "", BINS[0], BINS[1], BINS[2])
	SOverSqrtBUDD323 = TH1F("SOverSqrtBUDD323", "", BINS[0], BINS[1], BINS[2])
	for b in xrange( BINS[0] ):
#		signalUDD312 = PlotsSig312.GetBinContent(b)
		signalUDD323 = PlotsDATA.GetBinContent(b)
		bkg = Plots.GetBinContent(b)
#		try:
#			SBUDD312 = float(signalUDD312)/math.sqrt(bkg)
#		except ZeroDivisionError: continue
		try:
			SBUDD323 = float(signalUDD323)/float(bkg)
		except ZeroDivisionError: continue
#		SOverSqrtBUDD312.SetBinContent(b,SBUDD312)
		SOverSqrtBUDD323.SetBinContent(b,SBUDD323)

#	SOverSqrtBUDD312.Draw("histe")
	SOverSqrtBUDD323.GetXaxis().SetTitle(cutName)
	SOverSqrtBUDD323.GetYaxis().SetTitle("DATA/MC")
	SOverSqrtBUDD323.GetXaxis().SetLabelSize(.12)
	SOverSqrtBUDD323.GetXaxis().SetTitleSize(.12)
	SOverSqrtBUDD323.GetYaxis().SetTitleOffset(.3)
	SOverSqrtBUDD323.GetYaxis().SetLabelSize(.12)
	SOverSqrtBUDD323.GetYaxis().SetTitleSize(.12)

	Fit = TF1( "fit", "[0]", 0, 400 )
	Result = SOverSqrtBUDD323.Fit("fit", "SR", "", 0, 400 )

	SOverSqrtBUDD323.Draw("histe")
	Fit.Draw("same")
	SOverSqrtBUDD323.SetFillColorAlpha(kGray+3,0.5)
	SOverSqrtBUDD323.SetLineColor(kViolet+4)
	SOverSqrtBUDD323.SetLineWidth(2)
	SOverSqrtBUDD323.SetFillStyle(3454)
	gStyle.SetHatchesLineWidth(2)
	'''
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
	'''
	gStyle.SetHatchesLineWidth(2)

	FindAndSetMax( [ SOverSqrtBUDD323 ], False )
	
#	SOverSqrtBUDD312.Draw("hist")
	SOverSqrtBUDD323.Draw("hist")
	Fit.Draw("same")
	C.SaveAs("TCutPlots/"+NAME+".png")

	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print ""
	print ""


btag1 = "(subjet11btagCMVAv2>0.4432||subjet12btagCMVAv2>0.4432)"
btag2 = "(subjet21btagCMVAv2>0.4432||subjet22btagCMVAv2>0.4432)"
nobtag1 = "(subjet11btagCMVAv2<0.4432&subjet12btagCMVAv2<0.4432)"
nobtag2 = "(subjet21btagCMVAv2<0.4432&subjet22btagCMVAv2<0.4432)"
onebtag1 = "("+btag1+"&"+nobtag2+")"
onebtag2 = "("+nobtag1+"&"+btag2+")"

#zerobtag = nobtag1+"&"+nobtag2
#onebtag = onebtag1+"||"+onebtag2
#twobtag = btag1+"&"+btag2

zerobtag = "(jet1btagCMVAv2<0.4432&jet2btagCMVAv2<0.4432)"
onebtag = "((jet1btagCMVAv2<0.4432&jet2btagCMVAv2>0.4432)||(jet1btagCMVAv2>0.4432&jet2btagCMVAv2<0.4432))"
twobtag = "(jet1btagCMVAv2>0.4432&jet2btagCMVAv2>0.4432)"

zeroTop = "(jet1Tau32>0.51&jet2Tau32>.51)"
oneTop = "((jet1Tau32<=0.51&jet2Tau32>=0.51)||(jet1Tau32>0.51&jet2Tau32<0.51))"
twoTop = "(jet1Tau32<0.51&jet2Tau32<0.51)"

jet1Top = "((jet1Tau32>0.51&jet2Tau32<0.51))"
jet2Top = "((jet1Tau32<0.51&jet2Tau32>0.51))"
jet1btag = "((jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
jet2btag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484))"

#MakePlot( "prunedMassAve", [ 29, 60, 350 ], zeroTop+"&"+twobtag+"&(prunedMassAsym<0.1)&(deltaEtaDijet<1.0)&jet1Tau21<0.60&jet2Tau21<0.60", "prunedMassAveCMVAv2MA", "prunedMassAve", "Average Pruned Mass [GeV]" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "(prunedMassAsym<0.1)&(deltaEtaDijet>1.5)&jet1Tau21<0.45&jet2Tau21<0.45", "prunedMassAveCMVAv2MB", "prunedMassAve", "Average Pruned Mass [GeV]" )
MakePlot( "prunedMassAve", [ 40, 0, 400 ], "(abs(jet1Pt)>-999)", "prunedMassAve_n-1", "prunedMassAve", "Average Pruned Mass [GeV]" )
MakePlot( "prunedMassAsym", [ 20, 0, 1 ], "(abs(jet1Pt)>-999)", "prunedMassAsym", "prunedMassAsym", "Pruned Mass Asymmetry" )
MakePlot( "jet1Tau21", [ 20, 0, 1 ], "(abs(jet1Pt)>-999)", "jet1Tau21", "jet1Tau21", "Leading Jet Tau21" )
MakePlot( "jet2Tau21", [ 20, 0, 1 ], "(abs(jet1Pt)>-999)", "jet2Tau21", "jet2Tau21", "2nd Leading Jet Tau21" )
MakePlot( "deltaEtaDijet", [ 20, 0, 5 ], "(abs(jet1Pt)>-999)", "deltaEtaDijet", "deltaEtaDijet", "Delta Eta Dijet" )
MakePlot( "jet1Pt", [ 60, 400, 600 ], "(abs(jet1Pt)>-999)", "jet1Pt", "jet1Pt", "Leading Jet Pt" )
MakePlot( "jet2Pt", [ 60, 400, 600 ], "(abs(jet2Pt)>-999)", "jet2Pt", "jet2Pt", "2nd Leading Jet Pt" )
MakePlot( "numPV", [ 30, 0, 30 ], "(abs(jet1Pt)>-999)", "NPV", "numPV", "numPV" )
MakePlot( "HT", [ 130, 700, 2000 ], "(abs(jet1Pt)>-999)", "HT", "HT", "HT" )
MakePlot( "prunedMassAsym", [ 20, 0, 1 ], "(jet1Tau21<0.45&jet2Tau21<0.45&deltaEtaDijet<1.5)", "prunedMassAsym_n-1", "prunedMassAsym", "Pruned Mass Asymmetry n-1" )
MakePlot( "jet1Tau21", [ 20, 0, 1 ], "(prunedMassAsym<0.1&deltaEtaDijet<1.5)", "jet1Tau21_n-1", "jet1Tau21", "Leading Jet Tau21 n-1" )
MakePlot( "jet2Tau21", [ 20, 0, 1 ], "(prunedMassAsym<0.1&deltaEtaDijet<1.5)", "jet2Tau21_n-1", "jet2Tau21", "2nd Leading Jet Tau21 n-1" )
MakePlot( "deltaEtaDijet", [ 20, 0, 5 ], "(prunedMassAsym<0.1&jet1Tau21<0.45&jet2Tau21<0.45)", "deltaEtaDijet_n-1", "deltaEtaDijet", "Delta Eta Dijet n-1" )
#MakePlot( "prunedMassAve", [ 40, 0, 400 ], "(prunedMassAsym<0.1)&jet1Tau21<0.45&jet2Tau21<0.45", "prunedMassAveCMVAv2MC", "prunedMassAve", "Average Pruned Mass [GeV]" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "(prunedMassAsym>0.1)&(deltaEtaDijet<1.0)&jet1Tau21<0.60&jet2Tau21<0.60", "prunedMassAveCMVAv2MC", "prunedMassAve", "Average Pruned Mass [GeV]" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], zeroTop+"&"+twobtag+"&(prunedMassAsym>0.1)&(deltaEtaDijet>1.0)&jet1Tau21<0.60&jet2Tau21<0.60", "prunedMassAveCMVAv2MD", "prunedMassAve", "Average Pruned Mass [GeV]" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "(jet1btagCMVAv2>0.4432&jet2btagCMVAv2>0.4432)&(prunedMassAsym<0.1)&(deltaEtaDijet<1.0)&(jet1Tau32>0.51&jet2Tau32>0.51)&jet1Tau21<0.45&jet2Tau21<0.45", "prunedMassAveCMVAv2M45", "prunedMassAve", "Average Pruned Mass [GeV]" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "(jet1btagCMVAv2>0.9432&jet2btagCMVAv2>0.9432)&(prunedMassAsym<0.1)&(deltaEtaDijet<1.0)&(jet1Tau32>0.51&jet2Tau32>0.51)&jet1Tau21<0.60&jet2Tau21<0.60", "prunedMassAveCMVAv2T60", "prunedMassAve", "Average Pruned Mass [GeV]" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)&(prunedMassAsym<0.1)&(deltaEtaDijet<1.0)&(jet1Tau32>0.51&jet2Tau32>0.51)&jet1Tau21<0.60&jet2Tau21<0.60", "prunedMassAveCSVv2M60", "prunedMassAve", "Average Pruned Mass [GeV]" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "(jet1btagCSVv2>0.4432&jet2btagCSVv2>0.4432)&(prunedMassAsym<0.1)&(deltaEtaDijet>1.0)&(jet1Tau32>0.51&jet2Tau32>0.51)&jet1Tau21<0.45&jet2Tau21<0.45", "prunedMassAveCMVAv2MB", "prunedMassAve", "Average Pruned Mass" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "(jet1btagCSVv2>0.4432&jet2btagCSVv2>0.4432)&(prunedMassAsym>0.1)&(deltaEtaDijet<1.0)&(jet1Tau32>0.51&jet2Tau32>0.51)&jet1Tau21<0.45&jet2Tau21<0.45", "prunedMassAveCMVAv2MC", "prunedMassAve", "Average Pruned Mass" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "(jet1btagCSVv2>0.4432&jet2btagCSVv2>0.4432)&(prunedMassAsym>0.1)&(deltaEtaDijet>1.0)&(jet1Tau32>0.51&jet2Tau32>0.51)&jet1Tau21<0.45&jet2Tau21<0.45", "prunedMassAveCMVAv2MD", "prunedMassAve", "Average Pruned Mass" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "jet1Pt>-999", "prunedMassAve", "prunedMassAve", "Average Pruned Mass" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "prunedMassAsym<0.1&jet1Tau21<0.45&jet2Tau21<0.45&deltaEtaDijet<1.0&(jet1btagCSVv2>0.8000&jet2btagCSVv2>0.8000)", "prunedMassAve", "prunedMassAve", "Average Pruned Mass" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "prunedMassAsym<0.1&jet1Tau21<0.45&jet2Tau21<0.45&deltaEtaDijet<1.0&(jet1btagCSVv2>0.8000&jet2btagCSVv2>0.8000)&(jet1Tau32>0.51&jet2Tau32>0.51)", "prunedMassAveAntitop45", "prunedMassAve", "Average Pruned Mass" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "prunedMassAsym<0.1&jet1Tau21<0.60&jet2Tau21<0.60&deltaEtaDijet<1.0&(jet1btagCSVv2>0.8000&jet2btagCSVv2>0.8000)&(jet1Tau32>0.51&jet2Tau32>0.51)", "prunedMassAveAntitop60", "prunedMassAve", "Average Pruned Mass" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "prunedMassAsym<0.1&jet1Tau21<0.45&jet2Tau21<0.45&deltaEtaDijet<1.0&(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)&(jet1Tau32<0.51&jet2Tau32<0.51)", "prunedMassAveTop", "prunedMassAve", "Average Pruned Mass" )
#MakePlot( "prunedMassAve", [ 29, 60, 350 ], "prunedMassAsym<0.1&jet1Tau21<0.6&jet2Tau21<0.6&deltaEtaDijet<1.0&(jet1btagCSVv2<0.8&jet2btagCSVv2<0.8)", "prunedMassAve", "prunedMassAve", "Average Pruned Mass" )
#MakePlot( "puWeight", [ 1000, 0, 100 ], "jet1btagCSVv2>-9999", "puWeight", "puWeight", "PU Weight" )
'''
MakePlot( "jet1Pt", [ 100, 0, 2000 ], "jet1btagCSVv2>-9999", "jet1Pt", "jet1Pt", "Leading Jet pT" )
MakePlot( "jet2Pt", [ 100, 0, 2000 ], "jet2btagCSVv2>-9999", "jet2Pt", "jet2Pt", "2nd Leading Jet pT" )
MakePlot( "prunedMassAve", [ 5000, 0, 5000 ], "jet2btagCSVv2>-9999", "HT", "HT", "HT" )
MakePlot( "prunedMassAve", [ 100 , 0, 500 ], "jet2btagCSVv2>-9999", "prunedMassAve", "prunedMassAve", "Average Pruned Mass" )
MakePlot( "jet1Tau32", [ 20, 0, 2 ], "jet2btagCSVv2>-9999", "jet1Tau32", "jet1Tau32", "Leading Jet Tau32" )
MakePlot( "jet2Tau32", [ 20, 0, 2 ], "jet2btagCSVv2>-9999", "jet2Tau32", "jet2Tau32", "2nd Leading Jet Tau32" )
MakePlot( "jet1Tau21", [ 20, 0, 2 ], "jet2btagCSVv2>-9999", "jet1Tau21", "jet1Tau21", "Leading Jet Tau21" )
MakePlot( "jet2Tau21", [ 20, 0, 2 ], "jet2btagCSVv2>-9999", "jet2Tau21", "jet2Tau21", "2nd Leading Jet Tau21" )
MakePlot( "jet1btagCSVv2", [ 20, 0, 1 ], "jet2btagCSVv2>-9999", "jet1btagCSVv2", "jet1btagCSVv2", "Leading Jet btagCSVv2" )
MakePlot( "jet2btagCSVv2", [ 20, 0, 1 ], "jet2btagCSVv2>-9999", "jet2btagCSVv2", "jet2btagCSVv2", "2nd Leading Jet btagCSVv2" )
MakePlot( "jet1btagCMVAv2", [ 20, 0, 1 ], "jet2btagCMVAv2>-9999", "jet1btagCMVAv2", "jet1btagCMVAv2", "Leading Jet btagCMVAv2" )
MakePlot( "jet2btagCMVAv2", [ 20, 0, 1 ], "jet2btagCMVAv2>-9999", "jet2btagCMVAv2", "jet2btagCMVAv2", "2nd Leading Jet btagCMVAv2" )
MakePlot( "subjet11btagCSVv2", [ 20, 0, 1 ], "subjet12btagCSVv2>-9999", "subjet11btagCSVv2", "subjet11btagCSVv2", "Jet 1, Subjet 1 btagCSVv2" )
MakePlot( "subjet12btagCSVv2", [ 20, 0, 1 ], "subjet12btagCSVv2>-9999", "subjet12btagCSVv2", "subjet12btagCSVv2", "Jet 1, Subjet 2 btagCSVv2" )
MakePlot( "subjet21btagCSVv2", [ 20, 0, 1 ], "subjet12btagCSVv2>-9999", "subjet21btagCSVv2", "subjet21btagCSVv2", "Jet 2, Subjet 1 btagCSVv2" )
MakePlot( "subjet22btagCSVv2", [ 20, 0, 1 ], "subjet12btagCSVv2>-9999", "subjet22btagCSVv2", "subjet22btagCSVv2", "Jet 2, Subjet 2 btagCSVv2" )
MakePlot( "prunedMassAsym", [ 20 , 0, 2 ], "jet2btagCSVv2>-9999", "prunedMassAsym", "prunedMassAsym", "Pruned Mass Asymmetry" )
MakePlot( "deltaEtaDijet", [ 20 , 0, 5 ], "jet2btagCSVv2>-9999", "deltaEtaDijet", "deltaEtaDijet", "Delta Eta Dijet" )
MakePlot( "jet1PrunedMass", [ 100, 0, 500 ], "jet1btagCSVv2>-9999", "jet1PrunedMass", "jet1PrunedMass", "Leading Jet Pruned Mass" )
MakePlot( "jet2PrunedMass", [ 100 , 0, 500 ], "jet2btagCSVv2>-9999", "jet2PrunedMass", "jet2PrunedMass", "2nd Leading Jet Pruned Mass" )
'''

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

