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

def listOfCont( histo ):
 	"""docstring for listOfCont"""
	tmpListContent = []
	tmpListError = []
	for ibin in range( histo.GetNbinsX() ): 
		tmpListContent.append( histo.GetBinContent( ibin ) )
		tmpListError.append( histo.GetBinError( ibin ) )
	return tmpListContent, tmpListError

def BCDHisto( tmpHisto, BList, CList, DList ):
	"""docstring for BCDHisto"""

	#tmpHisto.Reset()
	for jbin in range( len( BList ) ):
		Nominal_Side = BList[ jbin ]
		Side_Side = CList[ jbin ]
		Side_Nominal = DList[ jbin ]
		if Side_Side != 0: 
			Bkg = Nominal_Side*Side_Nominal/Side_Side
			#BkgError = TMath.Sqrt( Bkg ) 
			try: BkgError = Bkg * TMath.Sqrt( TMath.Power(( TMath.Sqrt( Nominal_Side ) / Nominal_Side ), 2) + TMath.Power(( TMath.Sqrt( Side_Nominal ) / Side_Nominal ), 2) + TMath.Power(( TMath.Sqrt( Side_Side ) / Side_Side ), 2) )
			except ZeroDivisionError: BkgError = 0
		else: 
			Bkg = 0
			BkgError = 0
		tmpHisto.SetBinContent( jbin, Bkg )
		tmpHisto.SetBinError( jbin, BkgError )
	return tmpHisto

def addSysBand( histo, uncSys, colour ):
	"""docstring for addSysBand"""
	
	hclone = histo.Clone()
	hclone.Reset()
	for i in range( 0, histo.GetNbinsX()+1 ):
		cont = histo.GetBinContent( i )
		hclone.SetBinContent( i, cont )
		hclone.SetBinError( i, ((cont*uncSys) -cont) )
	hclone.SetFillStyle(3004)
	hclone.SetFillColor( colour )
	return hclone


def makePulls( histo1, histo2 ):
	"""docstring for makePulls"""

	histoPulls = histo1.Clone()
	histoPulls.Reset()
	pullsOnly = TH1F( 'pullsOnly', 'pullsOnly', 14, -3, 3 )
	for ibin in range(0, histo1.GetNbinsX() ):
		try: pull = ( histo1.GetBinContent( ibin ) - histo2.GetBinContent( ibin ) ) / histo1.GetBinError( ibin ) 
		except ZeroDivisionError: pull = 0
		histoPulls.SetBinContent( ibin, pull )
		histoPulls.SetBinError( ibin, 1 )
		pullsOnly.Fill( pull )

	return histoPulls, pullsOnly
	

def ratioPlots( histo1, histo2 ):
	"""docstring for ratioPlots"""

	chi2 = 0
	ndf = 0
	h1errFull = histo1.Clone()
	h1errFull.Reset()
	h1errh2 = histo1.Clone()
	h1errh2.Reset()
	for ibin in range( histo1.GetNbinsX()+1 ):
		x = histo1.GetBinContent( ibin )
		xErr = histo1.GetBinError( ibin )
		y = histo2.GetBinContent( ibin )
		yErr = histo2.GetBinError( ibin )
		try: 
			ratio = x/y
			ratioErrX = ratio * TMath.Sqrt( TMath.Power( xErr/x, 2) + TMath.Power( yErr/y, 2)  )
			ratioErrY = ratio* yErr / y
		except ZeroDivisionError: 
			ratio = 0
			ratioErrX = 0
			ratioErrY = 0
		print x, xErr, y, yErr, ratio, ratioErrX, ratioErrY
		h1errFull.SetBinContent( ibin, ratio )
		h1errFull.SetBinError( ibin, ratioErrX )
		h1errh2.SetBinContent( ibin, ratio )
		h1errh2.SetBinError( ibin, ratioErrY )
		if ibin < 35 :
			if (y>0):
				try: chi2 += ((y-x)*(y-x))/( (yErr*yErr) + (xErr*xErr) )
				except ZeroDivisionError: chi2 += 0
				ndf += 1
	return h1errFull, h1errh2, chi2, ndf-1


def plotBkgEstimation( dataFile, bkgFiles, signalFiles, Groom, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):
	"""docstring for plotBkgEstimation"""

	SRHistos = {}
	CRHistos = {}
	for bkgSamples in bkgFiles:
		SRHistos[ bkgSamples ] = bkgFiles[ bkgSamples ][0].Get( nameInRoot+'_'+bkgSamples+'_A' )
		CRHistos[ bkgSamples ] = bkgFiles[ bkgSamples ][0].Get( nameInRoot+'_'+bkgSamples+'_ABCDProj' )
		if rebinX > 1: 
			SRHistos[ bkgSamples ].Rebin( rebinX )
			CRHistos[ bkgSamples ].Rebin( rebinX )
		#SRHistos[ bkgSamples ] = SRHistos[ bkgSamples ].Rebin( len( boostedMassAveBins )-1, SRHistos[ bkgSamples ].GetName(), boostedMassAveBinSize )
		#CRHistos[ bkgSamples ] = CRHistos[ bkgSamples ].Rebin( len( boostedMassAveBins )-1, CRHistos[ bkgSamples ].GetName(), boostedMassAveBinSize )
		if bkgFiles[ bkgSamples ][1] != 1: 
			scale = bkgFiles[ bkgSamples ][1] 
			SRHistos[ bkgSamples ].Scale( scale ) 
			CRHistos[ bkgSamples ].Scale( scale )

	
	hDataCR =  dataFile.Get( nameInRoot+'_DATA_ABCDProj' )
	hDataCR.Rebin( rebinX )
	#hDataCR.Scale( 7.65453e-01 )
	#hDataCR = hDataCR.Rebin( len( boostedMassAveBins )-1, hDataCR.GetName(), boostedMassAveBinSize )
	
	for signalSamples in signalFiles:
		hSignalSR = signalFiles[ signalSamples ][0].Get( nameInRoot+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_A' )
		hSignalCR = signalFiles[ signalSamples ][0].Get( nameInRoot+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_ABCDProj' )
		#if rebinX > 1: 
		#	hSignalSR.Rebin( rebinX )
		#	hSignalCR.Rebin( rebinX )
		#hSignalCR = hSignalCR.Rebin( len( boostedMassAveBins )-1, hSignalCR.GetName(), boostedMassAveBinSize )
		#hSignalSR = hSignalSR.Rebin( len( boostedMassAveBins )-1, hSignalSR.GetName(), boostedMassAveBinSize )
		if signalFiles[ signalSamples ][1] != 1: 
			scale = signalFiles[ signalSamples ][1] 
			hSignalSR.Scale( scale ) 
			hSignalCR.Scale( scale )

	hSR = hDataCR.Clone()
	hSR.Reset()
	hCR = hDataCR.Clone()
	hCR.Reset()
	for samples in SRHistos:
		hSR.Add( SRHistos[ samples ].Clone() )
		hCR.Add( CRHistos[ samples ].Clone() )
	#print hDataCR.FindFirstBinAbove( 1, 1 ), hDataCR.GetBinContent( 0 )


	firstBinData = 40 #hDataCR.GetXaxis().GetLowEdge( hDataCR.FindFirstBinAbove( 0, 1 ) )  #40
	#locFirstBin = boostedMassAveBins.index( firstBinData )
	lastBinData = 300 #hDataCR.GetXaxis().GetLowEdge( hDataCR.FindLastBinAbove( 0, 1 ) )   #300
	tmpSR = hSR.Clone()
	tmpSR.GetXaxis().SetRangeUser( firstBinData, lastBinData )
	tmpCR = hCR.Clone()
	tmpCR.GetXaxis().SetRangeUser( firstBinData, lastBinData )
	res = array( 'd', ( [ 0 ] * tmpSR.GetNbinsX() ) )
	chi2NdfMC =  round( tmpSR.Chi2Test(tmpCR, 'WWCHI2/NDFP', res), 2 )
	chi2MC =  round( tmpSR.Chi2Test(tmpCR, 'WWCHI2'), 2 )

	
	#linearCR = TF1("linearCR", "pol0", 0, 500 ) 
	#linearCR = TF1("linearCR", "pol0", firstBinData, lastBinData ) 
	#hRatiohSRhDataCRerrhData.Fit(linearCR, 'MIR' )
	#fCR = hRatiohSRhDataCRerrhData.GetFunction("linearCR") 

	hSignalCRAlone = hSignalCR.Clone()
	hSignalCR.Add( hCR )
	#hSignalSR.Add( hSR )
	tmphSignalCR = hSignalCR.Clone()
	tmphSignalCR.Reset()
	tmphSignalCR.Divide( hSignalCR, hCR, 1., 1., '' )

#	linearSignalCR = TF1("pol0", "pol0", 50, 300 ) 
#	tmphSignalCR.Fit(linearSignalCR, 'MEIRLLF' )
#	fSignalCR = TF1( tmphSignalCR.GetFunction("pol0") )
#	linearSignalCRChi2 = fSignalCR.GetChisquare()
#	linearSignalCRNDF = fCR.GetNDF()

	hDataSignal =  hDataCR.Clone()
	hDataSignal.Add( hSignalCRAlone, -1 )
	tmphDataCR = hDataCR.Clone()
	tmphDataCR.Reset()
	tmphDataCR.Divide( hCR, hDataSignal, 1., 1., '' )

	hDataPlusSignal =  hDataCR.Clone()
	hDataPlusSignal.Add( hSignalSR )
	tmphDataCRPlusSignal = hDataCR.Clone()
	tmphDataCRPlusSignal.Reset()
	tmphDataCRPlusSignal.Divide( hDataCR, hDataPlusSignal, 1., 1., '' )

	binWidth = hSR.GetBinWidth(1) # '#sigma_{mass}'

	##### Bkg CR vs Bkg SR
	legend=TLegend(0.55,0.75,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)
	#legend.AddEntry( hSR, 'MC '+bkgLabel+' SR' , 'l' )
	#legend.AddEntry( hCR, 'MC '+bkgLabel+' ABCD Pred', 'pl' )
	legend.AddEntry( hSR, 'All MC Bkgs SR' , 'l' )
	legend.AddEntry( hCR, 'All MC Bkgs ABCD Pred', 'pl' )

	hSR.SetLineColor(kRed-4)
	hSR.SetLineWidth(2)
	hSR.GetYaxis().SetTitle('Events / '+str(binWidth))
	hSR.GetXaxis().SetRangeUser( xmin, xmax )
	hSR.SetMaximum( 1.2* max( hSR.GetMaximum(), hCR.GetMaximum() ) )
	hCR.SetLineColor(kBlue-4)
	hCR.SetLineWidth(2)
	hCR.SetLineStyle(2)
	hDataCR.SetMarkerStyle(8)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetGrid()
	#if log: pad1.SetLogy() 	
	hSR.Draw("histe")
	#hSRUncBand = addSysBand( hSR, 1.10, kRed )
	#legend.AddEntry( hSRUncBand, 'Syst. unc.', 'f' )
	#hSRUncBand.Draw("same E2")
	hCR.Draw('histe same')
	#hCRUncBand = addSysBand( hCR, 1.10, kBlue )
	#hCRUncBand.Draw("same E2")

	hRatiohSRhCRerrhCR, hRatiohSRhCRerrFull, hSRchi2, hSRndf = ratioPlots( hSR, hCR ) 

	#textkolTestMC = TLatex( 200, 550, 'Kolmogorov Test = '+ str( round( tmpSR.KolmogorovTest(tmpCR), 2 ) ) )
	#textkolTestMC.SetTextFont(42) ### 62 is bold, 42 is normal
	#textkolTestMC.SetTextSize(0.04)
	#textkolTestMC.Draw()

	textchi2TestMC = TLatex( 209, (2000 if 'low' in args.RANGE else 300) , '#chi^{2}/ndF Test = '+ str( chi2MC )+'/'+str( round(chi2MC/chi2NdfMC) ) )
	#textchi2TestMC = TLatex( 209, 2000, '#chi^{2}/ndF Test = '+ str( round(hSRchi2,2) )+'/'+str( hSRndf ) )
	textchi2TestMC.SetTextFont(42) ### 62 is bold, 42 is normal
	textchi2TestMC.SetTextSize(0.04)
	textchi2TestMC.Draw()

	textNumMC = TLatex( 209, (1600 if 'low' in args.RANGE else 200) , '#splitline{events SR/ABCD Pred = }{'+ str( round( hSR.Integral(),2 ) )+'/'+str( round( hCR.Integral(),2 ) )+'}' )
	textNumMC.SetTextFont(42) ### 62 is bold, 42 is normal
	textNumMC.SetTextSize(0.04)
	textNumMC.Draw()

	CMS_lumi.extraText = "Simulation Preliminary"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	legend.Draw()
	#if not (labX and labY): labels( name, '', '' )
	#labels( name1, '', '' ) #, labX, labY )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	
	#hRatiohSRhCRerrFull = hSR.Clone()
	#hRatiohSRhCRerrFull.Reset()
	#hRatiohSRhCRerrFull.Divide( hSR, hCR, 1., 1., '' )
	'''
	for ibin in range( hSR.GetNbinsX()+1 ):
		x = hSR.GetBinContent( ibin )
		xErr = hSR.GetBinError( ibin )
		y = hCR.GetBinContent( ibin )
		yErr = hCR.GetBinError( ibin )
		try: 
			ratio = x/y
			ratioErr = ratio * TMath.Sqrt( TMath.Power( xErr/x , 2) +  TMath.Power( yErr/y , 2) ) 
		except ZeroDivisionError: 
			ratio = 0
			ratioErr = 0
		hRatiohSRhCRerrFull.SetBinContent( ibin, ratio )
		hRatiohSRhCRerrFull.SetBinError( ibin, ratioErr )
	'''

	#for i in range( 0, len(res)) : 
	#	print locFirstBin+i+1, res[i], 
	#	hRatiohSRhCRerrFull.SetBinContent( locFirstBin+i+1, res[i] )
	#hRatiohSRhCRerrFull, hRatiohSRhCRerrFullPulls = makePulls( hCR, hSR )
	#hRatiohSRhCRerrFullCR, hRatiohSRhCRerrFullCRPulls = makePulls( hSR, hCR )
	'''
	#linearSR = TF1("SR", "pol0", 0, 500 ) 
	#linearSR = TF1("SR", "pol0", firstBinData, lastBinData ) 
	#hRatiohSRhCRerrFull.Fit(linearSR, 'MIR' )
	#fSR = hRatiohSRhCRerrFull.GetFunction("SR") 
	'''
	
	labelAxis( nameInRoot, hRatiohSRhCRerrFull, Groom )
	hRatiohSRhCRerrFull.GetXaxis().SetRangeUser( xmin, xmax )
	hRatiohSRhCRerrFull.SetMarkerStyle(8)
	hRatiohSRhCRerrFull.SetLineColor(kBlack)
	hRatiohSRhCRerrFull.GetXaxis().SetTitleOffset(1.1)
	hRatiohSRhCRerrFull.GetXaxis().SetLabelSize(0.12)
	hRatiohSRhCRerrFull.GetXaxis().SetTitleSize(0.12)
	hRatiohSRhCRerrFull.GetYaxis().SetTitle("MC (SR/Bkg Pred)")
	hRatiohSRhCRerrFull.GetYaxis().CenterTitle()
	#hRatiohSRhCRerrFull.GetYaxis().SetTitle("Pull")
	hRatiohSRhCRerrFull.GetYaxis().SetLabelSize(0.12)
	hRatiohSRhCRerrFull.GetYaxis().SetTitleSize(0.12)
	hRatiohSRhCRerrFull.GetYaxis().SetTitleOffset(0.55)
	hRatiohSRhCRerrFull.SetMaximum( 2. )
	hRatiohSRhCRerrFull.SetMinimum( 0. )
	#hRatiohSRhCRerrFull.SetMaximum( 3. )
	#hRatiohSRhCRerrFull.SetMinimum( -3. )
	hRatiohSRhCRerrFull.GetYaxis().SetNdivisions(505)
	hRatiohSRhCRerrFull.Draw('PE')
	hRatiohSRhCRerrhCR.SetFillStyle(3004)
	hRatiohSRhCRerrhCR.SetFillColor( kRed )
	hRatiohSRhCRerrhCR.Draw('same E2')
#	linearSR.SetLineWidth( 2 )
#	linearSR.SetLineColor( kGreen )
#	linearSR.Draw("same")
#	textChi2SR = TLatex( 10, 1.5, '#splitline{#chi^{2}/NdF = '+ str( round( fSR.GetChisquare(), 2 ) )+'/'+ str( round( fSR.GetNDF(), 2 ) )+'}{p0 = '+ str( round( fSR.GetParameter(0), 2 ) ) +', p1 = '+ str( round( fSR.GetParameter(1), 5 ) ) +'}' )
#	textChi2SR.SetTextFont(62) ### 62 is bold, 42 is normal
#	textChi2SR.SetTextSize(0.08)
#	textChi2SR.Draw()
#	#hRatiohSRhDataCRerrhData.Draw()
	line.Draw("same")
	#line0.Draw("same")

	outputFileName = nameInRoot+'_Bkg_'+Groom+'_'+args.RANGE+'_QCD'+args.qcd+'_bkgShapeEstimation'+args.boosted+'Plots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/'+ outputFileName )
	del can

	'''
	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	gStyle.SetOptStat(1)
	pullGaus = TF1( 'pullGaus', 'gaus', -3, 3 )
	hRatiohSRhCRerrFullPulls.Fit( 'pullGaus', 'MIR' )
	hRatiohSRhCRerrFullPulls.GetXaxis().SetTitle('Pulls')
	hRatiohSRhCRerrFullPulls.GetYaxis().SetTitle('Bins')
	hRatiohSRhCRerrFullPulls.Draw('PE')
	#can.Update()
	#gStyle.SetStatY(0.91)
	#gStyle.SetStatX(0.95)
	#gStyle.SetStatW(0.15)
	#gStyle.SetStatH(0.30) 
	#print hRatiohSRhCRerrFullPulls.GetListOfFunctions().FindObject("stats")
#	st1.SetX1NDC(.12);
#	st1.SetX2NDC(.32);
#	st1.SetY1NDC(.76);
#	st1.SetY2NDC(.91);
#	#st1.SetTextColor(4);
	can.Modified()
	outputFileNamePulls= nameInRoot+'_Pulls_Bkg_'+Groom+'_'+args.RANGE+'_QCD'+args.qcd+'_bkgShapeEstimation'+args.boosted+'Plots'+args.version+'.'+args.extension
	can.SaveAs('Plots/'+outputFileNamePulls)
	'''

	##### DATA CR vs Bkg SR
	legend2=TLegend(0.55,0.75,0.90,0.87)
	legend2.SetFillStyle(0)
	legend2.SetTextSize(0.04)
	#legend2.AddEntry( hSR, 'MC '+bkgLabel+' SR' , 'l' )
	legend2.AddEntry( hSR, 'All MC Bkgs SR' , 'l' )
	legend2.AddEntry( hDataCR, 'DATA ABCD Pred', 'pl' )
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetGrid()
	#if log: pad1.SetLogy() 	
	hSR.Draw("histe")
	#legend2.AddEntry( hSRUncBand, 'Syst. unc.', 'f' )
	#hSRUncBand.Draw("same E2")
	hDataCR.Draw('PE same')
	#hDataCRUncBand = addSysBand( hDataCR, 1.10, kBlack )
	#hDataCRUncBand.Draw("same E2")

	#hRatiohSRhDataCRerrhData.Divide( hSR, hDataCR, 1., 1., '' )
	hRatiohSRhDataCRerrFull, hRatiohSRhDataCRerrhData, hDataCRchi2, hDataCRndf = ratioPlots( hSR, hDataCR ) 

	tmpDataCR = hDataCR.Clone()
	tmpDataCR.GetXaxis().SetRangeUser( firstBinData, lastBinData )
	#textkolTestDataMC = TLatex( 200, 550, 'Kolmogorov Test = '+ str( round( tmpSR.KolmogorovTest(tmpDataCR ), 2 ) ) )
	#textkolTestDataMC.SetTextFont(42) ### 62 is bold, 42 is normal
	#textkolTestDataMC.SetTextSize(0.04)
	#textkolTestDataMC.Draw()

	chi2NdfDataMC =  round( tmpDataCR.Chi2Test(tmpSR, 'WWCHI2/NDFP'), 2 )
	chi2DataMC =  round( tmpDataCR.Chi2Test(tmpSR, 'WWCHI2'), 2 )
	textchi2TestDataMC = TLatex( 209,  (2000 if 'low' in args.RANGE else 300), '#chi^{2}/ndF Test = '+ str( chi2DataMC )+'/'+str( round(chi2DataMC/chi2NdfDataMC) ) )
	#textchi2TestDataMC = TLatex( 209, 2000, '#chi^{2}/ndF Test = '+ str( round(hDataCRchi2,2) )+'/'+str( hDataCRndf ) )
	textchi2TestDataMC.SetTextFont(42) ### 62 is bold, 42 is normal
	textchi2TestDataMC.SetTextSize(0.04)
	textchi2TestDataMC.Draw()

	textNumDataMC = TLatex( 209,  (1600 if 'low' in args.RANGE else 200), '#splitline{events SR/ABCD Pred = }{'+ str( round( hSR.Integral(),2 ) )+'/'+str( round( hDataCR.Integral(),2 ) )+'}' )
	textNumDataMC.SetTextFont(42) ### 62 is bold, 42 is normal
	textNumDataMC.SetTextSize(0.04)
	textNumDataMC.Draw()

	CMS_lumi.extraText = "Preliminary"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	legend2.Draw()
	#if not (labX and labY): labels( name, '', '' )
	#labels( name1, '', '' ) #, labX, labY )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	
	#hRatiohSRhDataCRerrhData, hRatiohSRhDataCRerrhDataPulls = makePulls( hSR, hDataCR )
	#tmphDataCRSR, tmphDataCRSRPulls = makePulls( hDataCR, hSR )

	labelAxis( nameInRoot, hRatiohSRhDataCRerrhData, Groom )
	hRatiohSRhDataCRerrhData.SetMarkerStyle(8)
	hRatiohSRhDataCRerrhData.GetXaxis().SetRangeUser( xmin, xmax )
	hRatiohSRhDataCRerrhData.SetMarkerStyle(8)
	hRatiohSRhDataCRerrhData.GetXaxis().SetTitleOffset(1.1)
	hRatiohSRhDataCRerrhData.GetXaxis().SetLabelSize(0.12)
	hRatiohSRhDataCRerrhData.GetXaxis().SetTitleSize(0.12)
	hRatiohSRhDataCRerrhData.GetYaxis().SetTitle("MC SR/ABCD Pred")
	#hRatiohSRhDataCRerrhData.GetYaxis().SetTitle("Pull")
	hRatiohSRhDataCRerrhData.GetYaxis().SetLabelSize(0.12)
	hRatiohSRhDataCRerrhData.GetYaxis().SetTitleSize(0.12)
	hRatiohSRhDataCRerrhData.GetYaxis().SetTitleOffset(0.55)
	hRatiohSRhDataCRerrhData.SetMaximum( 2. )
	hRatiohSRhDataCRerrhData.SetMinimum( 0. )
	#hRatiohSRhDataCRerrhData.SetMaximum( 3. )
	#hRatiohSRhDataCRerrhData.SetMinimum( -3. )
	hRatiohSRhDataCRerrhData.GetYaxis().SetNdivisions(505)
	#hRatiohSRhDataCRerrhData.SetFillStyle(3004)
	#hRatiohSRhDataCRerrhData.SetFillColor( kRed )
	hRatiohSRhDataCRerrhData.Draw('PE')
	hRatiohSRhDataCRerrFull.SetFillStyle(3004)
	hRatiohSRhDataCRerrFull.SetFillColor( kBlue )
	hRatiohSRhDataCRerrFull.Draw('same E2')
	'''
	#tmphDataCRSR.SetFillStyle(3004)
	#tmphDataCRSR.SetFillColor( kBlack )
	#tmphDataCRSR.Draw('same E2')
	linearCR.SetLineWidth( 2 )
	linearCR.SetLineColor( kGreen )
	linearCR.Draw("same")
	textChi2CR = TLatex( 10, 1.5, '#splitline{#chi^{2}/NdF = '+ str( round( fCR.GetChisquare(), 2 ) )+'/'+ str( round( fCR.GetNDF(), 2 ) )+'}{p0 = '+ str( round( fCR.GetParameter(0), 2 ) ) +', p1 = '+ str( round( fCR.GetParameter(1), 5 ) )+'}' )
	textChi2CR.SetTextFont(62) ### 62 is bold, 42 is normal
	textChi2CR.SetTextSize(0.08)
	textChi2CR.Draw()
	'''
	line.Draw("same")

	outputFileName = nameInRoot+'_DATA_Bkg_'+Groom+'_'+args.RANGE+'_QCD'+args.qcd+'_bkgShapeEstimation'+args.boosted+'Plots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/'+ outputFileName )
	del can
	sys.exit(0)
	#### signal plus bkg in CR
	legend3=TLegend(0.55,0.75,0.90,0.87)
	legend3.SetFillStyle(0)
	legend3.SetTextSize(0.03)
	legend3.AddEntry( hSignalCR, 'All MC Bkgs + RPV #tilde{t} '+str(args.mass)+' GeV - ABCD Pred' , 'l' )
	legend3.AddEntry( hCR, 'All MC Bkgs - ABCD Pred', 'pl' )

	hSignalCR.SetLineColor(kRed-4)
	hSignalCR.SetLineWidth(2)
	hSignalCR.GetYaxis().SetTitle('Events / '+str(binWidth))
	hSignalCR.GetXaxis().SetRangeUser( xmin, xmax )
	hSignalCR.SetMaximum( 1.2* max( hSignalCR.GetMaximum(), hCR.GetMaximum() ) )
	#hSignalCR.SetLineColor(kBlue-4)
	#hSignalCR.SetLineWidth(2)
	#hSignalCR.SetLineStyle(2)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetGrid()
	#if log: pad1.SetLogy() 	
	hSignalCR.Draw("histe")
	hCR.Draw('histe same')

	CMS_lumi.extraText = "Simulation Preliminary"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	legend3.Draw()
	#if not (labX and labY): labels( name, '', '' )
	#labels( name1, '', '' ) #, labX, labY )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	
	labelAxis( nameInRoot, hRatiohSRhCRerrFull, Groom )
	tmphSignalCR.GetXaxis().SetRangeUser( xmin, xmax )
	tmphSignalCR.SetMarkerStyle(8)
	tmphSignalCR.GetXaxis().SetTitleOffset(1.1)
	tmphSignalCR.GetXaxis().SetLabelSize(0.12)
	tmphSignalCR.GetXaxis().SetTitleSize(0.12)
	tmphSignalCR.GetYaxis().SetTitle("SR/CR")
	tmphSignalCR.GetYaxis().SetLabelSize(0.12)
	tmphSignalCR.GetYaxis().SetTitleSize(0.12)
	tmphSignalCR.GetYaxis().SetTitleOffset(0.55)
	tmphSignalCR.SetMaximum( 2. )
	tmphSignalCR.SetMinimum( 0. )
	tmphSignalCR.GetYaxis().SetNdivisions(505)
	tmphSignalCR.Draw()
#	linearSignalCR.SetLineWidth( 2 )
#	linearSignalCR.SetLineColor( kGreen )
#	linearSignalCR.Draw("same")
#	textChi2SignalCR = TLatex( 250, 1.5, '#chi^{2}/NdF = '+ str( round(linearSignalCRChi2, 2) ) +'/'+ str( round(linearSignalCRNDF, 2)  ) )
#	textChi2SignalCR.SetTextFont(62) ### 62 is bold, 42 is normal
#	textChi2SignalCR.SetTextSize(0.08)
#	textChi2SignalCR.Draw()
	line.Draw("same")

	outputFileName = nameInRoot+'_BkgPlusRPVSt'+str(args.mass)+'_'+Groom+'_'+args.RANGE+'_QCD'+args.qcd+'_bkgShapeEstimation'+args.boosted+'Plots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/'+ outputFileName )
	del can

	#### Data minus signal
	legend4=TLegend(0.55,0.75,0.90,0.87)
	legend4.SetFillStyle(0)
	legend4.SetTextSize(0.03)
	legend4.AddEntry( hCR, 'All MC Bkgs ABCD Pred', 'pl' )
	legend4.AddEntry( hDataSignal, '(DATA - RPV #tilde{t} '+str(args.mass)+' GeV) ABCD Pred' , 'pl' )

	hDataSignal.SetMarkerStyle(8)
	hDataSignal.SetMarkerColor(kRed-4)
	#hDataSignal.SetLineWidth(2)
	hDataSignal.GetYaxis().SetTitle('Events / '+str(binWidth))
	hDataSignal.GetXaxis().SetRangeUser( xmin, xmax )
	hDataSignal.SetMaximum( 1.2* max( hDataSignal.GetMaximum(), hCR.GetMaximum() ) )

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetGrid()
	#if log: pad1.SetLogy() 	
	hDataSignal.Draw("EP")
	hCR.Draw('histe same')

	CMS_lumi.extraText = "Simulation Preliminary"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	legend4.Draw()
	#if not (labX and labY): labels( name, '', '' )
	#labels( name1, '', '' ) #, labX, labY )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	
	labelAxis( nameInRoot, hRatiohSRhCRerrFull, Groom )
	tmphDataCR.GetXaxis().SetRangeUser( xmin, xmax )
	tmphDataCR.SetMarkerStyle(8)
	tmphDataCR.GetXaxis().SetTitleOffset(1.1)
	tmphDataCR.GetXaxis().SetLabelSize(0.12)
	tmphDataCR.GetXaxis().SetTitleSize(0.12)
	tmphDataCR.GetYaxis().SetTitle("MC/(DATA-Signal)")
	tmphDataCR.GetYaxis().SetLabelSize(0.12)
	tmphDataCR.GetYaxis().SetTitleSize(0.12)
	tmphDataCR.GetYaxis().SetTitleOffset(0.55)
	tmphDataCR.SetMaximum( 2. )
	tmphDataCR.SetMinimum( 0. )
	tmphDataCR.GetYaxis().SetNdivisions(505)
	tmphDataCR.Draw()
	line.Draw("same")

	outputFileName = nameInRoot+'_DATAMinusRPVSt'+str(args.mass)+'_'+Groom+'_'+args.RANGE+'_QCD'+args.qcd+'_bkgShapeEstimation'+args.boosted+'Plots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/'+ outputFileName )
	del can

	#### Signal stack on DATA
	hSignalSR.SetFillStyle( 1001 )
	hSignalSR.SetFillColor( kRed )
	stackHisto = THStack('stackHisto', 'stack')
	stackHisto.Add( hDataCR )
	stackHisto.Add( hSignalSR )

	legend5=TLegend(0.70,0.75,0.90,0.87)
	legend5.SetFillStyle(0)
	legend5.SetTextSize(0.03)
	legend5.AddEntry( hDataCR, 'DATA ABCD Pred', 'l' )
	legend5.AddEntry( hSignalSR, 'RPV #tilde{t} '+str(args.mass)+' GeV' , 'f' )

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetGrid()
	#if log: pad1.SetLogy() 	
	stackHisto.Draw('hist')
	hDataCR.Draw("EP same")
	#hCR.Draw('histe same')

	stackHisto.GetYaxis().SetTitle('Events / '+str(binWidth))
	stackHisto.GetXaxis().SetRangeUser( xmin, xmax )
	#stackHisto.SetMaximum( 1.2* max( hDataSignal.GetMaximum(), hCR.GetMaximum() ) )

	CMS_lumi.extraText = "Simulation Preliminary"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	legend5.Draw()
	#if not (labX and labY): labels( name, '', '' )
	#labels( name1, '', '' ) #, labX, labY )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	
	labelAxis( nameInRoot, hRatiohSRhCRerrFull, Groom )
	tmphDataCRPlusSignal.GetXaxis().SetRangeUser( xmin, xmax )
	tmphDataCRPlusSignal.SetMarkerStyle(8)
	tmphDataCRPlusSignal.GetXaxis().SetTitleOffset(1.1)
	tmphDataCRPlusSignal.GetXaxis().SetLabelSize(0.12)
	tmphDataCRPlusSignal.GetXaxis().SetTitleSize(0.12)
	tmphDataCRPlusSignal.GetYaxis().SetTitle("DATA/Bkg Pred")
	tmphDataCRPlusSignal.GetYaxis().SetLabelSize(0.12)
	tmphDataCRPlusSignal.GetYaxis().SetTitleSize(0.12)
	tmphDataCRPlusSignal.GetYaxis().SetTitleOffset(0.55)
	tmphDataCRPlusSignal.SetMaximum( 2. )
	tmphDataCRPlusSignal.SetMinimum( 0. )
	tmphDataCRPlusSignal.GetYaxis().SetNdivisions(505)
	tmphDataCRPlusSignal.Draw()
	line.Draw("same")

	outputFileName = nameInRoot+'_DATAStackRPVSt'+str(args.mass)+'_'+Groom+'_'+args.RANGE+'_QCD'+args.qcd+'_bkgShapeEstimation'+args.boosted+'Plots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/'+ outputFileName )
	del can

def tmpPlotBkgEstimation( dataFile, Groom, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):
	"""docstring for tmpPlotBkgEstimation"""

	hData_A =  dataFile.Get( 'BoostedAnalysisPlots/'+nameInRoot+'_A' )
	hData_A.Rebin( rebinX )
	hData_B =  dataFile.Get( 'BoostedAnalysisPlots/'+nameInRoot+'_B' )
	hData_B.Rebin( rebinX )
	hData_C =  dataFile.Get( 'BoostedAnalysisPlots/'+nameInRoot+'_C' )
	hData_C.Rebin( rebinX )
	hData_D =  dataFile.Get( 'BoostedAnalysisPlots/'+nameInRoot+'_D' )
	hData_D.Rebin( rebinX )
	
	tmpBC = hData_B.Clone()
	tmpBC.Reset()
	tmpBC.Multiply( hData_B, hData_C, 1, 1, '')
	tmpBCD = hData_B.Clone()
	tmpBCD.Reset()
	tmpBCD.Divide( tmpBC, hData_D, 1, 1, '')

	tmphSignalCR = hData_A.Clone()
	tmphSignalCR.Reset()
	tmphSignalCR.Divide( hData_A, tmpBCD, 1., 1., '' )

	binWidth = hData_A.GetBinWidth(1)

	legend3=TLegend(0.55,0.75,0.90,0.87)
	legend3.SetFillStyle(0)
	legend3.SetTextSize(0.03)
	legend3.AddEntry( hData_A, 'DATA - SR' , 'l' )
	legend3.AddEntry( tmpBCD, 'DATA - ABCD Pred', 'pl' )

	hData_A.SetLineColor(kRed-4)
	hData_A.SetLineWidth(2)
	hData_A.GetYaxis().SetTitle('Events / '+str(binWidth))
	hData_A.GetXaxis().SetRangeUser( xmin, xmax )
	hData_A.SetMaximum( 1.2* max( hData_A.GetMaximum(), tmpBCD.GetMaximum() ) )
	tmpBCD.SetLineColor(kBlue-4)
	tmpBCD.SetLineWidth(2)
	tmpBCD.SetLineStyle(2)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetGrid()
	#if log: pad1.SetLogy() 	
	hData_A.Draw("histe")
	tmpBCD.Draw('histe same')

	CMS_lumi.extraText = "Preliminary"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	legend3.Draw()
	#if not (labX and labY): labels( name, '', '' )
	#labels( name1, '', '' ) #, labX, labY )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	
	labelAxis( nameInRoot, hData_A, Groom )
	tmphSignalCR.GetXaxis().SetRangeUser( xmin, xmax )
	tmphSignalCR.SetMarkerStyle(8)
	tmphSignalCR.GetXaxis().SetTitleOffset(1.1)
	tmphSignalCR.GetXaxis().SetLabelSize(0.12)
	tmphSignalCR.GetXaxis().SetTitleSize(0.12)
	tmphSignalCR.GetYaxis().SetTitle("SR/ABCD Pred")
	tmphSignalCR.GetYaxis().SetLabelSize(0.12)
	tmphSignalCR.GetYaxis().SetTitleSize(0.12)
	tmphSignalCR.GetYaxis().SetTitleOffset(0.55)
	tmphSignalCR.SetMaximum( 2. )
	tmphSignalCR.SetMinimum( 0. )
	tmphSignalCR.GetYaxis().SetNdivisions(505)
	tmphSignalCR.Draw()
	line.Draw("same")

	outputFileName = nameInRoot+'_BkgPlusRPVSt'+str(args.mass)+'_'+Groom+'_'+args.RANGE+'_QCD'+args.qcd+'_bkgShapeEstimation'+args.boosted+'Plots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/'+ outputFileName )
	del can

def plot2DBkgEstimation( rootFile, sample, Groom, nameInRoot, titleXAxis, titleXAxis2, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, legX, legY ):
	"""docstring for plot"""

	outputFileName = nameInRoot+'_'+sample+'_'+Groom+'_'+args.RANGE+'_bkgShapeEstimation'+args.boosted+'Plots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName

	bkgHistos = OrderedDict()
	if isinstance(rootFile, dict):
		for bkg in rootFile:
			if not 'DATA' in bkg: bkgHistos[ bkg+'_A' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'_'+bkg+'_A' ), rebinx, rebiny )
			bkgHistos[ bkg+'_B' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'_'+bkg+'_B' ), rebinx, rebiny )
			bkgHistos[ bkg+'_C' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'_'+bkg+'_C' ), rebinx, rebiny )
			bkgHistos[ bkg+'_D' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'_'+bkg+'_D' ), rebinx, rebiny )

		hBkg = bkgHistos[ bkg+'_B' ].Clone()
		hBkg.Reset()
		for samples in bkgHistos:
			print samples
			hBkg.Add( bkgHistos[ samples ].Clone() )
	else: 
		if not 'DATA' in sample: bkgHistos[ sample+'_A' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+sample+'_A' ), rebinx, rebiny )
		bkgHistos[ sample+'_B' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+sample+'_B' ), rebinx, rebiny )
		bkgHistos[ sample+'_C' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+sample+'_C' ), rebinx, rebiny )
		bkgHistos[ sample+'_D' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+sample+'_D' ), rebinx, rebiny )

		hBkg = bkgHistos[ sample+'_B' ].Clone()
		for samples in bkgHistos:
			if sample+'_B' not in samples: hBkg.Add( bkgHistos[ samples ].Clone() )

	if 'DATA' in sample: CMS_lumi.extraText = "Preliminary"
	else: CMS_lumi.extraText = "Simulation Preliminary"
	hBkg.GetXaxis().SetTitle( titleXAxis )
	hBkg.GetYaxis().SetTitleOffset( 0.9 )
	hBkg.GetYaxis().SetTitle( titleXAxis2 )
	corrFactor = hBkg.GetCorrelationFactor()
	textBox=TLatex()
	textBox.SetNDC()
	textBox.SetTextSize(0.05) 
	textBox.SetTextFont(62) ### 62 is bold, 42 is normal
	textBox.SetTextAlign(31)

	if (Xmax or Ymax):
		hBkg.GetXaxis().SetRangeUser( Xmin, Xmax )
		hBkg.GetYaxis().SetRangeUser( Ymin, Ymax )

	tdrStyle.SetPadRightMargin(0.12)
	hBkg.SetMaximum( 1500 )
	hBkg.SetMinimum( 0.01 )
	can = TCanvas('c1', 'c1',  750, 500 )
	can.SetLogz()
	hBkg.Draw('colz')
	textBox.DrawLatex(0.85, 0.85, sample  )
	textBox1 = textBox.Clone()
	textBox1.DrawLatex(0.85, 0.8, 'Corr. Factor = '+str(round(corrFactor,2)))

	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(can, 4, 0)

	can.SaveAs( 'Plots/'+outputFileName )
	#can.SaveAs( 'Plots/'+outputFileName.replace(''+ext, 'gif') )
	del can


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='UDD312', dest='decay', help='Decay, example: UDD312, UDD323.' )
	parser.add_argument('-b', '--boosted', action='store', default='Boosted', help='Boosted or non boosted, example: Boosted' )
	parser.add_argument('-v', '--version', action='store', default='v04', help='Version: v01, v02.' )
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
    	#bkgFiles[ 'ZJetsToQQ' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_ZJetsToQQ_'+args.RANGE+'_'+args.version+'.root'), 1., 'Z + Jets', kOrange]
    	#bkgFiles[ 'WJetsToQQ' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_WJetsToQQ_'+args.RANGE+'_'+args.version+'.root'), 1., 'W + Jets', kMagenta ]
	bkgFiles[ 'WWTo4Q' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_WWTo4Q_'+args.RANGE+'_'+args.version+'.root'), 1 , 'WW (had)', kMagenta+2 ]
	bkgFiles[ 'ZZTo4Q' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_ZZTo4Q_'+args.RANGE+'_'+args.version+'.root'), 1, 'ZZ (had)', kOrange+2 ]
	bkgFiles[ 'WZ' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_WZ_'+args.RANGE+'_'+args.version+'.root'), 1, 'WZ', kCyan ]
	bkgFiles[ 'QCD'+args.qcd+'All' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_QCD'+args.qcd+'All_'+args.RANGE+'_'+args.version+'.root'), QCDSF, 'QCD', kBlue-4 ]
	#bkgFiles[ 'QCDPtAll' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_QCDPtAll_'+args.RANGE+'_'+args.version+'.root'), QCDSF, 'QCD', kBlue-4 ]


	massMinX = 0
	massMaxX = 350
	jetMassHTlabY = 0.20
	jetMassHTlabX = 0.85

	if 'Resolved' in args.boosted: args.grooming =  '' 
	if 'all' in args.grooming: Groommers = [ '', 'Trimmed', 'Pruned', 'Filtered', "SoftDrop" ]
	else: Groommers = [ args.grooming ]

	for optGroom in Groommers:
		if '2D' in args.proc: 
			for bkg in bkgFiles: plot2DBkgEstimation( bkgFiles[ bkg ][0], bkg, optGroom, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY)
			for bkg in signalFiles: plot2DBkgEstimation( signalFiles[ bkg ][0], 'RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass), optGroom, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY)
		else: 
			tmpListCuts = selection[ 'RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass) ][-2:]
			nameVarABCD = 'massAve_'+tmpListCuts[0][0]+'Vs'+tmpListCuts[1][0]
			plotBkgEstimation( dataFile, bkgFiles, signalFiles, optGroom, nameVarABCD, 0, massMaxX, 10, '', '', False )
