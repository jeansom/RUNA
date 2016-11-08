#!/usr/bin/env python

import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy


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
                j.GetYaxis().SetRangeUser(0,maximum*1.35)

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
	normSig = TH1F("NORMSig_"+VAR, "", BINS[0], BINS[1], BINS[2])
	
	PlotsQCD = TH1F("QCD_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsSig = TH1F("Sig_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsTT = TH1F("TT_"+VAR, "", BINS[0], BINS[1], BINS[2])

	quickplot("RootFiles/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", normQCD, VAR, "jet1Pt>-1.0", "1.0")
	quickplot("RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", normSig, VAR, "jet1Pt>-1.0", "1.0")
	quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", normTT, VAR, "jet1Pt>-1.0", "1.0")

	###
	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print "QCD Events considered: " + str(normQCD.Integral())
	print "TT Events considered: " + str(normTT.Integral())
	print "Signal Events considered: " + str(normSig.Integral())

	quickplot("RootFiles/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsSig, VAR, CUT, "lumiWeight*puWeight*2666")
	quickplot("RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTT, VAR, CUT, "lumiWeight*puWeight*2666")

	QCDrate = PlotsQCD.Integral()/normQCD.Integral()
	TTrate = PlotsTT.Integral()/normTT.Integral()
	SIGrate = PlotsSig.Integral()/normSig.Integral()

	###
	print "QCD rate = " + str(QCDrate)
	print "TT rate = " + str(TTrate)
	print "Signal rate = " + str(SIGrate)

	QCDrateS = formatFloatForPrint(QCDrate)
	TTrateS = formatFloatForPrint(TTrate)
	SIGrateS = formatFloatForPrint(SIGrate)

	PlotsQCD.SetLineColor(kViolet)
	PlotsTT.SetLineColor(kBlue)
	PlotsSig.SetLineColor(kRed)
	for i in [PlotsQCD, PlotsTT, PlotsSig]:
		i.SetStats(0)
		i.GetXaxis().SetTitle(Title)
		i.GetYaxis().SetTitle("A.U.")
		i.SetLineWidth(2)
#		i.Scale(1/i.Integral())
	leg = TLegend(0.5,0.6,0.89,0.89)
	leg.SetHeader(cutName)
	leg.SetLineColor(0)
	leg.SetFillColor(4001)
	leg.AddEntry(PlotsQCD, "QCD (eff= "+QCDrateS+" after preselection)", "L")
	leg.AddEntry(PlotsTT, "Powheg t#bar{t} (eff= "+TTrateS+" after preselection)", "L")
	leg.AddEntry(PlotsSig, "RPV Signal, M=100 GeV (eff= "+SIGrateS+" after preselection)", "L")
		

	FindAndSetMax([PlotsQCD,PlotsSig,PlotsTT])

	C = TCanvas("C"+VAR+CUT, "", 800, 600)
	C.cd()
	PlotsQCD.Draw("hist")
	PlotsSig.Draw("hist same")
	PlotsTT.Draw("hist same")
	leg.Draw("same")
	C.SaveAs(NAME+".gif")

	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print ""
	print ""



#MakePlot("massAve", [60, 50, 350], "prunedMassAsym<0.1", "massAveTestTCutPlot", "massAve", "test")
#MakePlot("massAve", [150, 50, 350], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.8||subjet12btagCSVv2>0.8)&(subjet21btagCSVv2>0.8||subjet22btagCSVv2>0.8)&jet1Tau32>0.51&jet2Tau32>0.51", "massAveTestTCutPlot", "massAve", "test")
