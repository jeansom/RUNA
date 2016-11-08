#!/usr/bin/env python

import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

gROOT.SetBatch()

def formatFloatForPrint(N):
        if N > 1000.:
                String = str(int(N))
        elif N > 1.:
                String = "{0:3.2f}".format(N)
        elif N > 0.001:
                String = "{0:2.1f}%".format(N*100.)
        elif N > 0.0000001:
                String = "{0:2.2f} ppm".format(N*1000000.)
        else:
                String = str(N)
        return String

def FindAndSetMax(someset):
        maximum = 0.0
        for i in someset:
                i.SetStats(0)
                t = i.GetMaximum()
                if t > maximum:
                        maximum = t
        for j in someset:
                j.GetYaxis().SetRangeUser(0.1,maximum*1.35)

def quickplot(File, tree, plot, var, Cut, Weight):
    temp = plot.Clone("temp")
    chain = ROOT.TChain(tree)
    chain.Add(File)
    chain.Draw(var+">>"+"temp", "("+Weight+")*("+Cut+")", "goff")
    plot.Add(temp)

def quick2dplot(File, tree, plot, var, var2, Cut, Weight): # Same as above, but 2D plotter
        temp = plot.Clone("temp")
        chain = ROOT.TChain(tree)
        chain.Add(File)
        chain.Draw(var2+":"+var+">>"+"temp", "("+Weight+")*("+Cut+")", "goff")
        plot.GetYaxis().SetTitleOffset(1.45)
        plot.Add(temp)

def MakePlot(VAR, BINS, CUT, NAME, Title, cutName):
	normQCD = TH1F("NORMQCD_"+VAR, "", BINS[0], BINS[1], BINS[2])
	normTT = TH1F("NORMTT_"+VAR, "", BINS[0], BINS[1], BINS[2])
	normSig312 = TH1F("NORMSig312_"+VAR, "", BINS[0], BINS[1], BINS[2])
	normSig323 = TH1F("NORMSig323_"+VAR, "", BINS[0], BINS[1], BINS[2])
	normWJets = TH1F("NORMWJets_"+VAR, "", BINS[0], BINS[1], BINS[2])
	
	PlotsQCD = TH1F("QCD_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsSig323 = TH1F("Sig323_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsSig312 = TH1F("Sig312_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsTT = TH1F("TT_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsWJets = TH1F("WJets_"+VAR, "", BINS[0], BINS[1], BINS[2])

	quickplot("RootFiles/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", normQCD, VAR, "jet1Pt>-1.0", "1.0")
	quickplot("RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", normSig323, VAR, "jet1Pt>-1.0", "1.0")
	quickplot("RootFiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-100_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", normSig312, VAR, "jet1Pt>-1.0", "1.0")
	quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", normTT, VAR, "jet1Pt>-1.0", "1.0")
	quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", normWJets, VAR, "jet1Pt>-1.0", "1.0")

	###
	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print "QCD Events considered: " + str(normQCD.Integral())
	print "TT Events considered: " + str(normTT.Integral())
	print "WJets Events considered: " + str(normWJets.Integral())
	print "Signal323 Events considered: " + str(normSig323.Integral())
	print "Signal312 Events considered: " + str(normSig312.Integral())

	quickplot("RootFiles/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsSig323, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-100_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsSig312, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTT, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsWJets, VAR, CUT, "lumiWeight*puWeight*2666")

	if normQCD.Integral() != 0:
		QCDrate = PlotsQCD.Integral()/normQCD.Integral()
	else:
		QCDrate = 0

	if normTT.Integral() != 0:
		TTrate = PlotsTT.Integral()/normTT.Integral()
	else:
		TTrate = 0

	if normWJets.Integral() != 0:
		WJetsrate = PlotsWJets.Integral()/normWJets.Integral()
	else:
		WJetsrate = 0

	if normSig323.Integral() != 0:
		SIG323rate = PlotsSig323.Integral()/normSig323.Integral()
	else:
		Sigrate323 = 0
	if normSig312.Integral() != 0:
		SIG312rate = PlotsSig312.Integral()/normSig312.Integral()
	else:
		Sigrate312 = 0

	###
	print "QCD rate = " + str(QCDrate)
	print "TT rate = " + str(TTrate)
	print "WJets rate = " + str(WJetsrate)
	print "Signal323 rate = " + str(SIG323rate)
	print "Signal312 rate = " + str(SIG312rate)

	QCDrateS = formatFloatForPrint(QCDrate)
	TTrateS = formatFloatForPrint(TTrate)
	WJetsrateS = formatFloatForPrint(WJetsrate)
	SIG323rateS = formatFloatForPrint(SIG323rate)
	SIG312rateS = formatFloatForPrint(SIG312rate)

#	PlotsQCD.SetLineColor(9)
#	PlotsWJets.SetLineColor(8)
#	PlotsTT.SetLineColor(2)
#	PlotsSig323.SetLineColor(kViolet)
#	PlotsSig312.SetLineColor(kGray)
	PlotsQCD.SetFillColor(9)
	PlotsTT.SetFillColor(2)
	PlotsWJets.SetFillColor(8)
	PlotsSig323.SetFillColorAlpha(kGray+3,0.5)
	PlotsSig323.SetLineColor(kViolet+4)
	PlotsSig323.SetFillStyle(3454)
	gStyle.SetHatchesLineWidth(2)
	PlotsSig312.SetFillColorAlpha(kGray+3,0.5)
	PlotsSig312.SetLineColor(13)
	PlotsSig312.SetFillStyle(3445)	
	gStyle.SetHatchesLineWidth(2)

	stackPlots = THStack( "Stack", "" )
	Plots = PlotsQCD.Clone()
	Plots.Reset()
	for i in [PlotsQCD, PlotsTT, PlotsWJets, PlotsSig323, PlotsSig312]:
		i.SetStats(0)
		i.GetXaxis().SetTitle(Title)
		i.GetYaxis().SetTitle("Events")
		i.SetLineWidth(2)
#		i.Scale(1/i.Integral())
#		Plots.Add(i)
		

	PlotsSig323.SetLineWidth(6)
	PlotsSig312.SetLineWidth(6)

	FindAndSetMax([PlotsQCD,PlotsTT,PlotsWJets, PlotsSig323, PlotsSig312])
	stackPlots.Add(PlotsWJets)
	stackPlots.Add(PlotsTT)
	stackPlots.Add(PlotsQCD)



	stackPlots.SetMaximum( stackPlots.GetMaximum() )
	stackPlots.SetMinimum( 0 )
	leg = TLegend(0.55,0.7,0.89,0.89)
	leg.SetHeader(cutName)
	leg.SetLineColor(0)
	leg.SetFillColor(4001)
	leg.AddEntry(PlotsQCD, "QCD", "F")
	leg.AddEntry(PlotsTT, "t#bar{t}", "F")
	leg.AddEntry(PlotsWJets, "W + Jets", "F")
	leg.AddEntry(PlotsSig323, "RPV UDD323 Signal, M=100 GeV", "F")
	leg.AddEntry(PlotsSig312, "RPV UDD312 Signal, M=100 GeV", "F")

	C = TCanvas("C"+VAR+CUT, "", 800, 600)
	C.cd()
#	C.SetLogy()

#	FindAndSetMax( [stackPlots] )

	stackPlots.Draw("hist")
	stackPlots.GetXaxis().SetTitle(cutName)
	stackPlots.GetYaxis().SetTitle("Events" )
#	PlotsQCD.Draw("hist")
#	for i in [PlotsTT, PlotsWJets, PlotsSig323, PlotsSig312]:
#		i.Draw("hist same")
#	PlotsQCD.Draw("hist")
	PlotsSig323.Draw("hist same")
	PlotsSig312.Draw("hist same")
#	PlotsTT.Draw("hist same")
	leg.Draw("same")
	C.SaveAs("TCutPlots/"+NAME+".png")

	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print ""
	print ""



#MakePlot("massAve", [60, 50, 350], "prunedMassAsym<0.1", "massAveTestTCutPlot", "massAve", "test")
#MakePlot("massAve", [150, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.8||subjet12btagCSVv2>0.8)&(subjet21btagCSVv2>0.8||subjet22btagCSVv2>0.8)&jet1Tau32>0.51&jet2Tau32>0.51", "massAveTestTCutPlot", "massAve", "test")

#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&!((subjet11btagCSVv2>0.800||subjet12btagCSVv2>0.800)&(subjet21btagCSVv2>0.800||subjet22btagCSVv2>0.800))&jet1Tau32>0.51&jet2Tau32>0.51", "massAveFailBtagFailTau32", "massAve", "Average Pruned Mass")
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&!((subjet11btagCSVv2>0.800||subjet12btagCSVv2>0.800)&(subjet21btagCSVv2>0.800||subjet22btagCSVv2>0.800))&jet1Tau32<0.51&jet2Tau32<0.51", "massAveFailBtagPassTau32", "massAve", "Average Pruned Mass")
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.800||subjet12btagCSVv2>0.800)&(subjet21btagCSVv2>0.800||subjet22btagCSVv2>0.800)&jet1Tau32>0.51&jet2Tau32>0.51", "massAvePassBtagFailTau32", "massAve", "Average Pruned Mass")
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.800||subjet12btagCSVv2>0.800)&(subjet21btagCSVv2>0.800||subjet22btagCSVv2>0.800)&jet1Tau32<0.51&jet2Tau32<0.51", "massAvePassBtagPassTau32", "massAve", "Average Pruned Mass")
#
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&!((subjet11btagCSVv2>0.800||subjet12btagCSVv2>0.800)&(subjet21btagCSVv2>0.800||subjet22btagCSVv2>0.800))&jet1Tau32>0.69&jet2Tau32>0.69", "massAveFailBtagFailTau32Loose", "massAve", "Average Pruned Mass")
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&!((subjet11btagCSVv2>0.800||subjet12btagCSVv2>0.800)&(subjet21btagCSVv2>0.800||subjet22btagCSVv2>0.800))&jet1Tau32<0.69&jet2Tau32<0.69", "massAveFailBtagPassTau32Loose", "massAve", "Average Pruned Mass")
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.800||subjet12btagCSVv2>0.800)&(subjet21btagCSVv2>0.800||subjet22btagCSVv2>0.800)&jet1Tau32>0.69&jet2Tau32>0.69", "massAvePassBtagFailTau32Loose", "massAve", "Average Pruned Mass")
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.800||subjet12btagCSVv2>0.800)&(subjet21btagCSVv2>0.800||subjet22btagCSVv2>0.800)&jet1Tau32<0.69&jet2Tau32<0.69", "massAvePassBtagPassTau32Loose", "massAve", "Average Pruned Mass")
#
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&!((subjet11btagCSVv2>0.460||subjet12btagCSVv2>0.460)&(subjet21btagCSVv2>0.460||subjet22btagCSVv2>0.460))&jet1Tau32>0.51&jet2Tau32>0.51", "massAveFailBtagLooseFailTau32", "massAve", "Average Pruned Mass")
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&!((subjet11btagCSVv2>0.460||subjet12btagCSVv2>0.460)&(subjet21btagCSVv2>0.460||subjet22btagCSVv2>0.460))&jet1Tau32<0.51&jet2Tau32<0.51", "massAveFailBtagLoosePassTau32", "massAve", "Average Pruned Mass")
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.460||subjet12btagCSVv2>0.460)&(subjet21btagCSVv2>0.460||subjet22btagCSVv2>0.460)&jet1Tau32>0.51&jet2Tau32>0.51", "massAvePassBtagLooseFailTau32", "massAve", "Average Pruned Mass")
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.460||subjet12btagCSVv2>0.460)&(subjet21btagCSVv2>0.460||subjet22btagCSVv2>0.460)&jet1Tau32<0.51&jet2Tau32<0.51", "massAvePassBtagLoosePassTau32", "massAve", "Average Pruned Mass")
#
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&!((subjet11btagCSVv2>0.460||subjet12btagCSVv2>0.460)&(subjet21btagCSVv2>0.460||subjet22btagCSVv2>0.460))&jet1Tau32>0.69&jet2Tau32>0.69", "massAveFailBtagLooseFailTau32Loose", "massAve", "Average Pruned Mass")
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&!((subjet11btagCSVv2>0.460||subjet12btagCSVv2>0.460)&(subjet21btagCSVv2>0.460||subjet22btagCSVv2>0.460))&jet1Tau32<0.69&jet2Tau32<0.69", "massAveFailBtagLoosePassTau32Loose", "massAve", "Average Pruned Mass")
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.460||subjet12btagCSVv2>0.460)&(subjet21btagCSVv2>0.460||subjet22btagCSVv2>0.460)&jet1Tau32>0.69&jet2Tau32>0.69", "massAvePassBtagLooseFailTau32Loose", "massAve", "Average Pruned Mass")
#MakePlot("massAve", [30, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.460||subjet12btagCSVv2>0.460)&(subjet21btagCSVv2>0.460||subjet22btagCSVv2>0.460)&jet1Tau32<0.69&jet2Tau32<0.69", "massAvePassBtagLoosePassTau32Loose", "massAve", "Average Pruned Mass")

MakePlot("deltaEtaDijet", [50, 0., 5.], "prunedMassAsym<0.1&jet1Tau21<0.6&jet2Tau21<0.6", "deltaEtaDijet", "deltaEtaDijet", "Delta Eta")
MakePlot("prunedMassAsym", [20, 0., 1.], "deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6", "prunedMassAsym", "prunedMassAsym", "Pruned Mass Asymmetry")
