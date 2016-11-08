#!/usr/bin/env python

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
	from RUNA.RUNAnalysis.MakePlots import *
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

yline11 = array('d', [1.1, 1.1])
line11 = TGraph(2, xline, yline11)
line11.SetLineColor(kGreen)

yline09 = array('d', [0.9, 0.9])
line09 = TGraph(2, xline, yline09)
line09.SetLineColor(kGreen)

yline0 = array('d', [0,0])
line0 = TGraph(2, xline, yline0)
line0.SetLineColor(kRed)

def StackHistos( nameInRoot, tmphistos1, labelh1, tmphisto2, labelh2, tmphistoerrs, binWidth, xmin, xmax, ratio, labelRatio, ratio2, typePlot, binning, version, grooming, plotFolder, log=False, reScale=False, addUncBand=True):
	

	stackHisto = THStack( "stackHisto", "")
	legend=TLegend(0.20,0.75,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)
	legend.SetNColumns(2)
	histos1 = OrderedDict()
	n = 8
	for histo in tmphistos1:
		if n == 9: n=2
		if n == 3: n = 9
		histos1[histo]=tmphistos1[histo].Clone()
		histos1[histo].SetFillColor( n )
		histos1[histo].SetLineWidth(2)
		histos1[histo].SetLineStyle(1)
		legend.AddEntry( histos1[histo], histo, "f" )
		stackHisto.Add( histos1[histo] )
		n += 1

#	histo1 = histos1[ "All MC Signal Region" ].Clone()

	histoerr = OrderedDict()
	for histo in tmphistoerrs:
		histoerr[ histo ] = tmphistoerrs[histo].Clone()
		histoerr[ histo ].SetLineStyle(2)
		histoerr[histo].SetLineWidth(5)
#		legend.AddEntry( histoerr[ histo ], labelh2 + " " + histo, "l" )

	histott = tmphistos1["tt + Jets"].Clone()
	histott.SetLineColor( kBlue )
	histott.SetLineWidth(2)

#	legend.AddEntry( histott, "tt + Jets", "l" )
	
	histow = tmphistos1["W + Jets"].Clone()
	histow.SetLineColor( kGreen )
	histow.SetLineWidth(2)

#	legend.AddEntry( histow, "W + Jets", "l" )

	histo2 = tmphistos1["tt + Jets"].Clone()
	histo2.SetLineColor(kBlack)
	histo2.SetLineWidth(2)
	histo2.SetLineStyle(1)

	stackHisto.Draw("hist")
	stackHisto.GetXaxis().SetTitle( 'Average Pruned Mass [GeV]' )
	stackHisto.GetYaxis().SetTitle( 'Events / '+(str(int(binWidth)) + ' GeV'))
	stackHisto.GetXaxis().SetRangeUser( 60, 350 )
	stackHisto.SetMaximum( 11.1*max( stackHisto.GetMaximum(), histo2.GetMaximum() ) )
	

#	for histo in histoerr:
#		histoerr[histo].Draw("same hist E0" )

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
#	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
#	pad2.Draw()




	pad1.cd()
	if log: 
		pad1.SetLogy() 	
		stackHisto.SetMinimum( 0.5 )
	else: 
		pad1.SetGrid()


	stackHisto.Draw('hist')
	'''
	if ('Pred' in labelh1) and ('Pred' in labelh2): 
		legend.AddEntry( histo2, labelh2, 'l' )
		histo2.Draw("histe same")
	elif 'DATA' in labelh2: 
		legend.AddEntry( histo2, labelh2, 'ep' )
		histo2.SetMarkerStyle(8)
		histo2.Draw("PE same")
	else: 
		histo2.SetLineColor(kRed)
		legend.AddEntry( histo2, labelh2, 'l' )
		histo2.Draw("histe same")
		'''

#	histott.Draw("hist E0 same")
#	histow.Draw("hist E0 same")


	tmpHisto1 = histo2.Clone()
#	tmpHisto2 = histo1.Clone()

	tmpHisto1.GetXaxis().SetRangeUser(55,345)
#	tmpHisto2.GetXaxis().SetRangeUser(55,345)

	'''
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
	'''
	if 'DATA' in labelh2: tmpLabel = 'DATA'
	else: tmpLabel = 'SR'
#	numEvents = TLatex( 0.6, 0.62, '#splitline{events '+tmpLabel+'/ABCD Pred = }{'+ str( round( histo1.Integral(),2 ) )+'/'+str( round( histo2.Integral(),2 ) )+'}' )
#	numEvents.SetNDC()
#	numEvents.SetTextFont(42) ### 62 is bold, 42 is normal
#	numEvents.SetTextSize(0.04)
#	numEvents.Draw()

	CMS_lumi.extraText = ("Preliminary" if 'DATA' in labelh1 else "Simulation Preliminary")
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	legend.Draw()
	
	'''
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
		line.Draw("same")
	if addUncBand:
		line11.Draw("same")
		line09.Draw("same")
		'''		
	outputFileName = nameInRoot+'_StackHisto_'+typePlot+'_'+str(grooming)+'_QCDPt_bkgShapeEstimationBoostedPlots'+str(version)+'.png'
	if not 'simple' in binning: outputFileName = outputFileName.replace( typePlot, typePlot+'_ResoBasedBin' )
	print 'Processing.......', outputFileName
	can.SaveAs( plotFolder + outputFileName )
	del can
