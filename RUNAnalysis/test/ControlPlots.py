#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy
import pdb

import Plotting_Header
from Plotting_Header import *

def MakeProfilePlot(VAR1, VAR2, BINS1, BINS2, CUT, NAME, Title1, Title2):
	QCD = TH2F("QCD", "QCD", BINS1[0], BINS1[1], BINS1[2], BINS2[0], BINS2[1], BINS2[2])
	TT = TH2F("TT", "hadronic t#bar{t}", BINS1[0], BINS1[1], BINS1[2], BINS2[0], BINS2[1], BINS2[2])
	SIG = TH2F("SIG", "RPV Signal, M=100 GeV", BINS1[0], BINS1[1], BINS1[2], BINS2[0], BINS2[1], BINS2[2])
	quick2dplot("/eos/uscms/store/user/osherson/RU_Boosted_B/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", QCD, VAR1, VAR2, CUT, "1.0")

	quick2dplot("/eos/uscms/store/user/osherson/RU_Boosted_B/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", TT, VAR1, VAR2, CUT, "1.0")

	quick2dplot("/eos/uscms/store/user/osherson/RU_Boosted_B/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", SIG, VAR1, VAR2, CUT, "1.0")

	profQCD = QCD.ProfileX("profQCD")
	profTT = TT.ProfileX("profTT")
	profSIG = SIG.ProfileX("profSIG")

	for i in [QCD,SIG,TT]:
		i.SetStats(0)
		i.GetYaxis().SetTitle(Title2)
		i.GetXaxis().SetTitle(Title1)
		i.Scale(1/i.Integral())

	opt = "COL"

	C = TCanvas("C"+VAR1+VAR2+CUT, "", 1500,500)
	C.Divide(3,1)
	C.cd(1)
	QCD.Draw(opt)
	profQCD.Draw("same")
	C.cd(2)
	TT.Draw(opt)
	profTT.Draw("same")
	C.cd(3)
	SIG.Draw(opt)
	profSIG.Draw("same")
	C.SaveAs(NAME+".gif")



def MakePlot(VAR, BINS, CUT, NAME, Title, cutName):
	normQCD = TH1F("NORMQCD_"+VAR, "", BINS[0], BINS[1], BINS[2])
	normTT = TH1F("NORMTT_"+VAR, "", BINS[0], BINS[1], BINS[2])
	normSig = TH1F("NORMSig_"+VAR, "", BINS[0], BINS[1], BINS[2])
	
	PlotsQCD = TH1F("QCD_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsSig = TH1F("Sig_"+VAR, "", BINS[0], BINS[1], BINS[2])
	PlotsTT = TH1F("TT_"+VAR, "", BINS[0], BINS[1], BINS[2])

	quickplot("/eos/uscms/store/user/osherson/RU_Boosted_B/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", normQCD, VAR, "jet1Pt>-1.0", "1.0")
	quickplot("/eos/uscms/store/user/osherson/RU_Boosted_B/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", normSig, VAR, "jet1Pt>-1.0", "1.0")
	quickplot("/eos/uscms/store/user/osherson/RU_Boosted_B/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", normTT, VAR, "jet1Pt>-1.0", "1.0")

	###
	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print "QCD Events considered: " + str(normQCD.Integral())
	print "TT Events considered: " + str(normTT.Integral())
	print "Signal Events considered: " + str(normSig.Integral())

	quickplot("/eos/uscms/store/user/osherson/RU_Boosted_B/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsQCD, VAR, CUT, "1.0")
	quickplot("/eos/uscms/store/user/osherson/RU_Boosted_B/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsSig, VAR, CUT, "1.0")
	quickplot("/eos/uscms/store/user/osherson/RU_Boosted_B/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", PlotsTT, VAR, CUT, "1.0")

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
		i.Scale(1/i.Integral())
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
#MakePlot("jet1PrunedMass", [60,0,300],"jet1Pt>0.","ControlPlot_Jet1PrunedMass_noCuts")
#MakePlot("jet1PrunedMass", [60,0,300],"jet1Pt>300.","ControlPlot_Jet1PrunedMass_jet1Pt>300")
#MakePlot("jet1PrunedMass", [60,0,300],"jet1Pt>500.","ControlPlot_Jet1PrunedMass_jet1Pt>500")
#MakePlot("jet2PrunedMass", [60,0,300],"jet1Pt>0.","ControlPlot_Jet2PrunedMass_noCut")
#MakePlot("jet2PrunedMass", [60,0,300],"jet2Pt>300.","ControlPlot_Jet2PrunedMass_jet2Pt>300")
#MakePlot("jet2PrunedMass", [60,0,300],"jet2Pt>500.","ControlPlot_Jet2PrunedMass_jet2Pt>500")


#MakePlot("jet1PrunedMass", [60,0,300],"jet1btagCSVv2>0.8","ControlPlot_Jet1PrunedMass_CSVM")
#MakePlot("jet1PrunedMass", [60,0,300],"jet1Pt>300.&jet1btagCSVv2>0.8","ControlPlot_Jet1PrunedMass_jet1Pt>300_CSVM")
#MakePlot("jet1PrunedMass", [60,0,300],"jet1Pt>500.&jet1btagCSVv2>0.8","ControlPlot_Jet1PrunedMass_jet1Pt>500_CSVM")
#MakePlot("jet2PrunedMass", [60,0,300],"jet2btagCSVv2>0.8","ControlPlot_Jet2PrunedMass_CSVM")
#MakePlot("jet2PrunedMass", [60,0,300],"jet2Pt>300.&jet2btagCSVv2>0.8","ControlPlot_Jet2PrunedMass_jet2Pt>300_CSVM")
#MakePlot("jet2PrunedMass", [60,0,300],"jet2Pt>500.&jet2btagCSVv2>0.8","ControlPlot_Jet2PrunedMass_jet2Pt>500_CSVM")

#MakePlot("jet1PrunedMass", [60,0,300],"(subjet12btagCSVv2>0.8||subjet11btagCSVv2>0.8)","ControlPlot_Jet1PrunedMass_sCSVM")
#MakePlot("jet1PrunedMass", [60,0,300],"jet1Pt>300.&(subjet12btagCSVv2>0.8||subjet11btagCSVv2>0.8)","ControlPlot_Jet1PrunedMass_jet1Pt>300_sCSVM")
#MakePlot("jet1PrunedMass", [60,0,300],"jet1Pt>500.&(subjet12btagCSVv2>0.8||subjet11btagCSVv2>0.8)","ControlPlot_Jet1PrunedMass_jet1Pt>500_sCSVM")
#MakePlot("jet2PrunedMass", [60,0,300],"(subjet22btagCSVv2>0.8||subjet21btagCSVv2>0.8)","ControlPlot_Jet2PrunedMass_sCSVM")
#MakePlot("jet2PrunedMass", [60,0,300],"jet2Pt>300.&(subjet22btagCSVv2>0.8||subjet21btagCSVv2>0.8)","ControlPlot_Jet2PrunedMass_jet2Pt>300_sCSVM")
#MakePlot("jet2PrunedMass", [60,0,300],"jet2Pt>500.&(subjet22btagCSVv2>0.8||subjet21btagCSVv2>0.8)","ControlPlot_Jet2PrunedMass_jet2Pt>500_sCSVM")


#MakePlot("jet1PrunedMass", [60,0,300],"((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))","ControlPlot_Jet1PrunedMass_sCSVMex")
#MakePlot("jet1PrunedMass", [60,0,300],"jet1Pt>300.&((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))","ControlPlot_Jet1PrunedMass_jet1Pt>300_sCSVMex")
#MakePlot("jet1PrunedMass", [60,0,300],"jet1Pt>500.&((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))","ControlPlot_Jet1PrunedMass_jet1Pt>500_sCSVMex")
#MakePlot("jet2PrunedMass", [60,0,300],"((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))","ControlPlot_Jet2PrunedMass_sCSVMex")
#MakePlot("jet2PrunedMass", [60,0,300],"jet2Pt>300.&((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))","ControlPlot_Jet2PrunedMass_jet2Pt>300_sCSVMex")
#MakePlot("jet2PrunedMass", [60,0,300],"jet2Pt>500.&((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))","ControlPlot_Jet2PrunedMass_jet2Pt>500_sCSVMex")


#MakePlot("jet1PrunedMass", [60,0,300],"((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))&((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))","ControlPlot_Jet1PrunedMass_2xsCSVMex")
#MakePlot("jet1PrunedMass", [60,0,300],"jet1Pt>300.&((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))&((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))","ControlPlot_Jet1PrunedMass_jet1Pt>300_2xsCSVMex")
#MakePlot("jet1PrunedMass", [60,0,300],"jet1Pt>500.&((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))&((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))","ControlPlot_Jet1PrunedMass_jet1Pt>500_2xsCSVMex")
#MakePlot("jet2PrunedMass", [60,0,300],"((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))&((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))","ControlPlot_Jet2PrunedMass_2xsCSVMex")
#MakePlot("jet2PrunedMass", [60,0,300],"jet2Pt>300.&((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))&((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))","ControlPlot_Jet2PrunedMass_jet2Pt>300_2xsCSVMex")
#akePlot("jet2PrunedMass", [60,0,300],"jet2Pt>500.&((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))&((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))","ControlPlot_Jet2PrunedMass_jet2Pt>500_2xsCSVMex")



#MakePlot("massAve", [80,0,400], "prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))&((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))","ControlPlot_JeanCuts", "Average Mass [GeV]", "Full Selection")

MakeProfilePlot("prunedMassAsym", "deltaEtaDijet", [25,0,1], [25,0,4], "jet1Pt>0.", "ControlPlot_ABCDcorr_noCut", "Mass Asymmetry", "#Delta#eta (j1,j2)")

MakeProfilePlot("prunedMassAsym", "deltaEtaDijet", [25,0,1], [25,0,4], "jet1Tau21<0.6&jet2Tau21<0.6", "ControlPlot_ABCDcorr_TauCuts", "Mass Asymmetry", "#Delta#eta (j1,j2)")

MakeProfilePlot("prunedMassAsym", "deltaEtaDijet", [25,0,1], [25,0,4], "jet1Tau21<0.6&jet2Tau21<0.6&((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))&((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))", "ControlPlot_ABCDcorr_FullSel", "Mass Asymmetry", "#Delta#eta (j1,j2)")

#MakePlot("massAve", [80,0,400], "jet1Tau32>0.51&jet2Tau32>0.51&prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))&((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))","ControlPlot_JeanCuts2", "Average Mass [GeV]", "Full Selection w/ anti-top tag")

#MakePlot("massAve", [80,0,400], "(jet1Tau32<0.6||jet2Tau32<0.6)&prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))&((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))","ControlPlot_JeanCuts4", "Average Mass [GeV]", "Full Selection w/ top tag")

#MakePlot("massAve", [80,0,400], "jet1Tau32>0.6&jet2Tau32>0.6&prunedMassAsym<0.1&deltaEtaDijet<1.0&jet1Tau21<0.6&jet2Tau21<0.6&((subjet22btagCSVv2>0.8&subjet21btagCSVv2<0.8)||(subjet21btagCSVv2>0.8&subjet22btagCSVv2<0.8))&((subjet12btagCSVv2>0.8&subjet11btagCSVv2<0.8)||(subjet11btagCSVv2>0.8&subjet12btagCSVv2<0.8))","ControlPlot_JeanCuts3", "Average Mass [GeV]", "Full Selection w/ harsh anti-top tag")



