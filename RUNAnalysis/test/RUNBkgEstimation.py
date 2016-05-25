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
	from RUNA.RUNAnalysis.cuts import selection 
	import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
except ImportError:
	sys.path.append('../python')
	from histoLabels import labels, labelAxis, finalLabels
	from scaleFactors import * #scaleFactor as SF
	from cuts import selection 
	import CMS_lumi as CMS_lumi 
	import tdrstyle as tdrstyle

gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)

xline = array('d', [0,2000])
yline = array('d', [1,1])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)


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

def plotBkgEstimation( dataFile, bkgFiles, signalFiles, Groom, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):
	"""docstring for plotBkgEstimation"""

	SRHistos = {}
	CRHistos = {}
	for bkgSamples in bkgFiles:
		#tmphSR = bkgFiles[ bkgSamples ][0].Get( nameInRoot+'_'+bkgSamples+'_A' )
		#tmphCR = bkgFiles[ bkgSamples ][0].Get( nameInRoot+'_'+bkgSamples+'_ABCDProj' )
		SRHistos[ bkgSamples ] = bkgFiles[ bkgSamples ][0].Get( nameInRoot+'_'+bkgSamples+'_A' )
		CRHistos[ bkgSamples ] = bkgFiles[ bkgSamples ][0].Get( nameInRoot+'_'+bkgSamples+'_ABCDProj' )
		if rebinX > 1: 
			SRHistos[ bkgSamples ].Rebin( rebinX )
			CRHistos[ bkgSamples ].Rebin( rebinX )
		#SRHistos[ bkgSamples ] = SRHistos[ bkgSamples ].Rebin( len( boostedMassAveBins )-1, SRHistos[ bkgSamples ].GetName(), boostedMassAveBins )
		#CRHistos[ bkgSamples ] = CRHistos[ bkgSamples ].Rebin( len( boostedMassAveBins )-1, SRHistos[ bkgSamples ].GetName(), boostedMassAveBins )
		if bkgFiles[ bkgSamples ][1] != 1: 
			scale = bkgFiles[ bkgSamples ][1] 
			SRHistos[ bkgSamples ].Scale( scale ) 
			CRHistos[ bkgSamples ].Scale( scale )

	
	hDataCR =  dataFile.Get( nameInRoot+'_DATA_ABCDProj' )
	hDataCR.Rebin( rebinX )
	#hDataCR = hDataCR.Rebin( len( boostedMassAveBins )-1, hDataCR.GetName(), boostedMassAveBins )
	
	for signalSamples in signalFiles:
		hSignalSR = signalFiles[ signalSamples ][0].Get( nameInRoot+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_A' )
		hSignalCR = signalFiles[ signalSamples ][0].Get( nameInRoot+'_RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass)+'_ABCDProj' )
		#if rebinX > 1: 
		#	hSignalSR.Rebin( rebinX )
		#	hSignalCR.Rebin( rebinX )
		#hSignalCR = hSignalCR.Rebin( len( boostedMassAveBins )-1, hSignalCR.GetName(), boostedMassAveBins )
		#hSignalSR = hSignalSR.Rebin( len( boostedMassAveBins )-1, hSignalSR.GetName(), boostedMassAveBins )
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

	tmphSR = hSR.Clone()
	tmphSR.Reset()
	tmphSR.Divide( hSR, hCR, 1., 1., '' )
#	linearSR = TF1("pol0", "pol0", 50, 300 ) 
#	tmphSR.Fit(linearSR, 'MEIRLLF' )
#	fSR = TF1( tmphSR.GetFunction("pol0") )
#	linearSRChi2 = fSR.GetChisquare()
#	linearSRNDF = fSR.GetNDF()
	
	tmphCR = hCR.Clone()
	tmphCR.Reset()
	tmphCR.Divide( hSR, hDataCR, 1., 1., '' )
#	linearCR = TF1("pol0", "pol0", 50, 300 ) 
#	tmphCR.Fit(linearCR, 'MEIRLLF' )
#	fCR = TF1( tmphCR.GetFunction("pol0") )
#	linearCRChi2 = fCR.GetChisquare()
#	linearCRNDF = fCR.GetNDF()

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


	binWidth = hSR.GetBinWidth(1)

	legend=TLegend(0.55,0.75,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)
	#legend.AddEntry( hSR, 'MC '+bkgLabel+' SR' , 'l' )
	#legend.AddEntry( hCR, 'MC '+bkgLabel+' ABCD Proj', 'pl' )
	legend.AddEntry( hSR, 'All MC Bkgs SR' , 'l' )
	legend.AddEntry( hCR, 'All MC Bkgs ABCD Proj', 'pl' )

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
	hCR.Draw('histe same')

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
	
	labelAxis( nameInRoot, tmphSR, Groom )
	tmphSR.GetXaxis().SetRangeUser( xmin, xmax )
	tmphSR.SetMarkerStyle(8)
	tmphSR.GetXaxis().SetTitleOffset(1.1)
	tmphSR.GetXaxis().SetLabelSize(0.12)
	tmphSR.GetXaxis().SetTitleSize(0.12)
	tmphSR.GetYaxis().SetTitle("SR/CR")
	tmphSR.GetYaxis().SetLabelSize(0.12)
	tmphSR.GetYaxis().SetTitleSize(0.12)
	tmphSR.GetYaxis().SetTitleOffset(0.55)
	tmphSR.SetMaximum( 2. )
	tmphSR.SetMinimum( 0. )
	tmphSR.GetYaxis().SetNdivisions(505)
	tmphSR.Draw()
#	linearSR.SetLineWidth( 2 )
#	linearSR.SetLineColor( kGreen )
#	linearSR.Draw("same")
#	textChi2SR = TLatex( 250, 1.5, '#chi^{2}/NdF = '+ str( round( linearSRChi2, 2 ) )+'/'+ str( round( linearSRNDF, 2 ) ) )
#	textChi2SR.SetTextFont(62) ### 62 is bold, 42 is normal
#	textChi2SR.SetTextSize(0.08)
#	textChi2SR.Draw()
	#tmphCR.Draw()
	line.Draw("same")

	outputFileName = nameInRoot+'_Bkg_'+Groom+'_'+args.RANGE+'_QCD'+args.qcd+'_bkgShapeEstimation'+args.boosted+'Plots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/'+ outputFileName )
	del can

	legend2=TLegend(0.55,0.75,0.90,0.87)
	legend2.SetFillStyle(0)
	legend2.SetTextSize(0.04)
	#legend2.AddEntry( hSR, 'MC '+bkgLabel+' SR' , 'l' )
	legend2.AddEntry( hSR, 'All MC Bkgs SR' , 'l' )
	legend2.AddEntry( hDataCR, 'DATA ABCD Proj', 'pl' )
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetGrid()
	#if log: pad1.SetLogy() 	
	hSR.Draw("histe")
	hDataCR.Draw('PE same')

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
	
	labelAxis( nameInRoot, tmphCR, Groom )
	tmphCR.GetXaxis().SetRangeUser( xmin, xmax )
	tmphCR.SetMarkerStyle(8)
	tmphCR.GetXaxis().SetTitleOffset(1.1)
	tmphCR.GetXaxis().SetLabelSize(0.12)
	tmphCR.GetXaxis().SetTitleSize(0.12)
	tmphCR.GetYaxis().SetTitle("MC/DATA")
	tmphCR.GetYaxis().SetLabelSize(0.12)
	tmphCR.GetYaxis().SetTitleSize(0.12)
	tmphCR.GetYaxis().SetTitleOffset(0.55)
	tmphCR.SetMaximum( 2. )
	tmphCR.SetMinimum( 0. )
	tmphCR.GetYaxis().SetNdivisions(505)
	tmphCR.Draw()
#	linearCR.SetLineWidth( 2 )
#	linearCR.SetLineColor( kGreen )
#	linearCR.Draw("same")
#	textChi2CR = TLatex( 250, 1.5, '#chi^{2}/NdF = '+ str( round( linearCRChi2, 2)  )+'/'+ str( round( linearCRNDF, 2 ) ) )
#	textChi2CR.SetTextFont(62) ### 62 is bold, 42 is normal
#	textChi2CR.SetTextSize(0.08)
#	textChi2CR.Draw()
	line.Draw("same")

	outputFileName = nameInRoot+'_DATA_Bkg_'+Groom+'_'+args.RANGE+'_QCD'+args.qcd+'_bkgShapeEstimation'+args.boosted+'Plots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/'+ outputFileName )
	del can

	legend3=TLegend(0.55,0.75,0.90,0.87)
	legend3.SetFillStyle(0)
	legend3.SetTextSize(0.03)
	legend3.AddEntry( hSignalCR, 'All MC Bkgs + RPV #tilde{t} '+str(args.mass)+' GeV - ABCD Proj' , 'l' )
	legend3.AddEntry( hCR, 'All MC Bkgs - ABCD Proj', 'pl' )

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
	
	labelAxis( nameInRoot, tmphSR, Groom )
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

	legend4=TLegend(0.55,0.75,0.90,0.87)
	legend4.SetFillStyle(0)
	legend4.SetTextSize(0.03)
	legend4.AddEntry( hCR, 'All MC Bkgs ABCD Proj', 'pl' )
	legend4.AddEntry( hDataSignal, '(DATA - RPV #tilde{t} '+str(args.mass)+' GeV) ABCD Proj' , 'pl' )

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
	
	labelAxis( nameInRoot, tmphSR, Groom )
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
	legend3.AddEntry( tmpBCD, 'DATA - ABCD Proj', 'pl' )

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
	tmphSignalCR.GetYaxis().SetTitle("SR/ABCD Proj")
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
		QCDSF = 0.88
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
