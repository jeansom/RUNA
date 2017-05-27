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

gROOT.SetBatch()
gStyle.SetOptStat(0)
def MakePlot(VAR, BINS, CUT, NAME, Title, cutName, log):

	PlotsQCD = TH1F("QCD_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsSig3231 = TH1F("Sig3231_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsSig3232 = TH1F("Sig3232_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsSig3233 = TH1F("Sig3233_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsSig3234 = TH1F("Sig3234_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsSig312 = TH1F("Sig312_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsTT = TH1F("TT_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsT = TH1F("T_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsWJets = TH1F("WJets_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsZJets = TH1F("ZJets_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsWW = TH1F("WW_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsZZ = TH1F("ZZ_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsWZ = TH1F("WZ_"+VAR, "", BINS[0], BINS[1], BINS[2])

	PlotsDATA = TH1F("DATA_"+VAR, "", BINS[0], BINS[1], BINS[2])

	f = TF1("f", "cos(x)/x", 0, 400 )
	
	MCScale = "(36555.21/15.)"
#	for i in [ "QCDPt170to300", "QCDPt300to470", "QCDPt470to600", "QCDPt600to800", "QCDPt800to1000", "QCDPt1000to1400", "QCDPt1400to1800", "QCDPt1800to2400", "QCDPt2400to3200", "QCDPt3200toInf" ]:
#		quickplot("80XRootFilesUpdated/RUNAnalysis_"+i+"_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "puWeight*.85*36555.21/15./15*"+str(scaleFactor(i) ) )
	rootFiles = "v08/"
#	quickplot(rootFiles+"/RUNAnalysis_QCDHTAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "36555.21/15.*lumiWeight*.69*puWeight" )
#	quickplot(rootFiles+"/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "36555.21/15.*lumiWeight*.62*puWeight" )
	quickplot(rootFiles+"/RUNAnalysis_JetHT_Run2016_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "1/15" )
#	quickplot(rootFiles+"/RUNAnalysis_QCDHTAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "1." )
#	quickplot(rootFiles+"RUNAnalysis_QCDHTAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "puWeight*.85*36555.21/15./15*lumiWeight")
	quickplot("80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-100_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", PlotsSig3231, VAR, CUT, "puWeight*"+str(scaleFactor("RPVStopStopToJets_UDD312_M-100"))+"*"+MCScale)
	quickplot("80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-160_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", PlotsSig3232, VAR, CUT, "puWeight*"+str(scaleFactor("RPVStopStopToJets_UDD312_M-160"))+"*"+MCScale)
#	quickplot(rootFiles+"Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-100_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", PlotsSig3233, VAR, CUT, "puWeight*"+str(scaleFactor("RPVStopStopToJets_UDD323_M-100"))+"*"+MCScale)
#	quickplot(rootFiles+"Signals/RUNAnalysis_RPVStopStopToJets_UDD312_M-220_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", PlotsSig3234, VAR, CUT, "puWeight*12.1575/158551*"+MCScale)
	quickplot("v08/RUNAnalysis_TT_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", PlotsTT, VAR, CUT, "puWeight*lumiWeight*1.06*exp(-0.0005*HT/2)*"+MCScale)
#	quickplot("v08/RUNAnalysis_TT_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", PlotsTT, VAR, CUT, "puWeight*lumiWeight*1*"+MCScale)
	quickplot("v08/RUNAnalysis_WJetsToQQ_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", PlotsWJets, VAR, CUT, "puWeight*lumiWeight*"+MCScale)
#	quickplot("v08/RUNAnalysis_JetHT_Run2016_80X_V2p4_v08_cut15_pruned.root", "BoostedAnalysisPlots/RUNATree", PlotsDATA, VAR, CUT, "1")
	quickplot("v08/RUNAnalysis_JetHT_Run2016_80X_V2p4_v08_cut15_pruned.root", "BoostedAnalysisPlots/RUNATree", PlotsDATA, VAR, CUT, "1")
	quickplot("80XRootFilesUpdated/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", PlotsT, VAR, CUT, "puWeight*lumiWeight*"+MCScale)

	PlotsSig3231.SetLineColor(kViolet)
	PlotsSig3232.SetLineColor(kGray)
	PlotsSig3233.SetLineColor(kViolet)
	PlotsSig3234.SetLineColor(kGray)
	PlotsSig312.SetLineColor(kGray)
	PlotsQCD.SetFillColor(kAzure-4)
	PlotsQCD.SetLineColor(1)
	PlotsQCD.SetLineWidth(1)
	PlotsTT.SetFillColor(2)
	PlotsTT.SetLineColor(1)
	PlotsTT.SetLineWidth(1)
	PlotsT.SetFillColor(6)
	PlotsT.SetLineColor(1)
	PlotsT.SetLineWidth(1)
	PlotsWJets.SetFillColor(8)
	PlotsWJets.SetLineColor(1)
	PlotsWJets.SetLineWidth(1)
	 
	PlotsSig3231.SetFillColorAlpha(kGray+3,0.5)
	PlotsSig3231.SetLineColor(kViolet+4)
	PlotsSig3231.SetFillStyle(3454)
	PlotsSig3232.SetFillColorAlpha(kGray+3,0.5)
	PlotsSig3232.SetLineColor(14)
	PlotsSig3232.SetFillStyle(3454)
	PlotsSig3233.SetFillColorAlpha(kGray+3,0.5)
	PlotsSig3233.SetLineColor(kBlue-4)
	PlotsSig3233.SetFillStyle(3445)
	PlotsSig3234.SetFillColorAlpha(kGray+3,0.5)
	PlotsSig3234.SetLineColor(12)
	PlotsSig3234.SetFillStyle(3445)
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
	PlotsBkg.Add(PlotsWJets)
	PlotsBkg.Add(PlotsTT)

	stackPlots = THStack( "Stack", "" )
	Plots = PlotsQCD.Clone()
	Plots.Reset()
	for i in [PlotsQCD, PlotsWJets, PlotsTT, PlotsT ]:
		i.SetStats(0)
		i.GetXaxis().SetTitle(Title)
		i.GetYaxis().SetTitle("Events")
		i.GetYaxis().SetTitleOffset(1.3)
		i.SetLineWidth(2)
		Plots.Add(i)
#	for i in [PlotsQCD, PlotsTT, PlotsT, PlotsWJets ]:
#		i.Scale(1/Plots.Integral())


	print NAME+", DATA/MC: " + str(float(PlotsDATA.Integral()/Plots.Integral()))
	'''
	B100 = Plots.Integral(Plots.FindBin(90), Plots.FindBin(110))
	B120 = Plots.Integral(Plots.FindBin(90), Plots.FindBin(110))
	B180 = Plots.Integral(Plots.FindBin(150), Plots.FindBin(170))

	S120 = PlotsSig3231.Integral(PlotsSig3231.FindBin(90), PlotsSig3231.FindBin(110))
	S180 = PlotsSig3232.Integral(PlotsSig3232.FindBin(150), PlotsSig3232.FindBin(170))

	SB120 = float(S120/math.sqrt(B120))
	SB180 = float(S180/math.sqrt(B180))

	print "M-100: " + str(SB120)
	print "M-160: " + str(SB180)
	'''
	PlotsSig3231.SetLineWidth(2)
	PlotsSig3232.SetLineWidth(2)
#	PlotsSig3233.SetLineWidth(6)
#	PlotsSig3234.SetLineWidth(6)
	PlotsSig312.SetLineWidth(6)
#	stackPlots.Add(PlotsT)
#	stackPlots.Add(PlotsTT)
#	stackPlots.Add(PlotsWJets)
	stackPlots.Add(PlotsQCD)

	leg = TLegend(0.55,0.70,0.89,0.89)
#	leg = TLegend(0.11,0.70,0.45,0.89)
#	leg.SetNColumns(2)
	leg.SetFillStyle(0)
	leg.SetFillStyle(0)
	leg.SetLineColor(0)
	leg.SetLineColor(0)
	leg.SetFillColor(4001)
	leg.AddEntry(PlotsQCD, "QCD", "F")
	leg.AddEntry(PlotsTT, "TT + Jets", "F")
	leg.AddEntry(PlotsWJets, "W + Jets", "F")
	leg.AddEntry(PlotsT, "Single Top", "F")
	leg.AddEntry(PlotsDATA, "Data", "PL")
#	leg.AddEntry(PlotsSig3231, "RPV #tilde{t}, M-120", "F")
#	leg.AddEntry(PlotsSig3232, "RPV #tilde{t}, M-180", "F")

	C = TCanvas("C"+VAR+CUT, "", 800, 800)
	pad1 = TPad( "pad1", "", 0, 0.20, 1, 1 )
	pad2 = TPad( "pad2", "", 0, 0, 1.0, 0.20 )
	pad1.SetBottomMargin(0)
	pad2.SetTopMargin(0)
	pad2.Draw()
	pad1.Draw()
	pad1.cd()
	if log:	
		pad1.SetLogy()
		FindAndSetMax([stackPlots,PlotsDATA],True)
#		stackPlots.SetMaximum(10000)
	else:
		FindAndSetMax([stackPlots,PlotsDATA],False)	
	
#	stackPlots.Scale(1/Plots.Integral())
	stackPlots.Draw()
	stackPlots.GetXaxis().SetTitle("")
	stackPlots.GetXaxis().SetLabelSize(0)
	stackPlots.GetYaxis().SetTitle("Events" )
	stackPlots.GetYaxis().SetTitleOffset(1.3)
	stackPlots.GetYaxis().SetLabelSize(0.03)
	stackPlots.Draw("hist")
#	PlotsQCD.DrawNormalized("histsame")
#	PlotsTT.DrawNormalized("histsame")
#	PlotsWJets.DrawNormalized("histsame")
#	PlotsQCD.SetMaximum(PlotsDATA.GetMaximum())
	stackPlots.Draw("hist")
	PlotsDATA.Draw("E0same")
#	PlotsSig3231.Draw("histsame")
#	PlotsSig3232.Draw("histsame")
	leg.Draw("same")
	CMS_lumi.extraText = "Simulation Preliminary"
	CMS_lumi.relPosX = 0.17
	CMS_lumi.CMS_lumi( (pad1), 4, 0)
	pad1.RedrawAxis()

	pad2.cd()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	'''
	for b in xrange( BINS[0] ):
		signalUDD323 = PlotsDATA.GetBinContent(b)
		bkg = Plots.GetBinContent(b)
		try:
			SBUDD323 = float(signalUDD323)/float(bkg)
		except ZeroDivisionError: continue
		SOverSqrtBUDD323.SetBinContent(b,SBUDD323)
		'''
	SOverSqrtBUDD323 = PlotsDATA.Clone("Ratio")
	SOverSqrtBUDD323.Divide(Plots)
	SOverSqrtBUDD323.GetXaxis().SetTitle(Title)
	SOverSqrtBUDD323.GetYaxis().SetRangeUser(0., 2)
	SOverSqrtBUDD323.GetYaxis().SetTitle("#frac{Data}{MC}")
	T1 = TLine(BINS[1],1.,BINS[2],1.)
	T1.SetLineColor(kRed)
	T1.SetLineStyle(3)
	T1.SetLineWidth(2)
	SOverSqrtBUDD323.GetXaxis().SetLabelSize(.12)
	SOverSqrtBUDD323.GetXaxis().SetTitleSize(.12)
	SOverSqrtBUDD323.GetYaxis().SetTitleOffset(.3)
	SOverSqrtBUDD323.GetYaxis().SetLabelSize(.12)
	SOverSqrtBUDD323.GetYaxis().SetTitleSize(.12)
	SOverSqrtBUDD323.SetMarkerStyle(20)
	SOverSqrtBUDD323.SetLineColor(1)
	SOverSqrtBUDD323.Draw("e0")
	T1.Draw("same")

#	FindAndSetMax( [ SOverSqrtBUDD323 ], False )
	
	SOverSqrtBUDD323.Draw("hist")

	C.SaveAs("TCutPlots/"+NAME+".png")
	
	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print ""
	print ""

zerobtag = "(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484)"
onebtag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484)||(jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
twobtag = "(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)"

zeroTop = "(jet1Tau32>0.67&jet2Tau32>.67)"
oneTop = "((jet1Tau32<=0.67&jet2Tau32>=0.67)||(jet1Tau32>0.67&jet2Tau32<0.67))"
twoTop = "(jet1Tau32<0.67&jet2Tau32<0.67)"

##### n-1 Plots
## Cuts
# Delta Eta
# Mass Asym
# Jet*Tau21
## Variables
# Delta Eta
# Mass Asym
# Jet*Tau21
# HT
# Mass
#MakePlot( "prunedMassAve", [ 58, 60, 350 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "prunedMassAve_A", "Average Mass", "prunedMassAve_A", True )
MakePlot( "prunedMassAve", [ 12, 50, 350 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet>1.5", "prunedMassAve_B", "Average Mass", "prunedMassAve_B", False )
MakePlot( "prunedMassAve", [ 58, 60, 350 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym>0.1&deltaEtaDijet<1.5", "prunedMassAve_C", "Average Mass", "prunedMassAve_C", False )
MakePlot( "prunedMassAve", [ 12, 50, 350 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym>0.1&deltaEtaDijet>1.5", "prunedMassAve_D", "Average Mass", "prunedMassAve_D", False )
'''
#for chan in [ [ "b0t0", zerobtag+"&"+zeroTop ], [ "b0t1", zerobtag+"&"+oneTop ], [ "b0t2", zerobtag+"&"+twoTop ], [ "b1t0", onebtag+"&"+zeroTop ], [ "b1t1", onebtag+"&"+oneTop ], [ "b1t2", onebtag+"&"+twoTop ], [ "b2t0", twobtag+"&"+zeroTop ], [ "b2t1", twobtag+"&"+oneTop ], [ "b2t2", twobtag+"&"+twoTop ] ]:
#	MakePlot( "prunedMassAve", [ 58, 60, 350 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&"+chan[1], "prunedMassAve_sel"+chan[0], "Average Mass", "prunedMassAve_sel"+chan[0], True )
#for var in [ ["deltaEtaDijet", "Delta Eta", [50, 0., 5.], True], ["prunedMassAsym", "Mass Asymmetry", [20, 0., 1.], False], ["jet1Tau21", "Leading Jet Tau_{2}/Tau_{1}", [20, 0., 1.], False], ["jet2Tau21", "2^{nd} Leading Jet #tau_{2}/#tau_{1}", [20, 0., 1.], False], ["prunedMassAve", "Average Mass", [60, 50., 350.], True], ["HT", "HT", [130, 700., 2000.], True] ]:
#	for cut in [ ["jet1Tau21<0.45&jet2Tau21<0.45&deltaEtaDijet<1.5&prunedMassAsym<0.1", "all"], ["deltaEtaDijet<1.5&prunedMassAsym<0.1", "tau21_n-1"], ["jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1", "deta_n-1"], ["jet1Tau21<0.45&jet2Tau21<0.45&deltaEtaDijet<1.5", "massasym_n-1"] ]:
#		MakePlot( var[0], var[2], cut[0], var[0]+"_"+cut[1], var[1],  var[0]+"_"+cut[1], var[3])

##### Additional Plots
## Variables
# NPV, pres [ 30, 0, 30 ]
MakePlot( "numPV", [ 50, 0, 50 ], "1.", "numPV_NoCuts", "numPV", "numPV_NoCuts", False )
MakePlot( "numPV", [ 30, 0, 30 ], "jet1Tau21<0.45&jet2Tau21<0.45", "numPV_pres", "numPV", "numPV_pres", False )
MakePlot( "numPV", [ 30, 0, 30 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "numPV_sel", "numPV", "numPV_sel", False )
MakePlot( "numPV", [ 30, 0, 30 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "numPV_selN", "numPV", "numPV_selN", False )

# numJets, pres, [10, 0, 10 ]
MakePlot( "numJets", [ 10, 0, 10 ], "1.", "numJets_NoCuts", "N Jets", "numJets_NoCuts", False )
MakePlot( "numJets", [ 10, 0, 10 ], "jet1Tau21<0.45&jet2Tau21<0.45", "numJets_pres", "N Jets", "numJets_pres", False )
MakePlot( "numJets", [ 10, 0, 10 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "numJets_sel", "N Jets", "numJets_sel", False )
MakePlot( "numJets", [ 10, 0, 10 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "numJets_selN", "N Jets", "numJets_selN", False )

# prunedMassAsym, pres [ 20, 0., 1. ], [20, 0., 0.1]
MakePlot( "prunedMassAsym", [ 20, 0., 1. ], "1.", "prunedMassAsym_NoCuts", "Mass Asymmetry", "prunedMassAsym_NoCuts", False )
MakePlot( "prunedMassAsym", [ 20, 0., 1. ], "jet1Tau21<0.45&jet2Tau21<0.45", "prunedMassAsym_pres", "Mass Asymmetry", "prunedMassAsym_pres", False )
MakePlot( "prunedMassAsym", [ 20, 0., 0.1 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "prunedMassAsym_sel", "Mass Asymmetry", "prunedMassAsym_sel", False )
MakePlot( "prunedMassAsym", [ 20, 0., 0.1 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "prunedMassAsym_selN", "Mass Asymmetry", "prunedMassAsym_selN", False )


# jet*Tau21, pres, [ 20, 0., 1. ], [20, 0., 0.45]
MakePlot( "jet1Tau21", [ 20, 0., 1. ], "1.", "jet1Tau21_NoCuts", "Leading Jet #tau_{21}", "jet1Tau21_NoCuts", False )
MakePlot( "jet1Tau21", [ 20, 0., 0.45 ], "jet1Tau21<0.45&jet2Tau21<0.45", "jet1Tau21_pres", "Leading Jet #tau_{21}", "jet1Tau21_pres", False )
MakePlot( "jet1Tau21", [ 20, 0., 0.45 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "jet1Tau21_sel", "Leading Jet #tau_{21}", "jet1Tau21_sel", False )
MakePlot( "jet1Tau21", [ 20, 0., 0.45 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "jet1Tau21_selN", "Leading Jet #tau_{21}", "jet1Tau21_selN", False )
MakePlot( "jet2Tau21", [ 20, 0., 1. ], "1.", "jet2Tau21_NoCuts", "2^{nd} Leading Jet #tau_{21}", "jet2Tau21_NoCuts", False )
MakePlot( "jet2Tau21", [ 20, 0., 0.45 ], "jet2Tau21<0.45&jet2Tau21<0.45", "jet2Tau21_pres", "2^{nd} Leading Jet #tau_{21}", "jet2Tau21_pres", False )
MakePlot( "jet2Tau21", [ 20, 0., 0.45 ], "jet2Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "jet2Tau21_sel", "2^{nd} Leading Jet #tau_{21}", "jet2Tau21_sel", False )
MakePlot( "jet2Tau21", [ 20, 0., 0.45 ], "jet2Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "jet2Tau21_selN", "2^{nd} Leading Jet #tau_{21}", "jet2Tau21_selN", False )


# deltaEtaDijet, pres (log), [ 50, 0., 5. ], [ 50, 0., 1.5 ]
MakePlot( "deltaEtaDijet", [ 50, 0., 5. ], "1.", "deltaEtaDijet_NoCuts", "Delta Eta", "deltaEtaDijet_NoCuts", True )
MakePlot( "deltaEtaDijet", [ 50, 0., 5. ], "jet1Tau21<0.45&jet2Tau21<0.45", "deltaEtaDijet_pres", "Delta Eta", "deltaEtaDijet_pres", True )
MakePlot( "deltaEtaDijet", [ 50, 0., 1.5 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "deltaEtaDijet_sel", "Delta Eta", "deltaEtaDijet_sel", True )
MakePlot( "deltaEtaDijet", [ 50, 0., 1.5 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "deltaEtaDijet_selN", "Delta Eta", "deltaEtaDijet_selN", True )


# prunedMassAve, pres (log), [ 40, 0, 400 ]
MakePlot( "prunedMassAve", [ 40, 0, 400 ], "1.", "prunedMassAve_NoCuts", "Average Mass", "prunedMassAve_NoCuts", True )
MakePlot( "prunedMassAve", [ 40, 0, 400 ], "jet1Tau21<0.45&jet2Tau21<0.45", "prunedMassAve_pres", "Average Mass", "prunedMassAve_pres", True )
MakePlot( "prunedMassAve", [ 40, 0, 400 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "prunedMassAve_sel", "Average Mass", "prunedMassAve_sel", True )
MakePlot( "prunedMassAve", [ 40, 0, 400 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "prunedMassAve_selN", "Average Mass", "prunedMassAve_selN", True )


# HT, (log), [ 130, 700, 2000 ]
MakePlot( "HT", [ 130, 700, 2000 ], "1.", "HT_NoCuts", "HT", "HT_NoCuts", True )
MakePlot( "HT", [ 130, 700, 2000 ], "jet1Tau21<0.45&jet2Tau21<0.45", "HT_pres", "HT", "HT_pres", True )
MakePlot( "HT", [ 130, 700, 2000 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "HT_sel", "HT", "HT_sel", True )
MakePlot( "HT", [ 130, 700, 2000 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "HT_selN", "HT", "HT_selN", True )


# jet*Tau32, pres, [ 20, 0., 1. ]
MakePlot( "jet1Tau32", [ 20, 0., 1. ], "1.", "jet1Tau32_NoCuts", "Leading Jet #tau_{32}", "jet1Tau32_NoCuts", False )
MakePlot( "jet1Tau32", [ 20, 0., 1. ], "jet1Tau21<0.45&jet2Tau21<0.45", "jet1Tau32_pres", "Leading Jet #tau_{32}", "jet1Tau32_pres", False )
MakePlot( "jet1Tau32", [ 20, 0., 1. ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "jet1Tau32_sel", "Leading Jet #tau_{32}", "jet1Tau32_sel", False )
MakePlot( "jet1Tau32", [ 20, 0., 1. ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "jet1Tau32_selN", "Leading Jet #tau_{32}", "jet1Tau32_selN", False )
MakePlot( "jet2Tau32", [ 20, 0., 1. ], "1.", "jet2Tau32_NoCuts", "2^{nd} Leading Jet #tau_{32}", "jet2Tau32_NoCuts", False )
MakePlot( "jet2Tau32", [ 20, 0., 1. ], "jet2Tau21<0.45&jet2Tau21<0.45", "jet2Tau32_pres", "2^{nd} Leading Jet #tau_{32}", "jet2Tau32_pres", False )
MakePlot( "jet2Tau32", [ 20, 0., 1. ], "jet2Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "jet2Tau32_sel", "2^{nd} Leading Jet #tau_{32}", "jet2Tau32_sel", False )
MakePlot( "jet2Tau32", [ 20, 0., 1. ], "jet2Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets", "jet2Tau32_selN", "2^{nd} Leading Jet #tau_{32}", "jet2Tau32_selN", False )


# jet*Tau31, pres, [ 20, 0., 1. ]
MakePlot( "jet1Tau31", [ 20, 0., 1. ], "1.", "jet1Tau31_NoCuts", "Leading Jet #tau_{31}", "jet1Tau31_NoCuts", False )
MakePlot( "jet1Tau31", [ 20, 0., 1. ], "jet1Tau21<0.45&jet2Tau21<0.45", "jet1Tau31_pres", "Leading Jet #tau_{31}", "jet1Tau31_pres", False )
MakePlot( "jet1Tau31", [ 20, 0., 1. ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "jet1Tau31_sel", "Leading Jet #tau_{31}", "jet1Tau31_sel", False )
MakePlot( "jet1Tau31", [ 20, 0., 1. ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "jet1Tau31_selN", "Leading Jet #tau_{31}", "jet1Tau31_selN", False )
MakePlot( "jet2Tau31", [ 20, 0., 1. ], "1.", "jet2Tau31_NoCuts", "2^{nd} Leading Jet #tau_{31}", "jet2Tau31_NoCuts", False )
MakePlot( "jet2Tau31", [ 20, 0., 1. ], "jet2Tau21<0.45&jet2Tau21<0.45", "jet2Tau31_pres", "2^{nd} Leading Jet #tau_{31}", "jet2Tau31_pres", False )
MakePlot( "jet2Tau31", [ 20, 0., 1. ], "jet2Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "jet2Tau31_sel", "2^{nd} Leading Jet #tau_{31}", "jet2Tau31_sel", False )
MakePlot( "jet2Tau31", [ 20, 0., 1. ], "jet2Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "jet2Tau31_selN", "2^{nd} Leading Jet #tau_{31}", "jet2Tau31_selN", False )


# jet*CosThetaStar??, pres, [20, 0., 1.]

# jet*SubjetPtRatio??, pres (log), [20, 0., 1.]


# jet*Pt, pres (log), [60, 400, 1000]
MakePlot( "jet1Pt", [ 60, 400., 1000. ], "1.", "jet1Pt_NoCuts", "Leading Jet p_{T}", "jet1Pt_NoCuts", True )
MakePlot( "jet1Pt", [ 60, 400., 1000. ], "jet1Tau21<0.45&jet2Tau21<0.45", "jet1Pt_pres", "Leading Jet p_{T}", "jet1Pt_pres", True )
MakePlot( "jet1Pt", [ 60, 400., 1000. ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "jet1Pt_sel", "Leading Jet p_{T}", "jet1Pt_sel", True )
MakePlot( "jet1Pt", [ 60, 400., 1000. ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "jet1Pt_selN", "Leading Jet p_{T}", "jet1Pt_selN", True )
MakePlot( "jet2Pt", [ 60, 400., 1000. ], "1.", "jet2Pt_NoCuts", "2^{nd} Leading Jet p_{T}", "jet2Pt_NoCuts", True )
MakePlot( "jet2Pt", [ 60, 400., 1000. ], "jet2Tau21<0.45&jet2Tau21<0.45", "jet2Pt_pres", "2^{nd} Leading Jet p_{T}", "jet2Pt_pres", True )
MakePlot( "jet2Pt", [ 60, 400., 1000. ], "jet2Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "jet2Pt_sel", "2^{nd} Leading Jet p_{T}", "jet2Pt_sel", True )
MakePlot( "jet2Pt", [ 60, 400., 1000. ], "jet2Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "jet2Pt_selN", "2^{nd} Leading Jet p_{T}", "jet2Pt_selN", True )


# jet*Eta, pres [12, -3, 3]
MakePlot( "jet1Eta", [ 12, -3, 3 ], "1.", "jet1Eta_NoCuts", "Leading Jet #eta", "jet1Eta_NoCuts", False )
MakePlot( "jet1Eta", [ 12, -3, 3 ], "jet1Tau21<0.45&jet2Tau21<0.45", "jet1Eta_pres", "Leading Jet #eta", "jet1Eta_pres", False )
MakePlot( "jet1Eta", [ 12, -3, 3 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "jet1Eta_sel", "Leading Jet #eta", "jet1Eta_sel", False )
MakePlot( "jet1Eta", [ 12, -3, 3 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "jet1Eta_selN", "Leading Jet #eta", "jet1Eta_selN", False )
MakePlot( "jet2Eta", [ 12, -3, 3 ], "1.", "jet2Eta_NoCuts", "2^{nd} Leading Jet #eta", "jet2Eta_NoCuts", False )
MakePlot( "jet2Eta", [ 12, -3, 3 ], "jet2Tau21<0.45&jet2Tau21<0.45", "jet2Eta_pres", "2^{nd} Leading Jet #eta", "jet2Eta_pres", False )
MakePlot( "jet2Eta", [ 12, -3, 3 ], "jet2Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "jet2Eta_sel", "2^{nd} Leading Jet #eta", "jet2Eta_sel", False )
MakePlot( "jet2Eta", [ 12, -3, 3 ], "jet2Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "jet2Eta_selN", "2^{nd} Leading Jet #eta", "jet2Eta_selN", False )


# jet*PrunedMass, pres (log), [ 60, 0, 600]
MakePlot( "jet1PrunedMass", [ 60, 0, 600 ], "1.", "jet1PrunedMass_NoCuts", "Leading Jet Mass", "jet1PrunedMass_NoCuts", True )
MakePlot( "jet1PrunedMass", [ 60, 0, 600 ], "jet1Tau21<0.45&jet2Tau21<0.45", "jet1PrunedMass_pres", "Leading Jet Mass", "jet1PrunedMass_pres", True )
MakePlot( "jet1PrunedMass", [ 60, 0, 600 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "jet1PrunedMass_sel", "Leading Jet Mass", "jet1PrunedMass_sel", True )
MakePlot( "jet1PrunedMass", [ 60, 0, 600 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "jet1PrunedMass_selN", "Leading Jet Mass", "jet1PrunedMass_selN", True )
MakePlot( "jet2PrunedMass", [ 60, 0, 600 ], "1.", "jet2PrunedMass_NoCuts", "2^{nd} Leading Jet Mass", "jet2PrunedMass_NoCuts", True )
MakePlot( "jet2PrunedMass", [ 60, 0, 600 ], "jet2Tau21<0.45&jet2Tau21<0.45", "jet2PrunedMass_pres", "2^{nd} Leading Jet Mass", "jet2PrunedMass_pres", True )
MakePlot( "jet2PrunedMass", [ 60, 0, 600 ], "jet2Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "jet2PrunedMass_sel", "2^{nd} Leading Jet Mass", "jet2PrunedMass_sel", True )
MakePlot( "jet2PrunedMass", [ 60, 0, 600 ], "jet2Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "jet2PrunedMass_selN", "2^{nd} Leading Jet Mass", "jet2PrunedMass_selN", True )


# MET, pres, [20, 0, 200]
MakePlot( "MET", [ 20, 0, 200 ], "1.", "MET_NoCuts", "MET", "MET_NoCuts", False )
MakePlot( "MET", [ 20, 0, 200 ], "jet1Tau21<0.45&jet2Tau21<0.45", "MET_pres", "MET", "MET_pres", False )
MakePlot( "MET", [ 20, 0, 200 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5", "MET_sel", "MET", "MET_sel", False )
MakePlot( "MET", [ 20, 0, 200 ], "jet1Tau21<0.45&jet2Tau21<0.45&prunedMassAsym<0.1&deltaEtaDijet<1.5&numJets==2", "MET_selN", "MET", "MET_selN", False )
'''
