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
from array import array


gROOT.Reset()
gROOT.SetBatch()
setTDRStyle()
gROOT.ForceStyle()
gROOT.SetStyle('tdrStyle')


gStyle.SetOptStat(0)


xline = array('d', [0,2000])
yline = array('d', [1,1])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)


def plotCompPU( inFileSignal, jetType, cat, name, xmax, log, PU, Norm=False ):
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
	elif 'Tau1' in name: histos['CHS'].GetXaxis().SetTitle( '#tau_{1}' )
	elif 'Tau2' in name: histos['CHS'].GetXaxis().SetTitle( '#tau_{2}' )
	elif 'Tau3' in name: histos['CHS'].GetXaxis().SetTitle( '#tau_{3}' )
#	else:
#		legend.AddEntry( histos[ 'Signal' ], 'RPV Stop 100 GeV' , 'lp' )
#		legend.AddEntry( histos[ 'QCD' ], 'QCD' , 'lp' )
#		histos['Signal'].GetYaxis().SetTitle( 'Normalized / '+str(binWidth) )
#		elif 'Tau21_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{21} ' )
#		elif 'Tau31_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{31} ' )
#		elif 'Tau32_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{32} ' )


	legend.Draw()

	setSelection( jetType+' Jets', cat.replace("_"," "), '13 TeV - PU40bx50', 'jet p_{T} > 100 GeV', 'jet |#eta| < 2.5' )
	#setSelection( jetType+' Jets', cat.replace("_"," "), 'RPV Stop 100 GeV', '13 TeV - PU40bx50', 'jet p_{T} > 100 GeV', 'jet |#eta| < 2.5' )
#	if 'cutHT' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'jet p_{T} > 150 GeV', 'jet |#eta| < 2.4', 'HT > 700 TeV')
#	elif 'cutAsym' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '' )
#	elif 'cutCosTheta' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3' )
#	elif 'cutSubjetPtRatio' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3' )
	can.SaveAs( 'Plots/'+outName )
	del can

def plotCompGrom( inFileSignal, jetType, name, xmax, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'Mass_'+jetType+'_'+cat+'_GromStudies.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Mass' ] = inFileSignal.Get( jetType+'/'+name+'Mass' )
	histos[ 'Pruned' ] = inFileSignal.Get( jetType+'/'+name+'PrunedMass' )
	histos[ 'SoftDrop' ] = inFileSignal.Get( jetType+'/'+name+'SoftDropMass' )
	histos[ 'Trimmed' ] = inFileSignal.Get( jetType+'/'+name+'TrimmedMass' )
	histos[ 'Filtered' ] = inFileSignal.Get( jetType+'/'+name+'FilteredMass' )

	histos[ 'Mass' ].SetLineWidth(2)
	histos[ 'Mass' ].SetLineColor(48)
	histos[ 'Pruned' ].SetLineWidth(2)
	histos[ 'Pruned' ].SetLineColor(38)
	histos[ 'SoftDrop' ].SetLineWidth(2)
	histos[ 'SoftDrop' ].SetLineColor(52)
	histos[ 'Trimmed' ].SetLineWidth(2)
	histos[ 'Trimmed' ].SetLineColor(30)
	histos[ 'Filtered' ].SetLineWidth(2)
	histos[ 'Filtered' ].SetLineColor(95)

	listMax = [ histos[ 'Mass'].GetMaximum(), histos[ 'Pruned' ].GetMaximum(), histos[ 'SoftDrop' ].GetMaximum(), histos[ 'Trimmed' ].GetMaximum(), histos[ 'Filtered' ].GetMaximum() ]
	histos[ 'Mass' ].SetMaximum( 1.2* max( listMax ) ) 
#	histos.values()[0].GetXaxis().SetRange( 0, xmax )
	binWidth = histos['Mass'].GetBinWidth(1)

	legend=TLegend(0.65,0.70,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	can = TCanvas('c1', 'c1',  10, 10, 800, 500 )
	if log: 
		can.SetLogy()
		outName = outputFileName.replace('_GromStudies','_Log_GromStudies')
	else:
		outName = outputFileName 

	#if not Norm:
	legend.AddEntry( histos[ 'Mass' ], 'No Grommer' , 'l' )
	legend.AddEntry( histos[ 'Pruned' ], 'Pruning' , 'l' )
	legend.AddEntry( histos[ 'SoftDrop' ], 'SoftDrop' , 'l' )
	legend.AddEntry( histos[ 'Trimmed' ], 'Trimming' , 'l' )
	legend.AddEntry( histos[ 'Filtered' ], 'Filtered' , 'l' )
	histos['Mass'].GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	histos['Mass'].Draw("hist ")
	histos['Pruned'].Draw("hist same")
	histos['SoftDrop'].Draw("hist same")
	histos['Trimmed'].Draw("hist same")
	histos['Filtered'].Draw("hist same")

	if 'jetMass' in name: histos['Mass'].GetXaxis().SetTitle( 'Jet Mass [GeV]' )
	elif 'jet1' in name: histos['Mass'].GetXaxis().SetTitle( 'Leading Jet Mass [GeV]' )
	elif 'jetPt' in name: histos['Mass'].GetXaxis().SetTitle( 'Jet p_{T} [GeV]' )
	elif 'jet1Pt' in name: histos['Mass'].GetXaxis().SetTitle( 'Leading Jet p_{T} [GeV]' )
	elif 'jetEta' in name: histos['Mass'].GetXaxis().SetTitle( 'Jet #eta' )
	elif 'HT' in name: histos['Mass'].GetXaxis().SetTitle( 'HT [GeV]' )
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

	setSelection( jetType+' Jets', 'RPV Stop 100 GeV', '13 TeV - PU40bx50', 'jet p_{T} > 100 GeV', 'jet |#eta| < 2.5' )
	#setSelection( jetType+' Jets', 'QCD', '13 TeV - PU40bx50', 'jet p_{T} > 100 GeV', 'jet |#eta| < 2.5' )
#	if 'cutHT' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'jet p_{T} > 150 GeV', 'jet |#eta| < 2.4', 'HT > 700 TeV')
#	elif 'cutAsym' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '' )
#	elif 'cutCosTheta' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3' )
#	elif 'cutSubjetPtRatio' in name: setSelection( '13 TeV - PU40bx50', 'Scaled to 1 fb^{-1}', 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3' )
	can.SaveAs( 'Plots/'+outName )
	del can

def plotCompJTBAODMiniAOD( cat1, cat2, jetType, name, xmax, log, PU, Norm=False ):
	"""docstring for plot"""

	inputFile1 = TFile.Open('PUStudies_'+cat1+'.root')
	inputFile2 = TFile.Open('PUStudies_'+cat2+'.root')
	outputFileName = name+'_'+jetType+'_'+cat1+'_'+cat2+'_JTBStudies.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ cat1 ] = inputFile1.Get( jetType+'/'+name )
	histos[ cat2 ] = inputFile2.Get( jetType+'/'+name )

	histos[ cat1 ].SetLineWidth(2)
	histos[ cat1 ].SetLineColor(48)
	histos[ cat2 ].SetLineWidth(2)
	histos[ cat2 ].SetLineColor(38)

	listMax = [ histos[ cat1 ].GetMaximum(), histos[ cat2 ].GetMaximum() ]
	histos[ cat1 ].SetMaximum( 1.2* max( listMax ) ) 
	#histos.values()[0].GetXaxis().SetRange( 0, xmax )
	binWidth = histos[cat1].GetBinWidth(1)

	legend=TLegend(0.65,0.70,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	#if not Norm:
	legend.AddEntry( histos[ cat1 ], cat1.replace("_"," ") , 'l' )
	legend.AddEntry( histos[ cat2 ], cat2.replace("_"," ") , 'l' )
	if 'jets' in name: histos[ cat1 ].GetYaxis().SetTitle( 'Jets / '+str(binWidth) )
	else: histos[ cat1 ].GetYaxis().SetTitle( 'Events / '+str(binWidth) )
	histos[ cat1 ].GetYaxis().SetTitleOffset(1.2)

	hRatio = histos[ cat1 ].Clone()
	for bin in range(0, hRatio.GetNbinsX()):
		hRatio.SetBinContent(bin, 0.)
		hRatio.SetBinError(bin, 0.)

	for ibin in range(0, hRatio.GetNbinsX()):

		binCat1Cont = histos[ cat1 ].GetBinContent(ibin)
		binCat1Err = histos[ cat1 ].GetBinError(ibin)
		binCat2Cont = histos[ cat2 ].GetBinContent(ibin)
		binCat2Err = histos[ cat2 ].GetBinError(ibin)

		if binCat2Cont > 0 : 
			diff = binCat1Cont/ binCat2Cont 
			#errDiff = diff * TMath.Sqrt( TMath.Power( P4Fit.GetParError(0) / P4Fit.GetParameter(0),2 ) + TMath.Power( P4Fit.GetParError(1)/ P4Fit.GetParameter(1), 2 )  + TMath.Power( P4Fit.GetParError(2)/ P4Fit.GetParameter(2), 2 )  + TMath.Power( P4Fit.GetParError(3)/ P4Fit.GetParameter(3), 2 ) )
			#if (( ibin >= FitStart/binSize) and (binCont != 0) and (ibin <= FitEnd/binSize)):

			hRatio.SetBinContent(ibin, diff)
			#hRatio.SetBinError(ibin, binErr/valIntegral )
			#hRatio.SetBinError(ibin, errDiff )#/valIntegral)

	#can = TCanvas('c1', 'c1',  10, 10, 800, 500 )
	can = TCanvas('c1', 'c1',  10, 10, 800, 750 )
	pad1 = TPad("pad1", "Histo",0,0.25,1.00,1.00,-1)
	pad2 = TPad("pad2", "Residual",0,0,1.00,0.27,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: 
		pad1.SetLogy()
		outName = outputFileName.replace('_JTBStudies','_Log_JTBStudies')
	else:
		outName = outputFileName 

	histos[ cat1 ].Draw("hist ")
	histos[ cat2 ].Draw("hist same")

	if 'Mass' in name: 
		if 'Trimmed' in name: histos[ cat1 ].GetXaxis().SetTitle( 'Trimmed Jet Mass [GeV]' )
		elif 'Filtered' in name: histos[ cat1 ].GetXaxis().SetTitle( 'Filtered Jet Mass [GeV]' )
		elif 'Pruned' in name: histos[ cat1 ].GetXaxis().SetTitle( 'Pruned Jet Mass [GeV]' )
		else: histos[ cat1 ].GetXaxis().SetTitle( 'Jet Mass [GeV]' )
	elif '1Mass' in name: 
		if 'Trimmed' in name: histos[ cat1 ].GetXaxis().SetTitle( 'Leading Trimmed Jet Mass [GeV]' )
		elif 'Filtered' in name: histos[ cat1 ].GetXaxis().SetTitle( 'Leading Filtered Jet Mass [GeV]' )
		elif 'Pruned' in name: histos[ cat1 ].GetXaxis().SetTitle( 'Leading Pruned Jet Mass [GeV]' )
		else: histos[ cat1 ].GetXaxis().SetTitle( 'Leading Jet Mass [GeV]' )
	elif 'Pt' in name: histos[ cat1 ].GetXaxis().SetTitle( 'Jet p_{T} [GeV]' )
	elif '1Pt' in name: histos[ cat1 ].GetXaxis().SetTitle( 'Leading Jet p_{T} [GeV]' )
	elif 'Eta' in name: histos[ cat1 ].GetXaxis().SetTitle( 'Jet #eta' )
	elif 'HT' in name: histos[ cat1 ].GetXaxis().SetTitle( 'HT [GeV]' )
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

	setSelection( jetType+' Jets', 'RPV Stop 100 GeV', '13 TeV - PU40bx50', 'jet p_{T} > 100 GeV', 'jet |#eta| < 2.5' )

	pad2.cd()
	hRatio.GetYaxis().SetLabelSize(0.12)
	hRatio.GetXaxis().SetLabelSize(0.12)
	hRatio.GetYaxis().SetTitleSize(0.12)
	hRatio.GetYaxis().SetTitleOffset(0.45)
	#hRatio.GetXaxis().SetTitleOffset(0.6)
	#hRatio.GetYaxis().SetLimits(-5,5)
	hRatio.SetMaximum(1.5)
	hRatio.SetMinimum(0.5)
	#hRatio.GetXaxis().SetTitle( histoInfo[1] )
	hRatio.GetYaxis().SetTitle( 'Ratio' )
	hRatio.Draw()
	line.Draw("same")

	can.SaveAs( 'Plots/'+outName )
	del can

def plotCompJTB( sample, jetType, name, xmax, log, PU, Norm=False ):
	"""docstring for plot"""

	inputFile1 = TFile.Open('comparisonJTB_'+sample+'_B2G.root')
	inputFile2 = TFile.Open('comparisonJTB_'+sample+'_RUNA.root')
	outputFileName = name+'_'+jetType+'_'+sample+'_JTBStudies.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'B2G' ] = inputFile1.Get( jetType+'/'+name )
	histos[ 'RUNA' ] = inputFile2.Get( jetType+'/'+name )

	histos[ 'B2G' ].SetLineWidth(2)
	histos[ 'B2G' ].SetLineColor(48)
	histos[ 'RUNA' ].SetLineWidth(2)
	histos[ 'RUNA' ].SetLineColor(38)

	listMax = [ histos[ 'B2G' ].GetMaximum(), histos[ 'RUNA' ].GetMaximum() ]
	histos[ 'B2G' ].SetMaximum( 1.2* max( listMax ) ) 
	#histos.values()[0].GetXaxis().SetRange( 0, xmax )
	binWidth = histos['B2G'].GetBinWidth(1)

	legend=TLegend(0.65,0.70,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	#if not Norm:
	legend.AddEntry( histos[ 'B2G' ], 'w/o jetToolbox', 'l' )
	legend.AddEntry( histos[ 'RUNA' ], 'with jetToolbox' , 'l' )
	if 'jet' in name: histos[ 'B2G' ].GetYaxis().SetTitle( 'Events / '+str(binWidth) )
	else: histos[ 'B2G' ].GetYaxis().SetTitle( 'Jets / '+str(binWidth) )
	histos[ 'B2G' ].GetYaxis().SetTitleOffset(1.2)

	hRatio = histos[ 'B2G' ].Clone()
	for bin in range(0, hRatio.GetNbinsX()):
		hRatio.SetBinContent(bin, 0.)
		hRatio.SetBinError(bin, 0.)

	for ibin in range(0, hRatio.GetNbinsX()):

		binCat1Cont = histos[ 'B2G' ].GetBinContent(ibin)
		binCat1Err = histos[ 'B2G' ].GetBinError(ibin)
		binCat2Cont = histos[ 'RUNA' ].GetBinContent(ibin)
		binCat2Err = histos[ 'RUNA' ].GetBinError(ibin)

		if binCat2Cont > 0 : 
			diff = binCat1Cont/ binCat2Cont 
			#errDiff = diff * TMath.Sqrt( TMath.Power( P4Fit.GetParError(0) / P4Fit.GetParameter(0),2 ) + TMath.Power( P4Fit.GetParError(1)/ P4Fit.GetParameter(1), 2 )  + TMath.Power( P4Fit.GetParError(2)/ P4Fit.GetParameter(2), 2 )  + TMath.Power( P4Fit.GetParError(3)/ P4Fit.GetParameter(3), 2 ) )
			#if (( ibin >= FitStart/binSize) and (binCont != 0) and (ibin <= FitEnd/binSize)):

			hRatio.SetBinContent(ibin, diff)
			#hRatio.SetBinError(ibin, binErr/valIntegral )
			#hRatio.SetBinError(ibin, errDiff )#/valIntegral)

	#can = TCanvas('c1', 'c1',  10, 10, 800, 500 )
	can = TCanvas('c1', 'c1',  10, 10, 800, 750 )
	pad1 = TPad("pad1", "Histo",0,0.25,1.00,1.00,-1)
	pad2 = TPad("pad2", "Residual",0,0,1.00,0.27,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: 
		pad1.SetLogy()
		outName = outputFileName.replace('_JTBStudies','_Log_JTBStudies')
	else:
		outName = outputFileName 

	histos[ 'B2G' ].Draw("hist ")
	histos[ 'RUNA' ].Draw("hist same")

	if 'Mass' in name: 
		if 'Trimmed' in name: histos[ 'B2G' ].GetXaxis().SetTitle( 'Trimmed Jet Mass [GeV]' )
		elif 'Filtered' in name: histos[ 'B2G' ].GetXaxis().SetTitle( 'Filtered Jet Mass [GeV]' )
		elif 'Pruned' in name: histos[ 'B2G' ].GetXaxis().SetTitle( 'Pruned Jet Mass [GeV]' )
		else: histos[ 'B2G' ].GetXaxis().SetTitle( 'Jet Mass [GeV]' )
	elif ('jet1' in name) and ('Mass' in name): 
		if 'Trimmed' in name: histos[ 'B2G' ].GetXaxis().SetTitle( 'Leading Trimmed Jet Mass [GeV]' )
		elif 'Filtered' in name: histos[ 'B2G' ].GetXaxis().SetTitle( 'Leading Filtered Jet Mass [GeV]' )
		elif 'Pruned' in name: histos[ 'B2G' ].GetXaxis().SetTitle( 'Leading Pruned Jet Mass [GeV]' )
		else: histos[ 'B2G' ].GetXaxis().SetTitle( 'Leading Jet Mass [GeV]' )
	elif 'Pt' in name: histos[ 'B2G' ].GetXaxis().SetTitle( 'Jet p_{T} [GeV]' )
	elif '1Pt' in name: histos[ 'B2G' ].GetXaxis().SetTitle( 'Leading Jet p_{T} [GeV]' )
	elif 'Eta' in name: histos[ 'B2G' ].GetXaxis().SetTitle( 'Jet #eta' )
	elif 'HT' in name: histos[ 'B2G' ].GetXaxis().SetTitle( 'HT [GeV]' )
	elif 'Tau1' in name: histos['B2G'].GetXaxis().SetTitle( '#tau_{1}' )
	elif 'Tau2' in name: histos['B2G'].GetXaxis().SetTitle( '#tau_{2}' )
	elif 'Tau3' in name: histos['B2G'].GetXaxis().SetTitle( '#tau_{3}' )
#		elif 'Tau21_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{21} ' )
#		elif 'Tau31_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{31} ' )
#		elif 'Tau32_' in name: histos['Signal'].GetXaxis().SetTitle( '#tau_{32} ' )


	legend.Draw()

	setSelection( jetType, sample, '13 TeV - PU20bx25', 'jet p_{T} > 100 GeV', 'jet |#eta| < 2.5' )

	pad2.cd()
	hRatio.GetYaxis().SetLabelSize(0.12)
	hRatio.GetXaxis().SetLabelSize(0.12)
	hRatio.GetYaxis().SetTitleSize(0.12)
	hRatio.GetYaxis().SetTitleOffset(0.45)
	#hRatio.GetXaxis().SetTitleOffset(0.6)
	#hRatio.GetYaxis().SetLimits(-5,5)
	hRatio.SetMaximum(1.1)
	hRatio.SetMinimum(0.9)
	#hRatio.GetXaxis().SetTitle( histoInfo[1] )
	hRatio.GetYaxis().SetTitle( 'Ratio' )
	hRatio.Draw()
	line.Draw("same")

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
	cat = 'TTJets_MiniAOD_JEC'
	
	inputFileSignal = TFile.Open('PUStudies_'+cat+'.root')

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


	#plotCompGrom( inputFileSignal, 'AK8CHS', 'jet1', '', True, PU )
	#plotCompGrom( inputFileSignal, 'AK8SK', 'jet1', '', False, PU )
	for i in Plots: 
		plotCompPU( inputFileSignal, 'AK8', cat, i[0], i[1], i[2], PU )
		#plotCompJTBAODMiniAOD( 'AOD_JEC', 'MiniAOD_JEC', 'AK8CHS', i[0], i[1], i[2], PU )
		#plotCompJTBAODMiniAOD( 'AOD_JEC', 'MiniAOD_JEC', 'AK8CS', i[0], i[1], i[2], PU )
		#plotCompJTBAODMiniAOD( 'AOD_JEC', 'MiniAOD_JEC', 'AK8SK', i[0], i[1], i[2], PU )
		#plotCompJTBAODMiniAOD( 'AOD_JEC', 'MiniAOD_JEC', 'AK8Puppi', i[0], i[1], i[2], PU )
	'''

	Plots = [
		[ 'jetMass', '', True],
		[ 'jetMass', '', False],
		[ 'jetPrunedMass', '', True],
		[ 'jetPrunedMass', '', False],
		[ 'jetTrimmedMass', '', True],
		[ 'jetTrimmedMass', '', False],
		[ 'jetTau1', '', True],
		[ 'jetTau1', '', False],
		[ 'jetTau2', '', True],
		[ 'jetTau2', '', False],
		[ 'jet1Mass', '', True],
		[ 'jet1Mass', '', False],
		[ 'jet1PrunedMass', '', True],
		[ 'jet1PrunedMass', '', False],
		[ 'jet1TrimmedMass', '', True],
		[ 'jet1TrimmedMass', '', False],
		[ 'jet1Tau1', '', True],
		[ 'jet1Tau1', '', False],
		[ 'jet1Tau2', '', True],
		[ 'jet1Tau2', '', False],
		]


	for i in Plots: 
		plotCompJTB( 'TTjets', 'ak8jets', i[0], i[1], i[2], PU )
	'''
