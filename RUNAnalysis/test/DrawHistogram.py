#!/usr/bin/env python
'''
File: DrawHistogram.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Draw histograms. Check for options at the end.
'''

#from ROOT import TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from ROOT import *
from setTDRStyle import *
import time, os, math, sys
#import tarfile
#import optparse


gROOT.Reset()
gROOT.SetBatch()
setTDRStyle()
gROOT.ForceStyle()
gROOT.SetStyle('tdrStyle')


gStyle.SetOptStat(0)

def plot( inFileSignal, inFileQCD, Grom, name, xmax, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_RPVSt100tojj_QCD_AnalysisPlots.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Signal' ] = inFileSignal.Get( 'AnalysisPlots'+Grom+'/'+name )
	histos[ 'QCD' ] = inFileQCD.Get( 'AnalysisPlots'+Grom+'/'+name )

	if not Norm:
		#histos[ 'Signal' ].Scale(100)
		histos[ 'Signal' ].SetFillColor(48)
		histos[ 'Signal' ].SetFillStyle(1001)
		#histos[ 'QCD' ].Scale(1)
		histos[ 'QCD' ].SetFillColor(38)
		histos[ 'QCD' ].SetFillStyle(1001)

		stackHisto = THStack('stackHisto', 'stack')
		stackHisto.Add( histos['QCD'] )
		stackHisto.Add( histos['Signal'] )

	else:
		histos[ 'Signal' ].SetLineWidth(2)
		histos[ 'Signal' ].SetLineColor(48)
		histos[ 'QCD' ].SetLineColor(38)
		histos[ 'QCD' ].SetLineWidth(2)

#	histos.values()[0].SetMaximum( 2* max( listMax ) ) 
#	histos.values()[0].GetXaxis().SetRange( 0, xmax )
	binWidth = histos['Signal'].GetBinWidth(1)

	legend=TLegend(0.65,0.70,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	can = TCanvas('c1', 'c1',  10, 10, 800, 500 )
	if log: 
		can.SetLogy()
		outName = outputFileName.replace('_AnalysisPlots','_Log_AnalysisPlots')
	else:
		outName = outputFileName 

	if not Norm:
		legend.AddEntry( histos[ 'Signal' ], 'RPV Stop 100 GeV' , 'f' )
		legend.AddEntry( histos[ 'QCD' ], 'QCD + Signal' , 'f' )
		stackHisto.SetMinimum(10)
		stackHisto.Draw('hist')
		histos['Signal'].Draw('hist same')
		stackHisto.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

		if 'massAve' in name: 
			if 'Trim' in Grom: stackHisto.GetXaxis().SetTitle( 'Average Trimmed Mass [GeV]' )
			elif 'Prun' in Grom: stackHisto.GetXaxis().SetTitle( 'Average Pruned Mass [GeV]' )
			elif 'Fil' in Grom: stackHisto.GetXaxis().SetTitle( 'Average Filtered Mass [GeV]' )
			else: stackHisto.GetXaxis().SetTitle( 'Average Mass [GeV]' )
		elif 'massAsymmetry' in name: stackHisto.GetXaxis().SetTitle( 'Mass Asymmetry (A)' )
		elif 'cosThetaStar' in name: stackHisto.GetXaxis().SetTitle( 'cos(#theta *)' )
		elif 'jetPt' in name: stackHisto.GetXaxis().SetTitle( 'Jet p_{T} [GeV]' )
		elif 'jetEta' in name: stackHisto.GetXaxis().SetTitle( 'Jet #eta' )
		elif 'HT' in name: stackHisto.GetXaxis().SetTitle( 'HT [GeV]' )
	else:
		legend.AddEntry( histos[ 'Signal' ], 'RPV Stop 100 GeV' , 'lp' )
		legend.AddEntry( histos[ 'QCD' ], 'QCD' , 'lp' )
		histos['Signal'].GetYaxis().SetTitle( 'Normalized / '+str(binWidth) )
		if 'cutflow' in name: histos['Signal'].SetMinimum(0.01)
		if 'Tau1_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{1}' )
		elif 'Tau2_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{2}' )
		elif 'Tau3_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{3}' )
		elif 'Tau21_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{21} ' )
		elif 'Tau31_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{31} ' )
		elif 'Tau32_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{32} ' )

		histos['Signal'].DrawNormalized('histe')
		histos['QCD'].DrawNormalized('histe same')

	legend.Draw()

	if 'cutHT' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'jet p_{T} > 150 GeV', 'jet |#eta| < 2.4', 'HT > 700 TeV')
	elif 'cutAsym' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '' )
	elif 'cutCosTheta' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3' )
	elif 'cutSubjetPtRatio' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3' )
	elif 'cutTau31' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', '#tau_{31} > 0.6' )
	can.SaveAs( 'Plots/'+outName )
	del can

def plot2D( inFile, trigger, name, outName, plotName, inPlotName, inPlotName2, xmax, xmax2, PU ):
	"""docstring for plot"""

	outputFileName = trigger+'_'+outName+'_'+PU+'_QCD_TriggerStudies.pdf' 
	print 'Processing.......', outputFileName
	h1 = inFile.Get( 'triggerPlotter'+trigger+'/'+name )

	h1.SetTitle( plotName )
	h1.GetXaxis().SetTitle( inPlotName )
	h1.GetYaxis().SetTitle( inPlotName2 )

	if not '' in (xmax or xmax2):
		h1.GetXaxis().SetRange( 0, xmax )
		h1.GetYaxis().SetRange( 0, xmax2 )

	can = TCanvas('c1', 'c1',  10, 10, 800, 500 )
	can.SetLogz()
	h1.Draw('colz')
	setSelectionTrigger2D( 'QCD 13 TeV '+PU, trigger )
	can.SaveAs( 'Plots/'+outputFileName )
	del can



if __name__ == '__main__':

	PU = 'PU40bx50'  #sys.argv[0]
	process = '1D' #sys.argv[1]
	
	inputFileSignal = TFile.Open('anaPlots_RPVSt100tojj_13TeV_pythia8_'+PU+'.root')
	inputFileQCD = TFile.Open('anaPlots_QCDALL_'+PU+'.root')

	if process is '2D':
		Plots_2D = [ 
			[ 'HT', 'HTvsJet1mass', 'HTvsJet1mass','HT vs Leading Jet Mass', 'HT [GeV]', 'Leading Jet Mass [GeV]', '', '' ],
			]

		for i in Plots_2D: plot2D( inputFile, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[6], PU )

	elif process is '1D':
		Plots = [
			[ 'jetPt', '', True],
			[ 'jetPt', '', False],
			[ 'jetEta', '', True],
			[ 'jetEta', '', False],
			[ 'jetMass', '', True],
			[ 'jetMass', '', False],
			[ 'HT', '', True],
			[ 'HT', '', False],
			[ 'massAsymmetry_cutHT', '', True],
			[ 'massAsymmetry_cutHT', '', False],
			[ 'massAve_cutHT', '', True],
			[ 'massAve_cutHT', '', False],
			[ 'massAve_cutAsym', '', True],
			[ 'massAve_cutAsym', '', False],
			[ 'cosThetaStar_cutAsym', '', True],
			[ 'cosThetaStar_cutAsym', '', False],
			[ 'massAve_cutCosTheta', '', True],
			[ 'massAve_cutCosTheta', '', False],
			[ 'massAve_cutSubjetPtRatio', '', True],
			[ 'massAve_cutSubjetPtRatio', '', False],
			[ 'massAve_cutTau31', '', True],
			[ 'massAve_cutTau31', '', False],
			[ 'jet1Subjet1Pt_cutHT', '', True],
			[ 'jet1Subjet1Pt_cutHT', '', False],
			[ 'jet1Subjet2Pt_cutHT', '', True],
			[ 'jet1Subjet2Pt_cutHT', '', False],
			[ 'jet2Subjet1Pt_cutHT', '', True],
			[ 'jet2Subjet1Pt_cutHT', '', False],
			[ 'jet2Subjet2Pt_cutHT', '', True],
			[ 'jet2Subjet2Pt_cutHT', '', False],
			]

		for i in Plots: 
			plot( inputFileSignal, inputFileQCD, '', i[0], i[1], i[2], PU )
			plot( inputFileSignal, inputFileQCD, 'Trimmed', i[0], i[1], i[2], PU )
			plot( inputFileSignal, inputFileQCD, 'Pruned', i[0], i[1], i[2], PU )
			plot( inputFileSignal, inputFileQCD, 'Filtered', i[0], i[1], i[2], PU )
		
		NormPlots = [
			[ 'jet1Tau1_cutHT', '', True],
			[ 'jet1Tau1_cutHT', '', False],
			[ 'jet1Tau2_cutHT', '', True],
			[ 'jet1Tau2_cutHT', '', False],
			[ 'jet1Tau3_cutHT', '', True],
			[ 'jet1Tau3_cutHT', '', False],
			[ 'jet1Tau21_cutHT', '', True],
			[ 'jet1Tau21_cutHT', '', False],
			[ 'jet1Tau31_cutHT', '', True],
			[ 'jet1Tau31_cutHT', '', False],
			[ 'jet1Tau32_cutHT', '', True],
			[ 'jet1Tau32_cutHT', '', False],
			[ 'jet1SubjetPtRatio_cutHT', '', True],
			[ 'jet1SubjetPtRatio_cutHT', '', False],
			[ 'jet2SubjetPtRatio_cutHT', '', True],
			[ 'jet2SubjetPtRatio_cutHT', '', False],
			[ 'subjetPtRatio_cutHT', '', True],
			[ 'subjetPtRatio_cutHT', '', False],
			[ 'cosThetaStar_cutAsym', '', True],
			[ 'cosThetaStar_cutAsym', '', False],
			[ 'jet1Tau21_cutAsym', '', True],
			[ 'jet1Tau21_cutAsym', '', False],
			[ 'jet1Tau31_cutAsym', '', True],
			[ 'jet1Tau31_cutAsym', '', False],
			[ 'jet1Tau32_cutAsym', '', True],
			[ 'jet1Tau32_cutAsym', '', False],
			[ 'subjetPtRatio_cutAsym', '', True],
			[ 'subjetPtRatio_cutAsym', '', False],
			[ 'jet1Tau21_cutCosTheta', '', True],
			[ 'jet1Tau21_cutCosTheta', '', False],
			[ 'jet1Tau31_cutCosTheta', '', True],
			[ 'jet1Tau31_cutCosTheta', '', False],
			[ 'jet1Tau32_cutCosTheta', '', True],
			[ 'jet1Tau32_cutCosTheta', '', False],
			[ 'subjetPtRatio_cutCosTheta', '', True],
			[ 'subjetPtRatio_cutCosTheta', '', False],
			[ 'jet1Tau21_cutSubjetPtRatio', '', True],
			[ 'jet1Tau21_cutSubjetPtRatio', '', False],
			[ 'jet1Tau31_cutSubjetPtRatio', '', True],
			[ 'jet1Tau31_cutSubjetPtRatio', '', False],
			[ 'jet1Tau32_cutSubjetPtRatio', '', True],
			[ 'jet1Tau32_cutSubjetPtRatio', '', False],
			[ 'cutflow', '', True],
			[ 'cutflow', '', False],
			]

		for i in NormPlots: 
			plot( inputFileSignal, inputFileQCD, '', i[0], i[1], i[2], PU, True )
			plot( inputFileSignal, inputFileQCD, 'Trimmed', i[0], i[1], i[2], PU, True )
			plot( inputFileSignal, inputFileQCD, 'Pruned', i[0], i[1], i[2], PU, True )
			plot( inputFileSignal, inputFileQCD, 'Filtered', i[0], i[1], i[2], PU, True )
