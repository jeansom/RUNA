#!/usr/bin/env python

#from ROOT import TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from ROOT import *
import ROOT as rt

def setSelection( listSel, xMin=0.65, yMax=0.65, align='right' ):

	for i in range( len( listSel ) ):
		textBox=rt.TLatex()
		textBox.SetNDC()
		textBox.SetTextSize(0.04) 
		if 'right' in align: textBox.SetTextAlign(31)
		textBox.SetTextFont(62) ### 62 is bold, 42 is normal
		textBox.DrawLatex(xMin, yMax, listSel[i])
		yMax = yMax -0.05
	

def labels( name, PU, camp, X=0.92, Y=0.50, align='right', listSel=[] ):

	if 'cutHT' in name: listSel = [ camp, PU, 'jet p_{T} > 150 GeV', 'jet |#eta| < 2.4', 'HT > 800 GeV' ] 
	elif 'cutDijet' in name: listSel = [ camp, PU, 'jet p_{T} > 150 GeV', 'jet |#eta| < 2.4', 'HT > 800 GeV', 'numJets > 1' ] 
	elif ( 'cutAsym' in name ) or ('cutMassAsym' in name): listSel = [ camp, PU, 'HT > 800 GeV', 'numJets > 1', 'A < 0.1' ]
	elif 'cutTau21' in name: listSel = [ camp, PU, 'HT > 800 GeV', 'numJets > 1', 'A < 0.1', '#tau_{21} < 0.4']
	elif 'cutCosTheta' in name: listSel = [ camp, PU,  'HT > 800 GeV', 'numJets > 1','A < 0.1', '#tau_{21} < 0.4', '|cos(#theta*)| < 0.4']
	elif 'cutDEta' in name: listSel = [ camp, PU,  'HT > 800 GeV', 'numJets > 1','A < 0.1, #tau_{21} < 0.4', '|cos(#theta*)| < 0.4', '#Delta #eta (j^{1},j^{2}) > 1']
	elif 'cutBtag' in name: listSel = [ camp, PU,  'HT > 800 GeV', 'numJets > 1','A < 0.1, #tau_{21} < 0.4', '|cos(#theta*)| < 0.4', '#Delta #eta (j^{1},j^{2}) > 1', 'num Btag = 1']
	#elif 'cutSubjetPtRatio' in name: listSel = [ camp, PU,  'HT > 800 GeV', 'numJets > 1','A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3']
	elif 'cutBtagAfterSubjetPtRatio' in name: listSel = [ camp, PU,  'HT > 800 GeV', 'numJets > 1','A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3', '1 btag CSVM']
	elif 'Standard' in name: listSel = [ camp, PU, 'HT > 800 GeV', 'numJets > 1', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3']
	elif 'PFHT800' in name: listSel = [ camp, PU, 'PFHT800', 'HT > 800 GeV', 'numJets > 1', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3']
	elif 'Brock' in name: listSel = [ camp, PU, 'HT > 1600 TeV', 'HT > 800 GeV', 'numJets > 1', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3']
	elif 'cutTau31' in name: listSel = [ camp, PU, 'HT > 800 GeV', 'numJets > 1', 'A < 0.1', '|cos(#theta*)| < 0.3', '#tau_{31} < 0.4']
	#elif 'triggerDATA' in name: listSel =  [  'Eff. (AK8 H_{T} > 700 GeV, trimmed AK8 jet mass > 50 GeV)']
	#elif 'triggerSignal' in name: listSel =  [ 'RPV Stop 100 GeV', triggerUsed.replace('650', '650TrimMass50')]
	#elif 'triggerSignal' in name: listSel =  [ 'pp #rightarrow #tilde{t}(jj) #tilde{t}(jj), M(#tilde{t}) = 100 GeV', 'Eff. (AK8 H_{T} > 650 GeV, trimmed AK8 jet mass > 50 GeV)']
	#elif 'trigger' in name: listSel = [ 'pp #rightarrow #tilde{t}(jj) #tilde{t}(jj), M(#tilde{t}) = 100 GeV', 'AK4 H_{T} > 800 GeV AND', 'AK8 H_{T} > 650 GeV, trimmed AK8 jet mass > 50 GeV' ] 
	#elif 'trigger' in name: listSel = [ 'pp #rightarrow #tilde{t}(jj) #tilde{t}(jj), M(#tilde{t}) = 100 GeV', 'AK4 H_{T} > 800 GeV' ] 
	#elif 'trigger' in name: listSel = [ 'pp #rightarrow #tilde{t}(jj) #tilde{t}(jj), M(#tilde{t}) = 100 GeV', 'AK8 H_{T} > 700 GeV, trimmed AK8 jet mass > 50 GeV' ] 
	#elif 'rigger' in name: listSel = [ 'pp #rightarrow #tilde{t}(jj) #tilde{t}(jj), M(#tilde{t}) = 100 GeV', 'NO Trigger' ] 
	elif 'cut4Jet' in name: listSel = [ camp, PU, 'jet p_{T} > 50 GeV', 'jet |#eta| < 2.4', 'numJets > 3' ] 
	elif 'cut4JetPt' in name: listSel = [ camp, PU, 'jet p_{T} > 50 GeV', 'jet |#eta| < 2.4', 'numJets > 3', 'HT > 800 GeV' ] 
	elif 'cutBestPair' in name: listSel = [ camp, PU, 'numJets > 3', 'HT > 800 GeV', 'dR_{dijet}' ] 
	elif 'cutMassRes' in name: listSel = [ camp, PU, 'numJets > 3', 'HT > 800 GeV', 'dR_{dijet}', 'mass balance < 0.30' ] 
	elif 'cutDelta' in name: listSel = [ camp, PU, 'numJets > 3', 'HT > 800 GeV', 'dR_{dijet}', 'mass balance < 0.30', '#Delta < 70 GeV' ] 
	elif 'cutEtaBand' in name: listSel = [ camp, PU, 'dR_{dijet}', 'mass balance < 0.30', '#Delta < 70 GeV', '| #eta_1 - #eta_2| < 1' ] 
	elif '' in name: listSel = [ '' ] 
	else: listSel = [ 'NO LABEL' ]

	setSelection( listSel, X, Y, align) 

def labelAxis(name, histo, Grom ):

	if 'massAve' in name: 
		if 'Trimmed' in Grom: histo.GetXaxis().SetTitle( 'Average Trimmed Mass [GeV]' )
		elif 'Pruned' in Grom: histo.GetXaxis().SetTitle( 'Average Pruned Mass [GeV]' )
		elif 'Filtered' in Grom: histo.GetXaxis().SetTitle( 'Average Filtered Mass [GeV]' )
		else: histo.GetXaxis().SetTitle( 'Average Mass [GeV]' )
	elif 'TrimmedMass' in name: histo.GetXaxis().SetTitle( 'Leading Trimmed Jet Mass [GeV]' )
	elif 'massAsymmetry' in name: histo.GetXaxis().SetTitle( 'Mass Asymmetry (A)' )
	elif 'jet1CosThetaStar' in name: histo.GetXaxis().SetTitle( 'cos(#theta *)_{1}' )
	elif 'jet2CosThetaStar' in name: histo.GetXaxis().SetTitle( 'cos(#theta *)_{2}' )
	elif 'jetEta' in name: histo.GetXaxis().SetTitle( 'Jet #eta' )
	elif 'Tau1_' in name: histo.GetXaxis().SetTitle( '#tau_{1}' )
	elif 'Tau2_' in name: histo.GetXaxis().SetTitle( '#tau_{2}' )
	elif 'Tau3_' in name: histo.GetXaxis().SetTitle( '#tau_{3}' )
	elif 'jet1Tau21_' in name: histo.GetXaxis().SetTitle( 'Leading Jet #tau_{21} ' )
	elif 'jet2Tau21_' in name: histo.GetXaxis().SetTitle( '2nd Leading Jet #tau_{21} ' )
	elif 'Tau31_' in name: histo.GetXaxis().SetTitle( '#tau_{31} ' )
	elif 'Tau32_' in name: histo.GetXaxis().SetTitle( '#tau_{32} ' )
	elif 'PtRatio_' in name: histo.GetXaxis().SetTitle( 'Subjet Pt_{2}/Pt_{1}' )
	elif 'Mass21' in name: histo.GetXaxis().SetTitle( 'Subjet m_{2}/m_{1}' )
	elif '112Mass' in name: histo.GetXaxis().SetTitle( 'Subjet m_{1}/m_{12}' )
	elif '212Mass' in name: histo.GetXaxis().SetTitle( 'Subjet m_{2}/m_{12}' )
	elif 'PolAngle13412_' in name: histo.GetXaxis().SetTitle( 'cos #psi_{1(34)}^{[12]}' )
	elif 'PolAngle31234_' in name: histo.GetXaxis().SetTitle( 'cos #psi_{3(12)}^{[34]}' )
	elif 'jetMass' in name: histo.GetXaxis().SetTitle( 'Jet Mass [GeV]' )
	elif 'jetPt' in name: histo.GetXaxis().SetTitle( 'Jet p_{T} [GeV]' )
	elif 'jet1Pt' in name: histo.GetXaxis().SetTitle( 'Leading Jet p_{T} [GeV]' )
	elif 'jet1Mass' in name: histo.GetXaxis().SetTitle( 'Leading Pruned Jet Mass [GeV]' )
	elif 'jet1Eta' in name: histo.GetXaxis().SetTitle( 'Leading Jet #eta' )
	elif 'jet2Pt' in name: histo.GetXaxis().SetTitle( '2nd Leading Jet p_{T} [GeV]' )
	elif 'jet3Pt' in name: histo.GetXaxis().SetTitle( '3rd Leading Jet p_{T} [GeV]' )
	elif 'jet4Pt' in name: histo.GetXaxis().SetTitle( '4th Leading Jet p_{T} [GeV]' )
	elif 'jet2Mass' in name: histo.GetXaxis().SetTitle( '2nd Leading Pruned Jet Mass [GeV]' )
	elif 'jet2Eta' in name: histo.GetXaxis().SetTitle( '2nd Leading Jet #eta' )
	elif 'jetNum' in name: histo.GetXaxis().SetTitle( 'Number of Jets' )
	elif 'deltaEta' in name: histo.GetXaxis().SetTitle( '#Delta #eta (j^{1}, j^{2})' )
	elif 'NPV' in name: histo.GetXaxis().SetTitle( 'Number of Primary Vertex' )
	elif 'HT' in name: histo.GetXaxis().SetTitle( 'HT [GeV]' )
	elif 'massRes' in name: histo.GetXaxis().SetTitle( 'Fractional mass difference' )
	elif 'neutralHadronEnergy' in name: histo.GetXaxis().SetTitle( 'Neutral hadron energy' )
	elif 'neutralEmEnergy' in name: histo.GetXaxis().SetTitle( 'Neutral EM energy' )
	elif 'chargedHadronEnergy' in name: histo.GetXaxis().SetTitle( 'Charged hadron energy' )
	elif 'chargedEmEnergy' in name: histo.GetXaxis().SetTitle( 'Charged EM energy' )
	elif 'chargedMultiplicity' in name: histo.GetXaxis().SetTitle( 'Charged multiplicity' )
	elif 'numConst' in name: histo.GetXaxis().SetTitle( 'Number of Constituents' )
	#elif '' in name: histo.GetXaxis().SetTitle( '' )
	else: histo.GetXaxis().SetTitle( 'NO LABEL' )
