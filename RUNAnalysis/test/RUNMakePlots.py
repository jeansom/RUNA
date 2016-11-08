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
import scipy
from collections import OrderedDict
from DrawHistogram import Rebin2D
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

class MakePlots:

	def __init__(self):
		gROOT.Reset()
		gROOT.SetBatch()
		gROOT.ForceStyle()
		tdrstyle.setTDRStyle()
		gStyle.SetOptStat(0)
	
		self.xline = array('d', [0,2000])
		self.yline = array('d', [1, 1])
		self.line = TGraph(2, xline, yline)
		self.line.SetLineColor(kRed)
		
		self.yline11 = array('d', [1.1, 1.1])
		self.line11 = TGraph(2, xline, yline11)
		self.line11.SetLineColor(kGreen)
		
		self.yline09 = array('d', [0.9, 0.9])
		self.line09 = TGraph(2, xline, yline09)
		self.line09.SetLineColor(kGreen)
		
		self.yline0 = array('d', [0,0])
		self.line0 = TGraph(2, xline, yline0)
		self.line0.SetLineColor(kRed)


	def ratioPlots( histo1, histo2 ):
		"""docstring for ratioPlots"""

		chi2 = 0
		ndf = 0
		ratioList = []
		binCenterList = []
		ratioLogNErrXPlusList = []
		ratioLogNErrXMinusList = []

		for ibin in range( 0, histo1.GetNbinsX() ):
			binCenterList.append( histo1.GetXaxis().GetBinCenter( ibin ) )
			x = histo1.GetBinContent( ibin )
			xErr = histo1.GetBinError( ibin )
			y = histo2.GetBinContent( ibin )
			yErr = histo2.GetBinError( ibin )
			try: 
				ratio = x/y
				ratioErrX = ratio * TMath.Sqrt( TMath.Power( xErr/x, 2) + TMath.Power( yErr/y, 2)  )
				ratioErrY = ratio* yErr / y
				ratioLogNErrXPlus = TMath.Sqrt( TMath.Power( ( (x/(y-yErr)) - ratio ), 2 )  + TMath.Power( ( ((x+xErr)/y) - ratio ) , 2) ) 
				ratioLogNErrXMinus = TMath.Sqrt( TMath.Power( ( (x/(y+yErr)) - ratio ), 2 )  + TMath.Power( ( ((x-xErr)/y) - ratio ) , 2) ) 
			except ZeroDivisionError: 
				ratio = 0
				ratioErrX = 0
				ratioErrY = 0
				ratioLogNErrXPlus = 0
				ratioLogNErrXMinus = 0

			ratioList.append( ratio )
			ratioLogNErrXPlusList.append( ratioLogNErrXPlus )
			ratioLogNErrXMinusList.append( ratioLogNErrXMinus )

		zeroArray = array( 'd', ( [ 0 ] * (len( ratioList )) ) )
		asymErrors = TGraphAsymmErrors( len(ratioList), array('d', binCenterList), array('d', ratioList), zeroArray, zeroArray, array('d',ratioLogNErrXMinusList), array('d', ratioLogNErrXPlusList) )

		return asymErrors

	def makePlots( nameInRoot, tmphisto1, labelh1, tmphisto2, labelh2, binWidth, xmin, xmax, ratio, labelRatio, ratio2, typePlot, log=False, reScale=False, addUncBand=True):

		histo1 = tmphisto1.Clone()
		histo2 = tmphisto2.Clone()
		legend=TLegend(0.55,0.75,0.90,0.87)
		legend.SetFillStyle(0)
		legend.SetTextSize(0.04)
		if ('Pred' in labelh1) and ('Pred' in labelh2): legend.AddEntry( histo1, labelh1, 'l' )
		elif 'DATA' in labelh1: legend.AddEntry( histo1, labelh1, 'ep' )
		else: legend.AddEntry( histo1, labelh1, 'l' )
		legend.AddEntry( histo2, labelh2, 'pl' )

		histo1.GetYaxis().SetTitle('Events / '+(str(int(binWidth)) if 'simple' in args.binning else binWidth )+' GeV')
		histo1.GetXaxis().SetRangeUser( 60, 350 )
		histo1.SetMaximum( 11.1* max( histo1.GetMaximum(), histo2.GetMaximum() ) )
		if 'MC' in labelh1: 
			histo1.SetLineColor(kRed-4)
			histo1.SetLineWidth(2)
		elif ('Pred' in labelh1) and ('Pred' in labelh2):
			histo1.SetLineColor(kGreen-2)
			histo1.SetLineWidth(2)
		if not isinstance( histo2, THStack ):
			histo2.GetXaxis().SetRangeUser( 60, 350 )
			histo2.SetLineColor(kBlue-4)
			histo2.SetLineWidth(2)
			if 'MC' in labelh2: histo2.SetLineStyle(2)
			else: histo2.SetLineStyle(1)

		tdrStyle.SetPadRightMargin(0.05)
		tdrStyle.SetPadLeftMargin(0.15)
		can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
		pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
		pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
		pad1.Draw()
		pad2.Draw()
		
		pad1.cd()
		if log: 
			pad1.SetLogy() 	
			if not 'Region' in labelh1: histo1.SetMaximum( (5000 if 'low' in args.RANGE else 500) )
			histo1.SetMinimum( 0.5 )
		else: 
			pad1.SetGrid()
		if ('Pred' in labelh1) and ('Pred' in labelh2): histo1.Draw("histe")
		elif 'DATA' in labelh1: 
			histo1.SetMarkerStyle(8)
			histo1.Draw("PE")
		else: histo1.Draw("histe")

		histo2.Draw('hist E0 same')

		tmpHisto1 = histo1.Clone()
		tmpHisto2 = histo2.Clone()

		if not isinstance( histo2, THStack ):
			try: 
				res = array( 'd', ( [ 0 ] * tmpHisto1.GetNbinsX() ) )
				chi2Ndf =  round( tmpHisto1.Chi2Test(tmpHisto2, 'WWCHI2/NDFP', res), 2 )
				chi2 =  round( tmpHisto1.Chi2Test(tmpHisto2, 'WWCHI2'), 2 )
				chi2Test = TLatex( 0.6, 0.7, '#chi^{2}/ndF Test = '+ str( chi2 )+'/'+str( round(chi2/chi2Ndf) ) )
				chi2Test.SetNDC()

				chi2Test.SetTextFont(42) ### 62 is bold, 42 is normal
				chi2Test.SetTextSize(0.04)
				chi2Test.Draw()
			except ZeroDivisionError: print ' |---> chi2Test failed. ZeroDivisionError'

			if 'DATA' in labelh1: tmpLabel = 'DATA'
			else: tmpLabel = 'SR'
			numEvents = TLatex( 0.6, 0.62, '#splitline{events '+tmpLabel+'/ABCD Pred = }{'+ str( round( histo1.Integral(),2 ) )+'/'+str( round( histo2.Integral(),2 ) )+'}' )
			numEvents.SetNDC()
			numEvents.SetTextFont(42) ### 62 is bold, 42 is normal
			numEvents.SetTextSize(0.04)
			numEvents.Draw()

		CMS_lumi.extraText = ("Preliminary" if 'DATA' in labelh2 else "Simulation Preliminary")
		CMS_lumi.relPosX = 0.13
		CMS_lumi.CMS_lumi(pad1, 4, 0)
		legend.Draw()

		pad2.cd()
		pad2.SetGrid()
		pad2.SetTopMargin(0)
		pad2.SetBottomMargin(0.3)
		tmpPad2= pad2.DrawFrame(60,0,350,2)
		tmpPad2.SetXTitle( 'Average pruned mass [GeV]' )
		tmpPad2.SetYTitle( labelRatio )
		tmpPad2.SetTitleSize(0.12, "x")
		tmpPad2.SetTitleSize(0.12, 'y')
		tmpPad2.SetLabelSize(0.12, 'x')
		tmpPad2.SetLabelSize(0.12, 'y')
		tmpPad2.SetTitleOffset(0.5, 'y')
		tmpPad2.SetNdivisions(505, 'x' )
		tmpPad2.SetNdivisions(505, 'y' )
		pad2.Modified()
	
		ratio.SetMarkerStyle(8)
		ratio.SetLineColor(kBlack)
		ratio.Draw('P')
		if isinstance( ratio2, TH1 ):
			ratio2.SetFillStyle(3004)
			ratio2.SetFillColor( kRed )
			ratio2.Draw('same E2')
			self.line.Draw("same")
		if addUncBand:
			self.line11.Draw("same")
			self.line09.Draw("same")

		outputFileName = nameInRoot+'_'+typePlot+'_'+args.grooming+'_'+args.RANGE+'_QCD'+args.qcd+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
		if not 'simple' in args.binning: outputFileName = outputFileName.replace( typePlot, typePlot+'_ResoBasedBin' )
		print 'Processing.......', outputFileName
		can.SaveAs( 'Plots/101916/'+ outputFileName )
		del can
