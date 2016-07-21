#!/usr/bin/env python
'''
File: DrawHistogram.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Draw histograms. Check for options at the end.
'''

#from ROOT import TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from ROOT import *
import time, os, math, sys
from array import array
import argparse
from collections import OrderedDict
try:
	from RUNA.RUNAnalysis.histoLabels import labels, labelAxis, finalLabels, setSelection
	from RUNA.RUNAnalysis.scaleFactors import * #scaleFactor as SF
	from RUNA.RUNAnalysis.commonFunctions import * 
	from RUNA.RUNAnalysis.cuts import selection 
	import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
except ImportError:
	sys.path.append('../python')
	from histoLabels import labels, labelAxis, finalLabels
	from scaleFactors import * #scaleFactor as SF
	from commonFunctions import * 
	from cuts import selection 
	import CMS_lumi as CMS_lumi 
	import tdrstyle as tdrstyle

gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)

xline = array('d', [0,2000])
yline = array('d', [1, 1])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)

yline0 = array('d', [0,0])
line0 = TGraph(2, xline, yline0)
line0.SetLineColor(kRed)


def getDictWithHistos( samFiles, nameInRoot, rebinX ):
	"""docstring for getDictWithHistos"""

	histosDict = {}
	for sample in samFiles:
		histosDict[ sample ] = samFiles[ sample ][0].Get( ( nameInRoot+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass) if 'Signal' in sample else nameInRoot+'_'+sample ) )
		if rebinX > 1: histosDict[ sample ].Rebin( rebinX )
		#histosDict[ sample ] = histosDict[ sample ].Rebin( len( boostedMassAveBins )-1, histosDict[ sample ].GetName(), boostedMassAveBinSize )
		if samFiles[ sample ][1] != 1: 
			scale = samFiles[ sample ][1] 
			histosDict[ sample ].Scale( scale ) 

	allHistos = histosDict[ histosDict.keys()[0] ].Clone()
	allHistos.Reset()
	for xsample in histosDict:
		allHistos.Add( histosDict[ xsample ] )

	return allHistos
	

def tauSystematics( dataFile, bkgFiles, signalFiles, nameInRoot, log, Norm=False ):
	"""docstring for plotBkgEstimation"""
	
	##### presel histos
	bkgHistos = getDictWithHistos( bkgFiles, nameInRoot+'_n-1', 1 )
	#sigHistos = getDictWithHistos( signalFiles, nameInRoot, 1 )
	dataHistos = dataFile.Get( nameInRoot+'_n-1_DATA' )

	##### n-1 histos
	bkgNm1Histos = getDictWithHistos( bkgFiles, nameInRoot+'_n-1', 1 )
	#sigHistos = getDictWithHistos( signalFiles, nameInRoot, 1 )
	dataNm1Histos = dataFile.Get( nameInRoot+'_n-1_DATA' )
	
	listRatios = []
	listRatiosErr = []
	ratioHisto = dataHistos.Clone()
	ratioHisto.Reset()
	bkgPreselCorrHisto = dataHistos.Clone()
	bkgPreselCorrHisto.Reset()
	bkgNm1CorrHisto = dataHistos.Clone()
	bkgNm1CorrHisto.Reset()
	for ibin in range( dataHistos.GetNbinsX()+1 ):
		dataBin = dataHistos.GetBinContent( ibin )
		dataBinErr = dataHistos.GetBinError( ibin )
		bkgBin = bkgHistos.GetBinContent( ibin )
		bkgBinErr = bkgHistos.GetBinError( ibin )

		try: 
			ratio = dataBin/bkgBin
			ratioErr = ratio * TMath.Sqrt( TMath.Power( dataBinErr/dataBin, 2) + TMath.Power( bkgBinErr/bkgBin, 2 )  )
		except ZeroDivisionError: 
			ratio = 0
			ratioErr = 0
		
		#### Simple ratio
		ratioHisto.SetBinContent( ibin, ratio )
		ratioHisto.SetBinError( ibin, ratioErr )
		listRatios.append( ratio )
		listRatiosErr.append( ratioErr )

		##### Correcting presel bkg
		bkgBinPreselCorr = bkgBin * ratio
		try: bkgBinErrPreselCorr = bkgBinPreselCorr * TMath.Sqrt( TMath.Power( ratioErr/ratio, 2) + TMath.Power( bkgBinErr/bkgBin, 2 )  )
		except ZeroDivisionError: bkgBinErrPreselCorr = 0
		bkgPreselCorrHisto.SetBinContent( ibin, bkgBinPreselCorr )
		bkgPreselCorrHisto.SetBinError( ibin, bkgBinErrPreselCorr )
	
		##### Correcting n-1 bkg
		bkgNm1Bin = bkgNm1Histos.GetBinContent( ibin )
		bkgNm1BinErr = bkgNm1Histos.GetBinError( ibin )
		bkgBinNm1Corr = bkgNm1Bin * ratio
		try: bkgBinErrNm1Corr = bkgBinNm1Corr * TMath.Sqrt( TMath.Power( ratioErr/ratio, 2) + TMath.Power( bkgNm1BinErr/bkgNm1Bin, 2 )  )
		except ZeroDivisionError: bkgBinErrNm1Corr = 0
		bkgNm1CorrHisto.SetBinContent( ibin, bkgBinNm1Corr )
		bkgNm1CorrHisto.SetBinError( ibin, bkgBinErrNm1Corr )
	
	print listRatios, listRatiosErr

	############# Plot preselection nominal
	binWidth = dataHistos.GetBinWidth(1)
	legend=TLegend(0.20,0.75,0.50,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)
	legend.AddEntry( dataHistos, 'DATA' , 'ep' )
	legend.AddEntry( bkgHistos, 'All MC Bkgs', 'lp' )

	bkgHistos.SetLineColor(kRed-4)
	bkgHistos.SetLineWidth(2)
	dataHistos.SetMarkerStyle(8)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	#dataHistos.GetYaxis().SetTitle( 'Normalized / '+str(binWidth) )
	if log: pad1.SetLogy() 	
	dataHistos.Draw("E")
	bkgHistos.Draw('hist same')
	dataHistos.SetMaximum( 1.2* max( dataHistos.GetMaximum(), bkgHistos.GetMaximum() )  )
	#dataHistos.GetYaxis().SetTitleOffset(1.2)
	dataHistos.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	CMS_lumi.cmsTextOffset = 0.1
	CMS_lumi.relPosX = 0.15
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	labelAxis( nameInRoot, dataHistos, 'pruned' )
	legend.Draw()
	setSelection( [ 'Preselection' ], 0.40, 0.65  )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	labelAxis( nameInRoot, ratioHisto, args.grooming )
	ratioHisto.SetMarkerStyle(8)
	ratioHisto.GetXaxis().SetTitleOffset(1.1)
	ratioHisto.GetXaxis().SetLabelSize(0.12)
	ratioHisto.GetXaxis().SetTitleSize(0.12)
	ratioHisto.GetYaxis().SetTitle("Data/Bkg")
	ratioHisto.GetYaxis().SetLabelSize(0.12)
	ratioHisto.GetYaxis().SetTitleSize(0.12)
	ratioHisto.GetYaxis().SetTitleOffset(0.55)
	#if( ratioHisto.GetMaximum() > 2 ): ratioHisto.SetMaximum( 2.0 )
	ratioHisto.SetMaximum( 1.5 )
	ratioHisto.SetMinimum( 0.5 )
	ratioHisto.GetYaxis().SetNdivisions(505)
	ratioHisto.GetYaxis().CenterTitle()
	ratioHisto.Draw('E')
	outputFileName = nameInRoot+'_preselection_TauSystematics.'+args.extension
	can.SaveAs( 'Plots/'+ outputFileName )
	del can

	############# Plot preselection corrected 
	legend1=TLegend(0.20,0.75,0.50,0.87)
	legend1.SetFillStyle(0)
	legend1.SetTextSize(0.04)
	legend1.AddEntry( dataHistos, 'DATA' , 'ep' )
	legend1.AddEntry( bkgPreselCorrHisto, 'All MC Bkgs Corrected', 'lp' )

	bkgPreselCorrHisto.SetLineColor(kRed-4)
	bkgPreselCorrHisto.SetLineWidth(2)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: pad1.SetLogy() 	
	dataHistos.Draw("E")
	bkgPreselCorrHisto.Draw('hist same')
	#dataHistos.SetMaximum( 1.1* max( dataHistos.GetMaximum(), bkgPreselCorrHisto.GetMaximum() )  )
	#dataHistos.GetYaxis().SetTitleOffset(1.2)
	dataHistos.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	CMS_lumi.cmsTextOffset = 0.1
	CMS_lumi.relPosX = 0.15
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	labelAxis( nameInRoot, dataHistos, 'pruned' )
	legend1.Draw()
	setSelection( [ 'Preselection' ], 0.40, 0.65  )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	ratioPreselCorrHisto = dataHistos.Clone()
	ratioPreselCorrHisto.Reset()
	ratioPreselCorrHisto.Divide( dataHistos, bkgPreselCorrHisto, 1, 1, '' )
	labelAxis( nameInRoot, ratioPreselCorrHisto, args.grooming )
	ratioPreselCorrHisto.SetMarkerStyle(8)
	ratioPreselCorrHisto.GetXaxis().SetTitleOffset(1.1)
	ratioPreselCorrHisto.GetXaxis().SetLabelSize(0.12)
	ratioPreselCorrHisto.GetXaxis().SetTitleSize(0.12)
	ratioPreselCorrHisto.GetYaxis().SetTitle("Data/Bkg")
	ratioPreselCorrHisto.GetYaxis().SetLabelSize(0.12)
	ratioPreselCorrHisto.GetYaxis().SetTitleSize(0.12)
	ratioPreselCorrHisto.GetYaxis().SetTitleOffset(0.55)
	#if( ratioPreselCorrHisto.GetMaximum() > 2 ): ratioPreselCorrHisto.SetMaximum( 2.0 )
	ratioPreselCorrHisto.SetMaximum( 1.5 )
	ratioPreselCorrHisto.SetMinimum( 0.5 )
	ratioPreselCorrHisto.GetYaxis().SetNdivisions(505)
	ratioPreselCorrHisto.GetYaxis().CenterTitle()
	ratioPreselCorrHisto.Draw('E')
	outputFileName = nameInRoot+'_preselectionCorrected_TauSystematics.'+args.extension
	can.SaveAs( 'Plots/'+ outputFileName )
	del can

	############# Plot preselection corrected 
	legend2=TLegend(0.20,0.75,0.50,0.87)
	legend2.SetFillStyle(0)
	legend2.SetTextSize(0.04)
	legend2.AddEntry( dataNm1Histos, 'DATA' , 'ep' )
	legend2.AddEntry( bkgNm1CorrHisto, 'All MC Bkgs Corrected', 'lp' )

	bkgNm1CorrHisto.SetLineColor(kRed-4)
	bkgNm1CorrHisto.SetLineWidth(2)
	dataNm1Histos.SetMarkerStyle(8)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: pad1.SetLogy() 	
	dataNm1Histos.Draw("E")
	bkgNm1CorrHisto.Draw('hist same')
	#dataNm1Histos.SetMaximum( 1.1* max( dataNm1Histos.GetMaximum(), bkgNm1CorrHisto.GetMaximum() )  )
	#dataNm1Histos.GetYaxis().SetTitleOffset(1.2)
	dataNm1Histos.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	CMS_lumi.cmsTextOffset = 0.1
	CMS_lumi.relPosX = 0.15
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	labelAxis( nameInRoot, dataNm1Histos, 'pruned' )
	legend2.Draw()
	setSelection( [ 'N-1 selection' ], 0.40, 0.65  )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	ratioNm1CorrHisto = dataNm1Histos.Clone()
	ratioNm1CorrHisto.Reset()
	ratioNm1CorrHisto.Divide( dataNm1Histos, bkgNm1CorrHisto, 1, 1, '' )
	labelAxis( nameInRoot, ratioNm1CorrHisto, args.grooming )
	ratioNm1CorrHisto.SetMarkerStyle(8)
	ratioNm1CorrHisto.GetXaxis().SetTitleOffset(1.1)
	ratioNm1CorrHisto.GetXaxis().SetLabelSize(0.12)
	ratioNm1CorrHisto.GetXaxis().SetTitleSize(0.12)
	ratioNm1CorrHisto.GetYaxis().SetTitle("Data/Bkg")
	ratioNm1CorrHisto.GetYaxis().SetLabelSize(0.12)
	ratioNm1CorrHisto.GetYaxis().SetTitleSize(0.12)
	ratioNm1CorrHisto.GetYaxis().SetTitleOffset(0.55)
	#if( ratioNm1CorrHisto.GetMaximum() > 2 ): ratioNm1CorrHisto.SetMaximum( 2.0 )
	ratioNm1CorrHisto.SetMaximum( 1.5 )
	ratioNm1CorrHisto.SetMinimum( 0.5 )
	ratioNm1CorrHisto.GetYaxis().SetNdivisions(505)
	ratioNm1CorrHisto.GetYaxis().CenterTitle()
	ratioNm1CorrHisto.Draw('E')
	outputFileName = nameInRoot+'_n-1Corrected_TauSystematics.'+args.extension
	can.SaveAs( 'Plots/'+ outputFileName )
	del can




if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='UDD312', dest='decay', help='Decay, example: UDD312, UDD323.' )
	parser.add_argument('-b', '--boosted', action='store', default='Boosted', help='Boosted or non boosted, example: Boosted' )
	parser.add_argument('-v', '--version', action='store', default='v05', help='Version: v01, v02.' )
	parser.add_argument('-g', '--grom', action='store', default='pruned', dest='grooming', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-m', '--mass', action='store', default='100', help='Mass of Stop, example: 100' )
	parser.add_argument('-q', '--qcd', action='store', default='Pt', dest='qcd', help='Type of QCD binning, example: HT.' )
	parser.add_argument('-l', '--lumi', action='store', default=2.6, help='Luminosity, example: 1.' )
	parser.add_argument('-r', '--range', action='store', default='low', dest='RANGE', help='Trigger used, example PFHT800.' )
	parser.add_argument('-e', '--extension', action='store', default='png', help='Extension of plots.' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)
	
	CMS_lumi.lumi_13TeV = str(args.lumi)+" fb^{-1}"
	
	if 'Pt' in args.qcd: 
		#bkgLabel='(w QCD pythia8)'
		QCDSF = 0.80
	else: 
		#bkgLabel='(w QCD madgraphMLM+pythia8)'
		QCDSF = 1.05

	bkgFiles = OrderedDict() 
	signalFiles = {}
	dataFile = TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_DATA_'+args.RANGE+'_'+args.version+'.root')
	signalFiles[ 'Signal' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_'+args.RANGE+'_'+args.version+'.root'), 1, args.decay+' RPV #tilde{t} '+str(args.mass)+' GeV', kRed-4]
	bkgFiles[ 'TTJets' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_TTJets_'+args.RANGE+'_'+args.version+'.root'),	1, 't #bar{t} + Jets', kGreen ]
    	bkgFiles[ 'ZJetsToQQ' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_ZJetsToQQ_'+args.RANGE+'_'+args.version+'.root'), 1., 'Z + Jets', kOrange]
    	bkgFiles[ 'WJetsToQQ' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_WJetsToQQ_'+args.RANGE+'_'+args.version+'.root'), 1., 'W + Jets', kMagenta ]
	bkgFiles[ 'WWTo4Q' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_WWTo4Q_'+args.RANGE+'_'+args.version+'.root'), 1 , 'WW (had)', kMagenta+2 ]
	bkgFiles[ 'ZZTo4Q' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_ZZTo4Q_'+args.RANGE+'_'+args.version+'.root'), 1, 'ZZ (had)', kOrange+2 ]
	bkgFiles[ 'WZ' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_WZ_'+args.RANGE+'_'+args.version+'.root'), 1, 'WZ', kCyan ]
	bkgFiles[ 'QCD'+args.qcd+'All' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_QCD'+args.qcd+'All_'+args.RANGE+'_'+args.version+'.root'), QCDSF, 'QCD', kBlue-4 ]
	#bkgFiles[ 'QCDPtAll' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_QCDPtAll_'+args.RANGE+'_'+args.version+'.root'), QCDSF, 'QCD', kBlue-4 ]


	#if 'Resolved' in args.boosted: args.grooming =  '' 
	#if 'all' in args.grooming: Groommers = [ '', 'Trimmed', 'Pruned', 'Filtered', "SoftDrop" ]
	#else: Groommers = [ args.grooming ]

	#for optGroom in Groommers:
	tauSystematics( dataFile, bkgFiles, signalFiles, 'jet1Tau21', False )
