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

def plot( inFileSignal, inFileQCD, name, xmax, log, PU ):
	"""docstring for plot"""

	outputFileName = name+'_RPVSt100tojj_QCD_AnalysisPlots.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Signal' ] = inFileSignal.Get( 'AnalysisPlots/'+name )
	histos[ 'QCD' ] = inFileQCD.Get( 'AnalysisPlots/'+name )

	histos[ 'Signal' ].SetFillColor(30)
	histos[ 'Signal' ].SetFillStyle(1001)
	histos[ 'QCD' ].SetFillColor(9)
	histos[ 'QCD' ].SetFillStyle(1001)

#	histos.values()[0].SetMaximum( 2* max( listMax ) ) 
#	histos.values()[0].GetXaxis().SetRange( 0, xmax )

	legend=TLegend(0.65,0.70,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)
	legend.AddEntry( histos[ 'Signal' ], 'RPV Stop 100 GeV' , 'f' )
	legend.AddEntry( histos[ 'QCD' ], 'QCD' , 'f' )

	stackHisto = THStack('stackHisto', 'stack')
	stackHisto.Add( histos['QCD'] )
	stackHisto.Add( histos['Signal'] )

	can = TCanvas('c1', 'c1',  10, 10, 800, 500 )
	if log: 
		can.SetLogy()
		outName = outputFileName.replace('_AnalysisPlots','_Log_AnalysisPlots')
	else:
		outName = outputFileName 
	stackHisto.Draw('hist')
	histos['Signal'].Draw('hist same')
	legend.Draw()

	if 'massAve' in name:
		if 'Trim' in name: stackHisto.GetXaxis().SetTitle( 'Average Trimmed Mass [GeV]' )
		elif 'Prun' in name: stackHisto.GetXaxis().SetTitle( 'Average Pruned Mass [GeV]' )
		elif 'Filt' in name: stackHisto.GetXaxis().SetTitle( 'Average Filtered Mass [GeV]' )
		else: stackHisto.GetXaxis().SetTitle( 'Average Mass [GeV]' )
	if 'massAsymmetry' in name:
		if 'Trim' in name: stackHisto.GetXaxis().SetTitle( 'Trimmed Mass Asymmetry (A)' )
		elif 'Prun' in name: stackHisto.GetXaxis().SetTitle( 'Pruned Mass Asymmetry (A)' )
		elif 'Filt' in name: stackHisto.GetXaxis().SetTitle( 'Filtered Mass Asymmetry (A)' )
		else: stackHisto.GetXaxis().SetTitle( 'Mass Asymmetry (A)' )
	elif 'cosThetaStar' in name: 
		if 'Trim' in name: stackHisto.GetXaxis().SetTitle( 'cos(#theta *)' )
		elif 'Prun' in name: stackHisto.GetXaxis().SetTitle( 'cos(#theta *)' )
		elif 'Filt' in name: stackHisto.GetXaxis().SetTitle( 'cos(#theta *)' )
		else: stackHisto.GetXaxis().SetTitle( 'cos(#theta *)' )
	else:
		if 'jetPt' in name: stackHisto.GetXaxis().SetTitle( 'Jet p_{T} [GeV]' )
		elif 'jetEta' in name: stackHisto.GetXaxis().SetTitle( 'Jet #eta' )
		elif 'HT' in name: stackHisto.GetXaxis().SetTitle( 'HT [GeV]' )

	binWidth = histos['Signal'].GetBinWidth(1)
	stackHisto.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	if 'cutHT' in name: setSelection( '13 TeV - PU20bx25', 'Scaled to 10 fb^{-1}', 'jet p_{T} > 40 GeV', 'jet |#eta| < 2.4', 'HT > 1 TeV')
	elif 'cutAsym' in name: setSelection( '13 TeV - PU20bx25', 'Scaled to 10 fb^{-1}', 'HT > 1 TeV', 'A < 0.1', '' )
	elif 'cutCosTheta' in name: setSelection( '13 TeV - PU20bx25', 'Scaled to 10 fb^{-1}', 'HT > 1 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3' )
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

	PU = 'PU20bx25'  #sys.argv[0]
	process = '1D' #sys.argv[1]
	
	inputFileSignal = TFile.Open('anaPlots_RPVSt100tojj_'+PU+'.root')
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
			[ 'HT', '', True],
			[ 'HT', '', False],
			[ 'massAsymmetry_cutHT', '', True],
			[ 'massAsymmetry_cutHT', '', False],
			[ 'massAsymmetryTrim_cutHT', '', True],
			[ 'massAsymmetryTrim_cutHT', '', False],
			[ 'massAsymmetryPrun_cutHT', '', True],
			[ 'massAsymmetryPrun_cutHT', '', False],
			[ 'massAsymmetryFilt_cutHT', '', True],
			[ 'massAsymmetryFilt_cutHT', '', False],
			[ 'massAve_cutHT', '', True],
			[ 'massAve_cutHT', '', False],
			[ 'massAveTrim_cutHT', '', True],
			[ 'massAveTrim_cutHT', '', False],
			[ 'massAvePrun_cutHT', '', True],
			[ 'massAvePrun_cutHT', '', False],
			[ 'massAveFilt_cutHT', '', True],
			[ 'massAveFilt_cutHT', '', False],
			[ 'massAve_cutAsym', '', True],
			[ 'massAve_cutAsym', '', False],
			[ 'massAveTrim_cutAsym', '', True],
			[ 'massAveTrim_cutAsym', '', False],
			[ 'massAvePrun_cutAsym', '', True],
			[ 'massAvePrun_cutAsym', '', False],
			[ 'massAveFilt_cutAsym', '', True],
			[ 'massAveFilt_cutAsym', '', False],
			[ 'cosThetaStar_cutAsym', '', True],
			[ 'cosThetaStar_cutAsym', '', False],
			[ 'cosThetaStarTrim_cutAsym', '', True],
			[ 'cosThetaStarTrim_cutAsym', '', False],
			[ 'cosThetaStarPrun_cutAsym', '', True],
			[ 'cosThetaStarPrun_cutAsym', '', False],
			[ 'cosThetaStarFilt_cutAsym', '', True],
			[ 'cosThetaStarFilt_cutAsym', '', False],
			[ 'massAve_cutCosTheta', '', True],
			[ 'massAve_cutCosTheta', '', False],
			[ 'massAveTrim_cutCosTheta', '', True],
			[ 'massAveTrim_cutCosTheta', '', False],
			[ 'massAvePrun_cutCosTheta', '', True],
			[ 'massAvePrun_cutCosTheta', '', False],
			[ 'massAveFilt_cutCosTheta', '', True],
			[ 'massAveFilt_cutCosTheta', '', False],
			]

		for i in Plots: plot( inputFileSignal, inputFileQCD, i[0], i[1], i[2], PU )
