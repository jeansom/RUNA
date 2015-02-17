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

def plot( inFileSignal, jetType, cat, name, xmax, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+jetType+'_'+cat+'_PUStudies.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'CHS' ] = inFileSignal.Get( jetType+'CHS/'+name )
	histos[ 'CS' ] = inFileSignal.Get( jetType+'CS/'+name )
	histos[ 'SK' ] = inFileSignal.Get( jetType+'SK/'+name )
	histos[ 'Puppi' ] = inFileSignal.Get( jetType+'Puppi/'+name )

	histos[ 'CHS' ].SetLineWidth(2)
	histos[ 'CHS' ].SetLineColor(48)
	histos[ 'CS' ].SetLineWidth(2)
	histos[ 'CS' ].SetLineColor(38)
	histos[ 'SK' ].SetLineWidth(2)
	histos[ 'SK' ].SetLineColor(52)
	histos[ 'Puppi' ].SetLineWidth(2)
	histos[ 'Puppi' ].SetLineColor(30)

#	histos.values()[0].SetMaximum( 2* max( listMax ) ) 
#	histos.values()[0].GetXaxis().SetRange( 0, xmax )
	binWidth = histos['CHS'].GetBinWidth(1)

	legend=TLegend(0.65,0.70,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	can = TCanvas('c1', 'c1',  10, 10, 800, 500 )
	if log: 
		can.SetLogy()
		outName = outputFileName.replace('_PUStudies','_Log_PUStudies')
	else:
		outName = outputFileName 

	#if not Norm:
	legend.AddEntry( histos[ 'CHS' ], 'CHS' , 'l' )
	legend.AddEntry( histos[ 'SK' ], 'Soft Killer' , 'l' )
	legend.AddEntry( histos[ 'CS' ], 'Const. Substraction' , 'l' )
	legend.AddEntry( histos[ 'Puppi' ], 'Puppi' , 'l' )
	histos['CHS'].GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	histos['CHS'].Draw("hist ")
	histos['CS'].Draw("hist same")
	histos['SK'].Draw("hist same")
	histos['Puppi'].Draw("hist same")

	if 'jetMass' in name: histos['CHS'].GetXaxis().SetTitle( 'Jet Mass [GeV]' )
	elif 'jet1Mass' in name: histos['CHS'].GetXaxis().SetTitle( 'Leading Jet Mass [GeV]' )
	elif 'jetPt' in name: histos['CHS'].GetXaxis().SetTitle( 'Jet p_{T} [GeV]' )
	elif 'jet1Pt' in name: histos['CHS'].GetXaxis().SetTitle( 'Leading Jet p_{T} [GeV]' )
	elif 'jetEta' in name: histos['CHS'].GetXaxis().SetTitle( 'Jet #eta' )
	elif 'HT' in name: histos['CHS'].GetXaxis().SetTitle( 'HT [GeV]' )
#	else:
#		legend.AddEntry( histos[ 'Signal' ], 'RPV Stop 100 GeV' , 'lp' )
#		legend.AddEntry( histos[ 'QCD' ], 'QCD' , 'lp' )
#		histos['Signal'].GetYaxis().SetTitle( 'Normalized / '+str(binWidth) )
#		if 'Tau1_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{1}' )
#		elif 'Tau2_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{2}' )
#		elif 'Tau3_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{3}' )
#		elif 'Tau21_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{21} ' )
#		elif 'Tau31_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{31} ' )
#		elif 'Tau32_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{32} ' )


	legend.Draw()

	setSelection( jetType+' Jets', cat.replace("_"," "), 'RPV Stop 100 GeV', '13 TeV - PU40bx50', 'jet p_{T} > 100 GeV', 'jet |#eta| < 2.5' )
#	if 'cutHT' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'jet p_{T} > 150 GeV', 'jet |#eta| < 2.4', 'HT > 700 TeV')
#	elif 'cutAsym' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '' )
#	elif 'cutCosTheta' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3' )
#	elif 'cutSubjetPtRatio' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3' )
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
	cat = 'MiniAOD_NOJEC'
	
	inputFileSignal = TFile.Open('PUStudies_'+cat+'.root')
	#inputFileSignal = TFile.Open('anaPlots_RPVSt100tojj_13TeV_pythia8_'+PU+'.root')
	#inputFileQCD = TFile.Open('anaPlots_QCDALL_'+PU+'.root')

	#if process is '2D':
	#	Plots_2D = [ 
	#		[ 'HT', 'HTvsJet1mass', 'HTvsJet1mass','HT vs Leading Jet Mass', 'HT [GeV]', 'Leading Jet Mass [GeV]', '', '' ],
	#		]

	#	for i in Plots_2D: plot2D( inputFile, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[6], PU )

	#elif process is '1D':
	Plots = [
		[ 'jetsPt', '', True],
		[ 'jetsPt', '', False],
		[ 'jetsEta', '', True],
		[ 'jetsEta', '', False],
		[ 'jetsMass', '', True],
		[ 'jetsMass', '', False],
		[ 'jetsPrunedMass', '', True],
		[ 'jetsPrunedMass', '', False],
		[ 'jetsFilteredMass', '', True],
		[ 'jetsFilteredMass', '', False],
		[ 'jetsMassDropFilteredMass', '', True],
		[ 'jetsMassDropFilteredMass', '', False],
		[ 'jetsTrimmedMass', '', True],
		[ 'jetsTrimmedMass', '', False],
		[ 'jetsSoftDropMass', '', True],
		[ 'jetsSoftDropMass', '', False],
		[ 'jetsHEPTopTagMass', '', True],
		[ 'jetsHEPTopTagMass', '', False],
		[ 'jetsTau1', '', True],
		[ 'jetsTau1', '', False],
		[ 'jetsTau2', '', True],
		[ 'jetsTau2', '', False],
		[ 'jetsTau3', '', True],
		[ 'jetsTau3', '', False],
		[ 'HT', '', True],
		[ 'HT', '', False],
		[ 'jet1Pt', '', True],
		[ 'jet1Pt', '', False],
		[ 'jet1Mass', '', True],
		[ 'jet1Mass', '', False],
		[ 'jet1PrunedMass', '', True],
		[ 'jet1PrunedMass', '', False],
		[ 'jet1FilteredMass', '', True],
		[ 'jet1FilteredMass', '', False],
		[ 'jet1MassDropFilteredMass', '', True],
		[ 'jet1MassDropFilteredMass', '', False],
		[ 'jet1TrimmedMass', '', True],
		[ 'jet1TrimmedMass', '', False],
		[ 'jet1SoftDropMass', '', True],
		[ 'jet1SoftDropMass', '', False],
		[ 'jet1HEPTopTagMass', '', True],
		[ 'jet1HEPTopTagMass', '', False],
		[ 'jet1Tau1', '', True],
		[ 'jet1Tau1', '', False],
		[ 'jet1Tau2', '', True],
		[ 'jet1Tau2', '', False],
		[ 'jet1Tau3', '', True],
		[ 'jet1Tau3', '', False],
		]

	for i in Plots: plot( inputFileSignal, 'AK8', cat, i[0], i[1], i[2], PU )
		
