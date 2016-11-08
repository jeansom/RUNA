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


def BkgEst2DPlots( rootFile, sample, Groom, nameInRoot, titleXAxis, titleXAxis2, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, legX, legY, plotFolder, version, mass ):
	"""docstring for plot"""

	outputFileName = nameInRoot+'_'+sample+'_'+Groom+'_bkgShapeEstimationBoostedPlots'+version+'.png'
	print 'Processing.......', outputFileName

	bkgHistos = OrderedDict()
	if isinstance(rootFile, dict):
		for bkg in rootFile:
			bkgHistos[ bkg+'_A' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'__A' ), rebinx, rebiny )
			bkgHistos[ bkg+'_B' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'__B' ), rebinx, rebiny )
			bkgHistos[ bkg+'_C' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'__C' ), rebinx, rebiny )
			bkgHistos[ bkg+'_D' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'__D' ), rebinx, rebiny )

		hBkg = bkgHistos[ bkg+'_B' ].Clone()
		hBkg.Reset()
		for samples in bkgHistos:
			print samples
			hBkg.Add( bkgHistos[ samples ].Clone() )
	else: 
		print nameInRoot+'__A'
		bkgHistos[ sample+'_A' ] = Rebin2D( rootFile.Get( nameInRoot+'__A' ), rebinx, rebiny )
		bkgHistos[ sample+'_B' ] = Rebin2D( rootFile.Get( nameInRoot+'__B' ), rebinx, rebiny )
		bkgHistos[ sample+'_C' ] = Rebin2D( rootFile.Get( nameInRoot+'__C' ), rebinx, rebiny )
		bkgHistos[ sample+'_D' ] = Rebin2D( rootFile.Get( nameInRoot+'__D' ), rebinx, rebiny )

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
	textBox.DrawLatex(0.85, 0.85, ( 'M_{#tilde{t}} = '+mass+' GeV' if 'RPV' in sample else sample ) )
	textBox1 = textBox.Clone()
	textBox1.DrawLatex(0.85, 0.8, 'Corr. Factor = '+str(round(corrFactor,2)))
	textBox2 = textBox.Clone()
	textBox2.SetTextSize(0.12)
	textBox2.DrawLatex(0.27, 0.30, 'B  D')
	textBox3 = textBox.Clone()
	textBox3.SetTextSize(0.12)
	textBox3.DrawLatex(0.27, 0.15, 'A  C')

	xline = array('d', [0,1])
	yline = array('d', [1.0, 1.0])
	line = TGraph(2, xline, yline)
	line.SetLineColor(kBlack)
	line.SetLineWidth(5)
	line.Draw("same")
	xline2 = array('d', [0.1,0.1])
	yline2 = array('d', [0, 5])
	line2 = TGraph(2, xline2, yline2)
	line2.SetLineColor(kBlack)
	line2.SetLineWidth(5)
	line2.Draw("same")

	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(can, 4, 0)

	can.SaveAs( plotFolder+outputFileName )
	del can
