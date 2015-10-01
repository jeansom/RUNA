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
	

def labels( name, triggerUsed, PU, camp, X=0.92, Y=0.50, align='right', listSet=[] ):
	if 'cutHT' in name: setSelection( [ camp, PU, triggerUsed, 'jet p_{T} > 150 GeV', 'jet |#eta| < 2.4', 'HT > 800 GeV' ] , X, Y, align)
	elif 'cutDijet' in name: setSelection( [ camp, PU, triggerUsed, 'jet p_{T} > 150 GeV', 'jet |#eta| < 2.4', 'HT > 800 GeV', 'numJets > 1' ] , X, Y, align)
	elif ( 'cutAsym' in name ) or ('cutMassAsym' in name): setSelection( [ camp, PU, triggerUsed, 'HT > 800 GeV', 'numJets > 1', 'A < 0.1' ], X, Y, align )
	elif 'cutTau21' in name: setSelection( [ camp, PU, triggerUsed, 'HT > 800 GeV', 'numJets > 1', 'A < 0.1', '#tau_{21} < 0.5'],  X, Y, align )
	elif 'cutCosTheta' in name: setSelection( [ camp, PU, triggerUsed,  'HT > 800 GeV', 'numJets > 1','A < 0.1', '#tau_{21} < 0.5', '|cos(#theta*)| < 0.4'], X, Y, align )
	elif 'cutDEta' in name: setSelection( [ camp, PU, triggerUsed,  'HT > 800 GeV', 'numJets > 1','A < 0.1, #tau_{21} < 0.5', '|cos(#theta*)| < 0.4', '#Delta #eta (j^{1},j^{2}) > 1'], X, Y, align )
	elif 'cutBtag' in name: setSelection( [ camp, PU, triggerUsed,  'HT > 800 GeV', 'numJets > 1','A < 0.1, #tau_{21} < 0.5', '|cos(#theta*)| < 0.4', '#Delta #eta (j^{1},j^{2}) > 1', 'num Btag = 1'], X, Y, align )
	#elif 'cutSubjetPtRatio' in name: setSelection( [ camp, PU, triggerUsed,  'HT > 800 GeV', 'numJets > 1','A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3'],  X, Y, align )
	elif 'cutBtagAfterSubjetPtRatio' in name: setSelection( [ camp, PU, triggerUsed,  'HT > 800 GeV', 'numJets > 1','A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3', '1 btag CSVM'],  X, Y+0.05, align )
	elif 'Standard' in name: setSelection( [ camp, PU, triggerUsed, 'HT > 800 GeV', 'numJets > 1', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3'],  X, Y, align )
	elif 'PFHT800' in name: setSelection( [ camp, PU, 'PFHT800', 'HT > 800 GeV', 'numJets > 1', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3'],  X, Y, align )
	elif 'Brock' in name: setSelection( [ camp, PU, 'HT > 1600 TeV', 'HT > 800 GeV', 'numJets > 1', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3'],  X, Y, align )
	elif 'cutTau31' in name: setSelection( [ camp, PU, triggerUsed, 'HT > 800 GeV', 'numJets > 1', 'A < 0.1', '|cos(#theta*)| < 0.3', '#tau_{31} < 0.4'],  X, Y, align )
	elif 'triggerDATA' in name: setSelection(  [ triggerUsed,  'Eff. (AK8 H_{T} > 700 GeV, trimmed AK8 jet mass > 50 GeV)'], X, Y, align )
	#elif 'triggerSignal' in name: setSelection(  [ 'RPV Stop 100 GeV', triggerUsed.replace('650', '650TrimMass50')], X, Y, align )
	elif 'triggerSignal' in name: setSelection(  [ 'pp #rightarrow #tilde{t}(jj) #tilde{t}(jj), M(#tilde{t}) = 100 GeV', 'Eff. (AK8 H_{T} > 650 GeV, trimmed AK8 jet mass > 50 GeV)'], X, Y, align )
	#elif 'trigger' in name: setSelection( [ 'pp #rightarrow #tilde{t}(jj) #tilde{t}(jj), M(#tilde{t}) = 100 GeV', 'AK4 H_{T} > 800 GeV AND', 'AK8 H_{T} > 650 GeV, trimmed AK8 jet mass > 50 GeV' ], X, Y, align) 
	#elif 'trigger' in name: setSelection( [ 'pp #rightarrow #tilde{t}(jj) #tilde{t}(jj), M(#tilde{t}) = 100 GeV', 'AK4 H_{T} > 800 GeV' ], X, Y, align) 
	elif 'trigger' in name: setSelection( [ 'pp #rightarrow #tilde{t}(jj) #tilde{t}(jj), M(#tilde{t}) = 100 GeV', 'AK8 H_{T} > 700 GeV, trimmed AK8 jet mass > 50 GeV' ], X, Y, align) 
	#elif 'rigger' in name: setSelection( [ 'pp #rightarrow #tilde{t}(jj) #tilde{t}(jj), M(#tilde{t}) = 100 GeV', 'NO Trigger' ], X, Y, align) 
	else: setSelection( '', X, Y, align) 

def labelAxis(name, histo, Grom ):

	if 'massAve' in name: 
		if 'Trimmed' in Grom: histo.GetXaxis().SetTitle( 'Average Trimmed Mass [GeV]' )
		elif 'Pruned' in Grom: histo.GetXaxis().SetTitle( 'Average Pruned Mass [GeV]' )
		elif 'Filtered' in Grom: histo.GetXaxis().SetTitle( 'Average Filtered Mass [GeV]' )
		else: histo.GetXaxis().SetTitle( 'Average Mass [GeV]' )
	elif 'TrimmedMass' in name: histo.GetXaxis().SetTitle( 'Leading Trimmed Jet Mass [GeV]' )
	elif 'massAsymmetry' in name: histo.GetXaxis().SetTitle( 'Mass Asymmetry (A)' )
	elif 'cosThetaStar' in name: histo.GetXaxis().SetTitle( 'cos(#theta *)' )
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
	elif 'jet2Mass' in name: histo.GetXaxis().SetTitle( '2nd Leading Pruned Jet Mass [GeV]' )
	elif 'jet2Eta' in name: histo.GetXaxis().SetTitle( '2nd Leading Jet #eta' )
	elif 'jetNum' in name: histo.GetXaxis().SetTitle( 'Number of Jets' )
	elif 'deltaEta' in name: histo.GetXaxis().SetTitle( '#Delta #eta (j^{1}, j^{2})' )
	elif 'NPV' in name: histo.GetXaxis().SetTitle( 'Number of Primary Vertex' )
	elif 'HT' in name: histo.GetXaxis().SetTitle( 'HT [GeV]' )
	else: histo.GetXaxis().SetTitle( 'NO LABEL' )
